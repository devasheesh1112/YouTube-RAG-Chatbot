
# NEW
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS



from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from dotenv import load_dotenv
load_dotenv()

def load_transcript(video_id: str) -> str:
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        return " ".join(chunk["text"] for chunk in transcript_list)
    except TranscriptsDisabled:
        raise Exception("Transcript not available for this video.")

def split_transcript(text: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.create_documents([text])

def embed_and_store(chunks: list[Document]):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store

def run_ingestion(video_id: str):
    transcript = load_transcript(video_id)
    chunks = split_transcript(transcript)
    vector_store = embed_and_store(chunks)
    return vector_store
