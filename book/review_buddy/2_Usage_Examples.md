# <i class="fa-solid fa-lightbulb"></i> Usage Examples

## The Workflow

Review Buddy runs three steps:

1. **📚 Fetch Metadata** → Search the databases, deduplicate, export BibTeX/RIS/CSV
2. **🎯 Filter Abstracts** → Exclude papers by keyword rules or with a local LLM
3. **📥 Download PDFs** → Retrieve the full texts

You can run them **with one command** - recommended - or one script at a time:

```bash
python main.py                  # 01 fetch → 02 keyword filter → 03 download
python main.py --ai             # same, with the LLM (Ollama) filter
python main.py --skip-download  # stop after filtering
python main.py --config my.yaml # use a different config file
python main.py --yes            # don't prompt (e.g. pull the Ollama model automatically)
```

```bash
python 01_fetch_metadata.py
python 02_abstract_filter.py      # or: python 02_abstract_filter_ai.py
python 03_download_papers.py
```

`main.py` adds a **preflight** before anything runs. It checks the packages and credentials each enabled step needs, starts Ollama (and pulls the model) for `--ai`, starts or offers to set up the Zotero translation server, and prints the exact fix for anything that is missing. At the end it prints how long each step took.

Every option for every step lives in **`config.yaml`** - you never edit the `.py` scripts. If you haven't created it yet:

```bash
cp config.example.yaml config.yaml
```

:::{admonition} How `config.yaml` is merged
:class: tip
`config.yaml` only needs the keys you want to change - everything else comes from `config.example.yaml`, the commented reference. Lists (such as `search.sources`) replace the default.

**Three sections are replaced as a whole** rather than merged: `filter.enabled`, `filter.keywords` and `ai_filter.filters`. If you define any of them, list *every* filter you want - the defaults are dropped. This is deliberate: a domain-specific config runs exactly the filters you wrote, and nothing else.
:::

---

## Step 1: Fetch Paper Metadata

### Configure Your Search

```yaml
# config.yaml
search:
  query: null                   # inline query, or null to read query_file
  query_file: query.txt         # used when query is null
  year_from: 2020
  year_to: null                 # null = up to the current year
  max_results_per_source: 50    # a big number (e.g. 999999) = as many as each API allows
  pubmed_field: tiab            # PubMed: Title/Abstract only (null = all fields)
  sources: [scopus, pubmed, arxiv]   # options: scopus, pubmed, arxiv, ieee, scholar
  output_dir: results
```

:::{admonition} Google Scholar is off by default
:class: warning
`scholar` is not in the default source list. Google blocks automated queries (CAPTCHA), so it usually returns 0 results without a proxy. Review Buddy hard-caps it at 45 seconds so it can't hang the run, but there is little point enabling it for a systematic search.
:::

### Write the Query in `query.txt` (Recommended)

For anything longer than a few words, leave `query: null` and put the query in `query.txt`. Newlines and indentation are normalised automatically:

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

### Run the Search

```bash
python 01_fetch_metadata.py      # or as part of: python main.py
```

**Output** (real run, arXiv only, abbreviated):
```
================================================================================
REVIEW BUDDY - FETCH PAPER METADATA
================================================================================

✓ Available sources: arXiv, Google Scholar

Search query: "machine learning" AND (healthcare OR clinical)
Year from: 2024
Max results per source: 25

================================================================================
SEARCHING...
================================================================================
Searching sources: ['arxiv']
...
arXiv: Successfully retrieved 25 papers
arXiv: Added 25 papers
Post-filter year validation: 25 papers in range 2024 to any

Total unique papers found: 25

================================================================================
FOUND 25 UNIQUE PAPERS
================================================================================

Papers by source:
  arXiv: 25

================================================================================
GENERATING OUTPUT FILES...
================================================================================
✓ BibTeX: results/references.bib
✓ RIS: results/references.ris
✓ CSV: results/papers.csv
```

"Available sources" lists every source your credentials allow, not the ones you selected; arXiv and Google Scholar are always available. If `config.yaml` asks for a source that can't run, step 1 says so instead of silently returning 0:

```
⚠ 'scopus' is listed in config.yaml sources but will be SKIPPED — SCOPUS_API_KEY not set in .env
```

"Papers by source" counts each unique paper once per database that returned it, so the numbers can add up to more than the unique total.

### What Happens During the Search

