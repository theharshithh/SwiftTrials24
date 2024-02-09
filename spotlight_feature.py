import streamlit as st
import keyboard
import time

st.set_page_config(page_title="Mapping Demo", page_icon="🔍")


st.title("Spotlight Search")
st.write("Press CTRL + M to activate the spotlight search")

def check_for_keypress():
    if keyboard.is_pressed('ctrl+m'):
        print("Log Detected")  # Log to terminal
        st.text_input("Spotlight Search", placeholder="Search Anything you want: Eg. LD50 of Aspirin?")  # Log to Streamlit

while True:
    with st.empty():
        check_for_keypress()
    time.sleep(0.1)  # Adjust polling interval as needed
    
