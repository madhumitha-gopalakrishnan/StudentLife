# Importing all the required libraries
import streamlit as st
import importlib

st.title('Dart Uni Dashboard')
st.write("This dashboard will give you a comprehensive view of what is happening in your class. You can view student's activities on Piazza and their wellbeing to prvoide the necessary interventions if and when required.")
# Dictionary of pages
pages = {
    "Learn more about the Piazza Activity": "piazza",
    "How are the students doing?": "wellbeing",
        }

# Sidebar selection
page = st.selectbox("Select a page to learn more", options=list(pages.keys()))

# Import the selected page module and call its show function
if page:
    page_module = importlib.import_module(pages[page])
    page_module.show()