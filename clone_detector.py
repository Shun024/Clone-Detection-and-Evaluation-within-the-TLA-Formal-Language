import difflib
import os
import csv
import time

from collections import defaultdict

# find clones within individual files
def detect_clones_individual(file_path):
    with open(file_path, 'r') as file:
        code = file.readlines()

    clones = []
    for i, line1 in enumerate(code):
        for j, line2 in enumerate(code[i + 1:], start=i + 1):
            similarity = difflib.SequenceMatcher(None, line1, line2).ratio()
            if similarity > 0.2:
                if similarity == 1:
                    clone_type = "Type-1 Clone"
                elif similarity > 0.9:
                    clone_type = "Type-2 Clone"
                elif similarity > 0.8:
                    clone_type = "Type-3 Clone"
                elif similarity > 0.7:
                    clone_type = "Type-4 Clone"
                else:
                    clone_type = "Type-5 Clone"
                clones.append((i + 1, j + 1, similarity, clone_type))

    return clones

def individual_process_directory(directory_path, clone_csv, statistics_csv):
    start_time = time.time()
    with open(clone_csv, 'w', newline='') as csv_file, open(statistics_csv, 'w', newline='') as stats_file:
        csv_writer = csv.writer(csv_file)
        stats_writer = csv.writer(stats_file)

        csv_writer.writerow(["File Name", "Line Numbers", "Similarity (%)", "Clone Type"])
        stats_writer.writerow(["File Name", "Clone Pairs", "Type-1 Clones", "Type-2 Clones", "Type-3 Clones", "Type-4 Clones", "Type-5 Clones"])

        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith(".tla"):  # Adjust the file extension as needed
                    file_path = os.path.join(root, file)
                    clones = detect_clones_individual(file_path)

                    clone_pairs = len(clones)
                    clone_types_count = defaultdict(int)
                    for _, _, _, clone_type in clones:
                        clone_types_count[clone_type] += 1

                    if clone_pairs > 0:
                        for line1, line2, similarity, clone_type in clones:
                            line_numbers = f"{line1} - {line2}"
                            similarity_percentage = f"{similarity * 100:.2f}%"
                            csv_writer.writerow([file_path, line_numbers, similarity_percentage, clone_type])

                        stats_writer.writerow([file_path, clone_pairs] + [clone_types_count[type] for type in ["Type-1 Clone", "Type-2 Clone", "Type-3 Clone", "Type-4 Clone", "Type-5 Clone"]])
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Individual process execution time: {execution_time} seconds")

# find clones between two different files
# from parsed directory
def parsed_detect_clones_files(file_path1, file_path2):
    clones = []
    
    with open(file_path1, 'r', encoding='utf-8', errors='ignore') as file1, open(file_path2, 'r', encoding='utf-8', errors='ignore') as file2:
        code1 = file1.readlines()
        code2 = file2.readlines()

        for i, line1 in enumerate(code1, start=1):
            for j, line2 in enumerate(code2, start=1):
                similarity = difflib.SequenceMatcher(None, line1, line2).ratio()
                clone_type = "Type-1 Clone" if similarity == 1 else None
                clones.append((os.path.basename(file_path1), os.path.basename(file_path2), i, j, similarity, clone_type, line1))

    return clones


def parsed_files_process_directory(directory_path, output_csv, output_txt):
    start_time = time.time()
    with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file, open(output_txt, 'w', encoding='utf-8') as txt_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["File Name 1", "File Name 2", "Line Numbers 1", "Line Numbers 2", "Similarity (%)", "Clone Type", "Code line"])

        type_1_clones = 0

        files = os.listdir(directory_path)
        for i, file1 in enumerate(files):
            for file2 in files[i + 1:]:
                file_path1 = os.path.join(directory_path, file1)
                file_path2 = os.path.join(directory_path, file2)
                clones_parsed = parsed_detect_clones_files(file_path1, file_path2)

                for clone in clones_parsed:
                    _, _, _, _, _, clone_type, _ = clone
                    if clone_type == "Type-1 Clone":
                        file_name1, file_name2, line_numbers1, line_numbers2, similarity, _, code_line = clone
                        similarity_percentage = f"{similarity * 100:.2f}%"
                        csv_writer.writerow([file_name1, file_name2, line_numbers1, line_numbers2, similarity_percentage, clone_type, code_line])
                        type_1_clones += 1

        # Write clone statistics to the text file
        txt_file.write(f"Type-1 Clones: {type_1_clones}\n")

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Files process execution time (parsed): {execution_time} seconds")


# find clones between two different files
# from tokenized directory 
def detect_clones_files(file_path1, file_path2):
    with open(file_path1, 'r', encoding='utf-8', errors='ignore') as file1, open(file_path2, 'r', encoding='utf-8', errors='ignore') as file2:
        code1 = file1.readlines()
        code2 = file2.readlines()

    clones = []
    for i in range(len(code1)):
        for j in range(len(code2)):
            similarity = difflib.SequenceMatcher(None, code1[i], code2[j]).ratio()
            if similarity == 1:
                clone_type = "Type-1 Clone"
            elif similarity > 0.9:
                clone_type = "Type-2 Clone"
            elif similarity > 0.8:
                clone_type = "Type-3 Clone"
            elif similarity > 0.7:
                clone_type = "Type-4 Clone"
            else: 
                clone_type = "Type-5 Clone"
            if similarity > 0.2:  # You can adjust this threshold
                clones.append((os.path.basename(file_path1), os.path.basename(file_path2), i + 1, j + 1, similarity, clone_type))

    return clones

