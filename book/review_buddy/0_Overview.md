# <i class="fa-brands fa-simplybuilt"></i> Review Buddy

## Overview

[GitHub Badge](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)(https://github.com/leonardozaggia/review_buddy)

**Review Buddy** is a production-ready toolkit for conducting automated systematic literature reviews. It provides a simple 3-script workflow that handles everything from multi-source searches to intelligent PDF downloads, with powerful abstract-based filtering (keyword or AI-powered) to streamline your screening process.

Perfect for:
- **Systematic reviews** following PRISMA guidelines
- **Meta-analyses** requiring comprehensive paper collection
- **Reproducible research** with documented workflows
- **Large-scale literature reviews** across multiple databases

## Key Features

### 🔍 Multi-Source Search (5 Databases)
- **Scopus**: Comprehensive coverage of peer-reviewed literature
- **PubMed**: Biomedical and life sciences focus with PMC access
- **arXiv**: Pre-prints and cutting-edge research
- **Google Scholar**: Broadest academic coverage
- **IEEE Xplore**: Engineering and computer science

### 🎯 Smart Filtering
- **Keyword-Based Filtering**: Rule-based abstract screening with customizable criteria
- **AI-Powered Filtering** (NEW): Local LLM-based filtering using Ollama
- **Built-in Filters**: Non-English, no abstract, animal studies, reviews, epilepsy, BCI
- **Custom Filters**: Easy to add domain-specific exclusion criteria
- **Manual Review Queue**: Papers flagged for manual verification (AI mode)

### 📥 Intelligent Paper Downloading
- **10+ Download Strategies**: Multiple fallback methods for PDF retrieval
- **Priority Order**: Direct PDF → arXiv → bioRxiv/medRxiv → Unpaywall → PMC → Publisher patterns → Crossref → HTML scraping → Sci-Hub (optional)
- **Open Access Focus**: Unpaywall, arXiv, PubMed Central (US & Europe)
- **Publisher Patterns**: MDPI, Frontiers, Nature, IEEE, ScienceDirect, Springer, PLOS
- **70-90% Success Rate** (depends on source mix and Sci-Hub usage)

### 📚 Export Formats
- **BibTeX**: For LaTeX and reference managers
- **RIS**: For EndNote, Mendeley, Zotero
- **CSV**: For data analysis and spreadsheets

### 🔄 Smart Deduplication
Automatic removal of duplicate papers across sources:
- Title matching with fuzzy logic
- DOI comparison
- **PubMed prioritization** (better download success)
- Source tracking for transparency

## Three-Step Workflow

Review Buddy uses a simple, production-ready workflow:

### 1️⃣ Fetch Metadata
```bash
python 01_fetch_metadata.py
```
Searches 5 databases, deduplicates, exports BibTeX/RIS/CSV.

### 2️⃣ Filter Abstracts (Optional)
```bash
python 02_abstract_filter.py        # Keyword-based
# OR
python 02_abstract_filter_AI.py     # AI-powered (Ollama)
```
Excludes unwanted papers based on abstract content.

### 3️⃣ Download PDFs
```bash
python 03_download_papers.py
```
Tries 10+ strategies to download full-text papers.

## Quick Start Example

**1. Configure your search** (`01_fetch_metadata.py`):
```python
QUERY = "machine learning AND healthcare"
YEAR_FROM = 2020
MAX_RESULTS_PER_SOURCE = 50
```

**2. Set up API keys** (`.env`):
```bash
SCOPUS_API_KEY=your_key_here
PUBMED_EMAIL=your.email@example.com
```

**3. Run the scripts**:
```bash
python 01_fetch_metadata.py     # Search → results/references.bib
python 02_abstract_filter.py    # Filter → results/references_filtered.bib  
python 03_download_papers.py    # Download → results/pdfs/
```

**Results**:
- `results/papers.csv` - All paper metadata
- `results/references.bib` - Bibliography for original search
- `results/references_filtered.bib` - Filtered bibliography (if using step 2)
- `results/pdfs/` - Downloaded papers

## Architecture

```
review_buddy/
├── 01_fetch_metadata.py         # Main search script
├── 02_abstract_filter.py        # Keyword-based filtering
├── 02_abstract_filter_AI.py     # AI-powered filtering (new!)
├── 03_download_papers.py        # PDF downloader
├── .env.example                 # Configuration template
├── query.txt                    # Optional: External query file
├── src/
│   ├── config.py               # Config management
│   ├── models.py               # Paper data model
│   ├── paper_searcher.py       # Search coordinator
│   ├── abstract_filter.py      # Keyword filtering logic
│   ├── ai_abstract_filter.py   # AI filtering logic (new!)
│   ├── llm_client.py           # Ollama client (new!)
│   ├── utils.py                # Helper functions
│   └── searchers/              # Source implementations
│       ├── scopus_searcher.py
│       ├── pubmed_searcher.py
│       ├── arxiv_searcher.py
│       ├── scholar_searcher.py
│       ├── ieee_searcher.py
│       └── paper_downloader.py # Download strategies
├── docs/                        # Comprehensive guides
│   ├── QUERY_SYNTAX.md         # Query building guide
│   ├── FILTER_WORKFLOW_EXAMPLE.md
│   ├── DOWNLOADER_GUIDE.md
│   └── DEDUPLICATION.md
└── results/                     # Output (auto-created)
    ├── papers.csv
    ├── references.bib
    ├── papers_filtered.csv     # After filtering
    ├── references_filtered.bib
    ├── filtered_out/           # Papers removed by each filter
    └── pdfs/
```
## When to Use Review Buddy vs Findpapers

| Feature | Review Buddy | Findpapers |
|---------|---------------|------------|
| **Workflow** | Script-based (3 steps) | Configuration-based (YAML) |
| **Filtering** | Keyword + AI options | Limited post-search filtering |
| **Learning Curve** | Easy (Python scripts) | Easy (YAML config) |
| **Customization** | Highly customizable filters | Limited to config options |
| **Integration** | Easy to integrate in pipelines | Standalone tool |
| **Best For** | Systematic reviews, large projects | Quick searches, one-off reviews |
| **Download Success** | 70-90% (10+ strategies) | 50-70% (fewer strategies) |

## Repository Information

**GitHub**: [https://github.com/leonardozaggia/review_buddy](https://github.com/leonardozaggia/review_buddy)

The Review Buddy codebase is actively maintained and welcomes contributions from the research community.

## Next Steps

Continue to the next sections to learn:
1. **Installation**: Setting up Review Buddy and obtaining API keys
2. **Usage Examples**: Complete workflows and code examples
3. **Advanced Features**: Custom searchers, batch processing, and more
