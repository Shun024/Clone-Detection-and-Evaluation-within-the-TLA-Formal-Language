import os
import re

def preprocess_and_parse(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()

    preprocessed_lines = []
    ignore_lines = False

    for line in lines:
        if re.search(r"\bBEGIN TRANSLATION\b", line):
            ignore_lines = True
        elif not ignore_lines:
            if re.match(r"\s{4,}", line):
                if preprocessed_lines:
                    preprocessed_lines[-1] += " " + line.strip()
            elif "==" in line and re.match(r"^[A-Za-z0-9 ]", line):
                preprocessed_lines.append(line.strip())

    return '\n'.join(preprocessed_lines)

def process_tla_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".tla"):
            input_file_path = os.path.join(input_dir, filename)
            output_file_path = os.path.join(output_dir, filename)

            parsed_code = preprocess_and_parse(input_file_path)

            with open(output_file_path, 'w') as output_file:
                output_file.write(parsed_code + '\n')

if __name__ == "__main__":
    input_dir = 'files'
    output_dir = 'parsed_files'

    process_tla_files(input_dir, output_dir)

    print("TLA+ code processing complete.")
