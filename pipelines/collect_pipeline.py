import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from pathlib import Path
from datetime import datetime

def run_collect_pipeline():
    print("=" * 60)
    print("SecNews Collector - RSS + Badsector")
    print("=" * 60)

    from data.collectors.rss_feed_collector import KNOWN_FEEDS, collect_feeds

    print(f"Configured {len(KNOWN_FEEDS)} RSS feeds\n")
    articles = collect_feeds(KNOWN_FEEDS, max_per_feed=3)

    if not articles:
        print("\nNo articles. Trying homepage scraper fallback...")
        from data.collectors.badsector_collector import load_urls, BadsectorCollector
        txt = Path(__file__).parent.parent / 'data' / 'blogs.txt'
        urls = load_urls(str(txt))
        collector = BadsectorCollector(urls[:15], max_urls=15)
        articles = collector.collect(delay=0.3)

    # Save
    output = Path(__file__).parent.parent / 'data' / 'raw' / 'collected.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"\nSaved {len(articles)} articles to {output}")
    return articles

if __name__ == '__main__':
    run_collect_pipeline()
