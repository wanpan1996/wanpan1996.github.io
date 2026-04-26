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

def sanitize_text(s):
    if not isinstance(s, str):
        return s
    s = s.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
    s = s.replace('\t', ' ')
    s = s.replace('\x00', '').replace('\x01', '').replace('\x02', '')
    s = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def sanitize_article(article):
    clean = {}
    for key, val in article.items():
        if isinstance(val, str):
            clean[key] = sanitize_text(val)
        elif isinstance(val, list):
            clean[key] = [sanitize_text(v) if isinstance(v,str) else v for v in val]
        else:
            clean[key] = val
    return clean

def generate_site(articles=None, digest=""):
    print("=" * 50)
    print("Site Generator - Update data + digest")
    print("=" * 50)

    if articles is None:
        analyzed_path = PROCESSED_DIR / 'analyzed.json'
        if analyzed_path.exists():
            articles = json.loads(analyzed_path.read_text(encoding='utf-8'))
            print(f"  Loaded {len(articles)} articles")
        else:
            print("  ERROR: No analyzed.json found")
            return

    articles = [sanitize_article(a) for a in articles]

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

    # Create safe JSON (escape </script> etc for HTML embedding)
    data_json = json.dumps(articles, ensure_ascii=False, indent=2)

    # Use string slicing instead of re.sub to avoid regex escape issues
    start_marker = '<script type="application/json" id="articles-json">'
    end_marker = '</script>'
    start = html.find(start_marker)
    end = html.find(end_marker, start)
    if start >= 0 and end >= 0:
        data_start = start + len(start_marker)
        html = html[:data_start] + '\n' + data_json + '\n' + html[end:]
    else:
        print("  WARNING: Could not find data block, appending")
        html = html.replace('</body>', f'<script type="application/json" id="articles-json">\n{data_json}\n</script>\n</body>')

    # Update date
    today = datetime.now().strftime('%Y-%m-%d')
    html = re.sub(
        r'(\d{4}-\d{2}-\d{2})\s*[-·]\s*实时更新',
        f'{today}  ·  实时更新',
        html
    )

    TEMPLATE_PATH.write_text(html, encoding='utf-8')
    print(f"  Updated {TEMPLATE_PATH} with {len(articles)} articles")
    return html

if __name__ == '__main__':
    generate_site()
    print("\nDone!")
