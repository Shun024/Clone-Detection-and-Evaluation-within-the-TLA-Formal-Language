import os
import re

# Define the input and output directories
input_dir = 'parsed_files'
output_dir = 'tokenized_files'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def anonymize_variable_names(tla_code):
    # Split the TLA+ code into lines
    lines = tla_code.split('\n')

    variable_count = 1
    variable_mapping = {}
    anonymized_lines = []

    for line in lines:
        # Remove comments
        line = re.sub(r'--.*', '', line)

        # Replace integers with #
        line = re.sub(r'\b\d+\b', '#', line)

        # Anonymize variable names
        words = re.findall(r'[A-Za-z_][\w.\\]*|\\\w+|"[A-Z_ ]+"|\S', line)
        anonymized_words = []

        for word in words:
            if re.match(r'^[A-Za-z_][\w.]*$', word) and not re.match(r'^[A-Z_]+$', word) and not re.match(r'^\\', word):
                if word not in variable_mapping:
                    variable_mapping[word] = f'$name{variable_count}'
                    variable_count += 1
                anonymized_words.append(variable_mapping[word])
            else:
                anonymized_words.append(word)

        anonymized_line = ''.join(anonymized_words)  # Remove whitespaces
        anonymized_lines.append(anonymized_line)

    return '\n'.join(anonymized_lines)

# Process all TLA+ files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".tla"):
        input_file_path = os.path.join(input_dir, filename)
        output_file_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_tokenized.tla")

        with open(input_file_path, 'r') as input_file:
            tla_code = input_file.read()

        # Anonymize, replace integers, and preserve symbols
        tokenized_code = anonymize_variable_names(tla_code)

        # Write the tokenized code to the output file
        with open(output_file_path, 'w') as output_file:
            output_file.write(tokenized_code)

print("TLA+ code tokenization complete.")
