import os
import json


# This module should be run after clean.py
# This parses the result from clean.py into a json to be used in other applications.

def postprocess(input_dir, output_dir):
    for file in os.listdir(input_dir):
        with open(f"{input_dir}/{file}", encoding="utf-8") as f:
            data = f.read().split("\n")

        json_data = []

        success = True
        for line in data:
            if not line:
                continue

            temp = line.split(" - ")
            if len(temp) != 3:
                print(line)
                success = False
                break

            json_data.append([temp[0], temp[1], [i.strip() for i in temp[2].split(",")]])

        if success:
            with open(f"{output_dir}/{file}.json", "w") as f:
                json.dump(json_data, f, indent=2)


if __name__ == "__main__":
    postprocess("../generated/cleaned", "../generated/json")
