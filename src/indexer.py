from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
import os


CHROMA_DIR = "data/chroma_db"


def split_text(transcript: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    """Split transcript into overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.create_documents([transcript])


def build_vectorstore(docs, google_api_key: str, collection_name: str = "youtube_rag") -> Chroma:
    """
    Embed documents using Gemini embeddings and store in ChromaDB.
    ChromaDB auto-saves to disk — no manual save needed!
    """
    print("[INFO] Building ChromaDB vectorstore with Gemini embeddings...")

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=google_api_key
    )

    # Delete existing collection to avoid duplicate chunks
    if os.path.exists(CHROMA_DIR):
        import shutil
        shutil.rmtree(CHROMA_DIR)
        print("[INFO] Cleared old ChromaDB collection")

    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
        collection_name=collection_name
    )

    print(f"[INFO] ChromaDB created with {len(docs)} chunks at '{CHROMA_DIR}'")
    return vectorstore


def load_vectorstore(google_api_key: str, collection_name: str = "youtube_rag") -> Chroma:
    """Load existing ChromaDB vectorstore from disk."""
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=google_api_key
    )
    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
        collection_name=collection_name
    )
