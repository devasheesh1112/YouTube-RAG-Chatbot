# MMR retriever
def build_retriever(vector_store):
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4, "fetch_k": 20, "lambda_mult": 0.5}
    )
    return retriever

def retrieve_docs(retriever, question: str):
    return retriever.invoke(question)  # or retriever.get_relevant_documents(question)
