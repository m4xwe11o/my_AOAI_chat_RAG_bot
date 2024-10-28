# Azure OPEN AI Chat bot with RAG

This project is designed to interface with the Azure Open AI Resource, providing functionality to perform RAG enabled prompting with user-friendly format. The project setup includes a virtual environment to manage dependencies.

<img width="1680" alt="image" src="https://github.com/user-attachments/assets/44ab2e30-ef28-4075-801a-81483cdf4684">

## Getting Started

Follow these instructions to set up the project on your local machine.

### Prerequisites

1. **Python 3** - Download and install from [python.org](https://www.python.org/).
2. **Git** - Download and install from [git-scm.com](https://git-scm.com/).
3. **GitHub CLI (`gh`)** - Optional, but recommended. Install from [cli.github.com](https://cli.github.com/).

### Project Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/m4xwe11o/my_AOAI_chat_RAG_bot.git
   cd my_AOAI_chat_RAG_bot

### Summary of Commands

1. **Clone the repository**: `git clone ...`
2. **Set up virtual environment**: `python3 -m venv venv`
3. **Activate environment**: `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows)
4. **Install dependencies**: `pip install -r requirements.txt`
5. **Create a `.env`file**: `touch .env`
   
   ```
   # Azure Blob Storage Configuration
   AZURE_BLOB_CONNECTION_STRING=
   AZURE_BLOB_CONTAINER=

   # Azure OpenAI Configuration
   AZURE_OPENAI_API_KEY=   AZURE_OPENAI_ENDPOINT=https://atclaoai18102024.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o  # This should match your deployed model (e.g., gpt-4)

   # Azure Cognitive Search Configuration
   AZURE_SEARCH_ENDPOINT=
   AZURE_SEARCH_API_KEY=
   AZURE_SEARCH_INDEX_NAME=
   ```
