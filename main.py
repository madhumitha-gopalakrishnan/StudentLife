# Importing all the required libraries
import streamlit as st
import importlib

st.title('Dart Uni Dashboard')
st.header('Click a page to learn more')

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