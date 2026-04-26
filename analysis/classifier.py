from typing import List, Dict, Any
import re
from datetime import datetime, timedelta

class ContentClassifier:
    CATEGORY_KEYWORDS = {
        '新闻': ['news', 'release', 'announce', '漏洞', 'vulnerability', 'alert'],
        '技术': ['technique', 'tutorial', 'write-up', '分析', 'analysis', 'research'],
        '工具': ['tool', 'utility', 'github', 'project'],
        '研究': ['research', 'paper', 'study', '发现', 'discovery']
    }
    
    PRIORITY_KEYWORDS = {
        '重要': ['critical', 'urgent', 'cve-', 'zeroday', '0day', 'patch', '紧急'],
        '新技术': ['new', 'first', 'innovative', 'novel', 'ai', 'llm', 'gpt'],
    }
    
    @staticmethod
    def classify_category(text: str) -> str:
        text_lower = text.lower()
        for category, keywords in ContentClassifier.CATEGORY_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                return category
        return '其他'
    
    @staticmethod
    def classify_priority(text: str) -> str:
        text_lower = text.lower()
        for priority, keywords in ContentClassifier.PRIORITY_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                return priority
        return '普通'
    
    @staticmethod
    def calculate_heat_score(article: Dict[str, Any]) -> int:
        score = 0
        text = (article.get('title', '') + ' ' + article.get('summary', '')).lower()
        
        score += text.count('cve-') * 3
        score += text.count('0day') * 5
        score += text.count('vulnerability') * 2
        
        priority = ContentClassifier.classify_priority(text)
        if priority == '重要':
            score += 3
        elif priority == '新技术':
            score += 2
            
        return min(score, 100)
    
    @staticmethod
    def analyze_article(article: Dict[str, Any]) -> Dict[str, Any]:
        text = article.get('title', '') + ' ' + article.get('summary', '')
        
        return {
            'category': ContentClassifier.classify_category(text),
            'priority': ContentClassifier.classify_priority(text),
            'heat_score': ContentClassifier.calculate_heat_score(article),
            'tags': []
        }
    
    @staticmethod
    def batch_classify(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for article in articles:
            analyzed = article.copy()
            analysis = ContentClassifier.analyze_article(article)
            analyzed.update(analysis)
            results.append(analyzed)
        return results