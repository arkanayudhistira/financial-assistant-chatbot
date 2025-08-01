import streamlit as st
from utils.agents import get_finance_agent
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from datetime import datetime 
import pytz

from utils.dialogs import finance_dialog


if "selectbox_selection" not in st.session_state:
    st.session_state['selectbox_selection'] = ["Default Chat"]

selectbox_selection = st.session_state['selectbox_selection']


if st.sidebar.button("✍️ Create New Chat", use_container_width=True):
    selectbox_selection.append(f"New Chat - {datetime.now(tz=pytz.timezone("Asia/Jakarta")).strftime('%H:%M:%S')}")

session_id = st.sidebar.selectbox("Chats", options=selectbox_selection, index=len(selectbox_selection)-1)

chat_history = StreamlitChatMessageHistory(key=session_id)

if 'ai_introduction' not in st.session_state:
    # Code to run only once per session
    st.session_state.ai_introduction = True
    chat_history.add_ai_message(
        '''
        Hello! I'm your AI financial assistant for the Indonesian stock market. I can help you with:

        - Analyzing company financial metrics: Get detailed reports on specific companies.
        - Tracking industry performance: See how different sectors are performing.
        - Providing investment advice: Get data-backed recommendations.

        To get started, tell me what you're interested in. For example, you can ask me:

        - "What are the top companies by market cap in 2024?"
        - "Show me the financial report for TLKM."
        - "What are the most traded stocks in the last 7 days?"

        Let me know how I can help you today!
        ''')
        
for message in chat_history.messages:
    with st.chat_message(message.type):
        st.markdown(message.content)

st.sidebar.markdown("#")

if st.sidebar.button("⚙️ How To Use", use_container_width=True):
    finance_dialog()

prompt = st.chat_input("Ask your question here!")
agent = get_finance_agent()
if prompt:
    with st.chat_message("human"):
        st.markdown(prompt)

    with st.chat_message("ai"):
        response = agent.invoke({"input": prompt},
                                config={"configurable": {"session_id": session_id}})

        st.markdown(response['output'])