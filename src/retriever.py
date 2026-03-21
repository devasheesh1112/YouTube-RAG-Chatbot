from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
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


def build_qa_chain(vectorstore: Chroma, google_api_key: str):
    """Build a RAG chain using Gemini LLM and ChromaDB retriever."""
    llm = ChatGoogleGenerativeAI(
        model="gemma-3-4b-it",
        temperature=0,
        google_api_key=google_api_key
    )

    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"]
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

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
