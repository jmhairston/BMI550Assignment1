#JHairston Assignment 1

from collections import defaultdict
import pandas as pd
import csv
import re

# Input and output file names
input_excel_file = '/Users/jmhairston/Desktop/Education/PhD/Fall 2023/BMI 550/Provided Files/UnlabeledSet.xlsx'
output_csv_file = '/Users/jmhairston/Desktop/Education/PhD/Fall 2023/BMI 550'
symptoms_file = '/Users/jmhairston/Desktop/Education/PhD/Fall 2023/BMI 550/Provided Files/COVID-Twitter-Symptom-Lexicon.txt'

# Read the list of symptoms from the text file
with open(symptoms_file, 'r') as symptoms_file:
    symptoms_list = [line.strip() for line in symptoms_file]

# List of negated terms for matching
negation_list = ["no", "not", "without", "negative", "absent"]

# RegExs for exact and inexact matching
exact_match_patterns = [re.escape(symptom) for symptom in symptoms_list]
inexact_match_patterns = [re.escape(negation) + r"\s+" + re.escape(symptom) for negation in negation_list for symptom in symptoms_list]

# Function to detect symptoms and negated symptoms in text
def detect_concepts(text):
    detected_entities = []
    
    # Initialize variables for symptoms and negations
    symptoms = []
    negations = []
    
    # Exact matching
    for pattern in exact_match_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            symptoms.append(pattern)
    
    # Inexact matching
    for pattern in inexact_match_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            negations.append(pattern)
    
    # Create strings for symptoms and negations, separated by '$$$'
    symptoms_str = '$$$'.join(symptoms)
    negations_str = '$$$'.join(negations)
    
    return symptoms_str, negations_str

# Read the Excel file into a DataFrame
df = pd.read_excel(input_excel_file)

# Create a list to store the processed data
processed_data = []

# Process each row in the DataFrame
for idx, row in df.iterrows():
    if pd.notnull(row['text']):  # Assuming the text is in the 'text' column
        post_text = row['text']
        symptoms, negations = detect_concepts(post_text)
        processed_data.append([idx + 1, post_text, symptoms, negations])

# Convert the processed data to a DataFrame
output_df = pd.DataFrame(processed_data, columns=['id', 'text', 'symptom', 'negation'])

# Save the output DataFrame to a CSV file
output_df.to_csv(output_csv_file, index=False)

print(f"Concepts detected and written to {output_csv_file}")
