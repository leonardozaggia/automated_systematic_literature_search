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

# <i class="fa-solid fa-flask"></i> Additional Tools & Resources

Beyond Findpapers, several other tools can enhance your automated systematic review workflow. This section introduces complementary tools and resources.

## Tools Overview

::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item-card} 🔬 Paperscraper
**Focus:** Biomedical literature

**Databases:**
- PubMed/MEDLINE
- bioRxiv
- medRxiv
- chemRxiv

**Best for:** Life sciences, medical research, biological studies

[Documentation](https://github.com/PhosphorylatedRabbits/paperscraper)
:::

:::{grid-item-card} 📚 Metapub
**Focus:** PubMed integration

**Features:**
- PubMed E-utilities wrapper
- Fetch article metadata
- Citation management
- Batch processing

**Best for:** Deep PubMed searches, MEDLINE data extraction

[Documentation](https://github.com/metapub/metapub)
:::

:::{grid-item-card} 🧬 Biopython
**Focus:** Biological databases

**Features:**
- NCBI Entrez utilities
- Sequence analysis
- Literature access via Bio.Entrez

**Best for:** Bioinformatics, genomics, molecular biology research

[Documentation](https://biopython.org/)
:::

:::{grid-item-card} 📊 ASReview
**Focus:** Active learning screening

**Features:**
- AI-assisted screening
- Interactive interface
- Machine learning prioritization

**Best for:** Large literature sets requiring intelligent prioritization

[Website](https://asreview.nl/)
:::

::::

---

## Paperscraper: Quick Start

### Installation

```bash
pip install paperscraper
```

### Basic Usage

```python
from paperscraper import get_papers

# Search PubMed
papers = get_papers(
    query="machine learning cancer",
    database="pubmed",
    max_results=100
)

# Display results
for paper in papers:
    print(f"{paper['title']}\n{paper['authors']}\n")
```

### Advantages of Paperscraper

✅ **Focused on biomedical research**  
✅ **Access to preprint servers**  
✅ **Clean, Pythonic API**  
✅ **Good for programmatic workflows**

### When to Use Paperscraper vs Findpapers

| Use Case | Recommended Tool |
|----------|-----------------|
| Multi-discipline search (CS, Engineering, Medicine) | **Findpapers** |
| Biomedical/life sciences only | **Paperscraper** or **Findpapers** |
| Need interactive refinement UI | **Findpapers** |
| Fully programmatic workflow | **Paperscraper** |
| Scopus/IEEE/ACM required | **Findpapers** |
| Need preprints (bioRxiv, medRxiv) | **Both** |

---

## Combining Tools

You can use multiple tools in your workflow:

### Example: Comprehensive Search Strategy

```python
# Step 1: Findpapers for broad multi-database search
# (Use command line as shown in tutorial)

# Step 2: Paperscraper for deep PubMed dive
from paperscraper import get_papers

additional_papers = get_papers(
    query="(machine learning OR deep learning) AND (mental health OR psychiatry)",
    database="pubmed",
    max_results=500
)

# Step 3: Merge results
# (Remove duplicates by DOI comparison)

# Step 4: Continue with Findpapers refine command
```

---

## Other Useful Resources

### Reference Management

**Zotero**
- Open-source reference manager
- Browser extensions for easy capture
- Integration with Word/LibreOffice
- [Website](https://www.zotero.org/)

**Mendeley**
- Reference manager with PDF annotation
- Institutional access to papers
- Collaboration features
- [Website](https://www.mendeley.com/)

### Screening & Review Management

**Rayyan**
- Web-based screening tool
- Collaboration features
- Mobile app available
- [Website](https://rayyan.ai/)

**Covidence**
- Systematic review management platform
- PRISMA compliance
- Team collaboration
- [Website](https://www.covidence.org/)

### Data Extraction

**REDCap**
- Research data capture platform
- Custom data extraction forms
- Secure and compliant
- [Website](https://projectredcap.org/)

### Meta-Analysis Software

**R packages:**
- `metafor`: Comprehensive meta-analysis
- `meta`: User-friendly meta-analysis
- `robvis`: Risk of bias visualization

**Python packages:**
- `meta`: Meta-analysis toolkit
- `statsmodels`: Statistical models

---

## Comparison Matrix

| Feature | Findpapers | Paperscraper | ASReview | Rayyan | Covidence |
|---------|-----------|--------------|----------|--------|-----------|
| **Free** | ✅ | ✅ | ✅ | Limited | ❌ |
| **Open Source** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Multi-database** | ✅ | Limited | Import | Import | Import |
| **Auto-download PDFs** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Interactive screening** | ✅ | ❌ | ✅ | ✅ | ✅ |
| **Collaboration** | ❌ | ❌ | ✅ | ✅ | ✅ |
| **AI-assisted** | ❌ | ❌ | ✅ | ✅ | ✅ |
| **Offline capable** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **BibTeX export** | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## Choosing Your Stack

### Minimal Stack (Solo Researcher)
```
Findpapers → Python analysis → BibTeX → LaTeX/Word
```

### Enhanced Stack (Small Team)
```
Findpapers → Rayyan (screening) → REDCap (extraction) → R (meta-analysis)
```

### Full Stack (Large Project)
```
Findpapers + Paperscraper → ASReview → Covidence → R/Python → Manuscript
```

---

## Best Practices

1. **Use Findpapers for initial search**
   - Comprehensive multi-database coverage
   - Automated deduplication
   - Download capabilities

2. **Supplement with specialized tools**
   - Paperscraper for biomedical deep dives
   - ASReview for large result sets
   - Rayyan for team collaboration

3. **Maintain consistency**
   - Document which tools you use
   - Keep version numbers
   - Save search configurations

4. **Stay open-source when possible**
   - Better reproducibility
   - No licensing issues
   - Community support

---

## Further Learning

### Tutorials & Courses

- **Cochrane Interactive Learning**: Free systematic review training
- **PRISMA Website**: Guidelines and checklists
- **YouTube**: Search for "systematic review tutorials"

### Communities

- **r/AskAcademia**: General academic advice
- **Twitter #SystematicReview**: Latest discussions
- **ResearchGate**: Q&A with researchers

### Books

- *Systematic Reviews in Health Research* (Egger et al.)
- *Introduction to Meta-Analysis* (Borenstein et al.)
- *Doing Meta-Analysis with R* (Harrer et al.) - Free online

---

## Summary

This section introduced complementary tools to enhance your automated systematic review workflow:

- **Paperscraper**: Biomedical literature specialization
- **ASReview**: AI-assisted screening
- **Rayyan/Covidence**: Collaboration platforms
- **R/Python packages**: Meta-analysis capabilities

Choose tools based on:
- Your discipline
- Team size
- Budget
- Technical comfort level
- Reproducibility requirements

:::{admonition} Recommendation
:class: tip
For most researchers, **Findpapers + Python/R** provides an excellent balance of power, flexibility, and reproducibility. Add specialized tools as needed for your specific use case.
:::

---

**Ready to put everything together?** Check out the [Complete Workflow](../workflow/0_end_to_end) chapter!


