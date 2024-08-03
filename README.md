# csfv
Comprehensive SFV

Overview

Comprehensive SFV provides functionality for generating and verifying checksum files using various hash functions. It supports both cryptographic and non-cryptographic hash functions, including CRC32, CRC64, MD5, SHA-256, SHA-384, SHA-512, SHA3-256, SHA3-384, SHA3-512, BLAKE2b, and BLAKE2s. Comprehensive SFV generates a .csfv file containing checksums for files in a specified directory or for a single file. It also verifies files against an existing .csfv file and logs the results.
Features

    Generate Checksums: Create a .csfv file with checksums for files using the selected hash type.
    Verify Checksums: Verify files against a .csfv file and log the results.
    Customizable Hash Types: Choose from various hash functions with different security levels.
    Formatted Output: Logs results with color-coded status and file size information.
    Error Handling: Provides detailed error messages for better debugging.

Installation

    Ensure you have Python 3.x installed on your system.

    Install the required dependencies:

    colorama

Usage
Running Comprehensive SFV

To run Comprehensive SFV, execute it using Python:

python3 csfv.py

Menu Options

When you run Comprehensive SFV, you'll be presented with a menu:

    Generate .csfv file: Create a .csfv file for a specified file or directory.
    Verify .csfv file: Verify files against an existing .csfv file.

Generating a .csfv File

    Select option 1 from the menu.
    Enter the file or directory path for which you want to generate the checksum file.
    Choose the hash type from the provided options. Hash types are categorized by their security levels:
        CRC32, CRC64, MD5: Non-cryptographic and vulnerable to collisions.
        SHA2-256, SHA2-384, SHA2-512: Cryptographic with varying levels of security.
        SHA3-256, SHA3-384, SHA3-512: Enhanced security compared to SHA2.
        BLAKE2b, BLAKE2s: High-performance cryptographic hash functions.

Verifying a .csfv File

    Select option 2 from the menu.
    Enter the file or directory path where the .csfv file is located.
    Comprehensive SFV will compare the stored checksums with the actual file checksums and generate a log file with the results.

Example

To generate a checksum file for a directory using SHA-256:

python3 csfv.py

    Select 1 to generate a checksum file.
    Enter the path to the directory.
    Select 7 for SHA3-256.
    The .csfv file will be created in the directory.

To verify the checksum file:

python3 csfv.py

    Select 2 to verify the checksum file.
    Enter the path to the directory containing the .csfv file.

Comprehensive SFV accepts two command line arguments: generate and verify. You can use these arguments with the following options:
Generate Checksum File

To generate a .csfv checksum file for a directory or file:

python csfv.py -g DIRECTORY

    -g DIRECTORY: Path to the directory or file for which you want to generate the checksum file. The .csfv file will be created in the same location as the specified path.

Verify Checksum File

To verify a .csfv checksum file:

python csfv.py -v DIRECTORY

    -v DIRECTORY: Path to the directory containing the .csfv file or the path to the .csfv file itself.

Error Handling

Comprehensive SFV handles errors related to file operations and hash computations. Error messages will be displayed in the console and logged to the verification results file.
License

Comprehensive SFV is provided as-is without any warranty. Use it at your own risk.
