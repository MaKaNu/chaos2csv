"""Module chaos2csv Parser"""
import argparse
import importlib
from pathlib import Path
import sys
import types

from commands import multiline_dict_tensor


def use_tomllib() -> types.ModuleType:
    """import tomllib module."""
    toml = importlib.import_module("tomllib")
    # Code, der tomllib verwendet
    return toml


def get_parser() -> argparse.ArgumentParser:
    """Create the Parser for the c2c CLI Tool

    Returns:
        argparse.ArgumentParser: The c2c parser
    """
    # MAINPARSER
    parser = argparse.ArgumentParser(description="chaos2csv. A plain text converter")
    parser.add_argument("--config", "-c", type=str, help="Path to TOML-configfile")
    parser.add_argument("-p", "--path", type=Path, help="Path to chaotic file.")
    subparsers = parser.add_subparsers(dest="command", help="Useable Commands")

    # SUBPARSERS
    subparsers.add_parser(
        "multiline-dict-tensor", help="Command for multiline-dict-tensor formated text"
    )

    return parser


def run_parser(parser: argparse.ArgumentParser):
    """Run the parse which is given by argument

    Args:
        parser (argparse.ArgumentParser): The Parser which should be executed.
    """
    args = parser.parse_args()
    try:
        toml = use_tomllib()

        if args.config:
            config = toml.load(args.config)
        else:
            config = None
    except ImportError:
        # TODO replace by propper logging
        print(f"No toml available in python {sys.version}")
        config = None

    if args.command == "multiline-dict-tensor":
        runner = multiline_dict_tensor.Runner()
        runner.run(args, config)
        runner.save(args, config)
