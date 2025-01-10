import os
import json
import csv
import re


# This module should be run after clean.py
# This parses the result from clean.py into a json to be used in other applications.

def clean_university_name(name):
    return re.sub(r"[^a-zA-Z& ]", "", name.replace("-", " "))


def postprocess_json(input_dir, output_dir):
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

            if temp[1] == "N/A":
                continue

            json_data.append([temp[0], clean_university_name(temp[1]), [i.strip() for i in temp[2].split(",")]])

        if success:
            with open(f"{output_dir}/{file}.json", "w") as f:
                json.dump(json_data, f, indent=2)


def postprocess_csv(input_dir, output_dir):
    for file in os.listdir(input_dir):
        with open(f"{input_dir}/{file}", encoding="utf-8") as f:
            data = f.read().split("\n")

        university_data = []
        major_data = []

        success = True
        for line in data:
            if not line:
                continue

            temp = line.split(" - ")
            if len(temp) != 3:
                print(line)
                success = False
                break

            if temp[1] == "N/A":
                continue

            university_data.append([temp[0], clean_university_name(temp[1])])
            major_data.extend([[temp[0], i.strip()] for i in temp[2].split(",")])

        if success:
            with open(f"{output_dir}/{file}_universities.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["name", "university"])
                writer.writerows(university_data)

            with open(f"{output_dir}/{file}_majors.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["name", "major"])
                writer.writerows(major_data)


if __name__ == "__main__":
    postprocess_json("../generated/cleaned", "../generated/json")
    postprocess_csv("../generated/cleaned", "../generated/csv")
