# 💡 Usage Examples

## Basic Workflow

Review Buddy follows a simple two-step workflow:

1. **Fetch metadata** - Search databases and collect paper information
2. **Download PDFs** - Automatically retrieve full-text papers

## Step 1: Fetch Paper Metadata

### Simple Example

```python
from src.paper_searcher import PaperSearcher
from src.config import Config

# Create searcher with configuration
searcher = PaperSearcher(Config(max_results_per_source=50))

# Search all available sources
papers = searcher.search_all(
    query="machine learning AND healthcare",
    year_from=2020
)

print(f"Found {len(papers)} unique papers")

# Export results
searcher.generate_bibliography(papers, format="bibtex", output_file="results.bib")
searcher.generate_bibliography(papers, format="ris", output_file="results.ris")
searcher.export_to_csv(papers, output_file="papers.csv")
```

### Query Syntax

**Simple queries:**
```python
query = "machine learning healthcare"
```

**Boolean operators:**
```python
query = "(machine learning OR deep learning) AND diagnosis"
```

**Exact phrases:**
```python
query = '"neural networks" AND medical imaging'
```

**Complex queries:**
```python
query = '("machine learning" OR AI) AND (diagnosis OR prognosis) NOT software'
```

### Year Filtering

```python
# Papers from 2020 onwards
papers = searcher.search_all(query="...", year_from=2020)

# Papers in specific range
papers = searcher.search_all(query="...", year_from=2018, year_to=2023)
```

### Single-Source Searches

```python
# Search only Scopus
scopus_papers = searcher.search_scopus("machine learning", max_results=100)

# Search only PubMed
pubmed_papers = searcher.search_pubmed("cancer treatment", max_results=100)

# Search only arXiv (no API key needed)
arxiv_papers = searcher.search_arxiv("neural networks", max_results=100)
```

## Step 2: Download PDFs

### Using the Script (Recommended)

After fetching metadata, run the download script:

```python
from pathlib import Path
from src.searchers.paper_downloader import PaperDownloader

# Configure downloader
downloader = PaperDownloader(
    output_dir="results/pdfs",
    use_scihub=False,  # Set to True for Sci-Hub fallback
    unpaywall_email="your@email.com"
)

# Download from BibTeX file
downloader.download_from_bib("results/references.bib")
```

### Download Strategies

Review Buddy tries multiple methods automatically:

1. **Direct PDF** - Publisher's direct link
2. **arXiv** - Preprint server (95%+ success)
3. **Unpaywall** - Open access aggregator
4. **PubMed Central** - Free full-text articles
5. **Crossref** - DOI-based full-text links
6. **Publisher patterns** - Known URL structures
7. **HTML scraping** - Extract PDF links from paper pages
8. **Sci-Hub** - Optional fallback (if enabled)

### Monitor Progress

```bash
# Watch download progress in real-time
tail -f results/pdfs/download.log
```

Log shows:
- Which papers downloaded successfully
- Which method was used
- Why downloads failed
- Overall statistics

## Complete Example Script

```python
"""
01_fetch_metadata.py
Complete example of searching and exporting papers
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from src.paper_searcher import PaperSearcher
from src.config import Config

# Load API keys
load_dotenv()

# Configuration
QUERY = "machine learning AND healthcare"
YEAR_FROM = 2020
MAX_RESULTS = 50
OUTPUT_DIR = Path("results")

def main():
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Create searcher
    config = Config(max_results_per_source=MAX_RESULTS)
    searcher = PaperSearcher(config)
    
    # Search all sources
    print(f"Searching: {QUERY}")
    papers = searcher.search_all(query=QUERY, year_from=YEAR_FROM)
    
    print(f"Found {len(papers)} unique papers")
    
    # Count papers by source
    source_counts = {}
    for paper in papers:
        for source in paper.sources:
            source_counts[source] = source_counts.get(source, 0) + 1
    
    print("\nPapers by source:")
    for source, count in sorted(source_counts.items()):
        print(f"  {source}: {count}")
    
    # Export results
    bib_file = OUTPUT_DIR / "references.bib"
    ris_file = OUTPUT_DIR / "references.ris"
    csv_file = OUTPUT_DIR / "papers.csv"
    
    searcher.generate_bibliography(papers, format="bibtex", output_file=str(bib_file))
    searcher.generate_bibliography(papers, format="ris", output_file=str(ris_file))
    searcher.export_to_csv(papers, output_file=str(csv_file))
    
    print(f"\n✓ BibTeX: {bib_file}")
    print(f"✓ RIS: {ris_file}")
    print(f"✓ CSV: {csv_file}")

if __name__ == "__main__":
    main()
```

