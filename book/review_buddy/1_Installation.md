# <i class="fa-solid fa-wrench"></i> Installation & Setup

## Prerequisites

| Requirement | Needed for | Notes |
|---|---|---|
| **Python 3.10 or 3.11** | Everything | Python 3.9 is the hard minimum (the code uses built-in generic type hints). The `autosearch` environment from the [Setup Guide](../introduction/1_Setup) is exactly right. |
| **pip** | Installing dependencies | Ships with Python / conda |
| **Git** | Cloning the repository | Optional - you can download the ZIP instead |
| **Ollama** | The AI (LLM) abstract filter | Optional - only for `python main.py --ai` |
| **Node.js** | The Zotero translation server | Optional - improves the PDF hit rate |

:::{admonition} Which version of Review Buddy does this book describe?
:class: note
This book documents the **config-driven version** of Review Buddy: one `config.yaml` file for every run setting and a `main.py` command that runs the whole pipeline. If your copy of `01_fetch_metadata.py` still contains a `# ===== CONFIGURATION =====` block with `QUERY = ...`, you have an older version - run `git pull` to update.
:::

## Installation Steps

### 1. Get Review Buddy

**Option A: Clone from GitHub (recommended)**
```bash
git clone https://github.com/leonardozaggia/review_buddy.git
cd review_buddy
```

**Option B: Download ZIP**
- Download from GitHub and extract
- Navigate to the folder in a terminal

:::{note}
The optional Zotero translation server lives in a git submodule (`vendor/translation-server`), which a normal clone leaves empty. You don't need to do anything now: `scripts/setup_zotero.py` (see [step 5](#rb-zotero)) initialises it, and `main.py` offers to run it for you.
:::

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt` installs everything in one go. The packages worth knowing about:

| Package | What it does for you |
|---|---|
| `requests`, `lxml`, `beautifulsoup4`, `tqdm`, `python-dotenv`, `pandas`, `PyYAML` | Core: HTTP, parsing, progress bars, reading `.env` and `config.yaml` |
| `bibtexparser`, `rispy` | Reading and writing BibTeX / RIS |
| `curl_cffi` | Browser-like TLS fingerprint. **Strongly recommended**: many publishers - including open-access ones such as MDPI, PLOS and PMC - answer a plain Python client with HTTP 403 |
| `langdetect` | The `non_english` keyword filter |
| `scholarly` | Google Scholar search (unreliable - see [Usage Examples](2_Usage_Examples)) |
| `camoufox[geoip]`, `playwright` | The optional real-browser PDF fetcher |
| `pymupdf` | Full-text extraction in the `scripts/` utilities |
| `matplotlib`, `pytest`, `scihub` | Benchmark charts, the test suite, the (off by default) Sci-Hub fallback |

(rb-env)=
### 3. Configure API Keys (`.env`)

API keys and emails live in a `.env` file in the project root - never in `config.yaml`, and never in git (`.env` is already in Review Buddy's `.gitignore`).

```bash
cp .env.example .env
```

Every line in `.env.example` is **commented out on purpose**. Uncomment and fill in **only** the lines you have values for:

```bash
# Scopus (required for Scopus searches)
SCOPUS_API_KEY=<your real key>

# PubMed (required for PubMed searches) - any valid email, no registration
PUBMED_EMAIL=<your real email>

# Optional - only raises the PubMed rate limit from 3 to 10 requests/second
#PUBMED_API_KEY=

# Optional - only needed if 'ieee' is in your config.yaml sources
#IEEE_API_KEY=

# Optional - falls back to PUBMED_EMAIL when unset
#UNPAYWALL_EMAIL=
```

:::{admonition} A placeholder is worse than an empty line
:class: warning
Never leave an invented value such as `PUBMED_API_KEY=my_key_goes_here` in `.env`. An absent optional key only costs you a lower rate limit, but a fake one is sent to the API as if it were real: NCBI rejects the whole request (`HTTP 400 {"error":"API key invalid"}`) and **PubMed silently returns 0 papers** while every other source works.

Review Buddy recognises the usual template patterns (`your_...`, `..._here`, `<...>`, `changeme`, `...@example.com`), ignores them and prints a warning - but anything else is passed through. Comment out what you don't fill in.
:::

**Minimum setup**: arXiv needs no key at all, so Review Buddy runs out of the box. For a real review you want at least `SCOPUS_API_KEY` and/or `PUBMED_EMAIL`.

### 4. Create Your Run Configuration (`config.yaml`)

Every run setting - query, years, sources, filters, model, download toggles - lives in **one file**:

```bash
cp config.example.yaml config.yaml
```

`config.yaml` is gitignored, so your query and filters never end up in git history, and `git pull` never conflicts with your settings. It only needs the keys you want to **change**; everything else falls back to `config.example.yaml`, which is the fully commented reference. For example, this is a complete, valid `config.yaml`:

```yaml
search:
  year_from: 2018
  sources: [scopus, pubmed]
