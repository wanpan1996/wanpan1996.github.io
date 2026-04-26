import sys
import os
import json
import re
from pathlib import Path
from datetime import datetime

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from analysis.deepseek_api import generate_daily_digest

PROCESSED_DIR = Path(project_root) / 'data' / 'processed'
TEMPLATE_PATH = Path(project_root) / 'index.html'

def generate_site(articles=None, digest=""):
    print("=" * 50)
    print("Site Generator - Update data + digest")
    print("=" * 50)

    if articles is None:
        analyzed_path = PROCESSED_DIR / 'analyzed.json'
        if analyzed_path.exists():
            articles = json.loads(analyzed_path.read_text(encoding='utf-8'))
            print(f"  Loaded {len(articles)} analyzed articles")
        else:
            print("  ERROR: No analyzed.json found. Run analyze_pipeline first.")
            return

    if not digest:
        digest_path = PROCESSED_DIR / 'digest.txt'
        if digest_path.exists():
            digest = digest_path.read_text(encoding='utf-8')
        else:
            print("  Generating daily digest via DeepSeek Flash...")
            digest = generate_daily_digest(articles)

    if not TEMPLATE_PATH.exists():
        print("  ERROR: index.html template not found")
        return

    html = TEMPLATE_PATH.read_text(encoding='utf-8')

    # Replace the data block
    data_json = json.dumps(articles, ensure_ascii=False, indent=2)
    html = re.sub(
        r'<script type="application/json" id="articles-json">.*?</script>',
        f'<script type="application/json" id="articles-json">\n{data_json}\n</script>',
        html,
        flags=re.DOTALL
    )

    # Replace digest date
    today = datetime.now().strftime('%Y-%m-%d')
    html = re.sub(
        r'(\d{4}-\d{2}-\d{2})\s*[-·]\s*实时更新',
        f'{today}  ·  实时更新',
        html
    )

    TEMPLATE_PATH.write_text(html, encoding='utf-8')
    print(f"  Updated {TEMPLATE_PATH} with {len(articles)} articles")
    print(f"  Digest date set to {today}")
    return html

if __name__ == '__main__':
    generate_site()
    print("\nDone!")
