import argparse
from assembler import assemble

def main() -> None:
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Assemble a .b file")
    parser.add_argument("filename", help="Path to the .b file")
    parser.add_argument("extra_args", nargs="*", help="Additional arguments")

    # Parse the arguments
    args = parser.parse_args()

    # Call the assemble function with the provided filename
    assemble(args.filename, args.extra_args if args.extra_args else None)

if __name__ == '__main__':
    main()