download:
  use_browser: true
```

The [Usage Examples](2_Usage_Examples) walk through every section.

### 5. Optional Services

None of these are required. Each one unlocks a feature.

#### Ollama - for the AI abstract filter

1. Install Ollama: [https://ollama.com](https://ollama.com)
2. That's it if you use `main.py`: `python main.py --ai` starts `ollama serve` and offers to pull the configured model (`--yes` pulls without asking).

If you run `02_abstract_filter_ai.py` on its own, do it by hand:
```bash
ollama pull gemma3:4b      # the default model, one-time download
ollama serve               # leave running in a separate terminal
```

The model, server URL and all filter prompts are set in `config.yaml` under `ai_filter:`. The `OLLAMA_MODEL` and `OLLAMA_URL` environment variables override them (handy on a cluster).

(rb-zotero)=
#### Zotero translation server - more PDFs

The download step works without it, but the vendored Zotero translation server extracts PDF links from publisher landing pages and measurably raises the hit rate. It needs **Node.js** and a one-time setup:

```bash
python scripts/setup_zotero.py                        # init submodule, npm install, apply patch
cd vendor/translation-server && node src/server.js    # start it (port 1969), leave it running
```

You rarely need the second line: `main.py` and `03_download_papers.py` detect a server that is set up but not running and offer to start it. After setup, `git status` shows the submodule as *modified* - that is the required patch, and it is expected.

#### Real-browser fetcher - Cloudflare-protected publishers

Elsevier/ScienceDirect, Wiley and MDPI block every plain HTTP client. Review Buddy can drive a patched Firefox ([Camoufox](https://github.com/daijro/camoufox)) as a last-resort strategy:

```bash
python -m camoufox fetch          # one-time: download the patched Firefox build
python scripts/browser_login.py   # one-time: log in / solve a CAPTCHA yourself in a visible window
```

Then set `download.use_browser: true` in `config.yaml`. The login session is stored in `.browser_profile/` and reused by headless downloads. See [Usage Examples](2_Usage_Examples) for what this costs in time and what it does - and does not - give you access to.

### 6. Obtain API Keys

#### Scopus (Highly Recommended)
- **Website**: [https://dev.elsevier.com/](https://dev.elsevier.com/)
- **How**: Create account → Request API key (an institutional email may be required)
- **Quota**: 20,000 Scopus Search requests per week
- **Per-query ceiling**: 5,000 records per query. Review Buddy works around this automatically by re-issuing a large search as one-year slices (needs `search.year_from`)
- **Coverage**: Best for peer-reviewed publications

#### PubMed (Free, Highly Recommended)
- **Email**: Any valid email address in `PUBMED_EMAIL` - no registration needed
- **API Key** (optional): [https://account.ncbi.nlm.nih.gov/](https://account.ncbi.nlm.nih.gov/) - raises the rate limit from 3 to 10 requests/second
- **Coverage**: Best for biomedical/life sciences

#### Unpaywall (Free, Recommended)
- **Email**: Any valid email in `UNPAYWALL_EMAIL`; if unset, `PUBMED_EMAIL` is used
- **Benefit**: Finds legal open-access copies during the download step

#### IEEE Xplore (Optional)
- **Website**: [https://developer.ieee.org/](https://developer.ieee.org/)
- **How**: Register → Request API key
- **Coverage**: Engineering and computer science
- **Note**: Only queried if `ieee` is listed in `search.sources`

## Verify Installation

### Quick Verification

Create a tiny throw-away config, `smoke_test.yaml`, in the project root:

```yaml
search:
  query: '"machine learning" AND (healthcare OR clinical)'
  year_from: 2024
  max_results_per_source: 25
  sources: [arxiv]       # no API key needed
```

Run the pipeline with it, skipping the download:

```bash
python main.py --config smoke_test.yaml --skip-download
```

You should see a preflight report followed by the two steps (abbreviated output from a real run):

```
==============================================================================
REVIEW BUDDY — full pipeline
==============================================================================
  Query:   "machine learning" AND (healthcare OR clinical)...
  Sources: arxiv
  Filter:  keyword
  Download: skipped  (browser=False, zotero=True, workers=4)

==============================================================================
PREFLIGHT
==============================================================================
  ✓ Core Python packages

Preflight passed.

