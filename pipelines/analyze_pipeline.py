import sys
import os
import json
import io
import re
from pathlib import Path
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from analysis.deepseek_api import analyze_article, generate_daily_digest

OUTPUT_DIR = Path(project_root) / 'data' / 'processed'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def _sanitize_result(d: dict) -> dict:
    clean = {}
    for k, v in d.items():
        if isinstance(v, str):
            v = v.replace('\r\n',' ').replace('\n',' ').replace('\r',' ').replace('\t',' ')
            v = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', v)
            v = re.sub(r'\s+', ' ', v).strip()
            clean[k] = v
        elif isinstance(v, list):
            clean[k] = [_sanitize_result(e) if isinstance(e,dict) else str(e).replace('\n',' ') for e in v]
        else:
            clean[k] = v
    return clean

def run_analyze_pipeline(articles=None):
    print("=" * 50)
    print("DeepSeek Flash AI Analysis Pipeline")
    print("=" * 50)

    if articles is None:
        data_dir = Path(project_root) / 'data' / 'raw'
        # Prefer Badsector collected data over generic raw data
        badsector_path = data_dir / 'badsector_collected.json'
        if badsector_path.exists():
            with open(badsector_path, 'r', encoding='utf-8') as f:
                articles = json.load(f)
            print(f"  Loaded {len(articles)} articles from Badsector Labs")
        else:
            files = sorted(data_dir.glob('raw_*.json'))
            if files:
                with open(files[-1], 'r', encoding='utf-8') as f:
                    articles = json.load(f)
                print(f"  Loaded {len(articles)} articles from {files[-1]}")
            else:
                from test_local import MOCK_ARTICLES
                articles = MOCK_ARTICLES
                print(f"  Using {len(articles)} mock articles")

    analyzed = []
    for i, article in enumerate(articles):
        title = article.get('title', '')[:80]
        try:
            print(f"  [{i+1}/{len(articles)}] Analyzing: {title}")
        except UnicodeEncodeError:
            print(f"  [{i+1}/{len(articles)}] Analyzing: {title.encode('ascii', 'replace').decode()}")
        try:
            result = analyze_article(
                title=article.get('title', ''),
                summary=article.get('summary', ''),
                source=article.get('source', '')
            )
            # Map to filter-compatible tags
            filter_tags = []
            if result.get('priority') == '重要':
                filter_tags.append('important')
            elif result.get('priority') == '新技术':
                filter_tags.append('newtech')
            cat = result.get('category', '')
            if cat == '新闻': filter_tags.append('news')
            elif cat == '技术': filter_tags.append('techniques')
            elif cat == '工具': filter_tags.append('tools')
            elif cat == '研究': filter_tags.append('news')
            result['tags'] = filter_tags
            # Sanitize all string fields
            result = _sanitize_result(result)
            merged = {**article, **result}
            analyzed.append(merged)
            try:
                print(f"    -> [{result.get('priority','')}] [{result.get('category','')}] hot={result.get('heat_score',0)}")
            except UnicodeEncodeError:
                print(f"    -> [{result.get('priority','')[:2]}] hot={result.get('heat_score',0)}")
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
