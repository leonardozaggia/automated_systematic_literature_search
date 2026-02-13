# 🛠️ Additional Tools & Resources

Beyond Review Buddy (the primary toolkit featured in this book), there are several excellent complementary tools that can enhance your literature review workflow. This section provides practical guides for:

## 📚 Tools Covered

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} 🔍 Paper-Finder
:link: 1_Paper_Finder
:link-type: doc

GUI-based tool for discovering and searching papers across multiple databases
:::

:::{grid-item-card} 📊 Info-Extractor
:link: 5_Info_Extractor
:link-type: doc

Extract information from papers in a structured way for systematic analysis
:::

:::{grid-item-card} ️🗺️ LitMaps
:link: 2_LitMaps
:link-type: doc

Visual citation mapping tool for discovering related papers through citation networks
:::

:::{grid-item-card} 💡 Consensus
:link: 3_Consensus
:link-type: doc

AI-powered search engine for finding scientific consensus across research papers
:::

:::{grid-item-card} 🤖 Elicit
:link: 4_Elicit
:link-type: doc

AI research assistant for literature review automation and data extraction
:::
::::

## Tool Selection Guide

Different tools excel at different stages of the literature review process:

```{mermaid}
graph TD
    A[Research Question] --> B{Initial Search}
    B -->|GUI Tool| PF[Paper-Finder]
    B -->|Primary Tool| C[Review Buddy]
    
    PF --> F{Enhancement Phase}
    C --> F
    
    F -->|Citation Discovery| G[LitMaps]
    F -->|Check Consensus| H[Consensus]
    F -->|AI Analysis| I[Elicit]
    
    G --> J[Complete Paper Set]
    H --> J
    I --> J
    
    J --> K[Info-Extractor]
    K --> L[Structured Data]
    
    style PF fill:#e1f5fe
    style C fill:#e3f2fd
    style G fill:#fff3e0
    style H fill:#fff3e0
    style I fill:#fff3e0
    style J fill:#e8f5e9
    style K fill:#f3e5f5
    style L fill:#f1f8e9
```

## Complementary Workflows

These tools work best when combined with Review Buddy:

### Workflow 1: Comprehensive Discovery
1. **Initial Search**: Use Review Buddy for systematic 5-database search
2. **Citation Mapping**: Upload key papers to LitMaps to discover related work
3. **Validation**: Check scientific consensus with Consensus

### Workflow 2: Preprint-Focused Research
1. **Preprint Search**: Use PaperScraper for latest research from arXiv/bioRxiv
2. **AI Analysis**: Use Elicit to extract key findings from large paper sets
3. **Integration**: Combine with peer-reviewed papers from Review Buddy

### Workflow 3: AI-Assisted Review
1. **Broad Search**: Use Review Buddy with AI-powered filtering
2. **AI Screening**: Use Elicit for additional screening and categorization
3. **Network Analysis**: Use LitMaps to ensure comprehensive coverage

## Quick Comparison

| Tool | Type | Best For | Access | Cost |
|------|------|----------|--------|------|
| **Review Buddy** | Python Scripts | Systematic reviews, advanced filtering | Local | Free |
| **LitMaps** | Web App | Citation network discovery | Web | Freemium |
| **Consensus** | Web App | Finding scientific consensus | Web | Freemium |
| **Elicit** | Web App | AI-powered screening & extraction | Web | Freemium |

---

:::{admonition} Recommended Approach
:class: tip
Start with **Review Buddy** as your primary tool, then enhance your workflow with these complementary tools as needed!
:::
