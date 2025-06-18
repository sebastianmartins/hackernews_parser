"""
Main entry point for the parser package.

This allows the package to be run as: python -m parser

Usage:
    python3 -m hackernews_parser --version 1 --data-file data/hackernews_v1.json
    python3 -m hackernews_parser --version 2 --data-file data/hackernews_v2.json
    python3 -m hackernews_parser --help
"""

import argparse

from hackernews_parser.hackernews_parser_v1 import main as main_v1
from hackernews_parser.hackernews_parser_v2 import main as main_v2


def main():
    """Main entry point for the parser package."""
    parser = argparse.ArgumentParser(
        description="HackerNews data parser package", prog="python -m parser"
    )

    parser.add_argument(
        "--version",
        "-v",
        choices=["1", "2"],
        default="2",
        help="Parser version to use (default: 2)",
    )

    parser.add_argument(
        "--data-file",
        "-f",
        type=str,
        required=True,
        help="Path to the data file to parse.",
    )

    args = parser.parse_args()

    if args.version == "1":
        main_v1(args.data_file)
    elif args.version == "2":
        main_v2(args.data_file)
    else:
        raise ValueError(f"Invalid version: {args.version}")


if __name__ == "__main__":
    main()
