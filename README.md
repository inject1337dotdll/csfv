Comprehensive SFV
Overview

Comprehensive SFV is a Python tool designed for generating and verifying checksum files using a range of hash functions. It supports both cryptographic and non-cryptographic hash functions, including CRC32, CRC64, MD5, SHA-256, SHA-384, SHA-512, SHA3-256, SHA3-384, SHA3-512, BLAKE2b, and BLAKE2s. This tool generates a .csfv file containing checksums for files in a specified directory or for a single file and allows for verification of files against an existing .csfv file, logging the results.
Features

    Generate Checksums: Create a .csfv file with checksums for files using the selected hash type.
    Verify Checksums: Verify files against a .csfv file and log the results.
    Customizable Hash Types: Choose from various hash functions with different security levels.
    Formatted Output: Logs results with color-coded status and file size information.
    Error Handling: Provides detailed error messages for better debugging and handles interruptions gracefully.

Installation

    Ensure Python 3.x is installed on your system.
    Install the required dependencies, including colorama. Install it using pip with the command pip install colorama.

Usage

To run Comprehensive SFV, use Python to execute the script:

python csfv.py

Command-Line Arguments
Comprehensive SFV accepts two command-line arguments: generate and verify.

Generate Checksum File
To generate a .csfv checksum file for a directory or file:

python csfv.py -g DIRECTORY
    -g DIRECTORY: Path to the directory or file for which you want to generate the checksum file. The .csfv file will be created in the same location as the specified path.

Verify Checksum File
To verify a .csfv checksum file:

python csfv.py -v DIRECTORY
    -v DIRECTORY: Path to the directory containing the .csfv file or the path to the .csfv file itself.

Error Handling
Comprehensive SFV handles errors related to file operations and hash computations. Error messages are displayed in the console, and interruptions (e.g., Ctrl+C) are managed gracefully. Results and errors are also logged to the verification results file.
License

Comprehensive SFV is provided as-is without any warranty. Use it at your own risk.
