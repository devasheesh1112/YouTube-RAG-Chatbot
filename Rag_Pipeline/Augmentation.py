from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate(
    template="""
    You are a helpful assistant.
    Answer ONLY from the provided transcript context.
    If the context is insufficient, just say you don't know.

    {context}
    Question: {question}
    """,
    input_variables=["context", "question"]
)

def create_prompt(context_docs, question: str):
    context = "\n\n".join(doc.page_content for doc in context_docs)
    return prompt_template.invoke({"context": context, "question": question})
