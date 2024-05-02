# Architectural Blueprints for RAG Automation: Advanced Document Understanding using Vertex AI Search

<div align="center">
    <img src="./img/blog-9.png" alt="Document Understanding using Vertex AI Search" width="500" height="500"/>
</div>

## Setup Instructions

Follow these steps to set up the RAG Automation project environment on your local machine.

### 1. Clone the Repository

First, ensure that you have git installed on your machine and then clone the repository using:

```bash
git clone <repository-url>
cd <repository-directory>
```

Replace `<repository-url>` and `<repository-directory>` with the actual URL and directory name of your repository.

### 2. Create a Virtual Environment

Create and activate a virtual environment to manage the project's dependencies:

```bash
python3 -m venv .vais-rag-patterns
source .vais-rag-patterns/bin/activate
```

### 3. Install Dependencies

Upgrade pip to the latest version and install required packages from `requirements.txt`:

```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Set Environment Variables

Append the project directory to your PYTHONPATH environment variable:

```bash
export PYTHONPATH=$PYTHONPATH:.
```

### 5. Configuration Files

Make sure to have your `credentials` and `config.yml` files set up in the project directory as these files are essential for the correct functioning of the project.