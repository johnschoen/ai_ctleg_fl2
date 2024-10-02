import requests
import logging
from PyPDF2 import PdfReader
from io import BytesIO
import streamlit as st

# Set up logging to capture SSL details
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("requests.packages.urllib3")
logger.setLevel(logging.DEBUG)
logger.propagate = True

# Path to the downloaded SSL certificate chain
CERT_FILE_PATH = 'config/cga_cert_chain.pem.crt'  # Replace with the actual path to your .pem file

def fetch_pdf_content(pdf_url):
    """
    Fetches the PDF document from the provided URL and extracts plain text using SSL verification with a custom certificate.
    """
    try:
        # Use the custom certificate chain for verification
        response = requests.get(pdf_url, verify=CERT_FILE_PATH)  
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching the PDF: {e}")
        logging.error(f"SSL Error or Request Exception: {e}")
        return ""

    # Use PdfReader to read the PDF content
    pdf_reader = PdfReader(BytesIO(response.content))
    text = ""
    for page_num in range(min(5, len(pdf_reader.pages))):  # Limit to the first 5 pages
        page = pdf_reader.pages[page_num]
        text += page.extract_text() + "\n"

    logging.info(f"Successfully fetched PDF content. Length of content: {len(text)} characters.")
    
    return text



# def fetch_pdf_content(pdf_url):
#     """
#     Fetches the PDF document from the provided URL and extracts plain text.
#     """
#     try:
#         # Disable SSL verification temporarily
#         response = requests.get(pdf_url, verify=False)  
#         response.raise_for_status()  # Raise an exception for HTTP errors
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error fetching the PDF: {e}")
#         return ""

#     # Use PdfReader to read the PDF content
#     pdf_reader = PdfReader(BytesIO(response.content))
#     text = ""
#     for page_num in range(min(5, len(pdf_reader.pages))):  # Limit to the first 5 pages
#         page = pdf_reader.pages[page_num]
#         text += page.extract_text() + "\n"

#     return text
