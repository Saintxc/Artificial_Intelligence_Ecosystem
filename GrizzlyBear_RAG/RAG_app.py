import os
import logging
import warnings
from pathlib import Path

import numpy as np
import faiss

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import logging as hf_logging
from openai import OpenAI   # new SDK client


# ---------------------------
# 3.1 Suppress Noisy Logs
# ---------------------------
logging.getLogger("langchain.text_splitter").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)
hf_logging.set_verbosity_error()
warnings.filterwarnings("ignore")


# ---------------------------
# 3.2 ChatGPT API credentials
# ---------------------------
# Load .env from the SAME DIRECTORY as this file (robust to where you run python)
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY is not set. Create a .env file next to RAG_app.py with:\n"
        "OPENAI_API_KEY=your_key_here"
    )

# Create OpenAI client with explicit key (works even if env isn’t exported)
client = OpenAI(api_key=api_key)


# ---------------------------
# 3.3 Parameters
# ---------------------------
chunk_size = 500
chunk_overlap = 50
model_name = "sentence-transformers/all-distilroberta-v1"
top_k = 5


# ---------------------------
# 3.4 Read the Pre-scraped Document
# ---------------------------
DOC_PATH = Path(__file__).resolve().parent / "Selected_Document.txt"
with open(DOC_PATH, "r", encoding="utf-8") as f:
    text = f.read()


# ---------------------------
# 3.5 Split into Appropriately-sized Chunks
# ---------------------------
splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " ", ""],
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
)
chunks = splitter.split_text(text)


# ---------------------------
# 3.6 Embed & Build FAISS Index
# ---------------------------
embedder = SentenceTransformer(model_name)
emb_list = embedder.encode(chunks, show_progress_bar=False)
emb_arr = np.asarray(emb_list, dtype=np.float32)

dim = emb_arr.shape[1]
faiss_index = faiss.IndexFlatL2(dim)
faiss_index.add(emb_arr)


# ---------------------------
# 3.7 Retrieval Function
# ---------------------------
def retrieve_chunks(question: str, k: int = top_k):
    """Return the top-k most relevant chunks from FAISS index for a given question."""
    q_vec = embedder.encode([question], show_progress_bar=False)
    q_arr = np.asarray(q_vec, dtype=np.float32)
    D, I = faiss_index.search(q_arr, k)
    return [chunks[i] for i in I[0]]


# ---------------------------
# 3.8 Q and A with ChatGPT
# ---------------------------
def answer_question(question: str) -> str:
    """Retrieve context and query ChatGPT for an answer."""
    retrieved = retrieve_chunks(question)
    context = "\n\n".join(retrieved)

    system_prompt = (
        "You are a knowledgeable assistant that answers questions based on the "
        "provided context. If the answer is not in the context, say you don’t know."
    )

    user_prompt = f"""Context:
{context}

Question: {question}

Answer:"""

    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
        max_tokens=500,
    )
    return resp.choices[0].message.content.strip()


# ---------------------------
# 3.9 Interactive Loop
# ---------------------------
if __name__ == "__main__":
    print("Enter 'exit' or 'quit' to end.")
    while True:
        question = input("Your question: ")
        if question.lower() in ("exit", "quit"):
            break
        print("Answer:", answer_question(question))