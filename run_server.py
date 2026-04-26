import sys
import os
import json
from pathlib import Path

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from http.server import HTTPServer, SimpleHTTPRequestHandler

PROCESSED_PATH = Path(project_root) / 'data' / 'processed' / 'analyzed.json'

MOCK_ARTICLES = [
    {"title": "Critical CVE-2024-1234 Exploit Found in Apache", "summary": "A new zero-day vulnerability in Apache HTTP server allows remote code execution. Patch immediately.", "source": "securityweek.com", "category": "技术", "priority": "重要", "heat_score": 95, "summary_short": "Apache HTTP Server 零日漏洞可远程代码执行。", "keywords": ["apache", "cve", "exploit", "rce"], "cve_ids": ["CVE-2024-1234"], "tags": ["important", "news"]},
    {"title": "New LLM-Based Attack Technique Bypasses Multi-Factor Authentication", "summary": "Researchers discover innovative AI-powered method to bypass MFA systems.", "source": "schneier.com", "category": "技术", "priority": "新技术", "heat_score": 85, "summary_short": "基于LLM的新型攻击技术首次绕过MFA认证。", "keywords": ["llm", "ai", "mfa", "authentication"], "cve_ids": [], "tags": ["newtech", "techniques"]},
    {"title": "Weekly Security News Roundup - April 2026", "summary": "This week in cybersecurity: several patches released.", "source": "krebsonsecurity.com", "category": "新闻", "priority": "普通", "heat_score": 30, "summary_short": "本周安全新闻汇总：多个补丁发布。", "keywords": ["weekly", "security", "news"], "cve_ids": [], "tags": ["news"]},
    {"title": "GitHub Releases New CodeQL Analysis Tool v3.0", "summary": "A major update to the open-source static code analysis tool.", "source": "github.blog", "category": "工具", "priority": "新技术", "heat_score": 72, "summary_short": "GitHub发布CodeQL 3.0，AI驱动漏洞检测。", "keywords": ["github", "codeql", "analysis"], "cve_ids": [], "tags": ["newtech", "tools"]},
    {"title": "APT29 Targets Financial Sector with Sophisticated Malware", "summary": "State-sponsored threat group deploys new malware variant. CISA alert.", "source": "threatpost.com", "category": "新闻", "priority": "重要", "heat_score": 94, "summary_short": "APT29针对金融行业部署新型恶意软件。", "keywords": ["apt29", "malware", "cisa"], "cve_ids": [], "tags": ["important", "news"]},
    {"title": "Rust-Based Ransomware BlackCat Evolves with New Evasion Techniques", "summary": "BlackCat ransomware group releases new version with advanced anti-detection.", "source": "bleepingcomputer.com", "category": "技术", "priority": "重要", "heat_score": 78, "summary_short": "BlackCat勒索软件Rust版升级，新增反检测能力。", "keywords": ["ransomware", "rust", "blackcat"], "cve_ids": [], "tags": ["important", "techniques"]},
    {"title": "OpenAI GPT-5 with Built-in Security Audit", "summary": "GPT-5 introduces automatic vulnerability scanning and secure code generation.", "source": "thehackernews.com", "category": "工具", "priority": "新技术", "heat_score": 88, "summary_short": "GPT-5内置自动漏洞扫描与安全代码生成功能。", "keywords": ["openai", "gpt5", "security"], "cve_ids": [], "tags": ["newtech", "tools"]},
]

class RequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=project_root, **kwargs)

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

    def log_message(self, format, *args):
        print("[%s] %s" % (self.log_date_time_string(), format % args))

if __name__ == '__main__':
    port = 8080
    server = HTTPServer(('0.0.0.0', port), RequestHandler)
    print(f"SecNews server running at http://localhost:{port}")
    print("Press Ctrl+C to stop")
    server.serve_forever()
