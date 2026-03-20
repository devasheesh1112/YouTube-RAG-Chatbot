from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings


def split_text(transcript: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    """Split transcript into overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.create_documents([transcript])


def build_vectorstore(docs, google_api_key: str) -> FAISS:
    """Embed documents using Gemini embedding model."""
    print("[INFO] Building vectorstore with Gemini embeddings...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=google_api_key
    )
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore


def load_vectorstore(path: str = "data/faiss_index", google_api_key: str = "") -> FAISS:
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=google_api_key
    )
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
