import os

# Directory containing the files
directory = 'files'

# Function to rename files with IDs and a specified extension
def rename_files_with_ids(directory, extension='tla'):
    # Get all files in the directory
    files = os.listdir(directory)

    # Initialize an ID counter
    id_counter = 1

    # Open a text file to log the renaming process
    log_file = open('renaming_log.txt', 'w')

    # Iterate through each file in the directory
    for filename in files:
        # Check if the file is a regular file
        if os.path.isfile(os.path.join(directory, filename)):
            # Construct the new file name with ID and extension
            new_filename = f"{id_counter:04d}.{extension}"  # Adjust the format as needed
            id_counter += 1

            # Rename the file
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
            
            # Write the renaming information to the log file
            log_file.write(f"Renamed {filename} to {new_filename}\n")
    
    # Close the log file
    log_file.close()

# Call the function to rename files in the specified directory
rename_files_with_ids(directory)
