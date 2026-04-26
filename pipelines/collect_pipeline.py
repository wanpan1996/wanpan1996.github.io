import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.collectors.rss_collector import RSSCollector

RSS_FEEDS = [
    'https://github.com/BadsectorLabs/feed/feed.xml',
    'https://krebsonsecurity.com/feed/',
    'https://www.schneier.com/feed/atom/',
]

def run_collect_pipeline():
    print("Starting collection pipeline...")
    collector = RSSCollector(RSS_FEEDS)
    articles = collector.save_raw()
    print(f"Collected {len(articles)} articles")
    return articles

if __name__ == '__main__':
    run_collect_pipeline()