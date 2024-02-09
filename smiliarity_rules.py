import pandas as pd

#swissadme similarity rules

df = pd.read_csv(r'swissadme.csv')

def get_parameters(smiles):
    # Filter the DataFrame based on the SMILES structure
    match = df[df['Canonical SMILES'] == smiles]

    # Check if any data matches the provided SMILES structure
    if match.empty:
        return "No data found for the provided SMILES structure."

    # Extract parameters for the matching SMILES structure
    parameters = match.iloc[0]  # Assuming there's only one match
    return parameters

# Take input SMILES structure from the user
input_smiles = input("Enter the SMILES structure: ")

# Get and print the corresponding parameters
parameters = get_parameters(input_smiles)
print(parameters)