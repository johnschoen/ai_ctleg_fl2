from flask import Flask, render_template, request, session
from modules.data_fetcher import fetch_document_list_selenium, construct_document_url
from modules.pdf_handler import fetch_pdf_content
from config.config import COMMITTEES, DOCUMENT_TYPES

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session handling

# Single route for handling everything
@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize variables to track state
    selected_committee = None
    selected_document_type = None
    documents = None
    selected_pdf_content = None

    # Step 1: User selects committee and document type
    if request.method == 'POST':
        # Check if the user selected the committee and document type
        if 'fetch_pdfs' in request.form:
            selected_committee = request.form.get('committee')
            selected_document_type = request.form.get('document_type')

            # Store the selections in session
            session['selected_committee'] = selected_committee
            session['selected_document_type'] = selected_document_type

            # Fetch the PDFs based on the selection
            committee_code = COMMITTEES[selected_committee]
            document_code = DOCUMENT_TYPES[selected_document_type]
            document_url = construct_document_url(committee_code, document_code)

            documents = fetch_document_list_selenium(document_url)

            # Store the documents list in session for future use
            session['documents'] = documents

        # Step 2: User selects a PDF
        elif 'view_pdf' in request.form:
            selected_document = request.form.get('document')
            session['selected_document'] = selected_document

            # Retrieve the previously fetched documents from session
            documents = session.get('documents', [])

            # Find the selected document URL
            selected_pdf_url = next(doc[1] for doc in documents if doc[0] == selected_document)

            # Fetch the PDF content
            selected_pdf_content = fetch_pdf_content(selected_pdf_url)

    return render_template(
        'index.html',
        committees=COMMITTEES,
        document_types=DOCUMENT_TYPES,
        documents=documents,
        selected_pdf_content=selected_pdf_content
    )

if __name__ == '__main__':
    app.run(debug=True)
