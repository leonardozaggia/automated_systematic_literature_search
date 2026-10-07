# <i class="fa-solid fa-book-open"></i> Understanding Systematic Reviews & Metanalysis

## What is a Systematic Review?

A **systematic review** is a rigorous, structured approach to reviewing existing research literature. Unlike traditional literature reviews, systematic reviews follow a predefined protocol to:

- **Minimize bias** through explicit, reproducible methods
- **Comprehensively search** multiple databases and sources
- **Systematically screen** and select relevant studies
- **Critically appraise** the quality of included studies
- **Synthesize findings** using transparent methods

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} Traditional Review
:class-header: bg-warning text-dark

❌ Narrative and subjective  
❌ Selective citation  
❌ Not reproducible  
❌ Prone to bias  
❌ Qualitative only
:::

:::{grid-item-card} Systematic Review
:class-header: bg-success

✅ Structured protocol  
✅ Comprehensive search  
✅ Reproducible methods  
✅ Minimizes bias  
✅ Can be quantitative
:::

::::

## What is a Metanalysis?

A **metanalysis** is a statistical technique that combines results from multiple studies to:

- **Increase statistical power** by pooling data
- **Resolve controversies** from conflicting studies
- **Generate new hypotheses** from synthesized evidence
- **Quantify effect sizes** across studies
- **Assess heterogeneity** in research findings

:::{admonition} Key Difference
:class: note
**Systematic Review** = comprehensive literature review methodology  
**Metanalysis** = statistical synthesis of systematic review results
:::

## The Stages of a Systematic Review

A systematic review follows a protocol written *before* the search starts. Methods handbooks such as the Cochrane Handbook {cite}`Higgins2024Handbook` describe the stages in detail; the typical workflow is:

```{mermaid}
graph TB
    A[Define Question] --> B[Develop Protocol]
    B --> C[Literature Search]
    C --> D[Screen Papers]
    D --> E[Full-Text Review]
    E --> F[Data Extraction]
    F --> G[Quality Assessment]
    G --> H[Data Synthesis]
    H --> I[Report Results]
    
    style A fill:#e1f5ff
    style C fill:#fff4e1
    style D fill:#fff4e1
    style E fill:#fff4e1
    style H fill:#e8f5e9
```

The tools in this book automate the orange stages: the literature search, the first screening pass and the full-text retrieval.

### Reporting: PRISMA

The **Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA 2020)** statement {cite}`Page2021PRISMA` is a **reporting** guideline, not a recipe for conducting the review: a 27-item checklist and a flow diagram that show readers what you searched, how many records you screened and excluded at each stage, and why. Two companions matter for automated reviews:

- **PRISMA-S** {cite}`Rethlefsen2021PRISMAS` - how to report the literature *search* itself: every database, the full search strings, limits, dates and deduplication.
- **Guidance on AI in evidence synthesis** - Cochrane, the Campbell Collaboration, JBI and the Collaboration for Environmental Evidence ask that AI tools be used under human oversight and that every AI-assisted judgement be reported transparently {cite}`Flemyng2025RAISE`.

No tool makes a review "PRISMA-compliant" - your report does. Review Buddy produces the records you need to write it; [Reporting & Validation](../review_buddy/3_Reporting_and_Validation) shows how to map its outputs onto the PRISMA flow diagram.

## Why Automate?

### The Traditional Approach is Challenging

Manual systematic reviews face several challenges:

| Challenge | Impact |
|-----------|--------|
| **Time-consuming** | Registered reviews take on average more than a year to complete {cite}`Borah2017Time` |
| **Multiple databases** | Each has different syntax and interfaces |
| **Duplicate detection** | Manual deduplication is error-prone |
| **Screen hundreds of papers** | Tedious and inconsistent |
| **Managing references** | Complex bibliography management |
| **Reproducibility** | Hard to document all decisions |

### The Automated Advantage

Automation tools can help with:

 **Speed**: Search multiple databases in one run  
 **Consistency**: The same criteria applied in the same way to every record  
 **Reproducibility**: Document and share exact search parameters  
 **Traceability**: Every exclusion recorded, with the rule or the model's reasoning behind it  
 **Organization**: Systematic tracking of decisions and classifications  
 **Efficiency**: Free up time for critical thinking and analysis

