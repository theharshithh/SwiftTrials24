import streamlit as st
import pandas as pd
import pubchempy as pcp
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import rdMolDescriptors
import requests
import streamlit as st
from PyPDF2 import PdfReader
from io import BytesIO
from openai import OpenAI

from data_management import get_classyfire_info, get_compound_name_from_smiles
from tox_as_api import toxicity_organ_mapping, get_toxicity_data, options
from patient_manage import read_pdf, patient_flag
from complete_tox_report import get_parameters

flag_result ='' 
st.markdown(
    """
    <style>
    .main-title {
        font-size: 36px;
        color: #333;
        margin-bottom: 30px;
        text-align: center;
    }
    .page-container {
        max-width: 800px;
        margin: auto;
        padding: 20px;
    }
    .btn-primary {
        background-color: #007bff;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .btn-primary:hover {
        background-color: #0056b3;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Home page dir; 
def home_page():
    st.title("Swift-Trials v1.0")
    st.markdown("<div class='page-container'>", unsafe_allow_html=True)
    st.write("#### Drug Data:")
    
    smiles_input_key = "smiles_input"  # Unique key for the input field
    smiles = st.text_input("Enter the SMILES string", key=smiles_input_key, placeholder="Eg. CC(=O)OC1=CC=CC=C1C(=O)O")
    search_btn_key = "search_button"  # Unique key for the search button
    if st.button("Search", key='search_btn_key'):
        inchi_key, superclass, class_, subclass, molecular_framework, pathway = get_classyfire_info(smiles)
        compound = Chem.MolFromSmiles(smiles)
        if compound is not None:
            image = Draw.MolToImage(compound)
            name = compound.GetProp("_Name") if "_Name" in compound.GetPropNames() else "N/A"
            if name is 'N/A':
                name= get_compound_name_from_smiles(smiles)
            
            formula = rdMolDescriptors.CalcMolFormula(compound)
            weight = rdMolDescriptors.CalcExactMolWt(compound)
            
            st.image(image)
            st.write("Molecular Formula", formula)
            st.write("Molecular Weight:", str(round(weight, 2)))
            st.write(f"InChIKey: {inchi_key}")
            st.write(f"Class: {class_}")
            st.write(f"Subclass: {subclass}")
            st.write(f"Superclass: {superclass}")
            st.write(f"Molecular Framework: {molecular_framework}")
        else:
            st.write("Invalid compound generated from SMILES.")

def toxicity():
    st.title("Toxicity Report")
    st.markdown("<div class='page-container'>", unsafe_allow_html=True)
    smile_st = st.text_input("Search for Individual Toxicity Parameter", placeholder="SMILE String Eg. CCN")
    toxicity_param = st.selectbox('Select a Parameter:', options)
    if st.button("Submit"):
        st.write(get_toxicity_data(smile_st, toxicity_param))
    st.markdown("</div>", unsafe_allow_html=True)
    complete_report_btn = st.button("Access Complete Report", key="center_aligned_button")
    if(complete_report_btn):
        parameters = get_parameters(smile_st)
        if isinstance(parameters, dict):
            st.write("Properties for the provided SMILES structure:")
            st.table(pd.DataFrame(parameters))
        else:
            st.write(parameters)


def patient_flagging_page():
    st.title("Patient Management")
    st.write("Flagging Patients for Clinical Trails")

    # Collect name and age as inputs
    name = st.text_input('Enter Patient Name:', placeholder='John')
    age = st.number_input('Enter Patient Age:', placeholder='31', max_value=150, step=1)

    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    reviewed_patients = []  # List to store reviewed patient details

    if uploaded_file is not None:
        medical_report = read_pdf(uploaded_file)

        if medical_report is not None:
            st.write("PDF Content:")
            st.write(medical_report)

            patient_details = ''

            if st.button('Submit'):
                result = patient_flag(patient_details, medical_report)
                st.write(result)  # Display the result of patient flagging
                if "True" in result:
                    flag_result = "Eligible"
                elif "False" in result:
                    flag_result = "Ineligible"
                # Append patient details and result to the list
                reviewed_patients.append({"Patient Name": name, "Patient Age": age, "Flagging Result": flag_result ,"Explanation": result })
                
        else:
            st.write("Please upload a valid PDF file.")

    # Display the reviewed patient details in a table below the page
    if reviewed_patients:
        st.write("Reviewed Patient Details:")
        st.table(reviewed_patients)

# Navigation
pages = {
    "Home": home_page,
    "Toxicity Report": toxicity,
    "Patient Flagging": patient_flagging_page
}

selection = st.sidebar.radio("Navigate:", list(pages.keys()))
pages[selection]()
