import streamlit as st

finance_page = st.Page("pages/finance.py", title="Financial Assistant Chatbot", icon="🪙")
document_page = st.Page("pages/document.py", title="Document Understanding Chatbot", icon="📚")

st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] {
        width: 350px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

pages = st.navigation([finance_page, document_page])
pages.run()