import hashlib
import os
import time
import zlib
import argparse
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
from colorama import Fore, Style, init

init(autoreset=True)

def hash_file(file_path, hash_type):
    try:
        if hash_type in [
            "sha256",
            "sha384",
            "sha512",
            "sha3_256",
            "sha3_384",
            "sha3_512",
            "md5",
            "blake2b",
            "blake2s",
        ]:
            hash_func = getattr(hashlib, hash_type)()
            with open(file_path, "rb") as f:
                while chunk := f.read(8192):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        elif hash_type == "crc32":
            buf = 0
            with open(file_path, "rb") as f:
                while chunk := f.read(8192):
                    buf = zlib.crc32(chunk, buf)
            return f"{buf & 0xFFFFFFFF:08x}"
        elif hash_type == "crc64":
            buf = 0
            with open(file_path, "rb") as f:
                while chunk := f.read(8192):
                    buf = zlib.crc32(chunk, buf)
            return f"{buf & 0xFFFFFFFFFFFFFFFF:016x}"
    except Exception as e:
        print(f"Error hashing file {file_path}: {e}")
        return None

def generate_chksum_file(path, hash_type):
    try:
        # Start the timer
        start_time = time.time()

        if os.path.isfile(path):
            files = [path]
            base_dir = os.path.dirname(path)
            chksum_filename = os.path.basename(path) + ".csfv"
        elif os.path.isdir(path):
            files = [
                os.path.join(root, file)
                for root, _, files in os.walk(path)
                for file in files
            ]
            base_dir = path
            chksum_filename = os.path.basename(path) + ".csfv"
        else:
            print("Invalid path. Please provide a valid file or directory.")
            return

        chksum_filepath = os.path.join(base_dir, chksum_filename)
        print(f"{Fore.GREEN}Generating checksum file: {chksum_filepath}")

        checksums = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with ProcessPoolExecutor() as executor:
            future_to_file = {executor.submit(hash_file, file, hash_type): file for file in files if os.path.isfile(file)}
            for future in as_completed(future_to_file):
                file = future_to_file[future]
                file_hash = future.result()
                if file_hash is not None:
                    checksums.append((file_hash, os.path.relpath(file, base_dir)))

        with open(chksum_filepath, "w") as chksum_file:
            chksum_file.write(f"# csfv v1.0 | Date: {timestamp}\n")
            chksum_file.write(f"# Hash type: {hash_type}\n")
            for file_hash, file_name in checksums:
                chksum_file.write(f"{file_hash}  {file_name}\n")

        with open(chksum_filepath, "r") as f:
            chksum_data = f.read()
        chksum_master_hash = hashlib.blake2b(chksum_data.encode()).hexdigest()

        with open(chksum_filepath, "a") as chksum_file:
            chksum_file.write(f"# Master BLAKE2b: {chksum_master_hash}\n")

        # End the timer
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time

        # Print the elapsed time
        print(f"{Fore.GREEN}Time elapsed: {elapsed_time:.4f} seconds")

    except Exception as e:
        print(f"{Fore.RED}Error generating .csfv file: {e}")

def format_file_size(size_bytes):
    """Format file size in KB, MB, GB, etc."""
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1048576:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1073741824:
        return f"{size_bytes / 1048576:.2f} MB"
    else:
        return f"{size_bytes / 1073741824:.2f} GB"

def verify_file_line(line, base_dir, hash_type):
    parts = line.strip().split("  ")
    if len(parts) != 2:
        return (None, f"{Fore.RED}ERROR: Incorrect format in .csfv file line: {line.strip()}\n", None, None)

    file_hash, file_name = parts
    file_path = os.path.join(base_dir, file_name)

    if not os.path.exists(file_path):
        return (None, f"{Fore.RED}File missing: {file_name}\n", file_name, None)

    actual_file_hash = hash_file(file_path, hash_type)
    file_size = os.path.getsize(file_path)
    file_size_formatted = format_file_size(file_size)

    if actual_file_hash != file_hash:
        return (None, f"{Fore.RED}FAILED: {actual_file_hash} {file_name}\n", file_name, None)
    else:
        return (file_hash, f"{Fore.GREEN}PASSED: {actual_file_hash} {file_name} - {file_size_formatted}\n", None, file_size_formatted)

