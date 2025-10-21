# 🤖 Research Buddy

## Overview

**Research Buddy** is a Python-based programmatic toolkit for conducting systematic literature searches across multiple academic databases. Unlike configuration-based tools, Research Buddy provides full programmatic control through a clean Python API, making it ideal for:

- **Automated workflows** requiring integration with other tools
- **Custom search logic** and advanced filtering
- **Reproducible research** with version-controlled search scripts
- **Large-scale literature reviews** with programmatic paper processing

## Key Features

### 🔍 Multi-Source Search
- **Scopus**: Comprehensive coverage of peer-reviewed literature
- **PubMed**: Biomedical and life sciences focus
- **arXiv**: Pre-prints and cutting-edge research
- **Google Scholar**: Broad academic coverage
- **IEEE Xplore**: Engineering and computer science

### 📥 Intelligent Paper Downloading
- **8-Strategy Downloader**: Multiple fallback methods for PDF retrieval
- **Open Access Prioritization**: Unpaywall, arXiv, PubMed Central
- **Publisher Patterns**: Direct PDF links for major publishers
- **HTML Scraping**: Automatic detection of PDF links
- **Crossref Integration**: Automatic DOI lookup by title
- **98% Success Rate** for open access content

### 📚 Export Formats
- **BibTeX**: For LaTeX and reference managers
- **RIS**: For EndNote, Mendeley, Zotero
- **CSV**: For data analysis and spreadsheets

### 🔄 Smart Deduplication
Automatic removal of duplicate papers across sources based on:
- Title matching
- DOI comparison
- Source tracking

## Architecture

```
research_buddy/
├── searchers/           # Database-specific searchers
│   ├── scopus_searcher.py
│   ├── pubmed_searcher.py
│   ├── arxiv_searcher.py
│   ├── scholar_searcher.py
│   └── paper_downloader.py
├── models.py            # Data models (Paper, Author)
├── config.py            # Configuration management
└── paper_searcher.py    # Main coordinator
```

## Quick Example

```python
from paper_searcher import PaperSearcher
from config import Config

# Configure with API keys
config = Config(
    scopus_api_key="your_key",
    pubmed_email="your@email.com",
    max_results_per_source=50
)

# Search across all sources
searcher = PaperSearcher(config)
papers = searcher.search_all(
    query="machine learning healthcare",
    year_from=2020
)

# Export results
searcher.generate_bibliography(papers, format="bibtex", output_file="results.bib")
```

## Repository Information

**GitHub**: [https://github.com/leonardozaggia/review_buddy](https://github.com/leonardozaggia/review_buddy)

The Research Buddy codebase is actively maintained and welcomes contributions from the research community.

---

```{admonition} Coming Soon
Detailed tutorials on installation, configuration, and advanced usage patterns will be added in the following sections.
```

## When to Use Research Buddy vs Findpapers

| Feature | Research Buddy | Findpapers |
|---------|---------------|------------|
| **Control Level** | Full programmatic control | Configuration-based |
| **Learning Curve** | Moderate (Python knowledge) | Easy (YAML config) |
| **Customization** | Unlimited | Limited to config options |
| **Integration** | Easy to integrate in pipelines | Standalone tool |
| **Best For** | Automated workflows, custom logic | Quick searches, one-off reviews |

## Next Steps

Continue to the next sections to learn:
1. **Installation**: Setting up Research Buddy and obtaining API keys
2. **Usage Examples**: Complete workflows and code examples
3. **Advanced Features**: Custom searchers, batch processing, and more
