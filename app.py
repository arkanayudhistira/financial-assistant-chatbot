import streamlit as st

finance_page = st.Page("pages/finance.py", title="Financial Assistant Chatbot", icon="🪙")
document_page = st.Page("pages/document.py", title="Document Understanding Chatbot", icon="📚")

pages = st.navigation([finance_page, document_page])
pages.run()