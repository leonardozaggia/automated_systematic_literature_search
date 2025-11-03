# <i class="fa-solid fa-wrench"></i> Installation & Setup

## Prerequisites

- **Python 3.7+** (Python 3.8+ recommended)
- **pip** (Python package manager)
- **Git** (optional - to clone from GitHub)
- **Ollama** (optional - for AI-powered filtering)

## Installation Steps

### 1. Get Review Buddy

**Option A: Clone from GitHub (recommended)**
```bash
git clone https://github.com/leonardozaggia/review_buddy.git
cd review_buddy
```

**Option B: Download ZIP**
- Download from GitHub and extract
- Navigate to the folder in terminal

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Core dependencies (always installed):**
- `requests>=2.31.0` - HTTP requests
- `lxml>=4.9.0` - HTML/XML parsing
- `python-dotenv>=1.0.0` - Environment variable management
- `beautifulsoup4>=4.12.0` - HTML parsing
- `tqdm>=4.66.0` - Progress bars
- `bibtexparser>=1.4.0` - BibTeX file handling
- `rispy>=0.7.0` - RIS file handling

**Optional dependencies:**
- `scholarly>=1.7.0` - Google Scholar (install if using Scholar search)
- `langdetect>=1.0.9` - Language detection (for abstract filtering)
- `scihub` - Sci-Hub access (install if using Sci-Hub downloads)

### 3. Configure API Keys

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your credentials (**at least one API key required**):

```bash
# Scopus (Recommended - best coverage)
SCOPUS_API_KEY=your_scopus_api_key_here

# PubMed (Required for biomedical papers and better downloads)
PUBMED_EMAIL=your.email@example.com
PUBMED_API_KEY=optional_key_for_higher_rate_limits

# Unpaywall (Highly recommended - improves download success)
UNPAYWALL_EMAIL=your.email@example.com

# IEEE Xplore (Optional - for engineering papers)
IEEE_API_KEY=your_ieee_api_key_here

# Ollama (Optional - for AI filtering)
OLLAMA_MODEL=llama3.1:8b
```

**Minimum setup**: Either `SCOPUS_API_KEY` OR `PUBMED_EMAIL` (both recommended)  
**For best results**: Configure all available sources

### 4. Obtain API Keys

#### Scopus (Highly Recommended)
- **Website**: [https://dev.elsevier.com/](https://dev.elsevier.com/)
- **How**: Create account → Request API key
- **Free tier**: 5,000 requests/week
- **Coverage**: Best for peer-reviewed publications

#### PubMed (Free, Highly Recommended)
- **Website**: [https://www.ncbi.nlm.nih.gov/account/](https://www.ncbi.nlm.nih.gov/account/)
- **Email**: Any valid email (no registration needed)
- **API Key** (optional): Register for key to increase rate limits (3→10 req/sec)
- **Coverage**: Best for biomedical/life sciences

#### Unpaywall (Free, Recommended)
- **Email**: Any valid email (no registration)
- **Benefit**: Significantly improves open access paper discovery
- **Use**: Add your email to `.env` as `UNPAYWALL_EMAIL`

#### IEEE Xplore (Optional)
- **Website**: [https://developer.ieee.org/](https://developer.ieee.org/)
- **How**: Register → Request API key
- **Free tier**: 200 queries/day
- **Coverage**: Engineering and computer science

#### Ollama (Optional - for AI Filtering)
- **Website**: [https://ollama.ai/](https://ollama.ai/)
- **How**: Download and install Ollama → Pull model: `ollama pull llama3.1:8b`
- **Models**: llama3.1:8b (recommended), mistral, etc.
- **Use**: Local LLM for intelligent abstract filtering

## Verify Installation

### Quick Verification

The easiest way to verify is to run the fetch script:

```bash
python 01_fetch_metadata.py
```

You should see:
```
================================================================================
REVIEW BUDDY - FETCH PAPER METADATA
================================================================================

✓ Available sources: Scopus, PubMed, arXiv, Google Scholar, IEEE Xplore
```

If you see `❌ ERROR: No API keys configured!`, check your `.env` file.

### Manual Test (Optional)

Create a test script to check configuration:

```python
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Config

config = Config()

print("Available sources:")
if config.has_scopus_access():
    print("  ✓ Scopus configured")
if config.has_pubmed_access():
    print("  ✓ PubMed configured")
if config.has_arxiv_access():
    print("  ✓ arXiv available (no key needed)")
if config.has_scholar_access():
    print("  ✓ Google Scholar available")
if config.has_ieee_access():
    print("  ✓ IEEE Xplore configured")
```

### Test Search (Optional)

Run a small test search:

```bash
# Edit 01_fetch_metadata.py to set:
# QUERY = "machine learning"
# MAX_RESULTS_PER_SOURCE = 5

python 01_fetch_metadata.py
```

Check that `results/references.bib` is created with papers.

## Troubleshooting

### No API Keys Configured
**Error**: `❌ ERROR: No API keys configured!`

**Solution**: 
1. Check that `.env` file exists in project root
2. Add at least one API key (Scopus or PubMed email)
3. Restart your terminal/IDE

### Import Errors
**Error**: `ModuleNotFoundError: No module named 'src'`

**Solution**:
```bash
# Run scripts from project root (where src/ folder is)
cd /path/to/review_buddy
python 01_fetch_metadata.py
```

### API Key Not Working
**Error**: `Invalid API key` or `Authentication failed`

**Solution**:
```bash
# Verify .env file is in project root
ls .env

# Check environment variables load correctly
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Scopus:', os.getenv('SCOPUS_API_KEY')[:10] if os.getenv('SCOPUS_API_KEY') else 'Not set')"
```

### Rate Limit Errors
**Error**: `Rate limit exceeded`

**Solution**:
- **PubMed**: Get API key to increase from 3→10 req/sec
- **Scopus**: Check weekly quota at [dev.elsevier.com](https://dev.elsevier.com)
- **Wait**: Rate limits reset after a few minutes

### No Papers Found
**Error**: Search completes but finds 0 papers

**Solution**:
1. Try a simpler query: `"machine learning"`
2. Check year range (some databases lag by 1-2 years)
3. Verify API keys are valid
4. Try a different source

### Language Detection Issues
**Error**: `langdetect not installed`

**Solution**:
```bash
pip install langdetect
```

Or disable language filtering in `02_abstract_filter.py`:
```python
FILTERS_ENABLED = {
    'non_english': False,  # Disable
    # ... other filters
}
```

### Ollama Not Working (AI Filtering)
**Error**: `Failed to initialize Ollama client`

**Solution**:
1. Install Ollama: [https://ollama.ai](https://ollama.ai)
2. Pull model: `ollama pull llama3.1:8b`
3. Check Ollama is running: `ollama list`
4. Verify URL in `.env`: `OLLAMA_URL=http://localhost:11434`

## What's Next?

Proceed to [Usage Examples](2_Usage_Examples) to learn how to:
- Configure and run searches across multiple databases
- Filter papers by abstract content (keyword or AI)
- Download PDFs with intelligent fallback strategies
- Export results in multiple formats
