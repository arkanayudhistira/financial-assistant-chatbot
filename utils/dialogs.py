import streamlit as st

@st.dialog("How To Use", width="large")
def finance_dialog():
    help_container = st.container(height=400, border=False)
    with help_container:
        st.markdown(
            '''
            ℹ️ **About Us**

            This Financial AI Chatbot helps you explore and analyze companies listed on the Indonesia Stock Exchange (IDX) using real-time financial data and smart tools.

            🧭 **How to Use**

            You can ask the chatbot anything about Indonesian-listed stocks — just type your question in plain language. Below are the key features you can use:

            🛠️ **Key Features**

            - **Company Report**: 
            Retrieve in-depth reports on any IDX-listed company, including its overview, financial performance, valuation metrics, and dividend history.

            - **Daily Stock Data**: 
            View daily stock data such as price movements, trading volume, and market capitalization within a selected date range (up to 90 days).

            - **Most Traded Stocks**: 
            Find out which stocks have the highest transaction volume during a given period to spot market trends and popular tickers.

            - **Top Ranked Companies**: 
            Discover the top companies based on key metrics like dividend yield, revenue, earnings, market cap, or valuation ratios — ranked by year.

            💬 **Examples You Can Try**

            - "Show me the company report for BBCA, including financials and valuation."
            - "Which stocks were most traded between June and July 2025?"
            - "Get daily data for TLKM from May 1st to July 30th."
            - "List the top 5 companies by dividend yield in 2024."
            '''
        )

@st.dialog("How To Use", width="large")
def document_dialog():
    help_container = st.container(height=400, border=False)
    with help_container:
        st.markdown(
            '''
            ℹ️ **About**

            This Document AI Chatbot helps you understand and extract insights from your own documents just by chatting.

            🧭 **How to Use**

            Upload a document, then ask questions about its contents using natural language. 
            The chatbot will read and understand the file, and provide answers or summaries.

            📂 **Supported File Types**

            - PDF (`.pdf`)
            - Excel (`.xlsx`, `.xls`)
            - CSV (`.csv`)
            - JSON (`.json`)

            🛠️ **Key Features**

            - **Upload & Analyze**  
            Upload your document and the chatbot will process them and get ready to answer your questions.

            - **Ask Questions Naturally**  
            Simply type your questions as if you're talking to a human.

            - **Multi-format Reading**  
            Understands structured (CSV, Excel, JSON) and unstructured (PDF text) data, and handles tables, numbers, and text sections.

            - **Extract & Summarize**  
            Get summaries, insights, or even specific values from large documents without needing to read them manually.

            💬 **Examples You Can Try**

            - "Summarize this PDF report in 3 sentences."
            - "What's the average revenue listed in this Excel file?"
            - "Find all rows in this CSV where the status is 'Failed'." 
            - "Which customers spent more than 10 million based on this JSON file?"

            '''
        )