# Findpapers

## What is Findpapers?

**Findpapers** is a Python command-line application for conducting systematic literature searches across multiple academic databases. It provides a configuration-based alternative to Review Buddy, ideal for researchers who prefer YAML configuration over Python scripting.

## Key Features

- **7+ Database Search**: ACM, IEEE, Scopus, PubMed, arXiv, bioRxiv, medRxiv
- **Boolean Query Support**: AND, OR, NOT operators with wildcards
- **Interactive Refinement**: Terminal-based screening and categorization
- **Auto-Deduplication**: Automatic duplicate detection across sources
- **PDF Download**: Batch download with proxy support
- **BibTeX Export**: Generate publication-ready bibliographies

## Installation

```bash
# Install via pip
pip install findpapers

# Verify installation
findpapers version
```

## Quick Start

Findpapers follows a simple 4-step workflow:

```bash
# 1. Search databases
findpapers search results.json --query "[machine learning] AND [healthcare]"

# 2. Refine results interactively
findpapers refine results.json --abstract

# 3. Download PDFs
findpapers download results.json ./papers/ --selected

# 4. Generate bibliography
findpapers bibtex results.json references.bib --selected
```

## Query Syntax

### Basic Rules

- **Terms in brackets**: `[machine learning]`
- **Operators UPPERCASE**: `AND`, `OR`, `NOT`
- **Wildcards**: `*` (multiple chars), `?` (single char)
- **Grouping**: Use parentheses for complex queries

### Examples

```bash
# Simple query
findpapers search results.json --query "[artificial intelligence]"

# Boolean logic
findpapers search results.json --query "([AI] OR [ML]) AND [healthcare]"

# Wildcards
findpapers search results.json --query "[predict*] AND [climate]"

# Exclusion
findpapers search results.json --query "[AI] AND [diagnosis] AND NOT [review]"

# Complex query
findpapers search results.json --query "([deep learning] OR [neural network*]) AND ([medical] OR [clinical]) AND NOT ([review] OR [survey])"
```

## Advanced Usage

### Date Range Filtering

```bash
findpapers search results.json \
  --query "[AI] AND [climate]" \
  --since 2020-01-01 \
  --until 2024-12-31
```

### Database Selection

```bash
# Specific databases only
findpapers search results.json \
  --query "[machine learning]" \
  --databases "scopus,ieee,pubmed"
```

### With API Keys

```bash
# Set environment variables
export SCOPUS_TOKEN="your_scopus_api_key"
export IEEE_TOKEN="your_ieee_api_key"

# Run search with authentication
findpapers search results.json \
  --query "[AI] AND [healthcare]" \
  --databases "scopus,ieee,pubmed,arxiv"
```

### Interactive Refinement

```bash
# Basic refinement
findpapers refine results.json

# With abstracts and categories
findpapers refine results.json \
  --abstract \
  --categories "Study Type:Empirical,Review,Methodology;AI Method:Deep Learning,Machine Learning,NLP"
```

**Refinement Actions:**
- `s` = Select paper
- `r` = Remove paper
- `n` = Next paper
- `p` = Previous paper
- `q` = Quit and save

### Download with Proxy

```bash
findpapers download results.json ./papers/ \
  --selected \
  --proxy "http://username:password@proxy.university.edu:8080"
```

## Programmatic Usage (Python API)

For automation workflows, Findpapers can be used as a Python library:

```python
import findpapers
import datetime

# Execute search
findpapers.search(
    outputpath="results.json",
    query="([AI] OR [machine learning]) AND [healthcare]",
    since=datetime.date(2020, 1, 1),
    databases=["pubmed", "arxiv", "scopus"],
    limit_per_database=50
)

# Refine results
findpapers.refine(
    search_path="results.json",
    categories={
        "Study Type": ["Empirical", "Review"],
        "AI Method": ["Deep Learning", "ML"]
    },
    show_abstract=True
)

# Download papers
findpapers.download(
    search_path="results.json",
    output_directory="./papers/",
    only_selected_papers=True
)

# Generate bibliography
findpapers.generate_bibtex(
    search_path="results.json",
    outputpath="references.bib",
    only_selected_papers=True
)
```

## When to Use Findpapers vs Review Buddy

| Feature | Findpapers | Review Buddy |
|---------|-----------|--------------|
| **Workflow** | 4 commands (CLI) | 3 Python scripts |
| **Configuration** | Command-line flags | Edit scripts directly |
| **Filtering** | Interactive only | Keyword + AI options |
| **Databases** | 7 sources | 5 sources |
| **Best For** | Quick searches | Systematic reviews |
| **Learning Curve** | Easy (CLI) | Easy (Python scripts) |
| **Customization** | Limited | Highly customizable |

**Use Findpapers if:**
- You prefer command-line tools
- You need quick, one-off searches
- You want minimal configuration
- You're searching 7+ databases

**Use Review Buddy if:**
- You're conducting systematic reviews
- You need advanced filtering (AI-powered)
- You want more control over the workflow
- You need better PDF download success rates

## Supported Databases

### Academic Databases

**ACM Digital Library**
- Computer science, IT
- No API key required

**IEEE Xplore**
- Engineering, computer science
- API key required (free tier available)

**Scopus**
- Multidisciplinary
- API key required (institutional access)

### Medical & Life Sciences

**PubMed**
- Biomedical sciences
- No API key required

**bioRxiv & medRxiv**
- Biology and medical preprints
- No API key required

### Preprints

**arXiv**
- Physics, math, CS, biology
- No API key required

## Tips & Best Practices

### Query Construction

✅ **Start broad, refine iteratively**
```bash
# First search
findpapers search results.json --query "[AI] AND [healthcare]"

# Review results, then refine query
findpapers search results_v2.json --query "([AI] OR [ML]) AND ([diagnosis] OR [treatment])"
```

✅ **Use wildcards wisely**
```bash
# Good: Captures variations
--query "[predict*]"  # matches: predict, prediction, predictive

# Avoid: Too broad
--query "[AI*]"  # matches too many irrelevant terms
```

✅ **Exclude unwanted content**
```bash
--query "[AI] AND [healthcare] AND NOT ([review] OR [survey])"
```

### Refinement Strategy

1. **First pass**: Quick title screening
2. **Second pass**: Abstract review for selected papers
3. **Third pass**: Categorization and final selection

### Download Success

- Use institutional proxy when available
- Check `download.log` for failed papers
- Try alternative sources for paywalled papers
- Consider Sci-Hub as last resort (check local laws)

## Resources

- **Documentation**: [github.com/jonatasgrosman/findpapers](https://github.com/jonatasgrosman/findpapers)
- **Issues**: [Report bugs](https://github.com/jonatasgrosman/findpapers/issues)
- **Citation**: [Research paper](https://github.com/jonatasgrosman/findpapers#citation)

## Common Issues

### "Invalid query syntax"
- Ensure terms are in brackets: `[term]`
- Use UPPERCASE operators: `AND`, `OR`, `NOT`
- Add spaces around operators

### "No results found"
- Broaden your query
- Check date range is reasonable
- Verify API keys for Scopus/IEEE

### "Download failed (403)"
- Paper is behind paywall
- Try institutional proxy
- Use VPN if on campus network

### "API key invalid"
```bash
# Verify environment variable is set
echo $SCOPUS_TOKEN

# Re-export if needed
export SCOPUS_TOKEN="your-key-here"
```

---

**For more comprehensive systematic review workflows with advanced filtering, see [Review Buddy](0_Overview).**
