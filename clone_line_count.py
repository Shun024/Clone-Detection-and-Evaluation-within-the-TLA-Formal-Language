import os
import csv

def find_duplicate_lines(directory):
    files = [file for file in os.listdir(directory) if file.endswith('.tla')]
    lines_count = {}
    
    for file in files:
        filepath = os.path.join(directory, file)
        with open(filepath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.strip():  # Ignore empty lines
                    line_key = line.strip()  # Use the line as the key
                    if line_key not in lines_count:
                        lines_count[line_key] = {'Count': 1, 'Files': [file]}
                    else:
                        lines_count[line_key]['Count'] += 1
                        if file not in lines_count[line_key]['Files']:
                            lines_count[line_key]['Files'].append(file)
    
    # Writing to CSV
    with open('duplicate_lines.csv', 'w', newline='') as csvfile:
        fieldnames = ['Line', 'Count', 'Files']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for line, data in lines_count.items():
            if data['Count'] > 1:  # Lines with count greater than 1 are duplicates
                writer.writerow({'Line': line, 'Count': data['Count'], 'Files': ', '.join(data['Files'])})

directory_path = 'parsed_files'
find_duplicate_lines(directory_path)
