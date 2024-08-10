ComprehensiveSFV

Overview

ComprehensiveSFV is a Python tool designed for file verification using a range of hash functions. It supports both cryptographic and non-cryptographic hash functions, including CRC32, CRC64, MD5, SHA-256, SHA-384, SHA-512, SHA3-256, SHA3-384, SHA3-512, BLAKE2b, and BLAKE2s. This tool generates a .csfv file containing checksums for files in a specified directory or for a single file and allows for verification of files against an existing .csfv file, logging the results.

Features

    Generate Checksums: Create a .csfv file with checksums for files using the selected hash type.
    Verify Checksums: Verify files against a .csfv file and log the results.
    Customizable Hash Types: Choose from various hash functions with different security levels.
    Formatted Output: Logs results with color-coded status and file size information.
    Multi-Threading: Improves Performance.
    Error Handling: Provides detailed error messages for better debugging and handles interruptions gracefully.

Installation

    Ensure Python 3.x is installed on your system.
    Install the required dependencies, including colorama. Install it using pip with the command pip install colorama.

Usage

Generate Checksum File

python csfv.py -g DIRECTORY

Verify Checksum File

python csfv.py -v DIRECTORY

Error Handling
ComprehensiveSFV handles errors related to file operations and hash computations. Error messages are displayed in the console.

ComprehensiveSFV is provided as-is without any warranty. Use it at your own risk.
