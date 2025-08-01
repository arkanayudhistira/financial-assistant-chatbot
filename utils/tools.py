import requests
import streamlit as st

from langchain_core.tools import tool


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
def get_company_report(stock: str, sections: str) -> dict:
    """
    Get company report of a given ticker, organized into distinct sections (overview, financials, valuation, dividend).
    Use this tool to retrieve metrics for a given company.
    
    @param stock: The stock symbol of the company
    @param sections: Sections of the company report that is to be retrieved (overview, financials, valuation, dividend)
    @return: The company report
    """

    url = f"https://api.sectors.app/v1/company/report/{stock}/?sections={sections}"

    return retrieve_from_endpoint(url)


@tool
def get_top_companies_by_tx_volume(start_date: str, end_date: str, top_n: int = 5) -> dict:
    """
    Return a list of the most traded tickers based on transaction volume on a certain interval (up to 90 days)

    @param start_date: The start date in YYYY-MM-DD format
    @param end_date: The end date in YYYY-MM-DD format
    @param top_n: Number of stocks to show (maximum: 10)
    @return: A list of most traded IDX stocks based on transaction volume for a certain interval
    """
    url = f"https://api.sectors.app/v1/most-traded/?start={start_date}&end={end_date}&n_stock={top_n}"

    return retrieve_from_endpoint(url)

@tool
def get_daily_tx(stock: str, start_date: str, end_date: str) -> list[dict]:
    """
    Return daily transaction data of a given ticker that includes the price, volume, 
    and market cap of the stock on a certain interval (up to 90 days).

    @param stock: The stock 4 letter symbol of the company
    @param start_date: The start date in YYYY-MM-DD format
    @param end_date: The end date in YYYY-MM-DD format
    @return: Daily transaction data that includes the price, volume, and market cap of a given stock for a certain interval
    """
    url = f"https://api.sectors.app/v1/daily/{stock}/?start={start_date}&end={end_date}"

    return retrieve_from_endpoint(url)


@tool
def get_top_companies_ranked(dimension: str, top_n: int, year: int) -> list[dict]:
    """
    Return a list of top tickers in a given year based on selected classifications 
    (dividend yield, total dividend, revenue, earnings, market cap, PB ratio, PE ratio, or PS ratio).


    @param dimension: The dimension to rank the companies by, Defaults to "all", 
    "dividend_yield", "total_dividend", "revenue", "earnings", "market_cap", "pb", "pe", "ps".


    @param top_n: Number of stocks to show (default: 5)
    @param year: Year of ranking, always show the most recent full calendar year that has ended
    @return: A list of top tickers in a given year based on certain classification
    """

    url = f"https://api.sectors.app/v1/companies/top/?classifications={dimension}&n_stock={top_n}&year={year}"

    return retrieve_from_endpoint(url)



