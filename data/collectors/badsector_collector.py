from typing import List, Dict, Any
import requests
import re
import json
import time
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

def load_urls(filepath: str) -> List[str]:
    """Load blog URLs from text file."""
    urls = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and line.startswith('http'):
                urls.append(line)
    return urls

def find_rss_feed(html: str, base_url: str) -> str:
    """Try to find RSS/Atom feed URL from page HTML."""
    soup = BeautifulSoup(html, 'lxml')
    for link in soup.find_all('link', rel=re.compile(r'alternate', re.I)):
        if 'rss' in link.get('type', '') or 'atom' in link.get('type', '') or 'xml' in link.get('type', ''):
            href = link.get('href', '')
            if href:
                if href.startswith('http'):
                    return href
                elif href.startswith('/'):
                    from urllib.parse import urljoin
                    return urljoin(base_url, href)
    return None

def scrape_page(url: str, timeout: int = 15) -> Dict[str, Any]:
    """Scrape a single blog page and extract article content."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'lxml')
        
        title = ''
        if soup.title:
            title = soup.title.get_text(strip=True)
        
        # Try to extract article content
        content_parts = []
        
        # Common article selectors
        for selector in ['article', 'main', '.post', '.entry', '.content', '#content', '.blog-post']:
            article = soup.select_one(selector)
            if article:
                paragraphs = article.find_all(['p', 'h2', 'h3', 'h4'])
                for p in paragraphs[:20]:
                    text = p.get_text(strip=True)
                    if len(text) > 30:
                        content_parts.append(text)
                if content_parts:
                    break
        
        # Fallback: get all paragraphs
        if not content_parts:
            for p in soup.find_all('p')[:15]:
                text = p.get_text(strip=True)
                if len(text) > 40:
                    content_parts.append(text)
        
        summary = ' '.join(content_parts[:3])[:500] if content_parts else ''
        content = ' '.join(content_parts[:5])[:1000]
        
        return {
            'url': url,
            'title': title,
            'summary': summary,
            'content': content,
            'source': _extract_domain(url),
            'status': 'ok'
        }
    except Exception as e:
        return {
            'url': url,
            'title': '',
            'summary': '',
            'content': '',
            'source': _extract_domain(url),
            'status': f'error: {str(e)[:100]}'
        }

def _extract_domain(url: str) -> str:
    m = re.search(r'https?://(?:www\.)?([^/]+)', url)
    return m.group(1) if m else url[:50]

class BadsectorCollector:
    """Collector that scrapes content from Badsector Labs blog list."""
    
    def __init__(self, urls: List[str], max_urls: int = 30):
        self.urls = urls[:max_urls]
        self.articles = []

    def collect(self, delay: float = 1.0) -> List[Dict[str, Any]]:
        print(f"Scraping {len(self.urls)} URLs...")
        for i, url in enumerate(self.urls):
            try:
                print(f"  [{i+1}/{len(self.urls)}] {url[:80]}")
                result = scrape_page(url)
                if result['status'] == 'ok' and result['summary']:
                    self.articles.append(result)
                    print(f"    -> {result['title'][:60]}")
                else:
                    print(f"    -> skipped (no content)")
            except Exception as e:
                print(f"    -> error: {e}")
            if delay and i < len(self.urls) - 1:
                time.sleep(delay)
        return self.articles
    
    def save(self, output_path: str = None):
        if not output_path:
            output_path = Path(__file__).parent.parent.parent / 'data' / 'raw' / 'badsector_collected.json'
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.articles, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(self.articles)} articles to {output_path}")
        return output_path


if __name__ == '__main__':
    import os, sys
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, project_root)
    
    txt_path = Path(project_root) / 'data' / 'blogs.txt'
    urls = load_urls(str(txt_path))
    print(f"Loaded {len(urls)} URLs")
    
    # Select high-signal domains for scraping
    priority_domains = [
        'krebsonsecurity.com', 'portswigger.net', 'schneier.com',
        'research.nccgroup.com', 'posts.specterops.io',
        'labs.sentinelone.com', 'blog.cloudflare.com',
        'unit42.paloaltonetworks.com', 'blog.google/threat',
        'googleblog.com', 'blog.fox-it.com', 'labs.f-secure.com',
        'blog.orange.tw', 'blog.talosintelligence.com',
    ]
    
    filtered = [u for u in urls if any(d in u for d in priority_domains)]
    if len(filtered) < 10:
        filtered = urls[:25]
    
    collector = BadsectorCollector(filtered, max_urls=20)
    articles = collector.collect(delay=0.5)
    collector.save()
