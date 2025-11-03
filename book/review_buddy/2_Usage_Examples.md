# <i class="fa-solid fa-lightbulb"></i> Usage Examples

## The Three-Step Workflow

Review Buddy provides a simple, production-ready workflow for systematic literature reviews:

1. **📚 Fetch Metadata** → Search databases and collect paper information
2. **🎯 Filter Abstracts** → Exclude unwanted papers (optional but recommended)
3. **📥 Download PDFs** → Automatically retrieve full-text papers

---

## Step 1: Fetch Paper Metadata

### Configure Your Search

Edit `01_fetch_metadata.py` to customize your search:

```python
# ============= CONFIGURATION =============

# Option 1: Inline query (simple)
QUERY = "machine learning AND healthcare"

# Option 2: From text file (recommended for complex queries)
QUERY = Path("query.txt").read_text(encoding="utf-8").strip()

YEAR_FROM = 2020                 # Starting year
MAX_RESULTS_PER_SOURCE = 50      # Per database (use 999999 for unlimited)
OUTPUT_DIR = Path("results")
```

### Create query.txt (Recommended)

For complex queries, create a `query.txt` file with multi-line formatting:

```
(
  "machine learning" OR "deep learning" OR "artificial intelligence"
)
AND
(
  healthcare OR medical OR clinical
)
NOT
(
  review OR "systematic review"
)
```

