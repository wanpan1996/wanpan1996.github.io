import sys
import os
import json
from pathlib import Path

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from analysis.deepseek_api import generate_html_page

OUTPUT_DIR = Path(project_root) / 'web' / 'static'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR = Path(project_root) / 'data' / 'processed'

def generate_site(articles=None, digest=""):
    print("=" * 50)
    print("DeepSeek Flash - Auto Website Generator")
    print("=" * 50)

    if articles is None:
        analyzed_path = PROCESSED_DIR / 'analyzed.json'
        if analyzed_path.exists():
            with open(analyzed_path, 'r', encoding='utf-8') as f:
                articles = json.load(f)
            print(f"  Loaded {len(articles)} analyzed articles")
        else:
            from test_local import MOCK_ARTICLES
            articles = MOCK_ARTICLES
            print(f"  Using {len(articles)} mock articles")

    if not digest:
        digest_path = PROCESSED_DIR / 'digest.txt'
        if digest_path.exists():
            digest = digest_path.read_text(encoding='utf-8')

    print("  Generating HTML page via DeepSeek Flash...")
    html = generate_html_page(articles, digest)

    output_path = OUTPUT_DIR / 'index.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  Page saved to {output_path} ({len(html)} chars)")
    return html

if __name__ == '__main__':
    analyzed_path = PROCESSED_DIR / 'analyzed.json'
    articles = json.loads(analyzed_path.read_text(encoding='utf-8'))
    digest = (PROCESSED_DIR / 'digest.txt').read_text(encoding='utf-8')
    generate_site(articles, digest)
    print("\nDone! Open web/static/index.html in your browser.")
