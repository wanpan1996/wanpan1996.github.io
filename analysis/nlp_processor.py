import re
from typing import List, Dict, Any

class NLPProcessor:
    @staticmethod
    def clean_text(text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\u4e00-\u9fff\-.,!?]', '', text)
        return text.strip()
    
    @staticmethod
    def extract_keywords(text: str, top_k: int = 10) -> List[str]:
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = re.findall(r'\b\w+\b', text.lower())
        word_freq = {}
        for word in words:
            if len(word) > 2 and word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [w[0] for w in sorted_words[:top_k]]
    
    @staticmethod
    def extract_cve_ids(text: str) -> List[str]:
        return re.findall(r'CVE-\d{4}-\d{4,}', text, re.IGNORECASE)
    
    @staticmethod
    def summarize(text: str, max_length: int = 200) -> str:
        if len(text) <= max_length:
            return text
        return text[:max_length].rsplit(' ', 1)[0] + '...'
    
    @staticmethod
    def process(article: Dict[str, Any]) -> Dict[str, Any]:
        title = article.get('title', '')
        summary = article.get('summary', '')
        text = f"{title} {summary}"
        
        return {
            'cleaned_title': NLPProcessor.clean_text(title),
            'cleaned_summary': NLPProcessor.clean_text(summary),
            'keywords': NLPProcessor.extract_keywords(text),
            'cve_ids': NLPProcessor.extract_cve_ids(text),
            'summary_short': NLPProcessor.summarize(summary)
        }