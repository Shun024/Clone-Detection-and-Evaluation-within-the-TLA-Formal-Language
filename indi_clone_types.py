import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
data = pd.read_csv('indi_file_statistics.csv')

# Extracting and shortening the file names
data['Shortened File Name'] = data['File Name'].apply(lambda x: x.split('/')[-1])  # Assuming the file names are paths

# Set 'Shortened File Name' column as index
data.set_index('Shortened File Name', inplace=True)

# Define colors for each clone type
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']  # Change/add colors as needed

# Plotting the bar graph 
fig, ax = plt.subplots(figsize=(12, 6))
clone_types = ['Type-1 Clones', 'Type-2 Clones', 'Type-3 Clones', 'Type-4 Clones', 'Type-5 Clones']

bottom = None
for index, clone_type in enumerate(clone_types):
    bars = ax.bar(data.index, data[clone_type], label=clone_type, bottom=bottom, color=colors[index])
    if bottom is None:
        bottom = data[clone_type]
    else:
        bottom += data[clone_type]

# Setting labels, title, legend, grid, and style
ax.set_xlabel('File Names', fontsize=12)
ax.set_ylabel('Total Number of Clone Types', fontsize=12)
ax.set_title('Clone Types of Each File', fontsize=14)
ax.legend(fontsize=10, loc='upper right')
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(rotation=90)
plt.style.use('seaborn-darkgrid')  # Change the style as desired

plt.tight_layout()
plt.savefig('indi_clone_types.png')
