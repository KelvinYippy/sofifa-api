from fastapi import HTTPException
from bs4 import BeautifulSoup
from utils import fetch


def valid_scrape(id: int) -> BeautifulSoup:
    soup = fetch(f"https://sofifa.com/team/{id}")
    if not soup:
        raise HTTPException(status_code=404, detail="Not a valid team id")
    return soup