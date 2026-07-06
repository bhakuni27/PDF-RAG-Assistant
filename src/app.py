import numpy as np
import faiss
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from sentence_transformers import SentenceTransformer
from src.utils import extract_text_from_pdf, chunk_text

class DocQAAssistant:
    def __init__(self, uploaded_file):
        self.text = extract_text_from_pdf(uploaded_file)
        self.chunks = chunk_text(self.text, chunk_size=300, overlap=50)

        # Load model
        self.qa_pipeline, self.embedder = self.load_model()

        # Build FAISS index
        self.index = self.build_index()

    def load_model(self):
        model_name = "google/flan-t5-base" 
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        qa_pipeline = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

        embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        return qa_pipeline, embedder

    def build_index(self):
        embeddings = self.embedder.encode(self.chunks, convert_to_numpy=True)
        # Normalize for cosine similarity
        embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        dim = embeddings.shape[1]

        index = faiss.IndexFlatIP(dim)  # inner product = cosine when normalized
        index.add(embeddings.astype("float32"))
        self.embeddings = embeddings
        return index

    def retrieve_chunks(self, question, top_k=2, threshold=0.25):
        q_emb = self.embedder.encode([question], convert_to_numpy=True)
        q_emb = q_emb / np.linalg.norm(q_emb, axis=1, keepdims=True)

        scores, indices = self.index.search(q_emb.astype("float32"), top_k)

        retrieved_chunks = []
        for score, idx in zip(scores[0], indices[0]):
            if score >= threshold:
                retrieved_chunks.append(self.chunks[idx])

        return retrieved_chunks

    def answer_question(self, question):
        retrieved_chunks = self.retrieve_chunks(question)

        if not retrieved_chunks:
            return "I don’t know based on this document.", []

        context = " ".join(retrieved_chunks)
        prompt = f"""
        You are a helpful assistant.
        Use ONLY the following context to answer the question.

        Context:
        {context}

        Question: {question}
        Answer:
        """

        result = self.qa_pipeline(prompt, max_new_tokens=150)
        answer = result[0]["generated_text"].strip()
        return answer, retrieved_chunks
