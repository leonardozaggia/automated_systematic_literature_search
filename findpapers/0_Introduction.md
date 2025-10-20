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

# <i class="fa-solid fa-magnifying-glass"></i> Findpapers Overview

## What is Findpapers?

**Findpapers** is a powerful Python application designed to help researchers conduct systematic literature searches across multiple academic databases simultaneously. It's specifically built for systematic reviews and metanalyses, automating many of the tedious tasks involved in literature discovery.

## Key Features

::::{grid} 1 1 2 3
:gutter: 2

:::{grid-item-card} 🔍 Multi-Database Search
Search 7+ databases at once:
- ACM Digital Library
- IEEE Xplore
- Scopus
- PubMed
- arXiv
- bioRxiv
- medRxiv
:::

:::{grid-item-card} 🎯 Advanced Queries
- Boolean operators (AND, OR, NOT)
- Wildcards (*, ?)
- Nested subqueries
- Field-specific searches
:::

:::{grid-item-card} ♻️ Auto-Deduplication
Automatically identifies and merges duplicate papers found across multiple databases
:::

:::{grid-item-card} 🎨 Interactive Refinement
Terminal-based UI for:
- Screening papers
- Categorizing results
- Highlighting keywords
- Making selections
:::

:::{grid-item-card} 📥 PDF Download
Automatic full-text download with:
- Proxy support
- Error logging
- Resume capability
:::

:::{grid-item-card} 📚 BibTeX Export
Generate publication-ready bibliographies with customizable formatting
:::

::::

## The Findpapers Workflow

Findpapers follows a four-step process that aligns with systematic review best practices:

```{mermaid}
graph LR
    A[1. SEARCH<br/>Multi-database query] --> B[2. REFINE<br/>Screen & categorize]
    B --> C[3. DOWNLOAD<br/>Get full-text PDFs]
    C --> D[4. BIBTEX<br/>Generate bibliography]
    
    style A fill:#e3f2fd
    style B fill:#fff3e0
    style C fill:#e8f5e9
    style D fill:#f3e5f5
```

### 1. Search Command

Execute searches across multiple databases with a single command:

```bash
findpapers search results.json --query "[machine learning] AND [healthcare]"
```

### 2. Refine Command

Interactively screen, categorize, and select relevant papers:

```bash
findpapers refine results.json --abstract --extra-info
```

### 3. Download Command

Download full-text PDFs of selected papers:

```bash
findpapers download results.json ./papers/ --selected
```

### 4. BibTeX Command

Generate bibliography files:

```bash
findpapers bibtex results.json references.bib --selected
```

## Why Use Findpapers?

### Compared to Manual Searching

| Task | Manual Approach | Findpapers |
|------|----------------|------------|
| Search 5 databases | 2-3 hours | 5-10 minutes |
| Remove duplicates | 1-2 hours | Automatic |
| Track decisions | Spreadsheets | Built-in JSON |
| Download PDFs | One by one | Batch process |
| Generate BibTeX | Manual entry | One command |
| Reproducibility | Difficult | Fully documented |

### Compared to Other Tools

| Feature | Findpapers | Rayyan | Covidence | Zotero |
|---------|-----------|--------|-----------|--------|
| **Free & Open Source** | ✅ | Limited | ❌ | ✅ |
| **Multi-database** | ✅ | Manual import | Manual import | Manual |
| **Automation** | ✅ | ❌ | ❌ | Limited |
| **Reproducibility** | ✅ | Limited | Limited | ❌ |
| **Offline capable** | ✅ | ❌ | ❌ | ✅ |
| **Customizable** | ✅ | ❌ | ❌ | Limited |

## Databases Covered

### Academic Databases

**ACM Digital Library**
- Focus: Computer science, information technology
- Coverage: Conference proceedings, journals, magazines
- API Key: Not required

**IEEE Xplore**
- Focus: Electrical engineering, computer science, electronics
- Coverage: Journals, conferences, standards
- API Key: Required for full access

**Scopus**
- Focus: Multidisciplinary
- Coverage: Peer-reviewed journals, conference papers, books
- API Key: Required (institutional access)

### Medical & Life Sciences

**PubMed**
- Focus: Biomedical and life sciences
- Coverage: MEDLINE database, medical journals
- API Key: Not required (optional for higher rate limits)

**bioRxiv & medRxiv**
- Focus: Biology and medical preprints
- Coverage: Unpublished manuscripts, preprints
- API Key: Not required

### Preprint Servers

**arXiv**
- Focus: Physics, mathematics, computer science, quantitative biology
- Coverage: Preprints and e-prints
- API Key: Not required

## What You'll Learn

In the next section, you'll learn how to:

✅ Construct complex search queries  
✅ Execute searches across multiple databases  
✅ Handle API keys and authentication  
✅ Refine and categorize search results  
✅ Download papers efficiently  
✅ Generate bibliographies  
✅ Create reproducible workflows  

## Prerequisites

Before proceeding, make sure you have:

- ✅ Completed the [Setup Guide](../introduction/1_Setup)
- ✅ Findpapers installed and working (`findpapers version`)
- ✅ Basic understanding of systematic reviews
- ✅ A research question in mind

:::{admonition} Ready to Start?
:class: tip
Continue to the [Findpapers Demo](1_demo_findpapers) for hands-on examples and tutorials!
:::

## Additional Resources

- 📖 [Official Documentation](https://github.com/jonatasgrosman/findpapers)
- 🐛 [Report Issues](https://github.com/jonatasgrosman/findpapers/issues)
- 💡 [Feature Requests](https://github.com/jonatasgrosman/findpapers/discussions)
- 📄 [Research Paper](https://github.com/jonatasgrosman/findpapers#citation)

---

:::{admonition} Pro Tip
:class: note
Findpapers stores all search results in a single JSON file, making your research fully reproducible and easy to share with collaborators!
:::