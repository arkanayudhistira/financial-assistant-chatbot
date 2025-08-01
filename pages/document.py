import streamlit as st
import pandas as pd
import os
import tempfile

from langchain_community.document_loaders import PyPDFLoader

from utils.agents import (
    get_tabular_document_agent,
    get_pdf_document_agent
)

from utils.dialogs import document_dialog

uploaded_file = st.sidebar.file_uploader('Upload Document', type=['pdf', 'csv', "xls", "xlsx", "json"])

st.sidebar.markdown("#")

if st.sidebar.button("⚙️ How To Use", use_container_width=True):
    document_dialog()

if not uploaded_file:
    st.error("Please upload a document before asking a question!")
else:
    ext = os.path.splitext(uploaded_file.name)[1].lower()

    try:
        if ext == ".csv":
            docs = pd.read_csv(uploaded_file)
        elif ext in [".xls", ".xlsx"]:
            docs = pd.read_excel(uploaded_file)
        elif ext == ".json":
            docs = pd.read_json(uploaded_file)
        elif ext == ".pdf":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            loader = PyPDFLoader(tmp_path)
            docs = loader.load()

        else:
            raise ValueError(f"Unsupported file type: {ext}")

    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}")


    if ext in ['.csv', ".xls", ".xlsx", ".json"]:
        agent = get_tabular_document_agent(docs=docs)

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["type"]):
                st.markdown(message["content"])

        prompt = st.chat_input("Ask your question here!")

        if prompt:

            st.session_state.messages.append({"type": "human", "content": prompt})
            
            with st.chat_message("human"):
                st.markdown(prompt)
                

            with st.chat_message("ai"):
                response = agent.invoke({"input":prompt})

                st.markdown(response['output'])
                st.session_state.messages.append({"type": "ai", "content": response['output']})

    elif ext == '.pdf':
        agent = get_pdf_document_agent(docs=docs)

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["type"]):
                st.markdown(message["content"])

        prompt = st.chat_input("Ask your question here!")

        if prompt:

            st.session_state.messages.append({"type": "human", "content": prompt})

            with st.chat_message("human"):
                st.markdown(prompt)

            # relevant_document = vector_store.similarity_search_with_score(prompt, k=5)

            # docs_content = "\n\n".join(doc[0].page_content for doc in relevant_document)
            # docs_metadata = "\n\n".join(str(doc[0].metadata) for doc in relevant_document)

            with st.chat_message("ai"):
                # response = chain.invoke({"context": docs_content, "metadata": docs_metadata, "input": prompt})
                response = agent.invoke({"input": prompt},
                                        config={"configurable": {"session_id": "session_id"}})

                st.markdown(response['output'])
                st.session_state.messages.append({"type": "ai", "content": response['output']})