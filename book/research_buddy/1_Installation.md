# 🔧 Installation & Setup

## Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- **Git** (to clone the repository)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/leonardozaggia/review_buddy.git
cd review_buddy
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- `requests` - HTTP requests
- `lxml` - HTML/XML parsing
- `python-dotenv` - Environment variable management
- `scholarly` - Google Scholar access

### 3. Configure API Keys

Copy the example configuration file:

```bash
cp .env.example .env
```

Edit `.env` with your API keys (at least one required):

```bash
# Required for Scopus searches
SCOPUS_API_KEY=your_scopus_api_key_here

# Required for PubMed and paper downloads
PUBMED_EMAIL=your.email@example.com

# Optional: Increases PubMed rate limits
PUBMED_API_KEY=your_pubmed_api_key_here

# Optional: For IEEE searches
IEEE_API_KEY=your_ieee_api_key_here

# Optional: For Unpaywall open access downloads
UNPAYWALL_EMAIL=your.email@example.com
```

### 4. Obtain API Keys

**Scopus (Recommended):**
- Visit: [https://dev.elsevier.com/](https://dev.elsevier.com/)
- Create account → Request API key
- Free tier: 5,000 requests/week

**PubMed (Free):**
- Email address required (any valid email)
- Optional API key: [https://www.ncbi.nlm.nih.gov/account/](https://www.ncbi.nlm.nih.gov/account/)
- Increases rate limits from 3 to 10 requests/second

**IEEE Xplore (Optional):**
- Visit: [https://developer.ieee.org/](https://developer.ieee.org/)
- Register → Request API key
- Free tier: 200 queries/day

## Verify Installation

Test that everything is configured correctly:

```python
from src.config import Config

config = Config()

# Check which sources are available
if config.has_scopus_access():
    print("✓ Scopus configured")
if config.has_pubmed_access():
    print("✓ PubMed configured")
if config.has_arxiv_access():
    print("✓ arXiv available (no key needed)")
if config.has_scholar_access():
    print("✓ Google Scholar available")
if config.has_ieee_access():
    print("✓ IEEE Xplore configured")
```

## Quick Test

Run a simple search to verify everything works:

```python
from src.paper_searcher import PaperSearcher
from src.config import Config

searcher = PaperSearcher(Config(max_results_per_source=5))
papers = searcher.search_all(query="machine learning", year_from=2023)

print(f"Found {len(papers)} papers")
```

## Troubleshooting

### Import Errors
```bash
# Ensure you're in the review_buddy directory
cd review_buddy

# Verify __init__.py files exist
ls src/__init__.py
ls src/searchers/__init__.py
```

### API Key Not Working
```bash
# Check .env file is in the correct location
ls .env

# Verify environment variables are loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('SCOPUS_API_KEY'))"
```

### Rate Limit Errors
- Wait a few minutes before retrying
- PubMed: Get API key to increase limits
- Scopus: Check weekly quota at dev.elsevier.com

## What's Next?

Proceed to [Usage Examples](2_Usage_Examples) to learn how to:
- Search for papers across multiple databases
- Download PDFs automatically
- Export results in multiple formats
