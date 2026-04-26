# Badsector-Inspired Cybersecurity News Aggregator

## Project Overview
- **Type**: Cybersecurity news aggregation platform (web-based)
- **Core Functionality**: Automated "Data Collection → Intelligent Analysis → Visualization" pipeline
- **Similar To**: Badsector Labs
- **Features**: 
  - News aggregation with automatic tagging (热度/重要/新技术)
  - Techniques and Write-ups sections
  - RSS feed support

## Project Structure

```
CybersecurityNewsAggregator/
├── data/
│   ├── collectors/        # Data collection modules
│   │   ├── rss_collector.py
│   │   └── web_scraper.py
│   └── raw/               # Raw data storage
│       └── .gitkeep
├── analysis/              # Intelligent analysis
│   ├── classifier.py      # Tag classification (热度/重要/新技术)
│   ├── nlp_processor.py  # Natural language processing
│   └── content_analyzer.py
├── web/                   # Web interface/frontend
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── templates/
│       ├── index.html
│       └── article.html
├── pipelines/             # Data pipelines
│   ├── collect_pipeline.py
│   └── analyze_pipeline.py
├── requirements.txt
└── README.md
```

## Technology Stack
- **Backend**: Python (FastAPI/Flask)
- **Frontend**: HTML/CSS/JS
- **Data Processing**: BeautifulSoup, Feedparser, OpenAI/Local LLM
- **Database**: SQLite/PostgreSQL (optional)

## Setup
```bash
pip install -r requirements.txt
python -m pipelines.collect_pipeline
python -m pipelines.analyze_pipeline
```

## License
MIT