# Why Downloads Failed & DOIs Are Missing: Root Cause Analysis

## 🔍 Root Cause

**Findpapers doesn't store PubMed IDs or other database identifiers in the search results.**

This causes a cascading effect:

1. ❌ No PubMed ID → Can't query PubMed for PDF links
2. ❌ No DOI stored → Can't resolve DOI to publisher PDF
3. ❌ No URLs in database response → "Empty URL list" error
4. ❌ No DOI → Missing DOI field in BibTeX

## 📊 What Findpapers Returns from PubMed

From your `search_results.json`:

```json
{
  "doi": null,           # PubMed API returned no DOI
  "pubmed_id": null,     # Not stored by Findpapers
  "urls": [],            # PubMed doesn't provide PDF URLs
  "databases": ["PubMed"]
}
```

**The data simply isn't there.**

## ❓ Why This Happens

### 1. PubMed API Limitations

PubMed's E-utilities API sometimes doesn't include DOI in responses, especially for:
- Very recent publications (2024-2025 papers)
- Papers still in "ahead of print" status
- Certain journals that don't consistently report DOIs

### 2. Findpapers Data Model

Findpapers focuses on:
- ✅ Title, authors, abstract
- ✅ Publication venue, date
- ✅ Keywords, citations
- ❌ Database-specific IDs (PMID, DOI, etc.)

### 3. Download Strategy

Findpapers tries to find download URLs by:
1. Checking if database provides direct PDF link
2. Attempting heuristic PDF URL construction
3. If neither works → "Empty URL list"

For PubMed:
- PubMed is metadata-only (no PDFs)
- No heuristic can construct PubMed Central URLs without PMCID
- Result: Always fails for non-PMC papers

## ✅ What Actually Works

### ✅ arXiv Papers
```json
{
  "doi": "10.48550/arXiv.2301.xxxxx",  # arXiv provides DOI
  "urls": ["https://arxiv.org/pdf/2301.xxxxx.pdf"],  # Direct PDF
  "databases": ["arXiv"]
}
```

**Why:** arXiv provides:
- Persistent URLs for PDFs
- DOIs for all papers
- No paywalls

### ✅ PubMed Central (PMC) Papers

If paper is in PMC (free full-text):
```json
{
  "urls": ["https://www.ncbi.nlm.nih.gov/pmc/articles/PMCxxxxxxx/pdf/"],
  "databases": ["PubMed"]
}
```

But your papers are in *Journal of Affective Disorders* - not in PMC.

## 🎯 Solutions That Work

### Solution 1: Use arXiv ⭐ BEST

```python
databases = ["arxiv"]  # Always works!
```

**Why:** All arXiv papers have:
- Direct PDF URLs
- DOI fields
- No paywalls

### Solution 2: Search Google Scholar

Since we have title + authors, we can find DOIs via Google Scholar:

```python
# Instead of using Findpapers' incomplete data,
# scrape DOI from Google Scholar search results
```

### Solution 3: Manual DOI Lookup

1. Take paper title from JSON
2. Search on Google Scholar
3. Find DOI
4. Use DOI to access paper

This is what `extract_paper_links.py` generates for you.

### Solution 4: Include Multiple Databases

```python
databases = ["pubmed", "arxiv", "biorxiv", "medrxiv"]
```

- PubMed: Comprehensive medical literature
- arXiv: AI/ML papers (downloadable!)
- bioRxiv/medRxiv: Preprints (downloadable!)

Some papers will be in multiple databases:
- arXiv version → Downloads successfully
- PubMed version → Fails, but has better metadata

## 📈 The Reality of Automated Literature Search

### What Works Perfectly
- ✅ Searching multiple databases
- ✅ Collecting metadata (title, authors, abstract)
- ✅ Refining and categorizing papers
- ✅ Generating citations
- ✅ Downloading from open-access sources

### What Has Limitations
- ⚠️ Downloading from paywalled journals
- ⚠️ Complete metadata (DOI, IDs) from all databases
- ⚠️ PDF extraction from publisher websites
- ⚠️ Handling ahead-of-print papers

### What Requires Manual Work
- 📝 Accessing paywalled papers (via institution)
- 📝 Finding DOIs for papers without them
- 📝 Verifying paper quality and relevance
- 📝 Full-text screening

## 🎓 Best Practices for Systematic Reviews

### 1. Multi-Database Strategy

```python
# Cast a wide net
databases = [
    "pubmed",      # Medical literature (comprehensive)
    "arxiv",       # AI/ML preprints (downloadable)
    "biorxiv",     # Biology preprints (downloadable)
    "medrxiv",     # Medical preprints (downloadable)
    "ieee",        # Engineering (via API if available)
]
```

### 2. Tiered Access Approach

**Tier 1: Automatic Downloads**
- arXiv papers
- bioRxiv/medRxiv papers
- PMC papers

**Tier 2: Institutional Access**
- PubMed papers via university library
- IEEE papers via institutional subscription
- Publisher websites via VPN

**Tier 3: Manual Requests**
- Contact authors directly
- ResearchGate requests
- Interlibrary loan

### 3. Use Findpapers for What It's Good At

**✅ Excellent for:**
- Initial search and discovery
- Screening titles/abstracts
- Categorizing papers
- Citation management
- Finding open-access versions

**❌ Don't rely on for:**
- Downloading all papers automatically
- Complete metadata extraction
- Accessing paywalled content
- Real-time database updates

## 💡 For Your Meeting

### What to Say About Failures

> "Automated literature search tools like Findpapers are excellent for the discovery phase - finding relevant papers across multiple databases. However, accessing full-text PDFs remains a challenge for paywalled journals. This is where institutional subscriptions and open-access alternatives like arXiv become crucial."

### What to Show

1. **Show Success:** Run `quick_arxiv_demo.py` - complete workflow with downloads
2. **Explain Limitations:** Show PubMed failures, explain why
3. **Demonstrate Solution:** Show helper scripts that generate access links
4. **Best Practices:** Explain multi-database + institutional access strategy

### Key Message

> "The tool automates 80% of the workflow - finding and organizing papers. The remaining 20% - accessing paywalled content - still requires institutional resources. This is a limitation of academic publishing, not the search tool."

## 📚 Additional Resources

### For Finding DOIs
- CrossRef API: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- Google Scholar: Most reliable for finding DOIs
- Publisher websites: Direct lookup

### For Accessing Papers
- Unpaywall: https://unpaywall.org/ (finds legal open-access versions)
- CORE: https://core.ac.uk/ (aggregator of open-access research)
- Author's institutional repository
- ResearchGate/Academia.edu (author-uploaded copies)

### For Preprints (Always Free)
- arXiv: https://arxiv.org/ (physics, CS, math, etc.)
- bioRxiv: https://www.biorxiv.org/ (biology)
- medRxiv: https://www.medrxiv.org/ (medical sciences)
- PsyArXiv: https://psyarxiv.com/ (psychology)

---

**Bottom Line:** The "failures" you encountered are actually normal limitations of automated academic paper access. Your demo should show:
1. What works amazingly well (arXiv)
2. What has limitations (PubMed downloads)
3. How to work around those limitations (DOI lookup, institutional access)

This demonstrates both technical competence AND understanding of the real-world research workflow! 🎯
