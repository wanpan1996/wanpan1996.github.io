import os
import re
import json
from openai import OpenAI

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "sk-81bfd68b425b4ec6a01805454a791838")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-v4-flash"

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

SYSTEM_PROMPT = """You are a cybersecurity news analyst. Analyze the given article and return a JSON object with these fields:
{
  "category": "新闻/技术/工具/研究" (choose one),
  "priority": "重要/新技术/普通" (重要=critical vulns/exploits/urgent, 新技术=new techniques/innovative, 普通=routine),
  "heat_score": 0-100 (based on severity and urgency),
  "summary_short": "Chinese summary under 100 chars",
  "keywords": ["keyword1", "keyword2", ...],
  "tags": ["tag1", "tag2"]
}

Return ONLY valid JSON, no markdown or explanation."""

def _strip_markdown(text: str) -> str:
    text = text.strip()
    text = re.sub(r'^```(?:html|json)?\s*\n?', '', text)
    text = re.sub(r'\n?```\s*$', '', text)
    return text.strip()

def analyze_article(title: str, summary: str, source: str = "") -> dict:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Title: {title}\nSummary: {summary}\nSource: {source}"}
        ],
        temperature=0.1,
        response_format={"type": "json_object"},
    )
    raw = response.choices[0].message.content
    cleaned = _strip_markdown(raw)
    return json.loads(cleaned)

def generate_daily_digest(articles: list) -> str:
    articles_text = "\n\n".join([
        f"[{a.get('priority','')}] {a.get('title','')}: {a.get('summary_short','')}"
        for a in articles[:20]
    ])

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a cybersecurity expert. Write a concise daily digest in Chinese summarizing the most important security news today. Highlight critical threats. Keep under 500 chars."},
            {"role": "user", "content": f"Today's articles:\n{articles_text}"}
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()

def generate_html_page(articles: list, digest: str) -> str:
    articles_text = "\n\n".join([
        f"[{a.get('priority','')}] [{a.get('category','')}] {a.get('title','')} | {a.get('summary_short','')}"
        for a in articles[:30]
    ])

    prompt = f"""Generate a complete, standalone HTML page for a cybersecurity news aggregator called "SecNews - AI Powered".
Requirements:
- Dark theme, professional look
- Hero section with daily digest: "{digest[:200]}"
- Article cards with tags (🔥热门, ⚠️重要, 🆕新技术)
- Filter buttons: All / Hot / Important / New Tech / News / Techniques
- Responsive, modern CSS (use inline <style>)
- Include all JS interactivity inline (filter, search)
- NO external dependencies

Articles to display (use ALL of them):
{articles_text}

Return ONLY the complete HTML code, no markdown wrapping."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a senior frontend developer. Generate production-quality HTML/CSS/JS. Return ONLY raw HTML, no code blocks."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )
    return _strip_markdown(response.choices[0].message.content)
