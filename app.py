import streamlit as st
from tools import get_finance_agent
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from datetime import datetime 


st.set_page_config(
    page_title="Financial Assistant Chatbot with LLM Agents and RAG",
    page_icon="🪙"
)

st.subheader("**Financial Assistant Chatbot with LLM Agents and RAG**")

if "selectbox_selection" not in st.session_state:
    st.session_state['selectbox_selection'] = ["Default Chat"]

selectbox_selection = st.session_state['selectbox_selection']


if st.sidebar.button("✍️ Create New Chat", use_container_width=True):
    selectbox_selection.append(f"New Chat - {datetime.now().strftime('%H:%M:%S')}")

session_id = st.sidebar.selectbox("Chats", options=selectbox_selection, index=len(selectbox_selection)-1)

st.sidebar.markdown("#")
st.sidebar.markdown('''
                    
ℹ️ **About**

Financial Assistant Chatbot with LLM Agents and RAG is an app that helps you get clear, accurate answers to your financial questions. 
Just type your question, and the assistant will provide smart, helpful responses in real time.
                    
🛠️ **Features**
                    
- 🏢 Company Overview
                    
    Gives information about any company, including sector, financial metrics, and other facts.
                                    
- 🔍 Top Companies by Transaction Volume
                    
    Shows a list of companies with the highest transaction volume over a specific period.

- 📆 Daily Transactions Summary
                    
    Provides a day-by-day breakdown of total transactions, helping to track market activity trends.

- 📊 Top Ranked Companies
                    
    Displays companies ranked by key metrics (dividend yield, total dividend, revenue, earnings, market cap).
                    
''')


chat_history = StreamlitChatMessageHistory(key=session_id)
agent_executor = get_finance_agent()


for message in chat_history.messages:
    with st.chat_message(message.type):
        st.markdown(message.content)

prompt = st.chat_input("Ask your question here!")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = agent_executor.invoke({"input": prompt},
                                         config={"configurable": {"session_id": session_id}})
        st.markdown(response['output'])
