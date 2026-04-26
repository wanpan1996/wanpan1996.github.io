"""
Real RSS/Atom feed collector for Badsector Labs blog list.
Fetches actual articles from known RSS feeds.
"""
import sys
import os
import json
import re
import time
import feedparser
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import requests

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

# Known working RSS/Atom feeds from the Badsector list
KNOWN_FEEDS = [
    # Major security news
    'https://krebsonsecurity.com/feed/',
    'https://www.schneier.com/feed/atom/',
    'https://feeds.feedburner.com/TheHackersNews',
    'https://www.bleepingcomputer.com/feed/',
    'https://threatpost.com/feed/',
    # Vendor blogs
    'https://blog.cloudflare.com/rss/',
    'https://unit42.paloaltonetworks.com/feed/',
    'https://labs.f-secure.com/feed/',
    'https://labs.sentinelone.com/feed/',
    'https://blog.fox-it.com/feed/',
    'https://research.nccgroup.com/feed/',
    'https://posts.specterops.io/feed',
    'https://blog.orange.tw/atom.xml',
    'https://blog.google/threat-analysis-group/rss/',
    'https://msrc.microsoft.com/blog/feed/',
    'https://security.googleblog.com/feeds/posts/default',
    'https://www.fortinet.com/blog/threat-research/rss.xml',
    'https://labs.detectify.com/feed/',
    'https://blog.sonarsource.com/feed/',
    'https://labs.watchtowr.com/feed/',
    'https://blog.quarkslab.com/feed/',
    'https://embracethered.com/blog/feed/',
    'https://blog.includesecurity.com/feed/',
    'https://www.trendmicro.com/en_us/research.html?category=trend-micro-research:threats/exploits-and-vulnerabilities/rss.xml',
    'https://blog.checkpoint.com/feed/',
    'https://portswigger.net/daily-swig/rss',
    'https://devco.re/en/blog/feed/',
    'https://blog.assetnote.io/feed.xml',
    'https://blog.talosintelligence.com/rss/',
    # GitHub security research blogs
    'https://securitylab.github.com/rss/',
    # Additional
    'https://www.wiz.io/blog/rss.xml',
    'https://blog.syss.com/feed/',
    'https://www.horizon3.ai/feed/',
    'https://positive.security/blog/feed.xml',
    'https://www.praetorian.com/blog/rss.xml',
    'https://blog.cobaltstrike.com/feed/',
    'https://www.trustedsec.com/blog/feed/',
    'https://www.mdsec.co.uk/feed/',
]


def sanitize(s):
    if not s:
        return ''
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\s+', ' ', s)
    s = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', s)
    return s.strip()


def collect_feeds(feeds: List[str], max_per_feed: int = 5) -> List[Dict[str, Any]]:
    articles = []
    total = len(feeds)

    for i, feed_url in enumerate(feeds):
        try:
            print(f"  [{i+1}/{total}] {feed_url[:70]}")
            feed = feedparser.parse(feed_url)
            if feed.bozo and not feed.entries:
                print(f"    -> no entries / parse error")
                continue

            entries = feed.entries[:max_per_feed]
            for entry in entries:
                title = sanitize(entry.get('title', ''))
                summary = sanitize(entry.get('summary', entry.get('description', '')))
                link = entry.get('link', '')
                published = entry.get('published', entry.get('updated', ''))

                if not title or len(title) < 5:
                    continue

                articles.append({
                    'title': title,
                    'summary': summary[:800],
                    'url': link,
                    'source': _domain(feed_url),
                    'published': published,
                })

            print(f"    -> {len(entries)} articles")
        except Exception as e:
            print(f"    -> error: {e}")

        if i % 5 == 0 and i > 0:
            time.sleep(0.5)

    return articles


def _domain(url):
    return re.search(r'https?://(?:www\.)?([^/]+)', url).group(1)


if __name__ == '__main__':
    print("=" * 60)
    print("RSS Feed Collector - Badsector Labs Sources")
    print("=" * 60)
    print(f"{len(KNOWN_FEEDS)} RSS feeds configured\n")

    articles = collect_feeds(KNOWN_FEEDS, max_per_feed=3)

    if not articles:
        print("\nNo articles collected from RSS feeds.")
        # Fallback: scrape known good feeds
        print("Trying fallback feeds...")
        fallback = [
            'https://krebsonsecurity.com/feed/',
            'https://feeds.feedburner.com/TheHackersNews',
            'https://www.bleepingcomputer.com/feed/',
            'https://www.schneier.com/feed/atom/',
        ]
        articles = collect_feeds(fallback, max_per_feed=5)

    output_path = Path(project_root) / 'data' / 'raw' / 'rss_articles.json'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"\nSaved {len(articles)} RSS articles to {output_path}")

    # Show preview
    if articles:
        print("\nSample:")
        for a in articles[:3]:
            print(f"  [{a['source']}] {a['title'][:70]}")
