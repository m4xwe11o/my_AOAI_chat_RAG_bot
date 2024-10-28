# Azure OPEN AI Chat bot with RAG

This project is designed to interface with the Azure Open AI Resource, providing functionality to perform RAG enabled prompting with user-friendly format. The project setup includes a virtual environment to manage dependencies.

<img width="1680" alt="image" src="https://github.com/user-attachments/assets/44ab2e30-ef28-4075-801a-81483cdf4684">

## Introduction

This python based application has been developed using OpenAIs Code Pilot and intends to showcase how RAG is performed using Azure and Azure Open AI services.
In order to execute the application successfully you need to have serveral Azure resources
1. Azure Storage Account to store documents
2. Azure Search Service is where the docuemts are indexed
3. Azure Open AI Service is where the model i.e. gpt-4o is hosted

### Things you can do

When entering a prompt you can send the prompt to the Azure Open AI resource and the deployed model i.e. gpt-4o is answering.
You can see the prompt und reponse as debug messages

When checking the RAG checkbox the prompt is modified based on the documents that are found based on the indexer.

You can upload and delete documents that are stored on the storage account
- The indexer should be configured to start indexing all documents every 5 minutes

## Getting Started

Follow these instructions to set up the project on your local machine.

### Prerequisites

1. **Python 3** - Download and install from [python.org](https://www.python.org/).
2. **Git** - Download and install from [git-scm.com](https://git-scm.com/).

### Project Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/m4xwe11o/my_AOAI_chat_RAG_bot.git
   cd my_AOAI_chat_RAG_bot

2. **Set up virtual environment**: `python3 -m venv venv`
3. **Activate environment**: `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows)
4. **Install dependencies**: `pip install -r requirements.txt`
5. **Create a `.env`file**: `touch .env`
   
   ```
   # Azure Blob Storage Configuration
   AZURE_BLOB_CONNECTION_STRING=
   AZURE_BLOB_CONTAINER=

   # Azure OpenAI Configuration
   AZURE_OPENAI_API_KEY=
   AZURE_OPENAI_ENDPOINT=
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o  # This should match your deployed model (e.g., gpt-4)

   # Azure Cognitive Search Configuration
   AZURE_SEARCH_ENDPOINT=
   AZURE_SEARCH_API_KEY=
   AZURE_SEARCH_INDEX_NAME=
   ```
