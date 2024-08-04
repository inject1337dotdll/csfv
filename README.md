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

Comprehensive SFV handles errors related to file operations and hash computations. Error messages will be displayed in the console and logged to the verification results file

License

Comprehensive SFV is provided as-is without any warranty. Use it at your own risk.
