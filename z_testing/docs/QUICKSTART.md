# Paper Searcher - Quick Start Guide

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API keys (at least one required):**
   
   **Scopus** (recommended for comprehensive results):
   - Get API key from: https://dev.elsevier.com/
   - Set environment variable: `SCOPUS_API_KEY=your_key`
   
   **PubMed** (free, no key needed):
   - Set environment variable: `PUBMED_EMAIL=your@email.com`
   - Optional: Get API key from https://www.ncbi.nlm.nih.gov/account/ for higher rate limits
   - Set: `PUBMED_API_KEY=your_key` (optional)

## Testing

Run tests to verify everything works:

```bash
# Test Scopus only
python test_scopus.py

# Test PubMed only
python test_pubmed.py

# Test everything together
python test_all.py
```

## Basic Usage

```python
from paper_searcher import PaperSearcher
from config import Config

# Create searcher
config = Config(max_results_per_source=100)
searcher = PaperSearcher(config)

# Search
papers = searcher.search_all(
    query="machine learning AND healthcare",
    year_from=2020
)

# Generate bibliography
searcher.generate_bibliography(papers, format="bibtex", output_file="refs.bib")
searcher.export_to_csv(papers, output_file="papers.csv")
```

## Query Syntax

The query syntax works across all sources:

- **AND**: `machine learning AND healthcare`
- **OR**: `machine learning OR deep learning`
- **Quotes**: `"neural networks"` (exact phrase)
- **Parentheses**: `(machine learning OR AI) AND healthcare`

## Output Formats

1. **BibTeX** (.bib) - For LaTeX/reference managers
2. **RIS** (.ris) - For Zotero, Mendeley, EndNote
3. **CSV** (.csv) - For Excel/spreadsheet analysis

## What Makes This Better Than findpapers?

1. **Simpler** - No complex configuration, just works
2. **More reliable** - Better error handling, continues on failures
3. **Cleaner code** - Easy to understand and modify
4. **Better deduplication** - Merges data from multiple sources
5. **More formats** - BibTeX, RIS, CSV export
6. **No refinement overhead** - Just find and download, that's it

## Next Steps

Once this is tested and working:
1. Add Google Scholar support (using `scholarly` library)
2. Add paper downloading capabilities
3. Add arXiv support
4. Integrate into the main Jupyter Book
