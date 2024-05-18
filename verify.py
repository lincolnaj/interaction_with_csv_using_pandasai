import pandas as pd

# Read the CSV file with specified encoding
df = pd.read_csv('Dataset.csv', encoding='latin1')

# Define a function to count non-empty values
def count_non_empty(series):
    counts = series.value_counts()
    if '' in counts.index:
        del counts['']
    return counts

# Count the number of unique values in the 'Link' column
num_unique_links = df['Link'].nunique()

# Print the result
print("Number of different advisories:", num_unique_links)

# Calculate frequency of each field
frequency_source = count_non_empty(df['Source']).reset_index()
frequency_source.columns = ['Source', 'Count']

frequency_actor = count_non_empty(df['Actor']).reset_index()
frequency_actor.columns = ['Actor', 'Count']

frequency_tactic_id = count_non_empty(df['Tactic ID']).reset_index()
frequency_tactic_id.columns = ['Tactic ID', 'Count']

frequency_tactic_name = count_non_empty(df['Tactic Name']).reset_index()
frequency_tactic_name.columns = ['Tactic Name', 'Count']

frequency_technique_id = count_non_empty(df['Technique ID']).reset_index()
frequency_technique_id.columns = ['Technique ID', 'Count']

frequency_technique = count_non_empty(df['Technique']).reset_index()
frequency_technique.columns = ['Technique', 'Count']

frequency_subtechnique_id = count_non_empty(df['Sub-technique ID']).reset_index()
frequency_subtechnique_id.columns = ['Sub-technique ID', 'Count']

frequency_subtechnique_name = count_non_empty(df['Sub-Technique Name']).reset_index()
frequency_subtechnique_name.columns = ['Sub-Technique Name', 'Count']

# Combine all frequency DataFrames into one
combined_frequencies = pd.concat([
    frequency_source,
    frequency_actor,
    frequency_tactic_id,
    frequency_tactic_name,
    frequency_technique_id,
    frequency_technique,
    frequency_subtechnique_id,
    frequency_subtechnique_name
], axis=1)

# Save the combined frequencies to a single CSV file
combined_frequencies.to_csv('verify_results.csv', index=False)

# Print the combined frequencies
print("\nCombined Frequencies:")
print(combined_frequencies)
