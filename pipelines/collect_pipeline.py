import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from pathlib import Path
from data.collectors.badsector_collector import load_urls, BadsectorCollector

def run_collect_pipeline(max_urls=25):
    print("=" * 60)
    print("Badsector Labs Blog Collector")
    print("=" * 60)

    txt_path = Path(__file__).parent.parent / 'data' / 'blogs.txt'
    if not txt_path.exists():
        print("ERROR: data/blogs.txt not found")
        return

    urls = load_urls(str(txt_path))
    print(f"Loaded {len(urls)} blog URLs from Badsector Labs list")

    # Priority cybersecurity blogs
    keywords = [
        'krebsonsecurity', 'portswigger', 'schneier',
        'research.nccgroup', 'posts.specterops', 'labs.sentinelone',
        'unit42.paloaltonetworks', 'blog.cloudflare',
        'labs.f-secure', 'blog.fox-it',
        'blog.orange.tw', 'fortinet.com/blog/threat',
        'blog.google/threat', 'msrc.microsoft',
        'blog.trendmicro', 'security.googleblog',
        'thehackernews', 'bleepingcomputer',
        'blog.checkpoint', 'labs.detectify',
        'blog.sonarsource', 'labs.watchtowr',
        'blog.quarkslab', 'embracethered',
        'vulncheck', 'blog.includesecurity',
    ]

    filtered = [u for u in urls if any(k in u.lower() for k in keywords)]
    if len(filtered) < 15:
        filtered = urls[:max_urls]
    else:
        filtered = filtered[:max_urls]

    print(f"Selected {len(filtered)} priority blogs for scraping")

    collector = BadsectorCollector(filtered, max_urls=len(filtered))
    articles = collector.collect(delay=0.3)

    # Save
    output_path = Path(__file__).parent.parent / 'data' / 'raw' / 'badsector_collected.json'
    collector.save(str(output_path))
    print(f"\nSaved {len(articles)} articles to {output_path}")
    return articles

if __name__ == '__main__':
    run_collect_pipeline()
