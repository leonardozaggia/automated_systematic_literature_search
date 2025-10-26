---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

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

## The PRISMA Framework

The **Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA)** provides guidelines for conducting and reporting systematic reviews. The typical workflow includes:

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

## Why Automate?

### The Traditional Approach is Challenging

Manual systematic reviews face several challenges:

| Challenge | Impact |
|-----------|--------|
| **Time-consuming** | Can take 6-18 months to complete |
| **Multiple databases** | Each has different syntax and interfaces |
| **Duplicate detection** | Manual deduplication is error-prone |
| **Screen hundreds of papers** | Tedious and inconsistent |
| **Managing references** | Complex bibliography management |
| **Reproducibility** | Hard to document all decisions |

### The Automated Advantage

Automation tools can help with:

 **Speed**: Search multiple databases simultaneously  
 **Accuracy**: Consistent application of inclusion/exclusion criteria  
 **Reproducibility**: Document and share exact search parameters  
 **Comprehensiveness**: Ensure no relevant papers are missed  
 **Organization**: Systematic tracking of decisions and classifications  
 **Efficiency**: Free up time for critical thinking and analysis

## Tools Overview

This book focuses on powerful Python tools for automated literature review:

### 1. **Review Buddy** (Primary Tool)
- **5-database search**: Scopus, PubMed, arXiv, Google Scholar, IEEE Xplore
- **Smart filtering**: Keyword-based OR AI-powered (Ollama) abstract screening
- **10+ download strategies**: 70-90% success rate including open access, arXiv, bioRxiv, PMC, publisher patterns
- **Simple 3-step workflow**: Fetch → Filter → Download
- **Production-ready**: Comprehensive error handling, logging, and documentation
- **Multiple exports**: BibTeX, RIS, CSV
- **Open source**: Available at [github.com/leonardozaggia/review_buddy](https://github.com/leonardozaggia/review_buddy)

### 2. **Complementary Tools**
- **LitMaps**: Visual citation network discovery
- **Consensus**: AI-powered scientific consensus search
- **Elicit**: AI data extraction and screening
- **Findpapers**: command-line configuration-based search tool
- **PaperScraper**: Preprint scraping (arXiv, bioRxiv, medRxiv)

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
```bash
# Step 1: Search all databases (5-10 minutes)
python 01_fetch_metadata.py
# Query: (machine learning OR AI) AND mental health AND diagnosis
# Result: 200+ papers from 5 databases → references.bib

# Step 2: Filter papers by abstract (5-10 minutes) - Optional
python 02_abstract_filter.py
# Exclude: non-English, animal studies, reviews
# Result: 200 → 145 papers → references_filtered.bib

# Step 3: Download PDFs automatically (10 minutes)
python 03_download_papers.py
# Result: 105 PDFs downloaded (72% success rate)
```

**Result:**
1. 200+ papers found across 5 databases (Scopus, PubMed, arXiv, Scholar, IEEE)
2. Automatic deduplication and PubMed prioritization
3. Intelligent abstract-based filtering (keyword or AI)
4. 105 PDFs downloaded using 10+ strategies
5. Ready for screening in BibTeX/RIS/CSV format
6. Everything documented, logged, and reproducible

## Expected Outcomes

By the end of this book, you will be able to:

1. ✅ Formulate research questions suitable for systematic reviews
2. ✅ Construct complex search queries using boolean logic
3. ✅ Execute searches across multiple academic databases
4. ✅ Efficiently screen and categorize hundreds of papers
5. ✅ Extract and organize relevant information
6. ✅ Generate publication-ready bibliographies
7. ✅ Create reproducible, documented workflows
8. ✅ Follow PRISMA guidelines systematically

## Next Steps

Ready to set up your environment? Head to the **[Setup Guide](1_Setup)** to install the necessary tools and configure your workspace!

---

:::{admonition} Stay Updated
:class: tip
Systematic review methodology and automation tools are constantly evolving. Bookmark this book and check back for updates!
:::




