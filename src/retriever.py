from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


PROMPT_TEMPLATE = """
You are a helpful assistant that answers questions based on the YouTube video transcript provided.
Use only the context below to answer. If the answer is not in the context, say "I don't know based on the video."

Context:
{context}

Question: {question}

Answer:
"""

# Models confirmed available on your account (from check_models.py output)
# Using gemma-3-4b-it as primary - lightweight and available on free tier
CHAT_MODELS = [
    "gemma-3-4b-it",       # lightweight, free tier friendly
    "gemma-3-1b-it",       # smallest, best for free tier
    "gemma-3-12b-it",      # medium
    "gemini-2.0-flash",    # fallback
]


def build_qa_chain(vectorstore: FAISS, google_api_key: str):
    """Build a RAG chain using Gemini/Gemma models."""
    llm = ChatGoogleGenerativeAI(
        model="gemma-3-4b-it",
        temperature=0,
        google_api_key=google_api_key
    )

    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"]
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


def get_answer(chain, question: str) -> str:
    return chain.invoke(question)
