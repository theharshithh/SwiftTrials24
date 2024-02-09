import streamlit as st
import pandas as pd

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(r'TEST_Database.csv')

def get_parameters(smiles):
    # Filter the DataFrame based on the SMILES structure
    match = df[df['SmilesRan'] == smiles]

    # Check if any data matches the provided SMILES structure
    if match.empty:
        return "No data found for the provided SMILES structure."

    # Extract parameters for the matching SMILES structure
    parameters = match.iloc[0]  # Assuming there's only one match
    return parameters

def main():
    st.title("SMILES Data Lookup")

    # Input SMILES structure
    smiles_input = st.text_input("Enter SMILES structure:")

    if st.button("Submit"):
        # Get and print the corresponding parameters
        parameters = get_parameters(smiles_input)
        st.write(parameters)

if __name__ == "__main__":
    main()