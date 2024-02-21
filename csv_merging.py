import pandas as pd

# Read the first CSV file
file1 = pd.read_csv('tokenized_line_count.csv')

# Read the second CSV file
file2 = pd.read_csv('indi_file_statistics.csv')

# Extract filenames from the second file and remove the text before '/'
file2['File Name'] = file2['File Name'].apply(lambda x: x.split('/')[-1])

# Merge the two dataframes on the 'filename' column
merged_df = pd.merge(file1, file2, on='File Name', how='left')

# Fill NaN values with 0 for columns from the second file
merged_df = merged_df.fillna(0)

# Convert relevant columns to integers
integer_columns = ['Clone Pairs', 'Type-1 Clones', 
                   'Type-2 Clones', 'Type-3 Clones', 
                   'Type-4 Clones', 'Type-5 Clones']

merged_df[integer_columns] = merged_df[integer_columns].astype(int)

# Sort the dataframe by 'number_of_code_lines' in descending order
merged_df = merged_df.sort_values(by='Line Count', ascending=False)

# Reorder columns as per the requirement
merged_df = merged_df[['File Name', 'Line Count', 'Clone Pairs', 'Type-1 Clones', 
                   'Type-2 Clones', 'Type-3 Clones', 
                   'Type-4 Clones', 'Type-5 Clones']]

# Save the result to a new CSV file
merged_df.to_csv('merged_result.csv', index=False)
