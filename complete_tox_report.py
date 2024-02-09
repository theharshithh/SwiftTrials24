import streamlit as st
import pandas as pd

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(r'tox-ultimate.csv')

def get_parameters(smiles):
    # Filter the DataFrame based on the SMILES structure
    matches = df[df['SMILES'] == smiles]

    # Check if any data matches the provided SMILES structure
    if matches.empty:
        return "No data found for the provided SMILES structure."

    # Extract parameters for the matching SMILES structures
    parameters_dict = {}

    for index, row in matches.iterrows():
        for key, value in row.items():
            if key != 'SMILES':
                if len(parameters_dict.get(key, [])) < 54:
                    if key not in parameters_dict:
                        parameters_dict[key] = [value]
                    else:
                        parameters_dict[key].append(value)

    return parameters_dict

def main():
    st.title("Toxicity Report")

    # Take input SMILES structure from the user
    input_smiles = st.text_input("Enter the SMILES structure:")

    # Get and print the corresponding parameters
    parameters = get_parameters(input_smiles)
    if isinstance(parameters, dict):
        st.write("Properties for the provided SMILES structure:")
        st.table(pd.DataFrame(parameters))
    else:
        st.write(parameters)

if __name__ == "__main__":
    main()
