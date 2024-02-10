import streamlit as st
from PyPDF2 import PdfReader
from io import BytesIO
from openai import OpenAI
from dotenv import dotenv_values


env_vars = dotenv_values('.env')

def read_pdf(uploaded_file):
    if uploaded_file is not None:
        pdf_content = uploaded_file.read()
        pdf_stream = BytesIO(pdf_content)  # Wrap the bytes content in a BytesIO object
        pdf_reader = PdfReader(pdf_stream)
        
        text_content = ""
        for page in pdf_reader.pages:
            text_content += page.extract_text()

        return text_content
    return None
flag_result = ""
# Your other functions remain unchanged
def patient_flag(patient_details, medical_report):
    api_key = env_vars['API_KEY']
    client = OpenAI(api_key=api_key)
    instructions = """I want u to act like a simple flagging bot. Lets keep it simple. I will share with you a medical report or a patient's condition, and I need u to give me the following thing: True if the patient is fit for the medical trials, false if the patient is not fit for the medical trials.
    Here is a reference of Vital Data: Patient ID,Age,Sex,Temperature,Heart Beat,Respiratory Rate,Systolic BP,Diastolic BP,Oxygen Saturation\n1,29,M,98.6,72,16,120,80,98\n2,34,F,96.9,75,14,115,75,99\n3,45,M,98.4,70,18,110,70,97\n4,26,F,97.8,78,16,118,76,98\n5,37,M,97.1,72,15,120,80,96\n6,50,F,98.6,74,16,122,82,97\n7,32,M,97.7,68,14,115,78,99\n8,28,F,98.5,76,18,117,75,98\n9,41,M,98.6,70,17,119,79,96\n10,28,M,97.06,72,16,120,80,98\n
        These are considered baseline data. If I give u a medical report/patient's health vitals. For it being true, the input values should be within the range of the baseline data. If the input values are not within the range, then it should be flagged as FALSE(if false, tell me why false- KEEP IT SHORT). If the input values are within the range, but not exactly the same, then it should be flagged as NEUTRAL."""

    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": instructions
                },
                {
                    "role": "user",
                    "content": ""
                },
                {
                    "role": "assistant",
                    "content": "Okay, I will give u True or False"
                },
                {
                    "role": "user",
                    "content": f"{patient_details}\n{medical_report}"
                },
            ],
            temperature=1,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
    response_message = response.choices[0].message.content
    
    return response_message


def main():
    st.title("Simple Web Portal")
    st.write("Welcome to the web portal!")

    # Collect name and age as inputs
    name = st.text_input('Enter Patient Name:')
    age = st.number_input('Enter Patient Age:', min_value=0, max_value=150, step=1)

    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    reviewed_patients = []  # List to store reviewed patient details

    if uploaded_file is not None:
        medical_report = read_pdf(uploaded_file)

        if medical_report is not None:
            st.write("PDF Content:")
            st.write(medical_report)

            patient_details = st.text_input('Enter Patient Details: ')

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

if __name__ == "__main__":
    main()