import pandas as pd

# Read the CSV file with specified encoding
df = pd.read_csv('Dataset.csv', encoding='latin1')

# Define a function to count non-empty values
def count_non_empty(series):
    counts = series.value_counts()
    if '' in counts.index:
        del counts['']
    return counts

# Calculate frequency of each field
frequency_source = count_non_empty(df['Source'])
frequency_link = count_non_empty(df['Link'])
frequency_actor = count_non_empty(df['Actor'])
frequency_tactic_id = count_non_empty(df['Tactic ID'])
frequency_tactic_name = count_non_empty(df['Tactic Name'])
frequency_technique_id = count_non_empty(df['Technique ID'])
frequency_technique = count_non_empty(df['Technique'])
frequency_subtechnique_id = count_non_empty(df['Sub-technique ID'])
frequency_subtechnique_name = count_non_empty(df['Sub-Technique Name'])

# Print the frequencies
print("Frequency of Source:")
print(frequency_source)
print("\nFrequency of Link:")
print(frequency_link)
print("\nFrequency of Actor:")
print(frequency_actor)
print("\nFrequency of Tactic ID:")
print(frequency_tactic_id)
print("\nFrequency of Tactic Name:")
print(frequency_tactic_name)
print("\nFrequency of Technique ID:")
print(frequency_technique_id)
print("\nFrequency of Sub-technique ID:")
print(frequency_subtechnique_id)
print("\nFrequency of Sub-Technique Name:")
print(frequency_subtechnique_name)


# Count the number of unique values in the 'Link' column
num_unique_links = df['Link'].nunique()

# Print the result
print("Number of different advisories:", num_unique_links)
