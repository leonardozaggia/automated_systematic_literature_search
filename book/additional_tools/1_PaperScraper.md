# 📄 PaperScraper

## Overview

**PaperScraper** is a Python library designed for efficiently scraping papers from preprint servers and open-access repositories. Unlike traditional database APIs, PaperScraper directly scrapes the websites of major preprint archives, making it ideal for accessing cutting-edge research before peer review.

**GitHub**: [https://github.com/PhosphorylatedRabbits/paperscraper](https://github.com/PhosphorylatedRabbits/paperscraper)

## Key Features

- 🔬 **Preprint Focus**: arXiv, medRxiv, bioRxiv, chemRxiv
- 🏥 **PubMed Integration**: Search PubMed with full metadata
- 📥 **PDF Downloads**: Automatic full-text retrieval
- 🔍 **Keyword Search**: Flexible query syntax
- 📊 **JSON Export**: Structured data output

## Installation

```bash
pip install paperscraper
```

Or for development:

```bash
git clone https://github.com/PhosphorylatedRabbits/paperscraper
cd paperscraper
pip install -e .
```

## Quick Start

### Basic arXiv Search

```python
from paperscraper.get_dumps import arxiv

# Search arXiv for papers about neural networks
papers = arxiv(
    query='neural networks',
    output_filepath='arxiv_results.jsonl'
)

print(f"Found {len(papers)} papers")

# Access paper metadata
for paper in papers:
    print(f"Title: {paper['title']}")
    print(f"Authors: {', '.join(paper['authors'])}")
    print(f"Abstract: {paper['abstract'][:200]}...")
    print(f"PDF: {paper['pdf_url']}")
    print("---")
```

### bioRxiv/medRxiv Search

```python
from paperscraper.get_dumps import biorxiv, medrxiv

# Search bioRxiv for COVID-19 research
covid_papers = biorxiv(
    query='COVID-19',
    output_filepath='biorxiv_covid.jsonl'
)

# Search medRxiv for vaccine studies
vaccine_papers = medrxiv(
    query='vaccine efficacy',
    output_filepath='medrxiv_vaccines.jsonl'
)
```

### PubMed Search

```python
from paperscraper.pubmed import get_and_dump_pubmed_papers

# Search PubMed for machine learning in healthcare
get_and_dump_pubmed_papers(
    query='machine learning healthcare',
    output_filepath='pubmed_results.jsonl',
    email='your.email@example.com'  # Required by NCBI
)
```

## Advanced Usage

### Date Filtering

```python
from datetime import datetime
from paperscraper.get_dumps import arxiv

# Get papers from 2024 only
recent_papers = arxiv(
    query='deep learning',
    output_filepath='recent_arxiv.jsonl',
    date_from=datetime(2024, 1, 1),
    date_until=datetime(2024, 12, 31)
)
```

### Combining Multiple Sources

```python
from paperscraper.get_dumps import arxiv, biorxiv
import json

# Search multiple sources
arxiv_papers = arxiv(query='protein folding')
biorxiv_papers = biorxiv(query='protein folding')

# Combine and deduplicate
all_papers = {}
for paper in arxiv_papers + biorxiv_papers:
    # Use DOI or title as key for deduplication
    key = paper.get('doi') or paper['title']
    if key not in all_papers:
        all_papers[key] = paper

print(f"Total unique papers: {len(all_papers)}")

# Save combined results
with open('combined_results.json', 'w') as f:
    json.dump(list(all_papers.values()), f, indent=2)
```

### Download PDFs

```python
from paperscraper.pdf import save_pdf
from paperscraper.get_dumps import arxiv

# Search and download PDFs
papers = arxiv(query='transformer models', output_filepath='transformers.jsonl')

for i, paper in enumerate(papers[:10]):  # Download first 10
    pdf_url = paper.get('pdf_url')
    if pdf_url:
        filename = f"paper_{i+1}.pdf"
        try:
            save_pdf(pdf_url, filename)
            print(f"✓ Downloaded: {paper['title'][:50]}...")
        except Exception as e:
            print(f"✗ Failed: {e}")
```

## Common Use Cases

### 1. Tracking Latest Research

```python
from paperscraper.get_dumps import arxiv
from datetime import datetime, timedelta

# Get papers from last 7 days
one_week_ago = datetime.now() - timedelta(days=7)

recent_papers = arxiv(
    query='artificial intelligence',
    date_from=one_week_ago,
    output_filepath='weekly_ai_papers.jsonl'
)

print(f"Found {len(recent_papers)} papers in the last week")
```

### 2. Building a Custom Dataset

```python
from paperscraper.get_dumps import arxiv, biorxiv
import pandas as pd

# Collect papers on a specific topic
ai_health_arxiv = arxiv(query='artificial intelligence healthcare')
ai_health_bio = biorxiv(query='artificial intelligence medical')

# Convert to DataFrame for analysis
data = []
for source, papers in [('arXiv', ai_health_arxiv), ('bioRxiv', ai_health_bio)]:
    for paper in papers:
        data.append({
            'source': source,
            'title': paper['title'],
            'authors': ', '.join(paper['authors']),
            'date': paper['date'],
            'abstract': paper['abstract']
        })

df = pd.DataFrame(data)
df.to_csv('ai_healthcare_dataset.csv', index=False)
print(f"Created dataset with {len(df)} papers")
```

### 3. Citation Analysis

```python
from paperscraper.get_dumps import arxiv
import re

# Get papers and analyze citations
papers = arxiv(query='graph neural networks', output_filepath='gnn_papers.jsonl')

# Extract arXiv IDs from abstracts/references
cited_arxiv_ids = set()
for paper in papers:
    # Find arXiv IDs in abstract (simple pattern)
    matches = re.findall(r'arXiv:(\d+\.\d+)', paper['abstract'])
    cited_arxiv_ids.update(matches)

print(f"Found {len(cited_arxiv_ids)} unique cited arXiv papers")
```

## Tips & Best Practices

### Rate Limiting

```python
import time
from paperscraper.get_dumps import arxiv

# Add delays between requests
queries = ['query1', 'query2', 'query3']
all_papers = []

for query in queries:
    papers = arxiv(query=query, output_filepath=f'{query}.jsonl')
    all_papers.extend(papers)
    time.sleep(3)  # Respectful delay
```

### Error Handling

```python
from paperscraper.get_dumps import arxiv

try:
    papers = arxiv(
        query='machine learning',
        output_filepath='ml_papers.jsonl'
    )
except Exception as e:
    print(f"Search failed: {e}")
    # Fallback or retry logic
```

### Metadata Quality Check

```python
from paperscraper.get_dumps import arxiv

papers = arxiv(query='deep learning')

# Filter for quality
quality_papers = [
    p for p in papers
    if p.get('abstract') and len(p['abstract']) > 100
    and p.get('authors') and len(p['authors']) > 0
]

print(f"High-quality papers: {len(quality_papers)}/{len(papers)}")
```
## Advantages & Limitations

### ✅ Advantages

- **Fast**: Direct scraping is often faster than API calls
- **No API Keys**: Works without authentication for most sources
- **Latest Research**: Access to preprints before peer review
- **Flexible**: Easy to customize and extend
- **Open Access**: Focuses on freely available content

### ⚠️ Limitations

- **Preprint Quality**: Papers are not peer-reviewed
- **Limited Filtering**: Fewer search operators than database APIs
- **Website Changes**: Scraping may break if sites update
- **Rate Limits**: Must be respectful of server loads
- **No Scopus/IEEE**: Doesn't cover major subscription databases

## Integration with Review Buddy

PaperScraper works great alongside Review Buddy:

```python
# Use Review Buddy for peer-reviewed papers
from paper_searcher import PaperSearcher
from config import Config

config = Config(scopus_api_key="key", pubmed_email="email")
searcher = PaperSearcher(config)
peer_reviewed = searcher.search_all(query="machine learning", year_from=2023)

# Use PaperScraper for latest preprints
from paperscraper.get_dumps import arxiv
preprints = arxiv(query='machine learning', date_from=datetime(2024, 1, 1))

print(f"Peer-reviewed: {len(peer_reviewed)}, Preprints: {len(preprints)}")
```

## Additional Resources

- 📖 [Official Documentation](https://github.com/PhosphorylatedRabbits/paperscraper)
- 🐛 [Report Issues](https://github.com/PhosphorylatedRabbits/paperscraper/issues)
- 📝 [Example Notebooks](https://github.com/PhosphorylatedRabbits/paperscraper/tree/main/examples)

---

:::{admonition} Next Tool
:class: tip
Continue to [LitMaps](2_LitMaps) to learn about visual citation mapping!
:::
