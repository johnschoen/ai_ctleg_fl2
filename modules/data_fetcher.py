import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import streamlit as st

# Base URL used for relative PDF URLs
PDF_BASE_URL = "https://www.cga.ct.gov"

# Base URL used to construct the committee page URL
BASE_URL = "https://www.cga.ct.gov/asp/menu/CommDocList.asp"

def construct_document_url(committee_code, document_type_code):
    """
    Constructs the URL for fetching documents based on the committee and document type.
    """
    return f"{BASE_URL}?comm_code={committee_code}&doc_type={document_type_code}"

def fetch_document_list_selenium(url):
    """
    Fetches the list of documents (e.g., PDFs) from the URL using Selenium with enhanced debugging.
    """
    options = uc.ChromeOptions()
    options.headless = True
    driver = uc.Chrome(options=options)

    try:
        st.write(f"Opening URL: {url}")

        # Open the webpage
        driver.get(url)

        # Wait for the page to fully load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        st.write("Page loaded successfully.")

        # Fetch all PDF links using the correct XPath
        document_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf')]")

        if not document_elements:
            st.write("Debug: No PDF links found on the page.")
            return []

        documents = []
        date_pattern = r'\d{4}'  # Pattern to look for a year in the title

        # Fetch document titles and URLs
        for element in document_elements:
            doc_title = element.text.strip()
            doc_url = element.get_attribute('href')

            # Ensure relative URLs are resolved correctly
            if doc_url.startswith("/"):
                doc_url = PDF_BASE_URL + doc_url

            if re.search(date_pattern, doc_title):
                documents.append((doc_title, doc_url))

        if not documents:
            st.write("Debug: No documents found after filtering by date.")
        else:
            st.write(f"Debug: {len(documents)} documents found with dates.")
        
        return documents

    except Exception as e:
        st.write(f"An error occurred while fetching documents: {e}")
        return []

    finally:
        driver.quit()
