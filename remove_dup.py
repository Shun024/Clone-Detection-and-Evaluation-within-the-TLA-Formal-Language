import os
import filecmp

def find_duplicate_files(directory):
    # Dictionary to store file contents and their paths
    files_by_content = {}

    # Walk through the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            # Check if the file is not a directory
            if os.path.isfile(filepath):
                # Read the file content
                with open(filepath, 'rb') as f:
                    content = f.read()
                # Check if content already exists in dictionary
                if content in files_by_content:
                    files_by_content[content].append(filepath)
                else:
                    files_by_content[content] = [filepath]

    # Filter out files with the same content and delete them
    removed_files_log = []  # List to store names of removed files
    for content, file_paths in files_by_content.items():
        if len(file_paths) > 1:
            for i in range(1, len(file_paths)):
                removed_file = file_paths[i]
                os.remove(removed_file)
                removed_files_log.append(removed_file)

    # Write the names of removed files to a log file outside the directory
    log_file_path = os.path.join(os.path.dirname(directory), 'removed_files_log.txt')
    with open(log_file_path, 'w') as log_file:
        log_file.write("List of Removed Files:\n")
        log_file.write("\n".join(removed_files_log))

directory_path = 'parsed_files'
find_duplicate_files(directory_path)
