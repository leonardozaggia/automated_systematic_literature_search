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
graph TD
    A[1. Define Research Question] --> B[2. Develop Protocol]
    B --> C[3. Literature Search]
    C --> D[4. Screen Titles/Abstracts]
    D --> E[5. Full-Text Review]
    E --> F[6. Data Extraction]
    F --> G[7. Quality Assessment]
    G --> H[8. Data Synthesis]
    H --> I[9. Report Results]
    
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

🚀 **Speed**: Search multiple databases simultaneously  
🎯 **Accuracy**: Consistent application of inclusion/exclusion criteria  
♻️ **Reproducibility**: Document and share exact search parameters  
🔍 **Comprehensiveness**: Ensure no relevant papers are missed  
📊 **Organization**: Systematic tracking of decisions and classifications  
⚡ **Efficiency**: Free up time for critical thinking and analysis

## Tools Overview

This book focuses on several powerful Python tools:

### 1. **Findpapers** (Primary Tool)
- Searches 7+ databases simultaneously
- Advanced query building with boolean logic
- Built-in refinement and categorization
- Automatic deduplication
- PDF download capabilities

### 2. **Paperscraper**
- Focused on biomedical literature
- Integration with PubMed, medRxiv, bioRxiv
- Clean API for programmatic access

### 3. **Supporting Tools**
- **Pandas**: Data manipulation and analysis
- **Jupyter**: Interactive documentation
- **BibTeX tools**: Reference management

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

Let's say you want to conduct a systematic review on **"Machine Learning Applications in Mental Health Diagnosis"**. Here's how automation helps:

**Without Automation:**
- 🕐 Manually search PubMed, Scopus, IEEE, ACM (2-3 days)
- 🕐 Export results from each database separately (3-4 hours)
- 🕐 Manually remove duplicates in Excel (4-6 hours)
- 🕐 Screen 500+ titles/abstracts manually (2-3 weeks)
- 🕐 Track everything in spreadsheets (ongoing confusion)

**With Automation (This Book):**
- ⚡ Single search command across all databases (30 minutes)
- ⚡ Automatic deduplication (instant)
- ⚡ Interactive screening with categorization (2-3 days)
- ⚡ Automatic BibTeX generation (instant)
- ⚡ Everything documented and reproducible

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




