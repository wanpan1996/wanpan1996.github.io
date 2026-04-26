from bs4 import BeautifulSoup
import requests
from typing import List, Dict, Any
import json
from pathlib import Path

class WebScraper:
    def __init__(self, headers: Dict[str, str] = None):
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    def scrape(self, url: str) -> Dict[str, Any]:
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        return {
            'url': url,
            'title': soup.title.string if soup.title else '',
            'content': soup.get_text(separator=' ', strip=True)
        }
    
    def scrape_multiple(self, urls: List[str]) -> List[Dict[str, Any]]:
        return [self.scrape(url) for url in urls]