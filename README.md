# BOT with BENEFITS: Government Scheme Retrieval System using LLMs

## Overview

Welcome to the **BOT with BENEFITS**, an intelligent RAG (Retrieval Augmented Generation) chatbot designed to help users discover and understand various government schemes. This system leverages Large Language Models (LLMs) and a vector database to provide accurate, concise, and personalized information based on user queries and eligibility criteria.

Our chatbot aims to simplify access to government benefits by offering a user-friendly interface that guides individuals through eligibility checks and provides detailed scheme information.


# Demo Video : 
https://drive.google.com/file/d/15btp71yAHjp0ImxSxrlQ_XkoNRXIWXVQ/view?usp=sharing
## Features

* **Guided Eligibility Check:** Collects user details (name, gender, age, state, rural/urban, family income, marital status, occupation, caste) to determine eligible schemes.
* **Detailed Scheme Information:** Provides comprehensive explanations of scheme purpose, eligibility, benefits, and application methods.
* **RAG-based Accuracy:** Retrieves information directly from a curated knowledge base (vector database) to ensure factual and relevant responses.
* **Friendly and Polite Interaction:** Designed with a user-centric system prompt for clear and empathetic communication.
* **Scalable Architecture:** Built to handle expanding datasets of government schemes.

## Architecture and Development Process

Our RAG system follows a multi-stage data pipeline and leverages n8n for workflow orchestration.

### Phase 1: Data Ingestion and Vectorization

This phase focuses on acquiring, processing, and storing government scheme data into a vector database for efficient retrieval.

1.  **Web Scraping:** URLs from official government portals hosting schemes are crawled, and textual content is scraped using libraries like `requests`, `BeautifulSoup`, or `Selenium`.
2.  **Text Extraction and Cleaning:** Relevant scheme details (e.g., name, objective, eligibility, benefits) are extracted, cleaned, and normalized.
3.  **JSON Conversion:** The extracted data is structured into a uniform JSON format. (Refer to `URLs to Json str using LLM.ipynb` and `scheme_1.json` for examples).
4.  **Text Chunking:** Long scheme descriptions are split into manageable chunks using a `Character Text Splitter` with a `chunkSize` of 1500 and `chunkOverlap` of 100.
5.  **Embedding Generation:** Text chunks are converted into high-dimensional vectors using the `models/text-embedding-004` from Google Gemini.
6.  **Vector Database Creation:** The generated embeddings are stored in a Pinecone vector store named `vector-db`.

The diagram below illustrates Phase 1 of the architecture:
![Phase 1 Architecture](phase%201.png)

### Phase 2: Chatbot Interaction and Response Generation

This phase outlines how the chatbot receives user queries, retrieves relevant information, and generates responses.

1.  **Chat Trigger:** The `When chat message received` node in n8n initiates the workflow upon a user message.
2.  **AI Agent:** An `AI Agent` orchestrates the conversation, leveraging a chat model, memory, and tools to respond to user queries.
3.  **Language Model:** The `Google Gemini Chat Model2` (`models/gemini-2.0-flash-lite`) is used as the conversational AI agent.
4.  **Memory:** A `Simple Memory` node (`Memory Buffer Window`) maintains conversational context for coherent interactions.
5.  **Vector Store Tool:** The `Pinecone Vector Store4` acts as a tool (`retrieve-as-tool` mode) for the AI agent to semantically search and retrieve relevant scheme information from the `vector-db` based on user queries.

The diagram below illustrates Phase 2 of the architecture:
![Phase 2 Architecture](phase%202.png)

## Key Technologies

* **n8n:** Workflow automation and orchestration platform.
* **Google Drive:** Used for storing the raw source documents of government schemes.
* **Pinecone:** Vector database for efficient storage and retrieval of scheme embeddings.
* **Google Gemini (formerly Google PaLM API):**
    * `models/text-embedding-004` for generating document embeddings.
    * `models/gemini-2.0-flash-lite` for the conversational AI agent.
* **Langchain Nodes for n8n:** Utilized for building the RAG pipeline components within n8n.
* **Python Libraries:** `selenium`, `requests`, `json`, `re`, `pandas` (for web scraping and data preparation).

