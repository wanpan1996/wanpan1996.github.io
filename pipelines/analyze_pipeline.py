import sys
import os
import json
from pathlib import Path
from datetime import datetime

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from analysis.deepseek_api import analyze_article, generate_daily_digest, generate_html_page

OUTPUT_DIR = Path(project_root) / 'data' / 'processed'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def run_analyze_pipeline(articles=None):
    print("=" * 50)
    print("DeepSeek Flash AI Analysis Pipeline")
    print("=" * 50)

    if articles is None:
        data_dir = Path(project_root) / 'data' / 'raw'
        files = sorted(data_dir.glob('raw_*.json'))
        if not files:
            from test_local import MOCK_ARTICLES
            articles = MOCK_ARTICLES
            print(f"  Using {len(articles)} mock articles")
        else:
            with open(files[-1], 'r', encoding='utf-8') as f:
                articles = json.load(f)
            print(f"  Loaded {len(articles)} articles from {files[-1]}")

    analyzed = []
    for i, article in enumerate(articles):
        print(f"  [{i+1}/{len(articles)}] Analyzing: {article.get('title','')[:60]}...")
        try:
            result_json = analyze_article(
                title=article.get('title', ''),
                summary=article.get('summary', ''),
                source=article.get('source', '')
            )
            result = json.loads(result_json) if isinstance(result_json, str) else result_json
            merged = {**article, **result}
            analyzed.append(merged)
            print(f"    → [{result.get('priority','')}] [{result.get('category','')}] hot={result.get('heat_score',0)}")
        except Exception as e:
            print(f"    ✗ Error: {e}")
            analyzed.append(article)

    # Save
    output_path = OUTPUT_DIR / 'analyzed.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analyzed, f, ensure_ascii=False, indent=2)
    print(f"\n  Saved {len(analyzed)} articles to {output_path}")

    # Generate digest
    print("\n  Generating daily digest...")
    try:
        digest = generate_daily_digest(analyzed)
        digest_path = OUTPUT_DIR / 'digest.txt'
        with open(digest_path, 'w', encoding='utf-8') as f:
            f.write(digest)
        print(f"  Digest saved to {digest_path}")
    except Exception as e:
        print(f"  Digest error: {e}")
        digest = ""

    return analyzed, digest

if __name__ == '__main__':
    run_analyze_pipeline()
