# web/app.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import streamlit as st
from Rag_Pipeline.Indexing import run_ingestion
from Rag_Pipeline.Retrieval import build_retriever, retrieve_docs
from Rag_Pipeline.Augmentation import create_prompt
from Rag_Pipeline.Generation import generate_answer

st.set_page_config(page_title="🎥 YouTube RAG Chatbot", page_icon="🤖", layout="centered")

st.title("🎥 YouTube RAG Chatbot")
st.markdown("This app allows you to ask questions about any YouTube video's content using RAG (Retrieval-Augmented Generation).")

# --- Input Section ---
with st.expander("📥 Step 1: Provide Input"):
    video_url = st.text_input("🔗 Enter YouTube Video URL:")
    question = st.text_area("❓ Ask a question about the video content:")

    run_rag = st.button("🚀 Run RAG Pipeline")

# --- Output Section ---
if run_rag and video_url and question:
    try:
        with st.spinner("⏳ Extracting transcript and building RAG components..."):
            if "v=" in video_url:
                video_id = video_url.split("v=")[-1].split("&")[0]
            else:
                st.error("⚠️ Please enter a valid YouTube URL with `v=` parameter.")
                st.stop()

            # Step 1: Load + Split + Embed
            vector_store = run_ingestion(video_id)

            # Step 2: Retrieve chunks
            retriever = build_retriever(vector_store)
            retrieved_docs = retrieve_docs(retriever, question)

            # Step 3: Augment prompt with context
            final_prompt = create_prompt(retrieved_docs, question)

            # Step 4: Generate answer
            answer = generate_answer(final_prompt)

        # Display answer
        st.success("✅ Answer generated!")
        st.markdown("### 🧠 Answer")
        st.markdown(answer)

        with st.expander("🔎 See Retrieved Chunks"):
            for i, doc in enumerate(retrieved_docs):
                st.markdown(f"**Chunk {i+1}**")
                st.code(doc.page_content.strip()[:1000])  # trim long text

        with st.expander("📄 Final Prompt Sent to LLM"):
            st.code(final_prompt, language="markdown")

    except Exception as e:
        st.error(f"❌ Error occurred: {e}")
