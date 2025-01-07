import csv
from datetime import datetime
import re

USER_ANOM = True


# This system essentially relies on the fact that people will post their commitment messages
# in the year they plan on going to the university.
# How the algorithm works is that it detects the largest year that comes before it and inserts
# itself into that year's messages
# Finally, we put the cleaned messages into an output directory to be processed later
def sanitize_message(message):
    matcher = re.compile("["
                         u"\U0001F600-\U0001F64F"  # emoticons
                         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                         u"\U0001F680-\U0001F6FF"  # transport & map symbols
                         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                         u"\U00002500-\U00002BEF"  # chinese char
                         u"\U00002702-\U000027B0"
                         u"\U000024C2-\U0001F251"
                         u"\U0001f926-\U0001f937"
                         u"\U00010000-\U0010ffff"
                         u"\u2640-\u2642"
                         u"\u2600-\u2B55"
                         u"\u200d"
                         u"\u23cf"
                         u"\u23e9"
                         u"\u231a"
                         u"\ufe0f"  # dingbats
                         u"\u3030"
                         "\n"
                         "]+", re.UNICODE)
    return re.sub(matcher, "", message)


def preprocess(file_location, output_location):
    # Step 1: Parsing the csv from the Discord Chat Exporter

    # To add a new year, just duplicate an entry and add a new year to it
    graduating_years = [
        ["2024", datetime(2023, 11, 1), []],
        ["2023", datetime(2022, 11, 1), []],
        ["2022", datetime(2021, 11, 1), []],
        ["2021", datetime(2020, 11, 1), []],
        ["Unknown", datetime(1972, 1, 1), []],
    ]

    with open(file_location, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skipping the first line since it's just header information

        for i, line in enumerate(reader):
            author, date_, message = f"user{i}", line[2], line[3]
            if not USER_ANOM:
                author = line[1]

            # Sanitizing the message
            message = sanitize_message(message)

            date = datetime.strptime(date_[:19], "%Y-%m-%dT%H:%M:%S")

            for year in graduating_years:
                if date > year[1]:
                    year[2].append(f"{author} wrote \"{message}\"")
                    break
            else:
                graduating_years[-1][2].append(f"{author} wrote \"{message}\"")

    # Step 2: Write the data into the proper years_messages
    for year in graduating_years:
        if not year[2]:
            continue

        with open(f"{output_location}/{year[0]}", "w", encoding="utf-8") as f:
            f.write("\n".join(year[2]))


if __name__ == "__main__":
    preprocess("../data/ApplyingToCollege - Results.csv", "../generated/years_messages")
