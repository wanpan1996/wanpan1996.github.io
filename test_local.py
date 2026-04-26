import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
from pathlib import Path
from analysis.classifier import ContentClassifier
from analysis.nlp_processor import NLPProcessor
from analysis.content_analyzer import ContentAnalyzer
from data.collectors.rss_collector import RSSCollector

MOCK_ARTICLES = [
    {"title": "Critical CVE-2024-1234 Exploit Found in Apache", "summary": "A new zero-day vulnerability in Apache HTTP server allows remote code execution. Patch immediately.", "source": "test"},
    {"title": "New LLM-Based Attack Technique Bypasses Authentication", "summary": "Researchers discover innovative AI-powered method to bypass MFA. First of its kind.", "source": "test"},
    {"title": "Weekly Security News Roundup", "summary": "This week in cybersecurity: several patches released, minor bugs fixed. Routine updates.", "source": "test"},
    {"title": "GitHub Releases New CodeQL Analysis Tool", "summary": "A new open-source tool for static code analysis has been released on GitHub.", "source": "test"},
    {"title": "Advanced Persistent Threat Group Targets Financial Sector", "summary": "State-sponsored hackers deploy sophisticated malware. Critical alert issued by CISA.", "source": "test"},
]

def test_classifier():
    print("=" * 50)
    print("TEST: ContentClassifier")
    print("=" * 50)
    
    for article in MOCK_ARTICLES:
        result = ContentClassifier.analyze_article(article)
        print(f"  [{result['priority']}] [{result['category']}] hot={result['heat_score']} | {article['title']}")
    print()

def test_nlp():
    print("=" * 50)
    print("TEST: NLPProcessor")
    print("=" * 50)
    
    for article in MOCK_ARTICLES:
        result = NLPProcessor.process(article)
        print(f"  Keywords: {result['keywords'][:5]}")
        print(f"  CVE IDs: {result['cve_ids']}")
        print()
    print()

def test_full_pipeline():
    print("=" * 50)
    print("TEST: Full Analysis Pipeline")
    print("=" * 50)
    
    analyzed = ContentAnalyzer.analyze_batch(MOCK_ARTICLES)
    
    # Save
    output_path = "data/processed/analyzed.json"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analyzed, f, ensure_ascii=False, indent=2)
    print(f"  Saved {len(analyzed)} articles to {output_path}")
    
    # Verify read
    with open(output_path, 'r', encoding='utf-8') as f:
        loaded = json.load(f)
    assert len(loaded) == len(MOCK_ARTICLES), "Data mismatch!"
    print(f"  Verified: {len(loaded)} articles loaded back")
    
    # Summary
    categories = {}
    for a in analyzed:
        cat = a.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1
    print(f"  Categories: {categories}")
    
    priorities = {}
    for a in analyzed:
        p = a.get('priority', 'unknown')
        priorities[p] = priorities.get(p, 0) + 1
    print(f"  Priorities: {priorities}")
    print()

if __name__ == '__main__':
    test_classifier()
    test_nlp()
    test_full_pipeline()
    print("All tests passed!")
