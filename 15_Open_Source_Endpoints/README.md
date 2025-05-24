In today's assignment, we'll be creating an Open Source LLM-powered LangChain RAG Application in Chainlit.

There are 2 main sections to this assignment:

## Build 🏗️

### Build Task 1: Deploy LLM and Embedding Model to SageMaker Endpoint Through Hugging Face Inference Endpoints - DONE

I followed the steps Chris showed in class and was able to create endpoints for both LLM and Embedding Model.

### Build Task 2: Create RAG Pipeline with LangChain - DONE

Follow the notebook to create a LangChain pipeline powered by Hugging Face endpoints! This was just plugging in my endpoints and running the notebook - it ran successfully.

# Paul Graham Essay Bot
## Overview
This is a **Chainlit-powered RAG (Retrieval Augmented Generation) application** that lets users chat with Paul Graham's essays. The bot can answer questions by retrieving relevant content from Paul Graham's writings and generating responses using Hugging Face language models.

## How It Works

### 🔧 **Setup & Configuration**
- Uses environment variables for Hugging Face endpoints and authentication
- Loads configuration from a `.env` file in the parent directory (or HF Secrets)
- Requires `HF_LLM_ENDPOINT`, `HF_EMBED_ENDPOINT`, and `HF_TOKEN`

### 📚 **Document Processing**
- Loads Paul Graham essays from `./data/paul_graham_essays.txt`
- Splits the text into chunks (1000 characters with 30 character overlap)
- Creates embeddings using my Hugging Face embedding endpoint
- Builds a FAISS vector database for fast similarity search

### 🔍 **RAG Pipeline**
1. **User Query**: User asks a question about Paul Graham's essays
2. **Retrieval**: System finds relevant essay chunks using vector similarity
3. **Context**: Retrieved chunks are added as context to the prompt
4. **Generation**: Your Hugging Face LLM generates a response based on the context
5. **Response**: Bot streams the answer back to the user

### ⚙️ **Technical Stack**
- **Frontend**: Chainlit web interface
- **Vector Store**: FAISS for document retrieval
- **Embeddings**: Custom Hugging Face endpoint
- **LLM**: Custom Hugging Face endpoint
- **Framework**: LangChain for RAG orchestration

Once you're done - please move on to Build Task 3!

### Build Task 3: Create a Chainlit Application - DONE

Here is my huggingface space: https://huggingface.co/spaces/geetach/aie6-assignment-15-geeta (it won't work once I bring the endpoints down)

### Deliverables (DONE - showcased in my loom video)

- Completed Notebook - on github. 
- Chainlit Application in a Hugging Face Space Powered by Hugging Face Endpoints - on hugging face. I will show this in my loom video, but I assume it will stop working once I stop my endpoints as instructed.
- Screenshot of endpoint usage - DONE

Screen shot of LLM endpoint usage: ![llm endpoint usage](llm_endpoint_usage.png)
Screen shot of Embedding endpoint usage: ![embed endpoint usage](embed_endpoint_usage.png)

## Ship 🚢

Create a Hugging Face Space powered by Hugging Face Endpoints!

### Deliverables (DONE)

- A short Loom of the space, and a 1min. walkthrough of the application in full

## Share 🚀

Make a social media post about your final application!

### Deliverables - DONE (Discord)

- Make a post on any social media platform about what you built!
