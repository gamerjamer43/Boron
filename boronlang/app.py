from assembler import assemble
import argparse, time
timer = False

def main() -> None:
    # parse args
    parser = argparse.ArgumentParser(description="Assemble a .b file")
    parser.add_argument("filename", help="Path to the .b file")
    parser.add_argument("extra_args", nargs="*", help="Additional arguments")
    args = parser.parse_args()

    # time and assemble
    if timer == True: start_time = time.perf_counter()
    assemble(args.filename, args.extra_args if args.extra_args else None)
    if timer == True: end_time = time.perf_counter()

    # print elapsed time
    if timer == True:
        elapsed_ms = (end_time - start_time) * 1000
        print(f"Execution time: {elapsed_ms:.2f} ms")

if __name__ == '__main__':
    main()