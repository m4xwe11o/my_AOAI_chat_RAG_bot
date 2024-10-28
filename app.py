import logging
from flask import Flask, render_template, request, jsonify
import openai
import os
from azure.storage.blob import BlobServiceClient
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Azure Blob Storage configuration
AZURE_BLOB_CONNECTION_STRING = os.getenv("AZURE_BLOB_CONNECTION_STRING")
AZURE_BLOB_CONTAINER = os.getenv("AZURE_BLOB_CONTAINER")

# Azure OpenAI configuration
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

# Azure Search configuration
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
AZURE_SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME")

# Set the API key for OpenAI
openai.api_key = AZURE_OPENAI_API_KEY
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"

# Initialize Azure Search client
search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX_NAME,
    credential=AzureKeyCredential(AZURE_SEARCH_API_KEY)
)

# Initialize Azure Blob Storage client
blob_service_client = BlobServiceClient.from_connection_string(AZURE_BLOB_CONNECTION_STRING)
blob_container_client = blob_service_client.get_container_client(AZURE_BLOB_CONTAINER)

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    # Render the index.html page
    return render_template('index.html')

# Helper function to check if the file is a PDF
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

# Route to handle document upload to Azure Blob Storage
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        blob_client = blob_container_client.get_blob_client(blob=filename)
        
        try:
            blob_client.upload_blob(file.stream, blob_type="BlockBlob", overwrite=True)
            logging.debug(f"File {filename} uploaded to Azure Blob Storage successfully.")
            return jsonify({"message": "File uploaded successfully"}), 200
        except Exception as e:
            logging.error(f"Failed to upload {filename} to Azure Blob Storage: {str(e)}")
            return jsonify({"error": f"Failed to upload file: {str(e)}"}), 500
    else:
        return jsonify({"error": "Invalid file type, only PDF is allowed"}), 400

# Route to list files in the Azure Blob Storage container
@app.route('/list-files', methods=['GET'])
def list_files():
    try:
        blob_list = blob_container_client.list_blobs()
        files = [{"name": blob.name} for blob in blob_list]
        logging.debug(f"Retrieved files from container: {[blob.name for blob in blob_list]}")
        return jsonify(files)
    except Exception as e:
        logging.error(f"Failed to list files in container: {str(e)}")
        return jsonify({"error": f"Failed to list files: {str(e)}"}), 500

# Route to delete a file from Azure Blob Storage
@app.route('/delete-file', methods=['POST'])
def delete_file():
    filename = request.json.get('filename')
    if not filename:
        return jsonify({"error": "No filename provided"}), 400

    try:
        blob_client = blob_container_client.get_blob_client(blob=filename)
        blob_client.delete_blob()
        logging.debug(f"File {filename} deleted from Azure Blob Storage successfully.")
        return jsonify({"message": f"File {filename} deleted successfully"}), 200
    except Exception as e:
        logging.error(f"Failed to delete {filename} from Azure Blob Storage: {str(e)}")
        return jsonify({"error": f"Failed to delete file: {str(e)}"}), 500

# Route to handle RAG and prompt submission
@app.route('/process-prompt', methods=['POST'])
def process_prompt():
    prompt = request.form['prompt']
    use_rag = request.form.get('use_rag', 'false') == 'true'

    logging.debug(f"Received prompt: {prompt}")
    logging.debug(f"RAG enabled: {use_rag}")

    try:
        # Step 1: If RAG is enabled, query Azure Cognitive Search for relevant documents
        if use_rag:
            logging.debug("Performing search query using Azure Cognitive Search...")
            search_results = search_client.search(search_text=prompt)
            document_text = ""

            # Collect the content of the search results (relevant documents)
            for result in search_results:
                logging.debug(f"Found document with content: {result.get('content', 'No content available')}")
                document_text += f"{result.get('content', '')}\n\n"  # Assumes 'content' field has the document text

            # Step 2: If relevant documents are found, use them to augment the user's prompt
            if document_text:
                logging.debug(f"Documents found, augmenting prompt with documents: {document_text}")
                full_prompt = f"Documents:\n{document_text}\n\nUser prompt: {prompt}"
            else:
                logging.debug("No documents found, proceeding with the original prompt.")
                full_prompt = prompt
        else:
            # If RAG is disabled, send the user's prompt directly to Azure OpenAI
            logging.debug("RAG disabled, sending original prompt to OpenAI.")
            full_prompt = prompt

        # Step 3: Send the combined prompt (or direct prompt) to Azure OpenAI
        logging.debug(f"Sending prompt to Azure OpenAI: {full_prompt}")
        response = openai.ChatCompletion.create(
            engine=AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )

        openai_response = response['choices'][0]['message']['content'].strip()
        logging.debug(f"OpenAI response: {openai_response}")

        return jsonify({"response": openai_response})

    except Exception as e:
        logging.error(f"Error during RAG or prompt processing: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Make the app accessible on the network by binding to 0.0.0.0
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)