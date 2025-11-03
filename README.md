# Automated Metanalysis & Systematic Reviews (AMSR)

[![Jupyter Book Badge](https://jupyterbook.org/_static/badge.svg)](https://leonardozaggia.github.io/automated_systematic_literature_search/)

A comprehensive tutorial book teaching researchers how to automate systematic literature reviews and metanalyses using modern Python tools.

## 📚 What's This Book About?

This interactive book guides you through conducting **automated systematic reviews** and **metanalyses** using powerful tools like **Findpapers**. Learn to:

- 🔍 Search multiple academic databases simultaneously (ACM, IEEE, Scopus, PubMed, arXiv, bioRxiv, medRxiv)
- 🤖 Automate paper collection and deduplication
- 📊 Streamline screening and categorization processes
- 📥 Download full-text papers automatically
- 📖 Generate publication-ready bibliographies
- ♻️ Create reproducible, documented research workflows

## 🎯 Who Is This For?

- Researchers conducting systematic literature reviews
- Graduate students working on thesis/dissertation literature reviews
- Anyone performing metanalyses
- Research teams wanting reproducible workflows
- Librarians supporting systematic review services

## 📖 Online Access (Recommended)

The book is best viewed online via GitHub Pages: 

👉 **[View the Book](https://leonardozaggia.github.io/automated_systematic_literature_search/)**

## 🚀 Quick Start

```bash
# Install the main tool
pip install findpapers

# Run your first search
findpapers search results.json --query "[machine learning] AND [healthcare]"
```

## 📑 Book Contents

### Part 1: Getting Started
- **Introduction**: Understanding systematic reviews and metanalysis
- **Setup Guide**: Installing tools and configuring your environment

### Part 2: Findpapers Tutorial
- **Overview**: Understanding the Findpapers workflow
- **Complete Tutorial**: Hands-on examples from search to bibliography generation

### Part 3: Additional Tools
- **Paperscraper**: Biomedical literature automation
- Other complementary tools

### Part 4: Complete Workflow
- **End-to-End Guide**: PRISMA-aligned workflow from research question to publication

## 💻 Local Development

To build and view the book locally:

```bash
# Clone the repository
git clone https://github.com/leonardozaggia/automated_systematic_literature_search.git
cd automated_systematic_literature_search

# Create environment
conda create -n amsr python=3.10 -y
conda activate amsr

# Install dependencies
pip install -r requirements.txt

# Build the book
jupyter-book build .

# View in browser
# Open _build/html/index.html in your browser
```

## 🤝 Contributing

Contributions are welcome! Whether it's:
- Fixing typos or errors
- Improving explanations
- Adding new examples
- Suggesting new tools or techniques

Please feel free to open an issue or submit a pull request.

## 📄 License

This book is licensed under a Creative Commons Attribution 4.0 International License (CC BY 4.0).

## 🙏 Acknowledgments

- **Findpapers** by [Jonatas Grosman](https://github.com/jonatasgrosman/findpapers)
- **Jupyter Book** for the excellent documentation framework
- All contributors and users who help improve this resource

## 📧 Contact

Created by Leonardo Zaggia

For questions, suggestions, or feedback, please open an issue on GitHub.

---

⭐ **Star this repository if you find it useful!**

