"""Main module."""
from c2cparser import get_parser, run_parser

def main():
    """Main function of chaos2csv CLI tool.
    """
    parser = get_parser()
    run_parser(parser)

if __name__ == "__main__":
    main()
