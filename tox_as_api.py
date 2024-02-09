import pandas as pd

options = [
    'Human Intestinal Absorption',
    'Caco-2',
    'Blood Brain Barrier',
    'Human oral bioavailability',
    'Subcellular localzation',
    'OATP2B1 inhibitior',
    'OATP1B1 inhibitior',
    'OATP1B3 inhibitior',
    'MATE1 inhibitior',
    'OCT2 inhibitior',
    'BSEP inhibitior',
    'P-glycoprotein inhibitior',
    'P-glycoprotein substrate',
    'CYP3A4 substrate',
    'CYP2C9 substrate',
    'CYP2D6 substrate',
    'CYP3A4 inhibition',
    'CYP2C9 inhibition',
    'CYP2C19 inhibition',
    'CYP2D6 inhibition',
    'CYP1A2 inhibition',
    'CYP2C8 inhibition',
    'CYP inhibitory promiscuity',
    'UGT catelyzed',
    'Carcinogenicity (binary)',
    'Carcinogenicity (trinary)',
    'Eye corrosion',
    'Eye irritation',
    'Skin irritation',
    'Skin corrosion',
    'Ames mutagenesis',
    'Human Ether-a-go-go-Related Gene inhibition',
    'Micronuclear',
    'Hepatotoxicity',
    'skin sensitisation',
    'Respiratory toxicity',
    'Reproductive toxicity',
    'Mitochondrial toxicity',
    'Nephrotoxicity',
    'Acute Oral Toxicity (c)',
    'Estrogen receptor binding',
    'Androgen receptor binding',
    'Thyroid receptor binding',
    'Glucocorticoid receptor binding',
    'Aromatase binding',
    'PPAR gamma',
    'Honey bee toxicity',
    'Biodegradation',
    'Crustacea aquatic toxicity',
    'Fish aquatic toxicity',
    'Water solubility',
    'Plasma protein binding',
    'Acute Oral Toxicity',
    'Tetrahymena pyriformis'
]

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(r'tox-ultimate.csv')

