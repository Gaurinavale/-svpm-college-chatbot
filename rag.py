import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


# ==============================
# Configuration
# ==============================

DATA_DIR = "data"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

TOP_K = 3


# ==============================
# Load Documents
# ==============================

def load_documents(data_dir=DATA_DIR):
    """
    Load all .txt files from the data directory.
    """

    documents = []

    if not os.path.exists(data_dir):
        raise FileNotFoundError(
            f"Data directory not found: {data_dir}"
        )

    for filename in os.listdir(data_dir):

        if filename.endswith(".txt"):

            filepath = os.path.join(data_dir, filename)

            with open(filepath, "r", encoding="utf-8") as file:
                text = file.read()

            documents.append({
                "text": text,
                "source": filename
            })

    return documents


# ==============================
# Text Chunking
# ==============================

def create_chunks(documents):
    """
    Split documents into overlapping text chunks.
    """

    chunks = []

    for document in documents:

        text = document["text"]
        source = document["source"]

        start = 0

        while start < len(text):

            end = start + CHUNK_SIZE

            chunk_text = text[start:end]

            chunks.append({
                "text": chunk_text,
                "source": source
            })

            start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


# ==============================
# Create Embeddings
# ==============================

def create_embeddings(chunks, model):
    """
    Convert text chunks into vector embeddings.
    """

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings


# ==============================
# Create FAISS Index
# ==============================

def create_vector_database(chunks):
    """
    Create FAISS vector database from document chunks.
    """

    model = SentenceTransformer(EMBEDDING_MODEL)

    embeddings = create_embeddings(chunks, model)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(
        embeddings.astype("float32")
    )

    return index, model


# ==============================
# Retrieve Relevant Documents
# ==============================

def retrieve_documents(
    query,
    index,
    chunks,
    model,
    top_k=TOP_K
):
    """
    Retrieve the most relevant chunks
    for a user query.
    """

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    query_embedding = query_embedding.astype("float32")

    scores, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for score, index_position in zip(
        scores[0],
        indices[0]
    ):

        if index_position == -1:
            continue

        result = chunks[index_position].copy()

        result["score"] = float(score)

        results.append(result)

    return results


# ==============================
# Build RAG Database
# ==============================

def build_rag():

    print("Loading college documents...")

    documents = load_documents()

    print(
        f"Loaded {len(documents)} documents."
    )

    print("Creating text chunks...")

    chunks = create_chunks(documents)

    print(
        f"Created {len(chunks)} chunks."
    )

    print("Creating FAISS vector database...")

    index, model = create_vector_database(chunks)

    print("RAG database created successfully.")

    return index, chunks, model


# ==============================
# Test RAG
# ==============================

if __name__ == "__main__":

    index, chunks, model = build_rag()

    question = input(
        "\nAsk a question about SVPM College: "
    )

    results = retrieve_documents(
        question,
        index,
        chunks,
        model
    )

    print("\nRelevant Information:\n")

    for result in results:

        print(
            f"Source: {result['source']}"
        )

        print(
            f"Similarity: {result['score']:.4f}"
        )

        print(
            result["text"]
        )

        print("-" * 60)
