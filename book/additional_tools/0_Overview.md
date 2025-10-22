# 🛠️ More tools
Beyond the primary tools covered in this guide (Review Buddy and Findpapers), there are several excellent complementary tools that can enhance your literature review workflow. This section provides brief tutorials for:

## 📚 Tools Covered

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} 🔍 PaperScraper
:link: 1_PaperScraper
:link-type: doc

Python library for scraping papers from arXiv, medRxiv, bioRxiv, and PubMed
:::

:::{grid-item-card} 🗺️ LitMaps
:link: 2_LitMaps
:link-type: doc

Visual citation mapping tool for discovering related papers
:::

:::{grid-item-card} 💡 Consensus
:link: 3_Consensus
:link-type: doc

AI-powered search engine for finding scientific consensus
:::

:::{grid-item-card} 🤖 Elicit
:link: 4_Elicit
:link-type: doc

AI research assistant for literature review automation
:::

::::

## Tool Selection Guide

Different tools excel at different stages of the literature review process:

```{mermaid}
graph TD
    A[Research Question] --> B{Search Strategy}
    B -->|Programmatic| C[Review Buddy]
    B -->|Configuration| D[Findpapers]
    B -->|Preprints| E[PaperScraper]
    
    C --> F{Discovery Phase}
    D --> F
    E --> F
    
    F -->|Find Related Papers| G[LitMaps]
    F -->|Check Consensus| H[Consensus]
    F -->|AI Analysis| I[Elicit]
    
    G --> J[Final Paper Set]
    H --> J
    I --> J
    
    style C fill:#e3f2fd
    style D fill:#e3f2fd
    style E fill:#e3f2fd
    style G fill:#fff3e0
    style H fill:#fff3e0
    style I fill:#fff3e0
    style J fill:#e8f5e9
```

## Complementary Workflows

These tools work best when combined with your primary search strategy:

### Workflow 1: Comprehensive Discovery
1. **Initial Search**: Use Review Buddy or Findpapers for systematic database searches
2. **Citation Mapping**: Upload key papers to LitMaps to discover related work
3. **Validation**: Check scientific consensus with Consensus

### Workflow 2: Preprint-Focused Research
1. **Preprint Search**: Use PaperScraper for latest research from arXiv/bioRxiv
2. **AI Analysis**: Use Elicit to extract key findings from large paper sets
3. **Integration**: Combine with peer-reviewed papers from Review Buddy

### Workflow 3: AI-Assisted Review
1. **Broad Search**: Initial search with Findpapers across multiple databases
2. **AI Screening**: Use Elicit to help screen and categorize papers
3. **Network Analysis**: Use LitMaps to ensure comprehensive coverage

## Quick Comparison

| Tool | Best For | Access | Cost |
|------|----------|--------|------|
| **Review Buddy** | Programmatic control | Python API | Free |
| **Findpapers** | Multi-database search | CLI/Python | Free |
| **PaperScraper** | Preprint archives | Python | Free |
| **LitMaps** | Citation networks | Web App | Freemium |
| **Consensus** | Finding consensus | Web App | Freemium |
| **Elicit** | AI-powered analysis | Web App | Freemium |

---

:::{admonition} Note
:class: tip
Each tool in this section includes practical examples and screenshots to help you get started quickly!
:::
