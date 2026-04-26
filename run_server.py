import sys
import os
import json
from pathlib import Path

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json

PROCESSED_PATH = Path(project_root) / 'data' / 'processed' / 'analyzed.json'

MOCK_ARTICLES = [
    {"title": "Critical CVE-2024-1234 Exploit Found in Apache", "summary": "A new zero-day vulnerability in Apache HTTP server allows remote code execution. Patch immediately.", "source": "securityweek.com", "category": "技术", "priority": "重要", "heat_score": 92, "summary_short": "A new zero-day vulnerability in Apache HTTP server allows remote code execution.", "keywords": ["apache", "cve", "exploit", "rce", "vulnerability"], "cve_ids": ["CVE-2024-1234"]},
    {"title": "New LLM-Based Attack Technique Bypasses Multi-Factor Authentication", "summary": "Researchers discover innovative AI-powered method to bypass MFA systems using adversarial prompts.", "source": "schneier.com", "category": "技术", "priority": "新技术", "heat_score": 85, "summary_short": "Researchers discover innovative AI-powered method to bypass MFA systems.", "keywords": ["llm", "ai", "mfa", "authentication", "adversarial"], "cve_ids": []},
    {"title": "Weekly Security News Roundup - April 2026", "summary": "This week in cybersecurity: several patches released, minor bugs fixed. Routine updates from major vendors.", "source": "krebsonsecurity.com", "category": "新闻", "priority": "普通", "heat_score": 15, "summary_short": "This week in cybersecurity: routine updates from major vendors.", "keywords": ["weekly", "security", "news", "roundup", "patches"], "cve_ids": []},
    {"title": "GitHub Releases New CodeQL Analysis Tool v3.0", "summary": "A major update to the open-source static code analysis tool with AI-powered vulnerability detection.", "source": "github.blog", "category": "工具", "priority": "新技术", "heat_score": 72, "summary_short": "Major update to the open-source static code analysis tool.", "keywords": ["github", "codeql", "analysis", "tool", "static"], "cve_ids": []},
    {"title": "APT29 Targets Financial Sector with Sophisticated Malware", "summary": "State-sponsored threat group deploys new malware variant. Critical alert issued by CISA and FBI.", "source": "threatpost.com", "category": "新闻", "priority": "重要", "heat_score": 94, "summary_short": "State-sponsored threat group deploys new malware variant.", "keywords": ["apt", "malware", "financial", "cisa", "fbi"], "cve_ids": []},
    {"title": "Rust-Based Ransomware 'BlackCat' Evolves with New Evasion Techniques", "summary": "BlackCat ransomware group releases new version with advanced anti-detection capabilities written in Rust.", "source": "bleepingcomputer.com", "category": "技术", "priority": "重要", "heat_score": 78, "summary_short": "BlackCat ransomware group releases new version with advanced anti-detection.", "keywords": ["ransomware", "rust", "blackcat", "evasion", "malware"], "cve_ids": []},
    {"title": "OpenAI Announces GPT-5 with Built-in Security Audit Capabilities", "summary": "GPT-5 introduces automatic vulnerability scanning and secure code generation features for developers.", "source": "thehackernews.com", "category": "工具", "priority": "新技术", "heat_score": 88, "summary_short": "GPT-5 introduces automatic vulnerability scanning and secure code generation.", "keywords": ["openai", "gpt5", "security", "audit", "code"], "cve_ids": []},
]

class RequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(project_root) / 'web'), **kwargs)

    def do_GET(self):
        if self.path == '/api/articles':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            if PROCESSED_PATH.exists():
                with open(PROCESSED_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = MOCK_ARTICLES
            
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        else:
            super().do_GET()

if __name__ == '__main__':
    port = 8080
    server = HTTPServer(('0.0.0.0', port), RequestHandler)
    print(f"Server running at http://localhost:{port}")
    print("Press Ctrl+C to stop")
    server.serve_forever()