def verify_chksum_file(path):
    try:
        # Start the timer
        start_time = time.time()

        if os.path.isfile(path):
            base_dir = os.path.dirname(path)
            chksum_filename = os.path.basename(path)
            chksum_filepath = os.path.join(base_dir, chksum_filename)
            log_filename = chksum_filename + ".log"
            log_filepath = os.path.join(base_dir, log_filename)
        elif os.path.isdir(path):
            chksum_filename = os.path.basename(path) + ".csfv"
            chksum_filepath = os.path.join(path, chksum_filename)
            log_filename = chksum_filename + ".log"
            log_filepath = os.path.join(path, log_filename)
            base_dir = path
        else:
            print(f"{Fore.RED}Invalid path. Please provide a valid file or directory.")
            return

        print(f"{Fore.GREEN}Verifying checksum file: {chksum_filepath}")

        if not os.path.exists(chksum_filepath):
            print("No .csfv file found.")
            return

        with open(chksum_filepath, "r") as chksum_file:
            lines = chksum_file.readlines()

        stored_master_hash = lines[-1].strip().split(": ")[1]

        chksum_content = "".join(lines[:-1])
        actual_master_hash = hashlib.blake2b(chksum_content.encode()).hexdigest()

        with open(log_filepath, "w") as log_file:
            if stored_master_hash != actual_master_hash:
                log_file.write(
                    f"{Fore.RED}FAILED: {chksum_filepath} failed master verification.\n"
                )
                print(
                    f"{Fore.RED}FAILED: {chksum_filepath} failed master verification."
                )
            else:
                log_file.write(
                    f"{Fore.GREEN}PASSED: {chksum_filepath} passed master verification.\n"
                )
                print(
                    f"{Fore.GREEN}PASSED: {chksum_filepath} passed master verification."
                )

            hash_type = lines[1].strip().split(": ")[1]

            passed_count = 0
            failed_count = 0
            failed_files = []

            with ProcessPoolExecutor() as executor:
                future_to_line = {executor.submit(verify_file_line, line, base_dir, hash_type): line for line in lines[2:-1] if not line.startswith("#") and line.strip()}
                for future in as_completed(future_to_line):
                    file_hash, result_line, failed_file, file_size_formatted = future.result()
                    if file_hash is None:
                        failed_count += 1
                        if failed_file:
                            failed_files.append(failed_file)
                    else:
                        passed_count += 1
                    log_file.write(result_line)
                    print(result_line.strip())

            if failed_count == 0:
                log_file.write(
                    f"{Fore.GREEN}PASSED: All {passed_count} file(s) passed verification.\n"
                )
                print(
                    f"{Fore.GREEN}PASSED: All {passed_count} file(s) passed verification."
                )
            else:
                log_file.write(f"{Fore.RED}Failed files:\n")
                print(f"{Fore.RED}Failed files:")
                for failed_file in failed_files:
                    log_file.write(f"{Fore.RED} - {failed_file}\n")
                    print(f"{Fore.RED} - {failed_file}")

        # End the timer
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time

        # Print the elapsed time
        print(f"{Fore.GREEN}Time elapsed: {elapsed_time:.4f} seconds")

    except Exception as e:
        print(f"Error verifying .csfv file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Generate or verify .csfv checksum files.")
    parser.add_argument('-g', '--generate', metavar='DIRECTORY', type=str, help='Directory to generate .csfv file.')
    parser.add_argument('-v', '--verify', metavar='DIRECTORY', type=str, help='Directory containing .csfv file for verification.')
    
    args = parser.parse_args()

    try:
        if args.generate:
            path = args.generate
            if os.path.exists(path):
                print("Choose hash type:")
                print(
                    f"{Fore.RED}1.  CRC32    - Broken    (Vulnerable to collisions.)"
                )
                print(
                    f"{Fore.RED}2.  CRC64    - Broken    (Vulnerable to collisions.)"
                )
                print(
                    f"{Fore.RED}3.  MD5      - Broken    (Vulnerable to collisions.)"
                )
                print(
                    f"{Fore.YELLOW}4.  SHA2-256 - Uncertain (Theoretical weaknesses, collisions.)"
                )
                print(
                    f"{Fore.GREEN}5.  SHA2-384 - Secure    (More secure than SHA-256 due to increased bit length.)"
                )
                print(
                    f"{Fore.GREEN}6.  SHA2-512 - Secure    (Offers even more security than SHA-384, may not be significant for all applications.)"
                )
                print(
                    f"{Fore.GREEN}7.  SHA3-256 - Secure    (Providing a different cryptographic approach and enhanced security compared to SHA-2.)"
                )
                print(
                    f"{Fore.GREEN}8.  SHA3-384 - Secure    (Provides more security than SHA3-256.)"
                )
                print(
                    f"{Fore.GREEN}9.  SHA3-512 - Secure    (The most secure in the SHA-3 family.)"
                )
                print(
                    f"{Fore.GREEN}10. BLAKE2b  - Secure    (A high-performance cryptographic hash function.)"
                )
                print(
                    f"{Fore.GREEN}11. BLAKE2s  - Secure    (A high-performance cryptographic hash function with smaller output size.)"
                )

                option = int(input("Enter option (1-11): "))

                hash_types = {
                    1: "crc32",
                    2: "crc64",
                    3: "md5",
                    4: "sha256",
                    5: "sha384",
                    6: "sha512",
                    7: "sha3_256",
                    8: "sha3_384",
                    9: "sha3_512",
                    10: "blake2b",
                    11: "blake2s",
                }

                hash_type = hash_types.get(option, None)

                if hash_type:
                    generate_chksum_file(path, hash_type)
                else:
                    print("Invalid option.")
            else:
                print("The specified path does not exist.")

        elif args.verify:
            path = args.verify
            if os.path.exists(path):
                verify_chksum_file(path)
            else:
                print("The specified path does not exist.")
        else:
            print("Please specify --generate or --verify with a valid path.")

    except KeyboardInterrupt:
        print("\nExiting.")

if __name__ == "__main__":
    main()
