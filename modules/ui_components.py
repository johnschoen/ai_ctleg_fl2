# modules/ui_components.py

import streamlit as st

def create_radio_buttons(document_titles, document_code):
    return st.radio("Select a document", document_titles, key=f"document_radio_{document_code}")

def display_pdf_content(pdf_text):
    if pdf_text:
        st.text_area("Document Content (First 50 Lines)", pdf_text[:5000], height=400)
    else:
        st.write("Failed to fetch or read the PDF content.")
