import csv
import re 

def read_abbreviation_table(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile)
        abbreviation_dict = {row[0]: row[1] for row in csvreader}
    return abbreviation_dict

def replace_abbreviations(text: str, abbreviation_dict: dict) -> str:
    for abbreviation, replacement in abbreviation_dict.items():
        text = text.replace(abbreviation, replacement)
    return text

def insert_hyphens(match):
    return '-'.join(match.group(0))

def replace_continuous_caps(text: str) -> str:
    continuous_caps_pattern = r'[A-Z]{2,}'
    return re.sub(continuous_caps_pattern, insert_hyphens, text)

def main(text: str, abbreviation_file: str) -> str:
    abbreviation_dict = read_abbreviation_table(abbreviation_file)
    cleaned_text = replace_continuous_caps(text)
    cleaned_text = replace_abbreviations(cleaned_text, abbreviation_dict)
    return cleaned_text

if __name__ == "__main__":
    with open("test_pdf/test.txt", "r", encoding="utf-8") as f:
        text = f.read()

    abbreviation_file = "Abbreviation_Replacement_Table.csv"

    cleaned_text = main(text, abbreviation_file)
    with open("test_pdf/test_cleaned.txt", "w", encoding="utf-8") as f:
        f.write(cleaned_text)