:::{admonition} Automation reduces the workload - not the responsibility
:class: caution
An automated filter is consistent, but it can be consistently wrong: a keyword rule cannot understand meaning, and a language model can misjudge an abstract. Automated screening should support human screening, with the exclusions checked and the method reported. See [Reporting & Validation](../review_buddy/3_Reporting_and_Validation).
:::

## Tools Overview

This book focuses on powerful Python tools for automated literature review:

### 1. **Review Buddy** (Primary Tool)
- **Multi-database search**: Scopus, PubMed, arXiv, IEEE Xplore (and Google Scholar, off by default), from one boolean query
- **Smart filtering**: Keyword-based OR AI-powered abstract screening with a local Ollama model
- **Zotero-style PDF retrieval**: a resolver chain with 10+ fallback strategies and an optional real-browser fetcher
- **One command, one config file**: `python main.py` runs Fetch → Filter → Download from `config.yaml`
- **Preflight checks**: missing keys, models or services are reported with the exact fix before anything runs
- **Multiple exports**: BibTeX, RIS, CSV
- **Open source**: Available at [github.com/leonardozaggia/review_buddy](https://github.com/leonardozaggia/review_buddy)

### 2. **Complementary Tools**
- **Paper-finder**: Gui based discovering tool
- **Info-extractor**: Convert unstructured PDFs into structured, machine-readable data
- **LitMaps**: Visual citation network discovery
- **Consensus**: AI-powered scientific consensus search
- **Elicit**: AI data extraction and screening


## What You'll Need

Before starting, you should have:

- ✅ Basic Python knowledge (or willingness to learn)
- ✅ A clear research question
- ✅ Access to relevant databases (some require API keys)
- ✅ Understanding of your field's literature

:::{admonition} Prerequisites
:class: tip
If you're new to Python, check out the [Setup Guide](1_Setup) in the next section, which includes links to Python tutorials and environment setup instructions.
:::

## A Real-World Example

Let's say you want to conduct a systematic review on **"Machine Learning Applications in Mental Health Diagnosis"**. Here's how Review Buddy helps:

**Without Automation:**
- Manually search PubMed, Scopus, IEEE, ACM (2-3 days)
- Export results from each database separately (3-4 hours)
- Manually remove duplicates in Excel (4-6 hours)
- Download PDFs one by one (1-2 weeks)
- Track everything in spreadsheets (ongoing confusion)

**With Review Buddy:**

Describe the search once, in `query.txt` and `config.yaml`:
```yaml
# config.yaml
search:
  query: '("machine learning" OR "artificial intelligence") AND "mental health" AND diagnosis'
  year_from: 2018
  sources: [scopus, pubmed, arxiv, ieee]
filter:
  enabled: {no_abstract: true, non_english: true, non_human: true, non_empirical: true}
```

Then run it:
```bash
python main.py
# Step 1: search all databases, deduplicate → references.bib, papers.csv
# Step 2: filter by abstract (non-English, animal studies, reviews) → references_filtered.bib
# Step 3: download the PDFs → results/pdfs/, plus failed_downloads.csv
```

**Result** (illustrative numbers):
1. 200+ papers found across 4 databases, merged into one deduplicated list
2. Every exclusion recorded per filter, ready to check - e.g. 200 → 145 papers
3. PDFs retrieved automatically for most of the kept papers, and a list of the rest to fetch by hand
4. Ready for screening in BibTeX/RIS/CSV format
5. The query and every setting saved in two text files you can publish with the review

How many PDFs you get depends mostly on your institution's access and the publisher mix - see [Usage Examples](../review_buddy/2_Usage_Examples) for measured numbers.

## Expected Outcomes

By the end of this book, you will be able to:

1. ✅ Formulate research questions suitable for systematic reviews
2. ✅ Construct complex search queries using boolean logic
3. ✅ Execute searches across multiple academic databases
4. ✅ Efficiently screen and categorize hundreds of papers
5. ✅ Extract and organize relevant information
6. ✅ Generate publication-ready bibliographies
7. ✅ Create reproducible, documented workflows
8. ✅ Report your search and screening following PRISMA 2020 and PRISMA-S

## Next Steps

Ready to set up your environment? Head to the **[Setup Guide](1_Setup)** to install the necessary tools and configure your workspace!

---

:::{admonition} Stay Updated
:class: tip
Systematic review methodology and automation tools are constantly evolving. Bookmark this book and check back for updates!
:::




