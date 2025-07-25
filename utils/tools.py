import json
import requests
from datetime import datetime
import streamlit as st
import pandas as pd
import os

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import InMemoryVectorStore


SECTORS_API_KEY = st.secrets["SECTORS_API_KEY"]

def retrieve_from_endpoint(url: str) -> dict:
    """
    A robust, reusable helper function to perform GET requests.
    """
    
    headers = {"Authorization": SECTORS_API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()

        return data

    except requests.exceptions.HTTPError as err:
        return {
            "error": f"HTTPError {err.response.status_code} - {err.response.reason}",
            "url": url,
            "detail": err.response.text
        }
    
    except Exception as e:
        return {
            "error": f"Unexpected error: {type(e).__name__} - {str(e)}",
            "url": url
        }


@tool
def get_company_overview(stock: str) -> dict:
    """
    Get company overview
    
    @param stock: The stock symbol of the company
    @return: The company overview
    """

    url = f"https://api.sectors.app/v1/company/report/{stock}/?sections=overview"

    return retrieve_from_endpoint(url)


@tool
def get_top_companies_by_tx_volume(start_date: str, end_date: str, top_n: int = 5) -> dict:
    """
    Get top companies by transaction volume

    @param start_date: The start date in YYYY-MM-DD format
    @param end_date: The end date in YYYY-MM-DD format
    @param top_n: Number of stocks to show
    @return: A list of most traded IDX stocks based on transaction volume for a certain interval
    """
    url = f"https://api.sectors.app/v1/most-traded/?start={start_date}&end={end_date}&n_stock={top_n}"

    return retrieve_from_endpoint(url)

@tool
def get_daily_tx(stock: str, start_date: str, end_date: str) -> list[dict]:
    """
    Get daily transaction for a stock

    @param stock: The stock 4 letter symbol of the company
    @param start_date: The start date in YYYY-MM-DD format
    @param end_date: The end date in YYYY-MM-DD format
    @return: Daily transaction data of a given ticker for a certain interval
    """
    url = f"https://api.sectors.app/v1/daily/{stock}/?start={start_date}&end={end_date}"

    return retrieve_from_endpoint(url)


@tool
def get_top_companies_ranked(dimension: str, top_n: int, year: int) -> list[dict]:
    """
    Return a list of top companies (symbol) based on certain dimension 
    (dividend yield, total dividend, revenue, earnings, market cap,...)

    @param dimension: The dimension to rank the companies by, one of: 
    "dividend_yield", "total_dividend", "revenue", "earnings", "market_cap", ...

    @param top_n: Number of stocks to show
    @param year: Year of ranking, always show the most recent full calendar year that has ended
    @return: A list of top tickers in a given year based on certain classification
    """

    url = f"https://api.sectors.app/v1/companies/top/?classifications={dimension}&n_stock={top_n}&year={year}"

    return retrieve_from_endpoint(url)

