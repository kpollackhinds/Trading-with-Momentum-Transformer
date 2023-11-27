import argparse
import sys
from typing import List

sys.path.append("data_preprocessing/")

from preprocess import chunk_clean


def clean_data(input_file: List[str]):

    clean_path_list = []
    for input_file in input_file:

        if "trades" in input_file:
            print("Cleaning trades file: {}".format(input_file))
            print(" ")

            clean_path = chunk_clean(input_file, False)

        elif "quotes" in input_file:
            print("Cleaning quotes file: {}".format(input_file))
            print(" ")

            clean_path = chunk_clean(input_file, True)

        else:
            print("Input file is not a trades or quotes file")

            return None

        clean_path_list.append(clean_path)

    return clean_path_list


# python clean_data.py --input_file <input_file>
if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--input_file", type=str, default="AAPL.csv")

    args = parser.parse_args()

    clean_data([args.input_file])
