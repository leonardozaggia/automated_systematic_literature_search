# <i class="fa-brands fa-simplybuilt"></i> Review Buddy

## Overview

[![GitHub Badge](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/leonardozaggia/review_buddy)

**Review Buddy** does the legwork of a systematic literature review end to end: it searches the databases, screens every abstract with keyword rules or a local LLM, and retrieves the PDFs. One configuration file describes the whole run, and one command executes it.

Perfect for:
- **Systematic reviews and meta-analyses** that need a comprehensive, documented search
- **Reproducible research**: the query and every setting live in two small text files
- **Large literature sets**: thousands of records, screened overnight on one machine
- **Confidential screening**: the AI filter runs locally - no abstract is sent to a third party

## Key Features

### Search: 5 Databases, One Query
- **Scopus**: Comprehensive coverage of peer-reviewed literature
- **PubMed**: Biomedical and life sciences, with PubMed Central access
- **arXiv**: Preprints - no API key needed
- **IEEE Xplore**: Engineering and computer science
- **Google Scholar**: Available, but off by default (Google blocks automated queries)

The searchers adapt one boolean query to each API and handle the API limits for you. A Scopus search over the 5,000-record ceiling is automatically split into one-year slices. Before searching, Review Buddy warns about query syntax that would silently fail on some sources.

### Screen: Keywords or a Local LLM
- **Keyword filters**: whole-word matching on title and abstract, one keyword list per filter, plus built-in `no_abstract` and `non_english` filters
- **AI filters**: your inclusion criteria as plain-English yes/no questions, answered by a model running in [Ollama](https://ollama.com) on your own machine
- **Every decision logged**: what each filter removed, the model's confidence and its reasoning
- **Manual review queue**: low-confidence AI calls are kept and flagged for a human, never silently dropped

### Download: A Zotero-Style Resolver Chain
- **Zotero resolver chain first** - the order the Zotero desktop app uses, including Zotero's own open-access index
- **10+ fallback strategies**: direct links, arXiv, bioRxiv/medRxiv, Unpaywall, Crossref, PubMed Central, publisher URL patterns, HTML scraping
- **Real-browser fetcher** (optional) for Cloudflare-protected publishers - Elsevier, Wiley, MDPI
- **Parallel downloads**, with a list of every failure (`failed_downloads.csv/.bib`) to fetch by hand

### Export Formats
- **BibTeX**: For LaTeX and reference managers
- **RIS**: For EndNote, Mendeley, Zotero
- **CSV**: For data analysis and spreadsheets

### Deduplication
Papers found in several databases are merged into one record:
- Same **DOI**, or same **normalised title** (case and punctuation ignored)
- **PubMed record preferred** as the primary entry (its PMID unlocks PubMed Central)
- Otherwise the **more recent** record wins; missing fields are filled from the duplicates
- The databases that found each paper are kept in the `Sources` column

## How a Run Works

```{mermaid}
graph LR
    Q["config.yaml<br>+ query.txt"] --> S1["01 Fetch<br>Scopus · PubMed · arXiv · IEEE"]
    S1 --> R1["references.bib<br>papers.csv"]
    R1 --> S2{"02 Filter"}
    S2 -->|keyword| R2["references_filtered.bib"]
    S2 -->|AI| R3["references_filtered_ai.bib<br>manual_review_ai.csv"]
    R2 --> S3["03 Download"]
    R3 --> S3
    S3 --> R4["pdfs/<br>failed_downloads.csv"]

    style Q fill:#e1f5ff
    style S2 fill:#fff4e1
    style R4 fill:#e8f5e9
```

You can run the whole pipeline with one command:
```bash
python main.py          # keyword filter
python main.py --ai     # LLM filter
```

or step by step:
```bash
python 01_fetch_metadata.py
python 02_abstract_filter.py        # Keyword-based
# OR
python 02_abstract_filter_ai.py     # AI-powered (Ollama)
python 03_download_papers.py
```

`main.py` checks everything each step needs before it starts (a *preflight*): packages, credentials, the Ollama model, the Zotero server. It starts what it can, prints the exact fix for anything it can't, and reports how long each step took.

## Quick Start Example

**1. Set up API keys** (`.env` - uncomment only what you fill in):
```bash
cp .env.example .env
```
```bash
SCOPUS_API_KEY=<your key>
PUBMED_EMAIL=<your email>
```

**2. Configure your search** (`config.yaml` - only the keys you change):
```bash
cp config.example.yaml config.yaml
```
```yaml
search:
  query: "machine learning AND healthcare"
  year_from: 2020
  max_results_per_source: 50
  sources: [scopus, pubmed, arxiv]
```

**3. Run**:
```bash
python main.py --ai
```

**Results** (in `results/`):
- `papers.csv`, `references.bib`, `references.ris` - every paper found
- `references_filtered.bib` / `references_filtered_ai.bib` - after the keyword / AI filter
- `filtered_out/` / `filtered_out_ai/` - what each filter removed
- `manual_review_ai.csv` - AI decisions for you to check
- `pdfs/` - the downloaded papers, `download.log` and `failed_downloads.csv/.bib`

:::{admonition} Using the AI filter? Point the download step at its output
:class: warning
Step 3 does **not** pick up the AI-filtered bibliography automatically, not even with `main.py --ai`. Add `download: {bib_file: results/references_filtered_ai.bib}` to `config.yaml` - see [Usage Examples](2_Usage_Examples).
:::

## What It Achieves - and What It Won't Do

These are the developer's own measurements with the benchmark scripts in the repository, on real corpora:

- **Screening**: `gemma3:4b` agrees with hand labels on 0.906 of decisions on a 48-paper benchmark (`gpt-oss:20b`: 0.971). A 5,295-paper run took about 5.4 hours on a 6 GB laptop GPU.
- **PDF retrieval**: on 123 real DOIs from a university network, 33% with the built-in chain and 39% with the Zotero resolver added. On 100 Elsevier DOIs, 14% without and **90% with** the real-browser fetcher.

Limits to keep in mind:
- **Paywalls are paywalls.** The resolvers *find* PDF links; you still need access (campus network or VPN).
- **Screening is a filter, not a reviewer.** Even at 0.971 agreement, a model disagrees with a human on about 1 paper in 34. Read `manual_review_ai.csv` and spot-check what was excluded - see [Reporting & Validation](3_Reporting_and_Validation).
- **Google Scholar is unreliable**, so it is off by default.
- **Local LLM screening costs wall time, not money**: thousands of abstracts is an overnight job.

## Architecture

```
review_buddy/
├── main.py                      # Runs all three steps from config.yaml
├── 01_fetch_metadata.py         # Search + dedup + export
├── 02_abstract_filter.py        # Keyword filtering
├── 02_abstract_filter_ai.py     # LLM filtering
├── 03_download_papers.py        # PDF retrieval
├── 04_deduplicate_extra.py      # Standalone dedup for merged files
├── config.example.yaml          # Run-configuration template (copy to config.yaml)
├── .env.example                 # API key template (copy to .env)
├── query.txt                    # Optional: external query file
├── run_filter_hpc.sh            # SLURM job for the AI filter
├── src/
│   ├── settings.py              # config.yaml loader
│   ├── config.py                # API keys and credentials
│   ├── models.py                # Paper data model
│   ├── paper_searcher.py        # Search coordinator and deduplication
│   ├── abstract_filter.py       # Keyword filtering logic
│   ├── ai_abstract_filter.py    # AI filtering logic
│   ├── llm_client.py            # Ollama client
│   ├── utils.py                 # Loading/saving helpers
│   └── searchers/
│       ├── scopus_searcher.py
│       ├── pubmed_searcher.py
│       ├── arxiv_searcher.py
│       ├── scholar_searcher.py
│       ├── ieee_searcher.py
│       ├── zotero_client.py     # Zotero resolver chain
│       ├── http_client.py       # requests + curl_cffi transport
│       ├── browser_fetcher.py   # Camoufox real-browser fetcher
│       └── paper_downloader.py  # Download strategy chain
├── scripts/                     # Setup, benchmarks and utilities
│   ├── setup_zotero.py          # One-time Zotero translation server setup
│   ├── browser_login.py         # One-time login for the browser fetcher
│   ├── compare_filters.py       # Compare AI vs keyword filtering
│   └── benchmark_*.py           # Model and download benchmarks
├── docs/                        # Detailed guides
├── tests/                       # Test suite (pytest)
├── vendor/translation-server/   # Zotero translation server (git submodule)
└── results/                     # Output (auto-created, gitignored)
    ├── papers.csv
    ├── references.bib / .ris
    ├── papers_filtered.csv         # After keyword filtering
    ├── references_filtered.bib
    ├── filtered_out/               # Papers removed by each keyword filter
    ├── papers_filtered_ai.csv      # After AI filtering
    ├── references_filtered_ai.bib
    ├── manual_review_ai.csv        # Papers needing review (AI)
    ├── filtered_out_ai/            # Papers removed by each AI filter
    ├── ai_filtering_log_*.json     # Detailed AI decisions
    ├── ai_cache/                   # Cached model answers
    └── pdfs/
        ├── download.log
        └── failed_downloads.csv / .bib
```

## Documentation in the Repository

| If you want to | Read |
|---|---|
| Install it, set API keys, add the optional services | [docs/SETUP.md](https://github.com/leonardozaggia/review_buddy/blob/main/docs/SETUP.md) |
| Configure a run - query, filters, models, download toggles | [docs/CONFIGURATION.md](https://github.com/leonardozaggia/review_buddy/blob/main/docs/CONFIGURATION.md) |
| Write a good boolean query | [docs/QUERY_SYNTAX.md](https://github.com/leonardozaggia/review_buddy/blob/main/docs/QUERY_SYNTAX.md) |
| Understand the download strategies | [docs/DOWNLOADER_GUIDE.md](https://github.com/leonardozaggia/review_buddy/blob/main/docs/DOWNLOADER_GUIDE.md) |
| Know how Zotero fetches PDFs, and how the browser fetcher gets past Cloudflare | [docs/ZOTERO_HOW_IT_WORKS.md](https://github.com/leonardozaggia/review_buddy/blob/main/docs/ZOTERO_HOW_IT_WORKS.md) |
| See how duplicates across sources are merged | [docs/DEDUPLICATION.md](https://github.com/leonardozaggia/review_buddy/blob/main/docs/DEDUPLICATION.md) |

The Review Buddy codebase is actively maintained and welcomes contributions from the research community.

## Next Steps

Continue to the next sections to learn:
1. **[Installation](1_Installation)**: Setting up Review Buddy, API keys and the optional services
2. **[Usage Examples](2_Usage_Examples)**: Every step in detail, a complete workflow, and advanced techniques
3. **[Reporting & Validation](3_Reporting_and_Validation)**: Turning a run into a PRISMA-ready, defensible method
