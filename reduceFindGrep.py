"""
v1.0

Reduce output from a find/grep operation

find , \( -name .git -o -name node_modules -o -name vendor \) -type d -prune -o -type f ! \( -name '*.csv' -o -name '*.json' -o -name '*.map' \) -print0 | xargs -0 -P 4 grep -nI -e 'statistic' > grepStatistic.txt

python3 reduceFindGrep.py -i "/mnt/a/Dev/grepCoreUi.txt"
"""

import argparse
import pandas as pd

def get_parser():
    parser = argparse.ArgumentParser(description="Reduce ouput from a find/grep operation")
    parser.add_argument(
        '-i',
        '--input_file',
        nargs='+',
        help='Path to input text file')
    parser.add_argument(
        '-o',
        '--output_file',
        nargs='+',
        help='Path to output file')
    parser.add_argument(
        '-m',
        '--mode',
        nargs='+',
        help='Possible modes: path/file')
    return parser


def main(input_file: str, output_file: str, mode: str):

    with open(input_file) as f:
        lines = f.readlines()

    files = [x.split(":")[0] for x in lines]

    if (mode == "path"):
        out = ["/".join(x.split("/")[:-1]) for x in files]
    if (mode == "file"):
        out = files

    with open(output_file, "w") as f:
        for e in list(set(out)):
            if (e != ""):
                f.write(e + "\n")

if __name__ == "__main__":
    args, random = get_parser().parse_known_args()
    main(args.input_file[0], args.output_file[0], args.mode[0])
