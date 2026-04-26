from typing import List, Dict, Any
from pathlib import Path

class ContentAnalyzer:
    @staticmethod
    def analyze_full(article: Dict[str, Any]) -> Dict[str, Any]:
        from .classifier import ContentClassifier
        from .nlp_processor import NLPProcessor
        
        base_analysis = ContentClassifier.analyze_article(article)
        nlp_analysis = NLPProcessor.process(article)
        
        return {
            **article,
            **base_analysis,
            **nlp_analysis
        }
    
    @staticmethod
    def analyze_batch(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [ContentAnalyzer.analyze_full(a) for a in articles]
    
    @staticmethod
    def save_processed(articles: List[Dict[str, Any]], output_path: str):
        import json
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)