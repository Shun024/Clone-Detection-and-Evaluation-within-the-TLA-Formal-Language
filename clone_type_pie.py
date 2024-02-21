import matplotlib.pyplot as plt

def clone_type_pie(parsed_stats, tokenized_stats, png_image):
	# Read content from file1.txt
	with open(parsed_stats, 'r') as file1:
	    lines_file1 = file1.readlines()

	# Read content from file2.txt
	with open(tokenized_stats, 'r') as file2:
	    lines_file2 = file2.readlines()

	# Extracting Type-1 Clones values from both files
	type1_file1 = int(lines_file1[0].split(': ')[1].strip())
	type1_file2 = int(lines_file2[1].split(': ')[1].strip())

	# Extracting Type-2 to Type-5 Clones values from file2
	type2_file2 = int(lines_file2[2].split(': ')[1].strip())
	type3_file2 = int(lines_file2[3].split(': ')[1].strip())
	type4_file2 = int(lines_file2[4].split(': ')[1].strip())
	type5_file2 = int(lines_file2[5].split(': ')[1].strip())

	#calculate percentage for legend
	total= type1_file1 + type1_file2 + type2_file2 + type3_file2 + type4_file2 + type5_file2
	t1f1_percentage = type1_file1 / total * 100
	t1f2_percentage = type1_file2 / total * 100
	t2f2_percentage = type2_file2 / total * 100
	t3f2_percentage = type3_file2 / total * 100
	t4f2_percentage = type4_file2 / total * 100
	t5f2_percentage = type5_file2 / total * 100

	# Creating data for the pie chart
	labels = ['Raw Type-1 Clones', 'Tokenized Type-1 Clones', 'Tokenized Type-2 Clones', 'Tokenized Type-3 Clones', 'Tokenized Type-4 Clones', 'Tokenized Type-5 Clones']
	sizes = [type1_file1, type1_file2, type2_file2, type3_file2, type4_file2, type5_file2]
	percentages = [t1f1_percentage, t1f2_percentage, t2f2_percentage, t3f2_percentage, t4f2_percentage, t5f2_percentage] 
	colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'orange', 'pink']
	explode = (0.1, 0, 0, 0, 0, 0)  # explode the 1st slice (Type-1 Clones from File1)

	# Plotting the pie chart
	plt.figure(figsize=(12, 6))
	patches, texts, _ = plt.pie(sizes, explode=explode, labels=None, colors=colors, autopct='%1.2f%%', startangle=140, pctdistance=1)
	plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
	plt.title('Distribution of Clones')
	plt.tight_layout()

	# Create legend with labels and percentages
	legend_labels = [f'{label}: {percentages:.2f}% ({sizes[i]})' for i, label, size, percentages in zip(range(len(labels)), labels, sizes, percentages)]
	plt.legend(patches, legend_labels, loc="best", bbox_to_anchor=(1, 0.5), title="Clone Types", fontsize='small')

	# Save the plot as an image file
	plt.savefig(png_image)

clone_type_pie('small_raw_statistics.txt', 'small_files_statistics.txt', 'small_clone_type_pie.png')
clone_type_pie('large_raw_statistics.txt', 'large_files_statistics.txt', 'large_clone_type_pie.png')
clone_type_pie('raw_statistics.txt', 'files_statistics.txt', 'whole_clone_type_pie.png')