==============================================================================
▶ STEP 1/3 — Fetch metadata
==============================================================================
...
FOUND 25 UNIQUE PAPERS
...
⏱ STEP 1/3 — Fetch metadata: 1s — done
==============================================================================
▶ STEP 2/3 — Filter abstracts (keyword)
==============================================================================
...
⏱ STEP 2/3 — Filter abstracts (keyword): 1s — done
==============================================================================
PIPELINE SUMMARY
==============================================================================
  Fetch metadata              1s   ok
  Filter abstracts            1s   ok
  TOTAL                       3s   (0.0 min)
  → results/references.bib
  → results/references_filtered.bib
  → results/papers.csv

Pipeline complete.
```

:::{note}
The smoke test writes to `results/`, like any run. Delete that folder (or move it aside) before starting your real search.
:::

### Check Your Credentials

Now point the preflight at your real configuration:

```bash
python main.py --skip-download
```

Preflight reports every source that will be skipped and why, for example:

```
  ⚠ SCOPUS_API_KEY not set (Scopus will be skipped)
      Add it to .env
```

Fix anything marked `⚠` that you care about. Anything marked `✗` blocks the run and comes with the exact command to fix it.

### Run the Test Suite (Optional)

```bash
pytest tests/
```

## Troubleshooting

### A Source Returns 0 Papers
**Symptom**: one database returns nothing while the others work.

**Solution**:
1. Read the preflight / step 1 output for a `⚠ ... will be SKIPPED` line - a missing key or email skips the source.
2. **PubMed returns 0**: check `.env` for a leftover placeholder in `PUBMED_API_KEY` (see the warning in [step 3](#rb-env)).
3. **PubMed or arXiv return 0 but Scopus works**: your query probably uses Scopus-only syntax (`TITLE-ABS-KEY(...)`, `W/5`, `PRE/3`). Review Buddy warns about this before searching; see *Query portability* in [Usage Examples](2_Usage_Examples).
4. A very long query (over ~3,000 characters) is rejected by the APIs (HTTP 413/414) - this is reported as a failure in the log, not as "0 results".

### Import Errors
**Error**: `ModuleNotFoundError: No module named 'src'` (or `yaml`, `pandas`, ...)

**Solution**:
```bash
# Run scripts from the project root (where src/ is)
cd /path/to/review_buddy
conda activate autosearch
python main.py
```

If you launch `main.py` from an environment that is missing dependencies, it automatically re-launches itself inside a conda environment named `autosearch` when one exists.

### Rate Limit Errors
**Error**: `Rate limit exceeded` / HTTP 429

**Solution**:
- **PubMed**: add a `PUBMED_API_KEY` to go from 3 to 10 requests/second
- **Scopus**: check your weekly quota at [dev.elsevier.com](https://dev.elsevier.com)
- **Wait**: limits reset after a few minutes

### No Papers Found At All
1. Try a simpler query: `"machine learning"`
2. Check the year range (some databases lag by 1-2 years)
3. Run one source at a time (`search.sources: [pubmed]`) to see which one fails

### Language Detection Issues
**Error**: `langdetect not installed - language filtering will be skipped`

**Solution**: `pip install langdetect`, or switch the filter off in `config.yaml`:
```yaml
filter:
  enabled:
    no_abstract: true
    non_english: false   # disabled
    non_human: true
```
Remember that `filter.enabled` **replaces** the default list, so list every filter you want to keep.

### Ollama Not Working (AI Filtering)
**Error**: `Cannot connect to Ollama server`

**Solution**:
1. Install Ollama: [https://ollama.com](https://ollama.com)
2. Prefer `python main.py --ai`: it starts the server and pulls the model for you
3. Running the script directly? Start the server (`ollama serve`) and pull the model (`ollama pull gemma3:4b`)
4. Check the server: `ollama list`
5. Verify `ai_filter.ollama_url` in `config.yaml` (or the `OLLAMA_URL` environment variable)

### Zotero Translation Server Not Running
**Message**: `⚠ Zotero translation server is not running.`

This is not an error: downloads continue with Zotero's hosted open-access index and the built-in strategies, you just get fewer PDFs. Run `python scripts/setup_zotero.py` once (needs Node.js) to enable it.

### Browser Profile Locked
**Message**: `⚠ Browser profile appears to be in use (.browser_profile locked)`

Close any open `browser_login.py` / Camoufox window before running the download step - a browser profile can only be opened by one process at a time.

## What's Next?

Proceed to [Usage Examples](2_Usage_Examples) to learn how to:
- Configure and run searches across multiple databases
- Filter papers by abstract content (keyword or AI)
- Download PDFs with the resolver chain and the browser fallback
- Export results in multiple formats
