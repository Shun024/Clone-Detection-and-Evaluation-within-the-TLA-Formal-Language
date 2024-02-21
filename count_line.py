import os
import csv
import shutil
import matplotlib.pyplot as plt

def count_lines_in_files(directory, csv_output, small_file, large_file):
    files = [file for file in os.listdir(directory) if file.endswith('.tla')]
    line_count_data = []

    total_line_count = 0

    for file_name in files:
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'r') as file:
            line_count = sum(1 for _ in file)  # Count the lines in the file
            line_count_data.append({'File Name': file_name, 'Line Count': line_count})

            # Update total line count
            total_line_count += line_count

    # Calculate mean line count
    mean_line_count = int(total_line_count / len(files))

    # Writing to CSV
    with open(csv_output, 'w', newline='') as csvfile:
        fieldnames = ['File Name', 'Line Count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(line_count_data)

    # Create directories for Small_files and Large_files outside of directory_path
    small_files_dir = os.path.join(os.path.dirname(directory), small_file)
    large_files_dir = os.path.join(os.path.dirname(directory), large_file)

    os.makedirs(small_files_dir, exist_ok=True)
    os.makedirs(large_files_dir, exist_ok=True)

    # Copy files to Small_files or Large_files based on line count
    for data in line_count_data:
        file_name = data['File Name']
        line_count = data['Line Count']
        source_path = os.path.join(directory, file_name)

        if line_count < mean_line_count:
            destination_path = os.path.join(small_files_dir, file_name)
        else:
            destination_path = os.path.join(large_files_dir, file_name)

        shutil.copyfile(source_path, destination_path)

count_lines_in_files("tokenized_files", "tokenized_line_count.csv", "tokenzied_small_file", "tokenized_large_file")
count_lines_in_files("parsed_files", "parsed_line_count.csv", "parsed_small_file", "parsed_large_file")

