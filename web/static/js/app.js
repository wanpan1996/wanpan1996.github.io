class NewsAggregator {
    constructor() {
        this.articles = [];
        this.currentFilter = 'all';
    }

    async fetchArticles() {
        try {
            const response = await fetch('/api/articles');
            this.articles = await response.json();
            this.render();
        } catch (error) {
            console.error('Failed to fetch articles:', error);
        }
    }

    getFilterClass(article) {
        const classes = [];
        if (article.heat_score >= 50) classes.push('hot');
        if (article.priority === '重要') classes.push('important');
        if (article.priority === '新技术') classes.push('new-tech');
        return classes;
    }

    filterArticles() {
        if (this.currentFilter === 'all') return this.articles;
        
        return this.articles.filter(article => {
            switch (this.currentFilter) {
                case 'hot':
                    return article.heat_score >= 50;
                case 'important':
                    return article.priority === '重要';
                case 'new-tech':
                    return article.priority === '新技术';
                case 'news':
                    return article.category === '新闻';
                case 'technique':
                    return article.category === '技术';
                default:
                    return true;
            }
        });
    }

    getCategoryLabel(category) {
        const labels = {
            '新闻': 'News',
            '技术': 'Technique',
            '工具': 'Tool',
            '研究': 'Research',
            '其他': 'Other'
        };
        return labels[category] || category;
    }

    render() {
        const container = document.getElementById('articles');
        const filtered = this.filterArticles();
        
        container.innerHTML = filtered.map(article => `
            <article class="article">
                <div class="article-header">
                    <h2>${article.title}</h2>
                    <div class="tags">
                        ${this.getFilterClass(article).map(c => `<span class="tag ${c}">${c === 'new-tech' ? '新技术' : c === 'hot' ? '热门' : c}</span>`).join('')}
                    </div>
                </div>
                <div class="article-meta">
                    <span>${this.getCategoryLabel(article.category)}</span>
                    <span> | </span>
                    <span>${article.source}</span>
                    <span> | </span>
                    <span>热度: ${article.heat_score}</span>
                </div>
                <p class="article-summary">${article.summary_short || article.summary}</p>
            </article>
        `).join('');
    }

    setFilter(filter) {
        this.currentFilter = filter;
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.filter === filter);
        });
        this.render();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const app = new NewsAggregator();
    app.fetchArticles();

    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            app.setFilter(btn.dataset.filter);
        });
    });
});