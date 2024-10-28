# Azure OPEN AI Chat bot with RAG

This project is designed to interface with the Azure Open AI Resource, providing functionality to perform RAG enabled prompting with user-friendly format. The project setup includes a virtual environment to manage dependencies.

<img width="1680" alt="image" src="https://github.com/user-attachments/assets/44ab2e30-ef28-4075-801a-81483cdf4684">

## Introduction

This python based application has been developed using OpenAIs Code Pilot and intends to showcase how RAG is performed using Azure and Azure Open AI services.
In order to execute the application successfully you need to have serveral Azure resources
1. Azure Storage Account to store documents
   - Create a simple azure stoprage account and a container called upload
     ![image](https://github.com/user-attachments/assets/12649106-5d45-462d-b1b6-2167d4fb3096)

2. Azure Search Service is where the docuemts are indexed
   - I recommend to create the indexer via the import data function
     ![image](https://github.com/user-attachments/assets/5f1d0689-fd52-4a8e-8b55-147b0ad9a822)

     <img width="1272" alt="image" src="https://github.com/user-attachments/assets/6df5cb6a-06c8-4aa7-be36-5aa67c37de24">

3. Azure Open AI Service is where the model i.e. gpt-4o is hosted
   - ![image](https://github.com/user-attachments/assets/abc87ccc-6e89-4807-86aa-636e77f25054)


This is the overview of the resources needed in Azure
<img width="1369" alt="image" src="https://github.com/user-attachments/assets/7d36661b-1e22-46e7-ba23-70d43e46b362">


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
   - All API keys can be optained from the azure resources
     - Azure Storage Account -> Security + Networking > Access Keys
     - Azure Search -> Settings > Keys (you need the primary admin key)
     - Azure Open AI -> Resource management > Keys and Endpoints
   
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
