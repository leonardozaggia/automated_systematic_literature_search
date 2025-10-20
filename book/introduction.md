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

# Welcome to Automated Metanalysis & Systematic Reviews!

This comprehensive tutorial teaches you how to **automate your literature review process** using modern Python tools. Whether you're conducting a systematic review, metanalysis, or comprehensive literature search for your research, this book will guide you through efficient, reproducible workflows that save time and improve accuracy.

## Why Automate Your Literature Review?

📚 **Systematic reviews** and **metanalyses** are essential for evidence-based research, but they're traditionally time-consuming and error-prone. This book teaches you to:

- **Search multiple databases simultaneously** (ACM, IEEE, Scopus, PubMed, arXiv, bioRxiv, medRxiv)
- **Automate paper collection and deduplication**
- **Streamline screening and selection processes**
- **Generate publication-ready bibliographies**
- **Create reproducible research workflows**
- **Reduce manual errors and bias**

## What You'll Learn

This book covers everything from basic setup to advanced automation techniques, including:

✅ Building complex search queries across multiple databases  
✅ Refining and categorizing search results efficiently  
✅ Downloading full-text papers automatically  
✅ Managing references and generating BibTeX files  
✅ Creating reproducible, documented workflows  
✅ Following PRISMA guidelines for systematic reviews

::::{grid} 1 1 2 3
:class-container: text-center
:gutter: 3

:::{grid-item-card}
:class-body: text-center
:class-header: bg-light text-center
:link: ./introduction/0_Introduction
:link-type: doc
**Getting Started** 🚀
^^^
```{image} ../_static/images/get_started.png
:height: 100
```

Learn what systematic reviews and metanalyses are, why automation matters, and set up your environment.
+++
Start here {fas}`arrow-right`
:::

:::{grid-item-card}
:class-body: text-center
:class-header: bg-light text-center
:link: ./findpapers/0_Introduction
:link-type: doc
**Findpapers Tutorial** �
^^^
```{image} ../_static/images/findpaper.png
:height: 100
```

Master the powerful Findpapers tool for searching, refining, and managing literature across multiple databases.
+++
Explore tutorial {fas}`arrow-right`
:::

:::{grid-item-card}
:class-body: text-center
:class-header: bg-light text-center
:link: ./AMSR/paperscraper/0_Introduction
:link-type: doc
**Additional Tools** �️
^^^
```{image} ../_static/images/other_tools.png
:height: 100
```

Discover complementary tools and advanced techniques for comprehensive literature analysis.
+++
Explore tools {fas}`arrow-right`
:::

::::

## Quick Start

```bash
# Install the main tool
pip install findpapers

# Run your first search
findpapers search results.json --query "[machine learning] AND [healthcare]"
```

---

### Useful Resources
- 📖 [PRISMA Guidelines](http://www.prisma-statement.org/) - Standards for systematic reviews
- 💾 [Findpapers Repository](https://github.com/jonatasgrosman/findpapers) - Original tool repository
- 🎓 [Getting Started with Python & VS Code](https://www.youtube.com/watch?v=6i3e-j3wSf0)
- 🔬 [PMUS Lab GitHub](https://github.com/pmus-lab)

:::{admonition} New to systematic reviews?
:class: tip
Start with the [Introduction section](./introduction/0_Introduction) to understand the fundamentals before diving into the tools!
:::

---

**Ready to revolutionize your literature review process?** Let's get started! 🎯