See [docs/QUERY_SYNTAX.md](https://github.com/leonardozaggia/review_buddy/blob/main/docs/QUERY_SYNTAX.md) for more examples.

### Run the Search

```bash
python 01_fetch_metadata.py
```

**Output**:
```
================================================================================
REVIEW BUDDY - FETCH PAPER METADATA
================================================================================

✓ Available sources: Scopus, PubMed, arXiv, Google Scholar, IEEE Xplore

Search query: machine learning AND healthcare
Year from: 2020
Max results per source: 50

================================================================================
SEARCHING...
================================================================================
Searching Scopus...
Found 45 papers from Scopus
Searching PubMed...
Found 38 papers from PubMed
Searching arXiv...
Found 22 papers from arXiv
Searching Google Scholar...
Found 50 papers from Google Scholar
Searching IEEE Xplore...
Found 31 papers from IEEE Xplore

================================================================================
FOUND 142 UNIQUE PAPERS
================================================================================

Papers by source:
  Scopus: 45
  PubMed: 38
  arXiv: 22
  Google Scholar: 50
  IEEE: 31

================================================================================
GENERATING OUTPUT FILES...
================================================================================
✓ BibTeX: results/references.bib
✓ RIS: results/references.ris
✓ CSV: results/papers.csv

Next step: Run 02_abstract_filter.py to filter papers by abstract
Or skip filtering and run 03_download_papers.py to download PDFs
```

### Query Syntax Quick Reference

| Syntax | Example | Meaning |
|--------|---------|---------|
| `AND` | `AI AND healthcare` | Both terms required |
| `OR` | `"ML" OR "machine learning"` | Either term |
| `NOT` | `AI NOT review` | Exclude term |
| `" "` | `"deep learning"` | Exact phrase |
| `( )` | `(AI OR ML) AND healthcare` | Grouping |

**More examples**: See [docs/QUERY_SYNTAX.md](https://github.com/leonardozaggia/review_buddy/blob/main/docs/QUERY_SYNTAX.md)

---

## Step 2: Filter Abstracts (Optional)

### Option A: Keyword-Based Filtering

Edit `02_abstract_filter.py` to configure your filters:

```python
# ============================================================================
# CONFIGURATION - CUSTOMIZE YOUR FILTERS HERE
# ============================================================================

# Enable/disable filters
FILTERS_ENABLED = {
    'no_abstract': True,        # Remove papers without abstracts
    'non_english': True,        # Remove non-English papers
    'epilepsy': True,          # Remove epilepsy papers (example)
    'bci': True,               # Remove BCI papers (example)
    'non_human': True,         # Remove animal studies
    'non_empirical': True,     # Remove review papers
}

# Define keyword filters
KEYWORD_FILTERS = {
    'epilepsy': [
        'epileptic spike', 'epileptic spikes', 'seizure spike',
        'epileptiform', 'interictal spike'
    ],
    
    'bci': [
        'brain-computer interface', 'brain computer interface',
        'brain-machine interface', 'bci', 'bmi'
    ],
    
    'non_human': [
        'rat', 'rats', 'mouse', 'mice', 'murine', 'rodent',
        'monkey', 'primate', 'in vitro', 'animal model'
    ],
    
    'non_empirical': [
        'systematic review', 'meta-analysis', 'literature review',
        'scoping review', 'review article'
    ],
    
    # Add your own custom filters:
    # 'custom_filter_name': [
    #     'keyword1', 'keyword2', 'keyword3'
    # ],
}
```

Run the filter:
```bash
python 02_abstract_filter.py
```

**Output**:
```
======================================================================
ABSTRACT-BASED PAPER FILTERING
======================================================================

Loaded 142 papers

Filters to apply: no_abstract, non_english, epilepsy, bci, non_human, non_empirical

======================================================================
FILTERING SUMMARY
======================================================================
Initial papers:        142
Papers kept:           89
Papers filtered out:   53
Retention rate:        62.7%

Breakdown by filter:
  - no_abstract       :    8 papers
  - non_english       :    3 papers
  - epilepsy          :   12 papers
  - bci               :    7 papers
  - non_human         :   18 papers
  - non_empirical     :    5 papers

✓ Filtered results: results/references_filtered.bib
✓ Filtered papers: results/papers_filtered.csv
✓ Filtered out papers: results/filtered_out/

Next step: Run 03_download_papers.py to download PDFs
```

### Option B: AI-Powered Filtering (New!)

For more intelligent filtering, use the AI-powered option with Ollama:

**Prerequisites**:
1. Install Ollama: [https://ollama.ai](https://ollama.ai)
2. Pull a model: `ollama pull llama3.1:8b`
3. Configure in `.env`: `OLLAMA_MODEL=llama3.1:8b`

Edit `02_abstract_filter_AI.py`:

```python
# ============================================================================
# CONFIGURATION - CUSTOMIZE YOUR FILTERS HERE
# ============================================================================

# AI Model Configuration
AI_CONFIG = {
    'model': 'llama3.1:8b',
    'temperature': 0.1,
    'confidence_threshold': 0.5,  # Min confidence to filter (0.0-1.0)
}

# Filter Definitions (use natural language!)
FILTERS_CONFIG = {
    'epilepsy': {
        'enabled': True,
        'prompt': "Does this paper focus primarily on epileptic spikes or seizure detection?",
        'description': "Papers about epilepsy-related spike detection"
    },
    
    'bci': {
        'enabled': True,
        'prompt': "Is this paper about brain-computer interfaces (BCI) or brain-machine interfaces (BMI)?",
        'description': "Papers about BCI/BMI systems"
    },
    
    'non_human': {
        'enabled': True,
        'prompt': "Is this paper based on animal studies, in-vitro experiments, or computational models only (not human subjects)?",
        'description': "Non-human or in-vitro studies"
    },
    
    # Add your own filters with natural language prompts!
}
```

Run the AI filter:
```bash
python 02_abstract_filter_AI.py
```

**Output**:
```
======================================================================
AI-POWERED ABSTRACT FILTERING (LOCAL OLLAMA)
======================================================================

Model: llama3.1:8b
Confidence threshold: 0.5

======================================================================
AI FILTERING SUMMARY
======================================================================
Initial papers:        142
Papers kept:           94
Papers filtered out:   43
Manual review needed:  5
Retention rate:        66.2%

Ollama Usage:
  - Model calls made:    142
  - Cache hits:          0
  - Cache hit rate:      0.0%
  - Model used:          llama3.1:8b

✓ Filtered results: results/references_filtered_ai.bib
✓ Manual review: results/manual_review_ai.csv
✓ Decision log: results/ai_filtering_log_*.json
```

**Comparing Strategies**: See [docs/FILTER_WORKFLOW_EXAMPLE.md](https://github.com/leonardozaggia/review_buddy/blob/main/docs/FILTER_WORKFLOW_EXAMPLE.md) for a complete example.

---

## Step 3: Download PDFs

The downloader automatically uses filtered results if available:
- `results/references_filtered.bib` (if you ran step 2)
- `results/references.bib` (if you skipped filtering)

### Run the Downloader

```bash
python 03_download_papers.py
```

**Optional: Enable Sci-Hub** (use responsibly per your local laws):

Edit `03_download_papers.py`:
```python
USE_SCIHUB = True  # Enable Sci-Hub as fallback
```

**Output**:
```
================================================================================
REVIEW BUDDY - DOWNLOAD PAPERS
================================================================================

Input file: results/references_filtered.bib
Output directory: results/pdfs
Sci-Hub enabled: False

================================================================================
STARTING DOWNLOAD...
================================================================================

Downloading PDFs: 100%|██████████████████████| 89/89 [05:23<00:00, 3.63s/paper]

================================================================================
DOWNLOAD COMPLETE!
================================================================================
Downloaded: 67 PDFs
Location: results/pdfs
Log file: results/pdfs/download.log

Success rate: 75.3%
```

### Download Strategies

The downloader tries **10+ methods automatically**:

1. **Direct PDF link** - Publisher's direct URL
2. **arXiv** - Preprint server (95%+ success)
3. **bioRxiv/medRxiv** - Biology/medicine preprints
4. **Unpaywall API** - Open access aggregator
5. **Crossref** - DOI-based full-text links
6. **PubMed Central (US)** - Free full-text articles
7. **PubMed Central (Europe)** - European mirror
8. **Publisher patterns** - MDPI, Frontiers, Nature, IEEE, ScienceDirect, Springer, PLOS
9. **ResearchGate/Academia** - Academic social networks
10. **HTML scraping** - Extract PDF links from paper pages
11. **Sci-Hub** - Optional fallback (if enabled)

**Expected Success Rates**:
- arXiv papers: **95%+**
- bioRxiv/medRxiv: **95%+**
- Open access publishers: **80-90%**
- Overall (without Sci-Hub): **50-70%**
- Overall (with Sci-Hub): **70-90%**

For details: [docs/DOWNLOADER_GUIDE.md](https://github.com/leonardozaggia/review_buddy/blob/main/docs/DOWNLOADER_GUIDE.md)

---

## Complete Workflow Example

### Scenario: Systematic Review on "EEG and Cognitive Assessment"

**Goal**: Find papers on EEG-based cognitive assessment, excluding animal studies, reviews, and BCI research.

#### 1. Configure Search

Create `query.txt`:
```
(
  EEG OR "event-related potential" OR electroencephalography
)
AND
(
  "cognitive assessment" OR "cognitive function" OR "cognitive performance"
)
```

Edit `01_fetch_metadata.py`:
```python
QUERY = Path("query.txt").read_text(encoding="utf-8").strip()
YEAR_FROM = 2018
MAX_RESULTS_PER_SOURCE = 100
```

#### 2. Run Search

```bash
python 01_fetch_metadata.py
```

**Result**: 287 papers from 5 sources → `results/references.bib`

#### 3. Configure Filtering

Edit `02_abstract_filter.py`:
```python
FILTERS_ENABLED = {
    'no_abstract': True,
    'non_english': True,
    'bci': True,            # Exclude BCI papers
    'non_human': True,      # Exclude animal studies
    'non_empirical': True,  # Exclude reviews
}

KEYWORD_FILTERS = {
    'bci': [
        'brain-computer interface', 'brain computer interface',
        'brain-machine interface', 'bci', 'bmi', 'neural interface'
    ],
    'non_human': [
        'rat', 'rats', 'mouse', 'mice', 'rodent', 'primate',
        'animal model', 'in vitro', 'in-vitro'
    ],
    'non_empirical': [
        'systematic review', 'meta-analysis', 'literature review',
        'review article', 'scoping review'
    ],
}
```

#### 4. Run Filtering

```bash
python 02_abstract_filter.py
```

**Result**: 287 → 156 papers → `results/references_filtered.bib`

**Breakdown**:
- No abstract: 12 papers
- Non-English: 8 papers
- BCI: 34 papers
- Non-human: 61 papers
- Non-empirical: 16 papers

#### 5. Review Filtered Papers (Optional)

Check what was removed:
```bash
# View BCI papers that were filtered
head results/filtered_out/bci.csv

# View animal studies that were removed
head results/filtered_out/non_human.csv
```

If you find false positives, refine your keywords and re-run step 4.

#### 6. Download PDFs

```bash
python 03_download_papers.py
```

**Result**: 156 papers → 117 PDFs (75% success) → `results/pdfs/`

#### 7. Final Output

```
results/
├── papers.csv                      # Original 287 papers
├── references.bib                  # Original bibliography
├── papers_filtered.csv             # ✅ 156 filtered papers
├── references_filtered.bib         # ✅ Bibliography for 156 papers
├── filtered_out/                   # Papers removed by each filter
│   ├── no_abstract.csv
│   ├── non_english.csv
│   ├── bci.csv
│   ├── non_human.csv
│   └── non_empirical.csv
└── pdfs/                           # ✅ 117 downloaded PDFs
    ├── paper1.pdf
    ├── paper2.pdf
    ├── ...
    └── download.log
```

---

## Advanced Techniques

### Custom Filter Examples

#### Exclude Pediatric Studies

```python
FILTERS_ENABLED = {
    'pediatric': True,
    # ... other filters
}

KEYWORD_FILTERS = {
    'pediatric': [
        'children', 'child', 'pediatric', 'paediatric',
        'infant', 'toddler', 'adolescent', 'school-age'
    ],
    # ... other filters
}
```

#### Exclude fMRI-Only Studies

```python
KEYWORD_FILTERS = {
    'fmri_only': [
        'fMRI only', 'exclusively fMRI', 'solely fMRI',
        # Be careful with broad terms like 'fMRI' alone
        # as they'll catch combined EEG+fMRI studies
    ],
}
```

#### Keep Only Clinical Trials

```python
KEYWORD_FILTERS = {
    # Use negative filters to exclude everything except trials
    'non_clinical': [
        'simulation', 'computational model', 'theoretical',
        'case report', 'review', 'survey'
    ],
}
```

### Batch Processing Multiple Queries

Create a script to process multiple related queries:

```python
queries = [
    "EEG AND attention",
    "EEG AND memory",
    "EEG AND executive function"
]

for i, query in enumerate(queries):
    print(f"\n{'='*60}")
    print(f"Processing query {i+1}: {query}")
    print('='*60)
    
    # Edit query in script
    with open("01_fetch_metadata.py", "r") as f:
        content = f.read()
    
    # Simple replacement (or use more robust method)
    content = content.replace(
        'QUERY = "..."',
        f'QUERY = "{query}"'
    )
    
    # Run search
    # ... (call script or import and run)
```

### Monitoring Download Progress

```python
from pathlib import Path
import time

pdf_dir = Path("results/pdfs")

# Watch downloads in real-time
while True:
    pdfs = list(pdf_dir.glob("*.pdf"))
    print(f"\rDownloaded: {len(pdfs)} PDFs", end="")
    time.sleep(2)
```

### Parsing Download Logs

```python
from pathlib import Path

log_file = Path("results/pdfs/download.log")

if log_file.exists():
    with open(log_file) as f:
        log = f.read()
    
    # Extract statistics
    if "SUCCESS:" in log:
        success_lines = [l for l in log.split('\n') if "SUCCESS:" in l]
        print(f"Successfully downloaded: {len(success_lines)}")
    
    if "FAILED:" in log:
        failed_lines = [l for l in log.split('\n') if "FAILED:" in l]
        print(f"Failed downloads: {len(failed_lines)}")
```

---

## Output Formats

### BibTeX (.bib)

Standard format for LaTeX and most reference managers:

```bibtex
@article{Smith2020,
    title = {Machine Learning in Healthcare},
    author = {Smith, John and Doe, Jane},
    journal = {Journal of Medical AI},
    year = {2020},
    volume = {15},
    number = {3},
    pages = {123-145},
    doi = {10.1234/jmai.2020.001},
    pmid = {12345678},
    url = {https://example.com/paper}
}
```

### RIS (.ris)

Format for EndNote, Mendeley, Zotero:

```
TY  - JOUR
TI  - Machine Learning in Healthcare
AU  - Smith, John
AU  - Doe, Jane
JO  - Journal of Medical AI
PY  - 2020
VL  - 15
IS  - 3
SP  - 123-145
DO  - 10.1234/jmai.2020.001
UR  - https://example.com/paper
AB  - This paper presents a novel approach to...
ER  -
```

### CSV (.csv)

For data analysis and spreadsheets:

| Title | Authors | Year | Journal | DOI | PMID | Citations | Sources |
|-------|---------|------|---------|-----|------|-----------|---------|
| Machine Learning... | Smith; Doe | 2020 | J Med AI | 10.1234... | 12345678 | 45 | Scopus, PubMed |

---

## Tips & Best Practices

### Maximize Paper Discovery

✅ **Use multiple sources** - Each database has different coverage  
✅ **Start with broad queries** - Filter afterwards programmatically  
✅ **Check year ranges** - Recent papers may not be indexed everywhere  
✅ **Use query.txt** - Better for complex, multi-line queries  
✅ **Save intermediate results** - Keep original and filtered versions

### Optimize Filtering

✅ **Start conservative** - Use specific keywords first  
✅ **Review filtered-out papers** - Check for false positives  
✅ **Iterate** - Refine filters based on review  
✅ **Use word boundaries** - Prevents substring matches  
✅ **Test AI filtering** - Compare with keyword approach

### Improve Download Success

✅ **Configure Unpaywall email** - Significantly increases success rate  
✅ **Enable PubMed sources** - Better access to biomedical papers  
✅ **Check institutional access** - May have more access than open sources  
✅ **Monitor logs** - Understand why specific downloads fail  
✅ **Consider Sci-Hub** - Only if legal in your jurisdiction

### Query Construction

✅ **Good:**
```python
"(machine learning OR deep learning) AND (healthcare OR medical)"
```

❌ **Too narrow:**
```python
'"machine learning for medical diagnosis in pediatric cardiology"'
```

✅ **Boolean logic:**
```python
"(EEG OR MEG OR iEEG) AND cognition NOT animal"
```

❌ **Too complex for some sources:**
```python
'(((A OR B) AND (C OR D)) NOT (E OR F)) AND ((G AND H) OR I)'
```

### Expected Success Rates

**Metadata Collection**: ~95% (depends on API availability)

**PDF Downloads**:
- Open access papers: **95%+**
- arXiv preprints: **98%+**
- bioRxiv/medRxiv: **95%+**
- PubMed papers: **60-70%**
- IEEE papers: **50-60%**
- Overall (no Sci-Hub): **50-70%**
- Overall (with Sci-Hub): **70-90%**

---

## Troubleshooting Common Issues

### No Papers Found

**Problem**: Search returns 0 papers

**Solutions**:
1. Simplify query: `"machine learning"` instead of complex boolean
2. Check year range (some databases lag 1-2 years)
3. Verify API keys are working
4. Try single source: Look for errors in specific searchers

### Filtering Too Aggressive

**Problem**: Too many papers filtered out

**Solutions**:
1. Review `filtered_out/*.csv` files
2. Make keywords more specific
3. Disable aggressive filters temporarily
4. Use AI filtering for nuanced decisions

### Low Download Success Rate

**Problem**: < 50% PDFs downloaded

**Solutions**:
1. Add `UNPAYWALL_EMAIL` to `.env`
2. Check you have PubMed-heavy sources (better access)
3. Enable Sci-Hub if appropriate
4. Check institutional VPN/access
5. Review `download.log` for specific failure reasons

### Import/Path Errors

**Problem**: `ModuleNotFoundError` or import errors

**Solutions**:
1. Run from project root: `cd /path/to/review_buddy`
2. Check `src/__init__.py` exists
3. Don't rename project folders
4. Use: `python 01_fetch_metadata.py` (not `python3`, not from subdirs)

---

## Next Steps

- Review [docs/QUERY_SYNTAX.md](https://github.com/leonardozaggia/review_buddy/blob/main/docs/QUERY_SYNTAX.md) for advanced query patterns
- Check [docs/FILTER_WORKFLOW_EXAMPLE.md](https://github.com/leonardozaggia/review_buddy/blob/main/docs/FILTER_WORKFLOW_EXAMPLE.md) for complete filtering example
- See [docs/DOWNLOADER_GUIDE.md](https://github.com/leonardozaggia/review_buddy/blob/main/docs/DOWNLOADER_GUIDE.md) for download troubleshooting
- Explore [Additional Tools](../additional_tools/0_Overview) for complementary resources
- Use [LitMaps](../additional_tools/2_LitMaps) for citation network discovery
