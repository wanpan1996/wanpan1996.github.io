from abc import ABC, abstractmethod
from typing import List, Dict, Any
import feedparser
from datetime import datetime
import json
from pathlib import Path

class BaseCollector(ABC):
    @abstractmethod
    def collect(self) -> List[Dict[str, Any]]:
        pass

class RSSCollector(BaseCollector):
    def __init__(self, feeds: List[str]):
        self.feeds = feeds
        
    def collect(self) -> List[Dict[str, Any]]:
        articles = []
        for feed_url in self.feeds:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                article = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'summary': entry.get('summary', ''),
                    'source': feed_url
                }
                articles.append(article)
        return articles
    
    def save_raw(self, output_dir: str = 'data/raw'):
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        articles = self.collect()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        with open(f'{output_dir}/raw_{timestamp}.json', 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        return articles