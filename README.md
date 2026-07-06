# Document Question Answering Assistant

This repository contains an example **PDF-based Question Answering assistant** that demonstrates how to combine **Large Language Models (LLMs)** with **retrieval techniques** to build grounded, reliable applications.

Instead of relying on a pre-trained model’s general knowledge, this assistant is designed to work **only with the content of the document you provide**. You upload a PDF, ask questions, and the system retrieves the most relevant parts of the text before generating an answer. If the assistant cannot find a meaningful answer in the document, it will not try to *hallucinate*. Instead, it responds with:

*"I don’t know based on this document."* 

This makes the project a simple but powerful example of **Retrieval-Augmented Generation (RAG)**, a widely used approach in modern LLM applications. It highlights how AI can be grounded in external data sources, ensuring **accuracy**, **transparency**, and **domain-specific answers**.

## Tech Stack

- [PyPDF2](https://pypi.org/project/PyPDF2/) - Extracts raw text from uploaded PDF
- [Sentence Transformers](https://www.sbert.net/) - Generates dense embeddings for semantic similarity
- [Hugging Face Transformers](https://huggingface.co/google/flan-t5-base) - Instruction-tuned LLM (`google/flan-t5-base`) used to generate answers from retrieved context
- [FAISS](https://github.com/facebookresearch/faiss) - Vector store for fast similarity search
