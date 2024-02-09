import streamlit as st
import pandas as pd
import pubchempy as pcp
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import rdMolDescriptors
import requests


st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

smiles = st.text_input("Enter the SMILES string of the compound", "CCO")

def get_compound_name_from_smiles(smiles):
    try:
        # Search PubChem with the provided SMILES
        compound = pcp.get_compounds(smiles, 'smiles', record_type='3d')[0]

        # Get the compound name
        compound_name = compound.iupac_name

        return compound_name

    except Exception as e:
        print(f"Error: {e}")
        return None

def get_classyfire_info(smiles):
    base_url = "https://structure.gnps2.org/classyfire"
    params = {"smiles": smiles}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad requests
        data = response.json()

        # Check if the response contains the expected keys
        if "inchikey" in data and "superclass" in data:
            inchl_key = data["inchikey"]
            superclass = data["superclass"].get("name", "")
            class_ = data.get("class", {}).get("name", "")
            
            # Check for the presence of 'subclass' key before accessing it
            subclass_data = data.get("subclass", {})
            subclass = subclass_data.get("name", "") if subclass_data else ""

            molecular_framework = data.get("molecular_framework", "")
            pathway = data.get("pathway", "")

            return inchl_key, superclass, class_, subclass, molecular_framework, pathway
        else:
            print("Error: Unexpected response format")
            return "", "", "", "", "", ""

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return "", "", "", "", "", ""

inchi_key, superclass, class_, subclass, molecular_framework, pathway = get_classyfire_info(smiles)

compound = Chem.MolFromSmiles(smiles)
st.image(Draw.MolToImage(compound))

#checking for compound in rdkit. -> returns molecular_name, weight, formula
if compound is not None:
    image = Draw.MolToImage(compound)

    name = compound.GetProp("_Name") if "_Name" in compound.GetPropNames() else "N/A"
    if name is 'N/A':
        name= get_compound_name_from_smiles(smiles)
    
    formula = rdMolDescriptors.CalcMolFormula(compound)
    weight = rdMolDescriptors.CalcExactMolWt(compound)
    
else:
    print("Invalid compound generated from SMILES.")

st.write("Molecular Formula", formula)
st.write("Molecular Weight:", str(round(weight, 2)))

st.write(f"InChIKey: {inchi_key}")
st.write(f"Class: {class_}")
st.write(f"Subclass: {subclass}")
st.write(f"Superclass: {superclass}")
st.write(f"Molecular Framework: {molecular_framework}")

# Check if the compound is valid