#create csv file to output clone information between two files
#create txt file to output the total number of clone pairs, and clone types in the directory
def files_process_directory(directory_path, output_csv, output_txt):
    start_time = time.time()  # Start time measurement
    with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file, open(output_txt, 'w', encoding='utf-8') as txt_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["File Name 1", "File Name 2", "Line Numbers 1", "Line Numbers 2", "Similarity (%)", "Clone Type"])

        total_clone_pairs = 0
        type_1_clones = 0
        type_2_clones = 0
        type_3_clones = 0
        type_4_clones = 0
        type_5_clones = 0

        for root, _, files in os.walk(directory_path):
            for i in range(len(files)):
                for j in range(i + 1, len(files)):
                    file_path1 = os.path.join(root, files[i])
                    file_path2 = os.path.join(root, files[j])
                    clones_tokenized = detect_clones_files(file_path1, file_path2)

                    if clones_tokenized:
                        total_clone_pairs += len(clones_tokenized)

                        for clone in clones_tokenized:
                            file_name1, file_name2, line_numbers1, line_numbers2, similarity, clone_type = clone
                            similarity_percentage = f"{similarity * 100:.2f}%"
                            csv_writer.writerow([file_name1, file_name2, line_numbers1, line_numbers2, similarity_percentage, clone_type])

                    # Count the different clone types
                    for clone in clones_tokenized:
                        _, _, _, _, _, clone_type = clone
                        if clone_type == "Type-1 Clone":
                            type_1_clones += 1
                        elif clone_type == "Type-2 Clone":
                            type_2_clones += 1
                        elif clone_type == "Type-3 Clone":
                            type_3_clones += 1
                        elif clone_type == "Type-4 Clone":
                            type_4_clones += 1
                        elif clone_type == "Type-5 Clone":
                            type_5_clones += 1


        # Write clone statistics to the text file
        txt_file.write(f"Total Clone Pairs: {type_1_clones+type_2_clones+type_3_clones+type_4_clones+type_5_clones}\n")
        txt_file.write(f"Type-1 Clones: {type_1_clones}\n")
        txt_file.write(f"Type-2 Clones: {type_2_clones}\n")
        txt_file.write(f"Type-3 Clones: {type_3_clones}\n")
        txt_file.write(f"Type-4 Clones: {type_4_clones}\n")
        txt_file.write(f"Type-5 Clones: {type_5_clones}\n")
    end_time = time.time()  # End time measurement
    execution_time = end_time - start_time
    print(f"Files process execution time (tokenized): {execution_time} seconds")


if __name__ == "__main__":
    raw_directory_path = 'parsed_files'
    tokenized_directory_path = 'tokenized_files'

    parsed_small_directory_path = 'parsed_small_file'
    parsed_large_directory_path = 'parsed_large_file'

    tokenized_small_directory_path = 'tokenzied_small_file'
    tokenized_large_directory_path = 'tokenized_large_file'

    indi_clone_csv = 'indi_file_clones.csv'  # Output CSV file for individual clone results
    indi_statistics_csv = 'indi_file_statistics.csv'  # Output CSV file for clone statistics

    raw_output_csv = 'raw_clones.csv'  # Output CSV file for clone results
    raw_output_txt = 'raw_statistics.txt'  # Output TXT file for clone statistics

    small_raw_output_csv = 'small_raw_clones.csv'  # Output CSV file for clone results
    small_raw_output_txt = 'small_raw_statistics.txt'  # Output TXT file for clone statistics

    large_raw_output_csv = 'large_raw_clones.csv'  # Output CSV file for clone results
    large_raw_output_txt = 'large_raw_statistics.txt'  # Output TXT file for clone statistics

    output_csv = 'files_clones.csv'  # Output CSV file for clone results
    output_txt = 'files_statistics.txt'  # Output TXT file for clone statistics

    small_output_csv = 'small_files_clones.csv'  # Output CSV file for clone results
    small_output_txt = 'small_files_statistics.txt'  # Output TXT file for clone statistics

    large_output_csv = 'large_files_clones.csv'  # Output CSV file for clone results
    large_output_txt = 'large_files_statistics.txt'  # Output TXT file for clone statistics


    #small files
    print("Detecting clones from the Small_files dataset...")
    parsed_files_process_directory(parsed_small_directory_path, small_raw_output_csv, small_raw_output_txt)
    files_process_directory(tokenized_small_directory_path, small_output_csv, small_output_txt)
    #large files
    print("Detecting clones from the Large_files dataset...")
    parsed_files_process_directory(parsed_large_directory_path, large_raw_output_csv, large_raw_output_txt)
    files_process_directory(tokenized_large_directory_path, large_output_csv, large_output_txt)
    #whole dataset
    print("Detecting clones from the whole dataset...")
    parsed_files_process_directory(raw_directory_path, raw_output_csv, raw_output_txt)
    individual_process_directory(tokenized_directory_path, indi_clone_csv, indi_statistics_csv)
    files_process_directory(tokenized_directory_path, output_csv, output_txt)
