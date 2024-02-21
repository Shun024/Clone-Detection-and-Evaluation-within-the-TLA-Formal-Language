import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def preprocess_similarity_values(similarity):
    # Remove '%' sign and convert to float
    return float(similarity.strip('%'))

def calculate_stats_per_clone_type(csv_filename):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_filename)

    # Preprocess 'Similarity (%)' column to handle percentage values
    df['Similarity (%)'] = df['Similarity (%)'].apply(preprocess_similarity_values)

    # Group data by Clone Type and calculate similarity, maximum percentage, and minimum percentage for each type
    grouped = df.groupby('Clone Type')['Similarity (%)']
    similarity = grouped.mean().reset_index()
    max_percentage = grouped.max().reset_index()
    min_percentage = grouped.min().reset_index()

    return similarity, max_percentage, min_percentage

def visualize_stats(similarity, max_percentage, min_percentage):
    # Merge dataframes on 'Clone Type'
    merged = similarity.merge(max_percentage, on='Clone Type', suffixes=('_mean', '_max')).merge(min_percentage, on='Clone Type')

    # Plot the results using Seaborn
    plt.figure(figsize=(10, 6))
    sns.set(style='whitegrid')
    sns.barplot(x='Similarity (%)_mean', y='Clone Type', data=merged, color='skyblue', label='Average Similarity')
    sns.scatterplot(x='Similarity (%)_max', y='Clone Type', data=merged, color='red', label='Max Similarity', s=100)
    sns.scatterplot(x='Similarity (%)', y='Clone Type', data=merged, color='green', label='Min Similarity', s=100)
    plt.xlabel('Similarity (%)')
    plt.ylabel('Clone Type')
    plt.title('Clone Type Similarity Stats')
    plt.legend()
    plt.tight_layout()

    plt.savefig('cloneType%_graph.png')

csv_file = 'files_clones.csv'

# Calculate similarity, max percentage, and min percentage of each clone type
similarity, max_percentage, min_percentage = calculate_stats_per_clone_type(csv_file)

# Visualize the stats
visualize_stats(similarity, max_percentage, min_percentage)