## Advanced Usage

### Custom Configuration

```python
from src.config import Config

config = Config(
    max_results_per_source=100,
    scopus_api_key="your_key",
    pubmed_email="your@email.com",
    pubmed_api_key="optional_key"
)
```

### Error Handling

```python
try:
    papers = searcher.search_all(query="...", year_from=2020)
except Exception as e:
    print(f"Search failed: {e}")
    # Continue with available results
```

### Batch Processing

```python
queries = [
    "machine learning diagnosis",
    "deep learning medical imaging",
    "neural networks healthcare"
]

all_papers = []
for query in queries:
    papers = searcher.search_all(query=query, year_from=2020)
    all_papers.extend(papers)

# Deduplicate
unique_papers = list({p.title: p for p in all_papers}.values())
```

### Download Monitoring

```python
from pathlib import Path

# Track download progress
pdf_dir = Path("results/pdfs")
downloaded = list(pdf_dir.glob("*.pdf"))
print(f"Downloaded {len(downloaded)} PDFs")

# Read log for details
log_file = pdf_dir / "download.log"
if log_file.exists():
    with open(log_file) as f:
        lines = f.readlines()
        # Parse statistics
        for line in lines:
            if "DOWNLOAD SESSION SUMMARY" in line:
                print("".join(lines[lines.index(line):]))
                break
```

## Output Formats

### BibTeX (.bib)

```bibtex
@article{Smith2020,
    title = {Machine Learning in Healthcare},
    author = {Smith, John and Doe, Jane},
    journal = {Journal of Medical AI},
    year = {2020},
    doi = {10.1234/jmai.2020.001},
    pmid = {12345678},
    arxiv_id = {2001.00001}
}
```

### RIS (.ris)

```
TY  - JOUR
TI  - Machine Learning in Healthcare
AU  - Smith, John
AU  - Doe, Jane
PY  - 2020
DO  - 10.1234/jmai.2020.001
ER  -
```

### CSV (.csv)

| Title | Authors | Year | Journal | DOI | PMID |
|-------|---------|------|---------|-----|------|
| Machine Learning... | Smith, Doe | 2020 | J Med AI | 10.1234... | 12345678 |

## Tips & Best Practices

### Maximize Paper Discovery

- **Use multiple sources** - Each database has different coverage
- **Start broad** - Then filter results programmatically
- **Check year ranges** - Recent papers may not be indexed everywhere

### Optimize Downloads

- **Configure Unpaywall** - Significantly increases success rate
- **Use arXiv** - Always available for preprints
- **Enable PubMed Central** - Free full-text for biomedical papers
- **Monitor logs** - Understand why downloads fail

### Query Construction

✅ **Good:**
```python
"(machine learning OR AI) AND (healthcare OR medical)"
```

❌ **Too narrow:**
```python
'"machine learning for medical diagnosis in pediatric cardiology"'
```

✅ **Boolean logic:**
```python
"(deep learning OR neural networks) AND diagnosis NOT software"
```

### Expected Success Rates

- **Metadata collection**: ~95% (depends on API availability)
- **PDF downloads**: 
  - Open access papers: 95%+
  - ArXiv preprints: 98%+
  - PubMed papers: 60%+
  - Overall: 65-75%

## Next Steps

- Check [Additional Tools](../additional_tools/0_Overview) for complementary resources
- Explore [LitMaps](../additional_tools/2_LitMaps) for citation network discovery
- Use [Consensus](../additional_tools/3_Consensus) for quick background research