- **Deduplication**: a paper found in several databases is merged into one record when the **DOI** matches or the **normalised title** matches (lowercase, punctuation stripped). The PubMed record is kept as the primary one (its PMID unlocks PubMed Central downloads); otherwise the more recent record wins. Missing fields are filled from the duplicates. Details: [docs/DEDUPLICATION.md](https://github.com/leonardozaggia/review_buddy/blob/main/docs/DEDUPLICATION.md).
- **Strict year filter**: after the search, papers outside `year_from`-`year_to` are removed - **and so are papers with no parsable publication date**. The log reports how many (`Post-filter: Removed N papers with no publication date`). Note that number for your PRISMA flow diagram (see [Reporting & Validation](3_Reporting_and_Validation)).
- **API ceilings**: `max_results_per_source` is a ceiling you *request*, not one you get. Each API has its own hard limit:

| Source | Hard limit per query | What Review Buddy does |
|---|---|---|
| Scopus | 5,000 records | Splits the search into one-year slices automatically (needs `year_from`) and concatenates them |
| PubMed | 9,999 records | Warns with the true number of matches |
| arXiv | ~30,000, then HTTP 500 | Stops and keeps what it has |

When a Scopus search is split, you'll see:
```
Scopus: Found 5751 total results
Scopus: 5751 matches exceed the 5000-record per-query ceiling —
        splitting into 7 one-year searches (2020–present) to retrieve all of them.
Scopus: Successfully retrieved 5751 papers
```

A single year with more than 5,000 matches can't be split further: you get that year's first 5,000 and a warning. Narrow the query to recover the rest.

### Query Syntax Quick Reference

| Syntax | Example | Meaning |
|---------|---------|---------|
| `AND` | `AI AND healthcare` | Both terms required |
| `OR` | `"ML" OR "machine learning"` | Either term |
| `NOT` | `AI NOT review` | Exclude term (rewritten per source automatically) |
| `" "` | `"deep learning"` | Exact phrase |
| `( )` | `(AI OR ML) AND healthcare` | Grouping |
| `*` | `Electroencephalogra*` | Wildcard - see the portability rules below |

### Query Portability: One Query, Every Source

Every source receives **the same query string**, and each searcher adapts it to its own API. That only works if you write plain boolean syntax. The traps:

1. **Never use Scopus-only syntax** - `TITLE-ABS-KEY(...)`, `ABS(...)`, `W/5`, `PRE/3`. Scopus honours it, but PubMed returns **0 results with no error** and arXiv returns unrelated papers. Review Buddy prints a warning when it detects these constructs. Scopus searches are already scoped to title/abstract/keywords for you.
2. **Wildcards differ per source.** PubMed ignores truncations with fewer than 4 leading characters (`tim*` contributes nothing; write `time*`). arXiv has no wildcards: the `*` is stripped, which leaves a stem that often matches nothing (`Ischemi*` → `Ischemi` → 0 hits). Review Buddy warns and names every truncated term; if arXiv matters, spell the variants out (`ischemia OR ischemic`).
3. **Keep queries under ~3,000 characters** - longer ones are rejected (HTTP 413/414). That is logged as a failure, not as "0 results".
4. **`pubmed_field: tiab` matters**: without it PubMed matches every field (references, affiliations, MeSH...). On the developer's neonatal-fMRI query that is ~13,900 results against ~800.
5. **arXiv's parser is the weak one**: deeply nested boolean queries can quietly return off-topic results. A low arXiv count on a complex query usually means "the query didn't translate", not "arXiv has nothing".

:::{admonition} Re-fetch Scopus corpora built with an older version
:class: important
Older versions of Review Buddy applied `TITLE-ABS-KEY(...)` only to the **first** group of a query shaped like `(A) AND (B) AND (C)`; the other groups matched every Scopus field, inflating results 10-21x on the developer's test queries. If you built a Scopus corpus before updating, run the search again - the old result set is a differently-scoped query, not a superset you can filter.
:::

**More examples**: [docs/QUERY_SYNTAX.md](https://github.com/leonardozaggia/review_buddy/blob/main/docs/QUERY_SYNTAX.md)

---

## Step 2: Filter Abstracts (Optional)

Pick **one** of the two filters. Both read `results/references.bib` and leave it untouched.

### Option A: Keyword-Based Filtering

A paper is removed when **any** keyword of an enabled filter matches **as a whole word** in its title or abstract. Two filters are built in and need no keywords: `no_abstract` and `non_english` (needs `langdetect`). Every other filter is just a name plus a keyword list:

```yaml
# config.yaml
filter:
  enabled:                # which filters run, in this order
    no_abstract: true
    non_english: true
    epilepsy: true
    bci: true
    non_human: true
    non_empirical: true
  keywords:               # one list per filter name
    epilepsy: [epileptic spike, interictal spike, epileptiform, seizure spike]
    bci: [brain-computer interface, brain computer interface, bci, neural interface]
    non_human: [rat, rats, mouse, mice, rodent, primate, in vitro, animal model]
    non_empirical: [systematic review, meta-analysis, literature review, scoping review]
    # add your own:
    # my_filter: [keyword one, keyword two]
```

The shipped `config.example.yaml` has much longer default lists - copy them from there. Remember that `filter.keywords` replaces the defaults **as a whole**: if you only list your custom filter, the default `non_human` list is gone.

`non_empirical` is special: a paper is only removed if it contains a review keyword **and none** of a set of empirical indicators (`participants`, `cohort`, `n =`, `dataset`, `recorded`, `trial`...). A systematic review that pools data, or a methods paper with a validation dataset, is kept.

Run the filter:
```bash
python 02_abstract_filter.py     # or as part of: python main.py
```

**Output** (real run on the 25 papers above; log prefixes removed):
```
======================================================================
ABSTRACT-BASED PAPER FILTERING
======================================================================
Loaded 25 papers
Registered filter 'epilepsy' with 11 keywords
Registered filter 'bci' with 11 keywords
Registered filter 'non_human' with 41 keywords
Registered filter 'non_empirical' with 11 keywords

Filters to apply: no_abstract, non_english, epilepsy, bci, non_human, non_empirical
...
======================================================================
FILTERING SUMMARY
======================================================================
Initial papers:        25
Papers kept:           22
Papers filtered out:   3
Retention rate:        88.0%

Breakdown by filter:
  - no_abstract         :    0 papers
  - non_english         :    0 papers
  - epilepsy            :    0 papers
  - bci                 :    0 papers
  - non_human           :    2 papers
  - non_empirical       :    1 papers
...
Filtered results saved to:
  - results/papers_filtered.csv
  - results/references_filtered.bib

Filtered out papers saved to: results/filtered_out/
```

:::{admonition} Always read `filtered_out/` - a real false positive
:class: warning
In that run, `non_human` removed two papers. One was correct (a study of *canine* tumours). The other was a robotics study **with autistic children**, removed because its abstract abbreviates *robot-assisted therapy* as **(RAT)** - and `rat` is a `non_human` keyword. Whole-word matching prevents substring hits, but it can't understand meaning.

This is why the default `bci` list deliberately leaves out `bmi`: it would also match *BMI (body mass index)*, which is common in exactly the human clinical abstracts you want to keep.

Open each `results/filtered_out/<filter>.csv`, look for papers that should have stayed, tighten the keywords and run the filter again - it always starts again from `references.bib`.
:::

### Option B: AI-Powered Filtering

Each filter is a **yes/no question in plain language**, answered for every abstract by a local model running in [Ollama](https://ollama.com). Nothing leaves your machine.

**Prerequisites**: install Ollama. `python main.py --ai` does the rest (starts the server, pulls the model). Running `02_abstract_filter_ai.py` directly? Then run `ollama serve` and `ollama pull gemma3:4b` first.

```yaml
# config.yaml
ai_filter:
  model: gemma3:4b              # any Ollama model; the OLLAMA_MODEL env var overrides
  ollama_url: http://localhost:11434
  confidence_threshold: 0.5     # min confidence (0-1) to actually exclude a paper
  temperature: 0.1
  retry_attempts: 3
  cache_responses: true         # cache answers in results/ai_cache/
  structured_output: true       # constrain replies to a JSON schema
  max_workers: 4                # concurrent requests to Ollama; 1 = serial
  filters:
    non_human:
      enabled: true
      prompt: "Is this paper based on animal studies, in-vitro experiments, or computational models only (not human subjects)?"
      description: "Non-human or in-vitro studies"
    is_empirical:
      enabled: true
      invert: true              # YES = keep, NO = exclude (see below)
      prompt: "Does this paper report an original study with its own participants, rather than being a review, meta-analysis, protocol, editorial, or commentary?"
      description: "Keep only original empirical studies"
```

:::{admonition} Ask "is this a paper we want?" and set `invert: true`
:class: tip
Small models (under ~10B parameters) often answer **negated** questions ("does this study *lack* fMRI?") with sound reasoning and the opposite answer. Phrase the question positively ("does this study report fMRI data?") and set `invert: true`, so that a **NO** excludes the paper. On the developer's corpus this single change took one filter from 0.35 to 0.91 agreement with hand labels.
:::

**How a decision is made**:
- Papers **without an abstract are always excluded** in AI mode (counted as `no_abstract`).
- A paper is excluded when a filter fires with confidence ≥ `confidence_threshold`.
- If a filter fires with *lower* confidence, or the model call fails, the paper is **kept and flagged** in `manual_review_ai.csv`. Manual-review papers are therefore a subset of the kept papers.
- Every decision, with its confidence and the model's one-line reason, goes to `results/ai_filtering_log_<timestamp>.json`.
- Answers are cached per model and filter set, so an interrupted run resumes cheaply. Changing the model or the prompts correctly re-evaluates every paper.

Run the AI filter:
```bash
python main.py --ai              # whole pipeline
python 02_abstract_filter_ai.py  # this step only
```

**Output** (illustrative numbers; log prefixes removed):
```
======================================================================
AI FILTERING SUMMARY
======================================================================
Initial papers:        142
Papers kept:           97
Papers filtered out:   45
Manual review needed:  6
Retention rate:        68.3%

Breakdown by filter:
  - no_abstract         :    5 papers
  - non_human           :   21 papers
  - is_empirical        :   22 papers

Ollama Usage:
  - Model calls made:    137
  - Cache hits:          0
  - Failed calls:        0
  - Cache hit rate:      0.0%
  - Model used:          gemma3:4b
...
Decision log saved to: results/ai_filtering_log_*.json
```

`Papers kept + Papers filtered out` always equals `Initial papers`. A paper can be counted under more than one filter in the breakdown, so the breakdown can add up to more than the filtered total. Only papers with an abstract are sent to the model (here 142 − 5 = 137 calls).

**AI filter outputs**:

| File | Contents |
|---|---|
| `results/papers_filtered_ai.csv` | Papers kept |
| `results/references_filtered_ai.bib` | Bibliography of kept papers |
| `results/manual_review_ai.csv` | Low-confidence or failed decisions - **read these yourself** |
| `results/filtered_out_ai/<filter>.csv` | What each filter removed |
| `results/ai_filtering_log_*.json` | Per-paper decision, confidence and reasoning |
| `results/ai_cache/` | Cached model answers |

### Choosing a Model

Measured by the developer on a 6 GB-VRAM laptop GPU, against 48 hand-labelled papers (`scripts/benchmark_ollama_models.py`):

| Model | Agreement with hand labels | Per paper (serial) |
|---|---|---|
| `gemma3:4b` (default) | 0.906 | ~7-16 s |
| `gemma3:12b` | 0.935 | ~37 s |
| `gpt-oss:20b` | 0.971 | ~20 s |

With `max_workers: 4`, a real 5,295-paper run averaged **3.7 s per paper** with `gemma3:4b` - about 5.4 hours, unattended. Iterate on your prompts with `gemma3:4b` and do the final pass with a larger model if the accuracy is worth the time. Avoid reasoning models such as `qwen3`: their "thinking" can't be switched off reliably and they take ~90 s per paper.

These numbers come from **one** corpus. Before trusting a model on yours, measure it - see [Reporting & Validation](3_Reporting_and_Validation).

**Large corpora on a cluster**: `run_filter_hpc.sh` is a ready-made SLURM job that starts Ollama, runs the AI filter and stops the server.

**Comparing strategies**: if you ran both filters on the same corpus,
```bash
python scripts/compare_filters.py
```
reports how many papers each filter kept and which papers they disagree on. It currently looks for the default filter names (`bci`, `no_abstract`, `non_human`, `non_empirical`). A complete keyword-filtering example is in [docs/FILTER_WORKFLOW_EXAMPLE.md](https://github.com/leonardozaggia/review_buddy/blob/main/docs/FILTER_WORKFLOW_EXAMPLE.md).

---

## Step 3: Download PDFs

### Which Bibliography Gets Downloaded

```yaml
# config.yaml
download:
  bib_file: null          # null = auto-pick (see below)
  output_dir: results/pdfs
  max_workers: 4          # parallel downloads (1 = sequential)
  use_zotero: true        # Zotero resolver chain
  use_scihub: false       # Sci-Hub fallback - use responsibly, per your local law
  use_browser: false      # real-browser fetcher for Cloudflare-protected publishers
```

With `bib_file: null` the downloader uses `results/references_filtered.bib` (the **keyword** filter's output) if it exists, otherwise the unfiltered `results/references.bib`.

:::{admonition} Using the AI filter? Set `bib_file` explicitly
:class: warning
The AI-filtered bibliography is **never picked automatically** - not even by `python main.py --ai`. Without the line below, step 3 downloads either a `references_filtered.bib` left over from an earlier keyword run, or the whole unfiltered set:

```yaml
download:
  bib_file: results/references_filtered_ai.bib
```
:::

### Run the Downloader

```bash
python 03_download_papers.py     # or as part of: python main.py
```

If the Zotero translation server isn't running, the standalone script tells you and offers to set it up or start it (`main.py` already asked during preflight). Answering *no* is fine: downloads continue with Zotero's hosted open-access index.

**Output** (illustrative numbers, abbreviated):
```
================================================================================
REVIEW BUDDY - DOWNLOAD PAPERS
================================================================================

Input file: results/references_filtered.bib
Output directory: results/pdfs
Unpaywall email: you@university.edu
Sci-Hub enabled: False
Browser fetcher enabled: False

Zotero translation server: running (127.0.0.1:1969)
================================================================================
STARTING DOWNLOAD...
================================================================================
[INFO] Downloading with 4 parallel workers...
[INFO] PROCESSING: Deep learning for ...
[INFO]   DOI: 10.3389/...
[INFO]   → Trying Zotero resolver chain...
[INFO]   ✓ SUCCESS via zotero:doi:meta
...
================================================================================
SAVING FAILED DOWNLOADS...
================================================================================
Saved 22 failed downloads to:
  - results/pdfs/failed_downloads.csv
  - results/pdfs/failed_downloads.bib

================================================================================
DOWNLOAD COMPLETE!
================================================================================
Downloaded: 67 PDFs
Failed: 22 papers
Location: results/pdfs
Log file: results/pdfs/download.log
Failed downloads list: results/pdfs/failed_downloads.csv
```

`failed_downloads.bib` is ready to import into Zotero (or your institution's library tools) to fetch the rest by hand. Re-running the downloader skips every PDF that already exists, so you can safely run it again later - for example from the campus network.

### Download Strategies

For each paper the downloader tries, in order:

1. **Zotero resolver chain** - the same order the Zotero desktop app uses: DOI → URL → PMCID → Zotero's own open-access index, with the translation server (if running) parsing publisher pages
2. **Real browser, fast path** - only with `use_browser: true` and only for domains known to block every HTTP client (ScienceDirect, Wiley, MDPI)
3. **Direct PDF link** from the metadata
4. **arXiv**
5. **bioRxiv / medRxiv**
6. **Unpaywall** (open-access copies, needs an email)
7. **Crossref** full-text links
8. **PubMed Central** (NCBI open-access service and Europe PMC)
9. **Publisher URL patterns** - MDPI, Frontiers, Nature, IEEE, ScienceDirect, Springer, PLOS
10. **HTML scraping** of the landing page
11. **Real browser** (Camoufox), last resort - only with `use_browser: true`
12. **Sci-Hub** - only with `use_scihub: true`

A paper with neither DOI nor arXiv ID first gets a DOI lookup on Crossref by title. PDFs are named after the DOI (or arXiv ID, or title) plus a short hash, so two papers never collide. ResearchGate/Academia scraping has been removed - it almost never worked and risked IP blocks.

For details, see [docs/DOWNLOADER_GUIDE.md](https://github.com/leonardozaggia/review_buddy/blob/main/docs/DOWNLOADER_GUIDE.md) and, for why the chain is built this way, [docs/ZOTERO_HOW_IT_WORKS.md](https://github.com/leonardozaggia/review_buddy/blob/main/docs/ZOTERO_HOW_IT_WORKS.md).

### What Success Rate to Expect

There is no single number: it depends far more on **your network's institutional access** and the **publisher mix** than on the tool. These are the developer's measurements with the repository's benchmark scripts:

| Measurement | Result |
|---|---|
| 123 real DOIs, university network: built-in chain → + Zotero resolver | 41/123 (33%) → **48/123 (39%)** |
| Same set, by publisher | Springer 8/8, Frontiers 11/12, PLOS 3/3, **Elsevier 4/49** |
| 100 Elsevier DOIs, university network: HTTP + Zotero → + browser fetcher | 14/100 → **90/100**, at ~8.5 s instead of ~1.3 s per paper |
| Small mixed run (Scopus + PubMed + arXiv), browser on, university network | 47/56 PDFs (84%) |

Read these as: open-access and preprint papers download reliably; **Elsevier, Wiley and MDPI need the browser fetcher**; and paywalled content you have no subscription to stays out of reach - no resolver fixes that. Institutional access is IP-based, so run downloads from campus or over the VPN.

:::{admonition} Responsible downloading
:class: caution
The browser fetcher and Sci-Hub change the legal and contractual picture. The browser fetcher only retrieves what your own network is entitled to, but it automates a browser on sites whose terms of service may restrict automated access - check your institution's and the publishers' rules before running it on thousands of papers. Sci-Hub is off by default; enabling it is your decision under your local law.
:::

---

## Complete Workflow Example

### Scenario: Systematic Review on "EEG and Cognitive Assessment"

**Goal**: Find papers on EEG-based cognitive assessment, excluding animal studies, reviews, and BCI research.

#### 1. Write the Query

`query.txt`:
```
(
  EEG OR "event-related potential" OR electroencephalography
)
AND
(
  "cognitive assessment" OR "cognitive function" OR "cognitive performance"
)
```

#### 2. Write the Configuration

`config.yaml`:
```yaml
search:
  query: null                       # read query.txt
  year_from: 2018
  max_results_per_source: 999999    # as many as each API allows
  sources: [scopus, pubmed, arxiv]

filter:
  enabled:
    no_abstract: true
    non_english: true
    bci: true
    non_human: true
    non_empirical: true
  keywords:
    bci: [brain-computer interface, brain computer interface, brain-machine interface, bci, neural interface]
    non_human: [rat, rats, mouse, mice, rodent, primate, animal model, in vitro, in-vitro]
    non_empirical: [systematic review, meta-analysis, literature review, review article, scoping review]
```

#### 3. Run Search and Filtering

```bash
python main.py --skip-download
```

**Result** (illustrative numbers): 287 papers → `results/references.bib`, then 287 → 156 papers → `results/references_filtered.bib`

**Breakdown**:
- No abstract: 12 papers
- Non-English: 8 papers
- BCI: 34 papers
- Non-human: 61 papers
- Non-empirical: 16 papers

#### 4. Review the Filtered Papers

```bash
# View BCI papers that were filtered
head results/filtered_out/bci.csv

# View animal studies that were removed
head results/filtered_out/non_human.csv
```

On Windows PowerShell, use `Get-Content results/filtered_out/bci.csv -TotalCount 10`. If you find false positives, refine the keywords and run `python 02_abstract_filter.py` again.

#### 5. Download PDFs

```bash
python 03_download_papers.py
```

**Result** (illustrative): 156 papers → 117 PDFs → `results/pdfs/`, plus `failed_downloads.csv/.bib` for the other 39.

#### 6. Final Output

```
results/
├── papers.csv                      # All 287 papers
├── references.bib / references.ris # Original bibliography
├── papers_filtered.csv             # ✅ 156 filtered papers
├── references_filtered.bib         # ✅ Bibliography for 156 papers
├── filtered_out/                   # Papers removed by each filter
│   ├── no_abstract.csv
│   ├── non_english.csv
│   ├── bci.csv
│   ├── non_human.csv
│   └── non_empirical.csv
└── pdfs/
    ├── 10_3389_fnhum_2021_..._1a2b3c4d.pdf   # one PDF per paper
    ├── ...
    ├── download.log                # every attempt, per paper
    ├── failed_downloads.csv        # ✅ the 39 you need to get by hand
    └── failed_downloads.bib
```

---

## Advanced Techniques

### Custom Filter Examples

Filter names describe what you want to **exclude** - unless you use `invert: true` in the AI filter.

#### Exclude Pediatric Studies

```yaml
filter:
  enabled:
    no_abstract: true
    pediatric: true
    # ... every other filter you want to keep
  keywords:
    pediatric: [children, child, pediatric, paediatric, infant, toddler, adolescent, school-age]
    # ... keyword lists for the other filters
```

#### Exclude fMRI-Only Studies

```yaml
filter:
  keywords:
    fmri_only:
      - fMRI only
      - exclusively fMRI
      - solely fMRI
      # Be careful with broad terms like 'fMRI' alone:
      # they also catch combined EEG+fMRI studies
```

Exclusions like this, that depend on *what a study did*, are where the AI filter does better than keywords:

```yaml
ai_filter:
  filters:
    has_eeg:
      enabled: true
      invert: true
      prompt: "Does this study record EEG data from its participants?"
      description: "Keep only studies with EEG data"
```

### Combining Several Searches

To run several related queries and screen them as one corpus, give each query its own config file and keep each result:

```bash
# 1. Fetch each query (here with --skip-download; filtering is redone in step 3)
python main.py --config q_attention.yaml --skip-download
cp results/references.bib searches/attention.bib
python main.py --config q_memory.yaml --skip-download
cp results/references.bib searches/memory.bib

# 2. Merge, then remove the papers both searches found
cat searches/attention.bib searches/memory.bib > results/references.bib
python 04_deduplicate_extra.py results/references.bib

# 3. Filter and download the merged set
python 02_abstract_filter.py
python 03_download_papers.py
```

On Windows PowerShell, replace step 2's first line with:
```powershell
Get-Content searches/attention.bib, searches/memory.bib | Set-Content -Encoding utf8 results/references.bib
```

`04_deduplicate_extra.py` matches duplicates by title, DOI or PMID (keeping PubMed records and the most recent entry), saves a timestamped backup next to the file, and then **overwrites the file in place**. It works on `.bib` and `.csv` files.

:::{note}
The filter scripts always read and write `results/` (they ignore `search.output_dir`), which is why the example copies each search out of `results/` before running the next one.
:::

### Reading the Download Log

The downloader writes every attempt to `results/pdfs/download.log`, and **appends** to it on every run. For the latest run, the most reliable summary is the CSV of failures:

```python
import pandas as pd
from pathlib import Path

pdf_dir = Path("results/pdfs")
failed = pd.read_csv(pdf_dir / "failed_downloads.csv")

print(f"PDFs on disk:     {len(list(pdf_dir.glob('*.pdf')))}")
print(f"Failed downloads: {len(failed)}")
print(failed[["Title", "DOI", "Year"]].head())
```

To see which strategy won each paper across all runs, count the success lines in the log:

```python
import re
from collections import Counter
from pathlib import Path

log = Path("results/pdfs/download.log").read_text(encoding="utf-8")  # the log is UTF-8
methods = Counter(re.findall(r"SUCCESS via (\S+)", log))
print(methods.most_common())
print("Failed attempts:", log.count("✗ FAILED"))
```

The log also ends every session with a `DOWNLOAD SESSION SUMMARY` block: totals, success rate, and the number of papers and average time per strategy.

---

## Output Formats

### BibTeX (.bib)

Standard format for LaTeX and most reference managers. Cite keys are `<first author's last name>_<year>`, with a counter added for duplicates:

```bibtex
@article{Smith_2020,
  title = {Machine Learning in Healthcare},
  author = {John Smith and Jane Doe},
  journal = {Journal of Medical AI},
  year = {2020},
  volume = {15},
  number = {3},
  pages = {123-145},
  doi = {10.1234/jmai.2020.001},
  url = {https://example.com/paper},
  pmid = {12345678},
  abstract = {This paper presents a novel approach to...},
}
```

arXiv preprints (no journal) come out as `@misc` entries with an `arxiv_id` field.

### RIS (.ris)

Format for EndNote, Mendeley, Zotero:

```
TY  - JOUR
TI  - Machine Learning in Healthcare
AU  - John Smith
AU  - Jane Doe
JO  - Journal of Medical AI
PY  - 2020
VL  - 15
IS  - 3
SP  - 123-145
DO  - 10.1234/jmai.2020.001
AB  - This paper presents a novel approach to...
UR  - https://example.com/paper
ER  -
```

### CSV (.csv)

`results/papers.csv`, for data analysis and spreadsheets:

| Title | Authors | Journal | Year | DOI | PMID | Citations | URL | Sources | Keywords |
|-------|---------|---------|------|-----|------|-----------|-----|---------|----------|
| Machine Learning... | John Smith; Jane Doe | J Med AI | 2020 | 10.1234... | 12345678 | 45 | https://... | PubMed, Scopus | ... |

The filtered CSVs (`papers_filtered.csv`, `papers_filtered_ai.csv`, `filtered_out*/`) use a shorter schema - `Title, Authors, Journal, Year, DOI, PMID, URL, Has_Abstract` - without `Sources` and `Citations`. Join them back to `papers.csv` on the DOI or title if you need those columns.

---

## Tips & Best Practices

### Maximize Paper Discovery

✅ **Use multiple sources** - Each database has different coverage  
✅ **Start with broad queries** - Filter afterwards programmatically  
✅ **Check year ranges** - Recent papers may not be indexed everywhere  
✅ **Use query.txt** - Better for complex, multi-line queries  
✅ **Keep `config.yaml` and `query.txt` with your results** - together they *are* your search strategy

### Optimize Filtering

✅ **Start conservative** - Use specific keywords first  
✅ **Review filtered-out papers** - Check for false positives (remember `RAT`)  
✅ **Iterate** - Refine filters based on review  
✅ **Phrase AI prompts positively** - and use `invert: true`  
✅ **Read `manual_review_ai.csv`** - These are the calls the model wasn't sure about

### Improve Download Success

✅ **Configure an Unpaywall email** - Free open-access lookups  
✅ **Install `curl_cffi`** - Avoids HTTP 403 from many publishers  
✅ **Set up the Zotero translation server** - Measurably more PDFs  
✅ **Turn on `use_browser`** for Elsevier/Wiley/MDPI-heavy corpora  
✅ **Download from campus or VPN** - Institutional access is IP-based  
✅ **Monitor logs** - `download.log` records why each paper failed

### Query Construction

✅ **Good:**
```
(machine learning OR deep learning) AND (healthcare OR medical)
```

❌ **Too narrow:**
```
"machine learning for medical diagnosis in pediatric cardiology"
```

✅ **Boolean logic:**
```
(EEG OR MEG OR iEEG) AND cognition NOT animal
```

❌ **Scopus-only syntax** (PubMed returns 0, arXiv returns noise):
```
TITLE-ABS-KEY(EEG W/5 cognition)
```

❌ **Short wildcards** (ignored by PubMed, broken on arXiv):
```
EEG AND (response tim* OR RT*)
```

---

## Troubleshooting Common Issues

### No Papers Found

**Problem**: Search returns 0 papers

**Solutions**:
1. Look for `⚠ ... will be SKIPPED` lines - a missing key or email skips the source
2. Look for the Scopus-only syntax or wildcard warnings before the search starts
3. Simplify the query: `"machine learning"` instead of a complex boolean
4. Run one source at a time (`search.sources: [pubmed]`) to isolate the failing one

### Filtering Too Aggressive

**Problem**: Too many papers filtered out

**Solutions**:
1. Review the `filtered_out/*.csv` (or `filtered_out_ai/*.csv`) files
2. Make keywords more specific, or drop the ones that cause false positives
3. AI filter: raise `confidence_threshold`, or rephrase the prompt positively with `invert: true`
4. Use the AI filter for distinctions keywords can't make

### Low Download Success Rate

**Problem**: Few PDFs downloaded

**Solutions**:
1. Add `UNPAYWALL_EMAIL` (or `PUBMED_EMAIL`) to `.env`
2. Check that `curl_cffi` is installed (preflight warns if it isn't)
3. Set up and start the Zotero translation server
4. Enable `download.use_browser` for Cloudflare-protected publishers
5. Run from your institution's network or VPN
6. Read `download.log` for the reason behind each failure

### Import/Path Errors

**Problem**: `ModuleNotFoundError` or import errors

**Solutions**:
1. Run from the project root: `cd /path/to/review_buddy`
2. Activate your environment: `conda activate autosearch`
3. Don't rename the project's folders

---

## Next Steps

- Read [Reporting & Validation](3_Reporting_and_Validation) to turn a run into a PRISMA-ready, defensible method
- Review [docs/CONFIGURATION.md](https://github.com/leonardozaggia/review_buddy/blob/main/docs/CONFIGURATION.md) for every configuration option
- Review [docs/QUERY_SYNTAX.md](https://github.com/leonardozaggia/review_buddy/blob/main/docs/QUERY_SYNTAX.md) for advanced query patterns
- See [docs/DOWNLOADER_GUIDE.md](https://github.com/leonardozaggia/review_buddy/blob/main/docs/DOWNLOADER_GUIDE.md) for download troubleshooting
- Explore [Additional Tools](../additional_tools/0_Overview) for complementary resources
- Use [LitMaps](../additional_tools/2_LitMaps) for citation network discovery
