from requests import get
from bs4 import BeautifulSoup

def fetch(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    fetch_html = get(url, headers=headers).text
    soup = BeautifulSoup(fetch_html, "html.parser")
    return soup