# Define the dictionary mapping toxicity to organ and category
toxicity_organ_mapping = {
    'Human Intestinal Absorption': {'category': 'PKA/PKD', 'organ': 'Intestine'},
    'Caco-2': {'category': 'PKA/PKD', 'organ': 'Intestine'},
    'Blood Brain Barrier': {'category': 'PKA/PKD', 'organ': 'Brain'},
    'Human oral bioavailability': {'category': 'PKA/PKD', 'organ': 'Oral cavity'},
    'Subcellular localization': {'category': 'PKA/PKD', 'organ': 'Cellular level'},
    'OATP2B1 inhibitor': {'category': 'PKA/PKD', 'organ': 'Liver'},
    'OATP1B1 inhibitor': {'category': 'PKA/PKD', 'organ': 'Liver'},
    'OATP1B3 inhibitor': {'category': 'PKA/PKD', 'organ': 'Liver'},
    'MATE1 inhibitor': {'category': 'PKA/PKD', 'organ': 'Kidney'},
    'OCT2 inhibitor': {'category': 'PKA/PKD', 'organ': 'Kidney'},
    'BSEP inhibitor': {'category': 'PKA/PKD', 'organ': 'Liver'},
    'P-glycoprotein inhibitor': {'category': 'PKA/PKD', 'organ': 'Liver'},
    'P-glycoprotein substrate': {'category': 'PKA/PKD', 'organ': 'Liver'},
    'CYP3A4 substrate': {'category': 'PKA/PKD', 'organ': 'Liver'},
    'CYP2C9 substrate': {'category': 'PKA/PKD', 'organ': 'Liver'},
    'CYP2D6 substrate': {'category': 'PKA/PKD', 'organ': 'Liver'},
    'CYP3A4 inhibition': {'category': 'PKA/PKD', 'organ': 'Liver'},
    'CYP2C9 inhibition': {'category': 'PKA/PKD', 'organ': 'Liver'},
    'CYP2C19 inhibition': {'category': 'PKA/PKD', 'organ': 'Liver'},
    'CYP2D6 inhibition': {'category': 'PKA/PKD', 'organ': 'Liver'},
    'CYP1A2 inhibition': {'category': 'PKA/PKD', 'organ': 'Liver'},
    'CYP2C8 inhibition': {'category': 'PKA/PKD', 'organ': 'Liver'},
    'CYP inhibitory promiscuity': {'category': 'PKA/PKD', 'organ': 'Liver'},
    'UGT catalyzed': {'category': 'PKA/PKD', 'organ': 'Liver'},
    'Estrogen receptor binding': {'category': 'Toxicity', 'organ': 'Reproductive system'},
    'Androgen receptor binding': {'category': 'Toxicity', 'organ': 'Reproductive system'},
    'Thyroid receptor binding': {'category': 'Toxicity', 'organ': 'Thyroid'},
    'Glucocorticoid receptor binding': {'category': 'Toxicity', 'organ': 'Adrenal glands'},
    'Aromatase binding': {'category': 'Toxicity', 'organ': 'Reproductive system'},
    'PPAR gamma': {'category': 'Toxicity', 'organ': 'Adipose tissue'},
    'Biodegradation': {'category': 'Toxicity', 'organ': 'Environmental'},
    'Water solubility': {'category': 'Toxicity', 'organ': 'Environmental'},
    'Plasma protein binding': {'category': 'Toxicity', 'organ': 'Blood'},
    'Tetrahymena pyriformis': {'category': 'Toxicity', 'organ': 'Aquatic organism'},
    'Carcinogenicity (binary)': {'category': 'Toxicity', 'organ': 'General'},
    'Carcinogenicity (trinary)': {'category': 'Toxicity', 'organ': 'General'},
    'Eye corrosion': {'category': 'Toxicity', 'organ': 'Eye'},
    'Eye irritation': {'category': 'Toxicity', 'organ': 'Eye'},
    'Skin irritation': {'category': 'Toxicity', 'organ': 'Skin'},
    'Skin corrosion': {'category': 'Toxicity', 'organ': 'Skin'},
    'Ames mutagenesis': {'category': 'Toxicity', 'organ': 'General'},
    'Human Ether-a-go-go-Related Gene inhibition': {'category': 'Toxicity', 'organ': 'Heart'},
    'Micronuclear': {'category': 'Toxicity', 'organ': 'General'},
    'Hepatotoxicity': {'category': 'Toxicity', 'organ': 'Liver'},
    'Skin sensitization': {'category': 'Toxicity', 'organ': 'Skin'},
    'Respiratory toxicity': {'category': 'Toxicity', 'organ': 'Lungs'},
    'Reproductive toxicity': {'category': 'Toxicity', 'organ': 'Reproductive system'},
    'Mitochondrial toxicity': {'category': 'Toxicity', 'organ': 'Cellular level'},
    'Nephrotoxicity': {'category': 'Toxicity', 'organ': 'Kidney'},
    'Acute Oral Toxicity (c)': {'category': 'Toxicity', 'organ': 'General'},
    'Honey bee toxicity': {'category': 'Toxicity', 'organ': 'Insects'},
    'Crustacea aquatic toxicity': {'category': 'Toxicity', 'organ': 'Aquatic organism'},
    'Fish aquatic toxicity': {'category': 'Toxicity', 'organ': 'Aquatic organism'},
    'ADMET predicted profile --- Regressions': {'category': 'Toxicity', 'organ': 'General'},
    'Acute Oral Toxicity': {'category': 'Toxicity', 'organ': 'General'},
}

def get_toxicity_data(smiles, toxicity_name):
    # Filter the DataFrame based on the SMILES structure and toxicity name
    filtered_df = df[(df['SMILES'] == smiles) & (df['Toxicity '] == toxicity_name)]

    # Check if any data matches the provided SMILES structure and toxicity name
    if filtered_df.empty:
        return f"No data found for the provided SMILES structure '{smiles}' and toxicity '{toxicity_name}'."

    # Extract the probability of the specified toxicity
    sign = filtered_df['Effect'].iloc[0]
    probability = filtered_df['Probability'].iloc[0]
    if sign == '+':
        flag = 'Toxic'
    else:
        flag = 'Safe'
    # Get the organ affected by the toxicity
    organ = toxicity_organ_mapping[toxicity_name]['organ']

    check_patient = f"The probability of '{toxicity_name}' for the structure '{smiles}' is {probability}. This toxicity affects the {organ}. It is {flag}"
    return check_patient 


output_data = get_toxicity_data("CCCCOC(=O)C=C", "Blood Brain Barrier")
print(output_data)

