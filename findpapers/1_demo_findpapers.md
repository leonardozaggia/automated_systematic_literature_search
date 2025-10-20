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

# <i class="fa-solid fa-laptop-code"></i> Findpapers Complete Tutorial

This comprehensive tutorial will walk you through a complete systematic literature search using Findpapers, from query construction to final bibliography generation.

## Learning Objectives

By the end of this tutorial, you will be able to:
- ✅ Construct sophisticated search queries
- ✅ Execute multi-database searches
- ✅ Refine and categorize results
- ✅ Download full-text papers
- ✅ Generate BibTeX bibliographies

## Tutorial Scenario

**Research Question:** *"What are the applications of artificial intelligence in climate change prediction and mitigation?"*

Let's work through this systematically!

---

## Part 1: Understanding Search Queries

### Query Construction Rules

Findpapers uses a specific syntax for building search queries:

#### ✅ Valid Query Rules

1. **Terms must be in square brackets**: `[artificial intelligence]`
2. **Boolean operators must be UPPERCASE**: `AND`, `OR`, `NOT`
3. **Operators need whitespace**: `[term a] AND [term b]` ✅ not `[term a]AND[term b]` ❌
4. **NOT must follow AND**: `[term a] AND NOT [term b]` ✅
5. **Parentheses for subqueries**: `([term a] OR [term b]) AND [term c]`

#### Wildcards

- **`?`** = exactly one character: `[clim?te]` matches "climate"
- **`*`** = zero or more characters: `[climat*]` matches "climate", "climatic", "climatology"

**Wildcard Rules:**
- ❌ Cannot start with wildcard: `[*climate]` 
- ✅ Minimum 3 characters before `*`: `[cli*]`
- ✅ `*` only at end: `[climat*]`
- ✅ Single terms only: `[AI*]` not `[artificial intelligence*]`
- ✅ One wildcard per term: `[clim?te]` not `[cl?m?te]`

### Query Examples

::::{grid} 1 1 1 2
:gutter: 2

:::{grid-item-card} ✅ Valid Queries
```
[machine learning]

[AI] OR [artificial intelligence]

[climate] AND [prediction]

[deep learning] AND NOT [review]

([AI] OR [ML]) AND [climate change]

[predict*]
```
:::

:::{grid-item-card} ❌ Invalid Queries
```
machine learning
(missing brackets)

[ai] or [ml]
(lowercase operator)

[AI]AND[ML]
(no whitespace)

[AI] NOT [review]
(NOT without AND)

[*predict]
(wildcard at start)
```
:::

::::

### Building Our Query

For our research question about AI in climate change, let's build a query step by step:

**Step 1:** Define AI-related terms
```
[artificial intelligence] OR [AI] OR [machine learning] OR [ML] OR [deep learning]
```

**Step 2:** Define climate-related terms
```
[climate change] OR [climate] OR [global warming] OR [greenhouse]
```

**Step 3:** Define application terms
```
[predict*] OR [forecast*] OR [mitigat*] OR [model*]
```

**Step 4:** Combine with AND logic
```
([artificial intelligence] OR [AI] OR [machine learning] OR [ML] OR [deep learning]) 
AND 
([climate change] OR [climate] OR [global warming] OR [greenhouse])
AND
([predict*] OR [forecast*] OR [mitigat*] OR [model*])
```

**Step 5:** Exclude unwanted topics
```
([artificial intelligence] OR [AI] OR [machine learning] OR [ML] OR [deep learning]) 
AND 
([climate change] OR [climate] OR [global warming] OR [greenhouse])
AND
([predict*] OR [forecast*] OR [mitigat*] OR [model*])
AND NOT
([review] OR [survey])
```

:::{admonition} Pro Tip: Use Query Files
:class: tip
Save complex queries in text files for better readability and version control!
:::

---

## Part 2: Executing Your First Search

### Basic Search Command

```bash
findpapers search results.json --query "[AI] AND [climate change]"
```

**What happens:**
- Searches all available databases
- Saves results to `results.json`
- Shows progress for each database
- Automatically removes duplicates

### Advanced Search with Options

Let's perform a more sophisticated search with our full query:

#### Option 1: Inline Query (Simple)

```bash
findpapers search climate_ai_search.json \
  --query "([AI] OR [machine learning]) AND [climate change]" \
  --since 2020-01-01 \
  --until 2024-12-31
```

#### Option 2: Query File (Recommended)

First, create a query file:

**query_climate_ai.txt:**
```
([artificial intelligence] OR [AI] OR [machine learning] OR [ML] OR [deep learning]) 
AND 
([climate change] OR [climate] OR [global warming] OR [greenhouse])
AND
([predict*] OR [forecast*] OR [mitigat*] OR [model*])
AND NOT
([review] OR [survey])
```

Then run the search:

```bash
findpapers search climate_ai_search.json \
  --query-file query_climate_ai.txt \
  --since 2020-01-01 \
  --until 2024-12-31 \
  --databases "scopus,ieee,acm,pubmed" \
  --publication-types "journal,conference proceedings" \
  --limit-db 50
```

### Understanding Search Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--query` | Inline search query | `"[AI] AND [climate]"` |
| `--query-file` | Path to query file | `query.txt` |
| `--since` | Start date (YYYY-MM-DD) | `2020-01-01` |
| `--until` | End date (YYYY-MM-DD) | `2024-12-31` |
| `--databases` | Comma-separated list | `"scopus,ieee,acm"` |
| `--publication-types` | Filter by type | `"journal,conference proceedings"` |
| `--limit` | Total papers limit | `100` |
| `--limit-db` | Limit per database | `50` |
| `--token-scopus` | Scopus API key | `$SCOPUS_TOKEN` |
| `--token-ieee` | IEEE API key | `$IEEE_TOKEN` |

### Search with API Keys

If you have API keys for Scopus and IEEE:

```bash
# Set environment variables (do this once per session)
export SCOPUS_TOKEN="your-scopus-api-key-here"
export IEEE_TOKEN="your-ieee-api-key-here"

# Run search with authentication
findpapers search climate_ai_search.json \
  --query-file query_climate_ai.txt \
  --token-scopus "$SCOPUS_TOKEN" \
  --token-ieee "$IEEE_TOKEN" \
  --since 2020-01-01 \
  --limit-db 50
```

### Understanding Search Output

During search, you'll see output like:

```
Searching papers...
- ACM: Found 23 papers
- IEEE: Found 45 papers (API key used)
- Scopus: Found 67 papers (API key used)
- arXiv: Found 34 papers
- PubMed: Found 12 papers

Removing duplicates...
Total unique papers: 147 (34 duplicates removed)

Results saved to: climate_ai_search.json
```

---

## Part 3: Refining Search Results

The refine command provides an interactive terminal interface for screening papers.

### Basic Refinement

```bash
findpapers refine climate_ai_search.json
```

This opens an interactive screen showing:
- Paper title
- Authors
- Publication year
- Abstract (if available)

**Actions:**
- `s` = Select this paper
- `r` = Remove this paper
- `n` = Next paper (no decision)
- `p` = Previous paper
- `q` = Quit and save

### Advanced Refinement with Categories

Let's add custom categories to organize our papers:

```bash
findpapers refine climate_ai_search.json \
  --selected \
  --abstract \
  --extra-info \
  --categories "Study Type:Empirical,Theoretical,Methodological,Review" \
  --categories "Application:Prediction,Mitigation,Adaptation,Monitoring" \
  --categories "AI Method:Deep Learning,Machine Learning,Neural Networks,Ensemble" \
  --highlights "climate,predict,model,accuracy,temperature,emissions"
```

**What each option does:**

| Option | Description |
|--------|-------------|
| `--selected` | Review only previously selected papers |
| `--removed` | Review only previously removed papers |
| `--abstract` | Show full abstract |
| `--extra-info` | Show citations, DOI, database source |
| `--categories` | Add custom classification categories |
| `--highlights` | Highlight specific keywords in abstract |
| `--list` | Just list papers without interactive mode |

### Understanding the Refine Interface

When you run refine with options, you'll see:

```
==================================================
Paper 1 of 147
==================================================

Title: Deep Learning for Climate Change Prediction: A Survey
Authors: Smith, J., Johnson, A., Williams, B.
Year: 2023
Publication: IEEE Transactions on Neural Networks
DOI: 10.1109/TNNLS.2023.12345

Paper found in: IEEE, Scopus
Citations: 45
Publication is potentially predatory: No

Abstract:
Climate change PREDICTION using deep learning has gained 
significant attention. This paper surveys recent advances in
neural network-based CLIMATE MODELS, achieving 95% ACCURACY
in temperature forecasting...

==================================================
Categories (use spacebar to select):
Study Type:
  [ ] Empirical
  [ ] Theoretical  
  [x] Methodological
  [ ] Review

Application:
  [x] Prediction
  [ ] Mitigation
  [ ] Adaptation
  [ ] Monitoring

AI Method:
  [x] Deep Learning
  [ ] Machine Learning
  [ ] Neural Networks
  [ ] Ensemble
==================================================

Actions: [s]elect | [r]emove | [n]ext | [p]rev | [q]uit
>
```

### Refinement Strategies

**First Pass:** Basic screening (title only)
```bash
findpapers refine climate_ai_search.json
```
- Quick elimination of obviously irrelevant papers
- Focus on title and publication year

**Second Pass:** Detailed review (selected papers with abstracts)
```bash
findpapers refine climate_ai_search.json --selected --abstract --extra-info
```
- Read abstracts carefully
- Check publication venue and citations
- Verify not from predatory publishers

**Third Pass:** Categorization
```bash
findpapers refine climate_ai_search.json \
  --selected \
  --abstract \
  --categories "Study Type:..." \
  --categories "Application:..."
```
- Organize papers by characteristics
- Prepare for systematic data extraction

### Listing Papers

View all selected papers without interactive mode:

```bash
findpapers refine climate_ai_search.json --selected --abstract --list
```

View all removed papers:

```bash
findpapers refine climate_ai_search.json --removed --list
```

---

## Part 4: Downloading Full-Text Papers

### Basic Download

Download all selected papers:

```bash
findpapers download climate_ai_search.json ./papers/ --selected
```

**What happens:**
- Creates `./papers/` directory
- Downloads PDFs with original filenames
- Creates `download.log` with success/failure records
- Shows progress bar

### Download with Filters

Download only papers with specific categories:

```bash
findpapers download climate_ai_search.json ./papers/ \
  --selected \
  --categories "Study Type:Empirical" \
  --categories "Application:Prediction"
```

### Download with Proxy (Institutional Access)

Many papers require institutional access. Use a proxy:

```bash
findpapers download climate_ai_search.json ./papers/ \
  --selected \
  --proxy "http://username:password@proxy.university.edu:8080"
```

:::{admonition} Proxy Configuration
:class: tip
Contact your institution's IT department for proxy settings. Common formats:
- `http://proxy.institution.edu:port`
- `http://username:password@proxy.institution.edu:port`
:::

### Understanding Download Results

After download completes, check the log file:

```bash
cat ./papers/download.log
```

You'll see:

```
✅ papers/smith2023_deep_learning_climate.pdf - Downloaded successfully
❌ papers/johnson2023_ai_climate.pdf - 403 Forbidden (paywall)
✅ papers/williams2023_neural_networks.pdf - Downloaded successfully
⚠️ papers/brown2023_climate_model.pdf - Timeout, retrying...
```

**Common download issues:**
- **403 Forbidden:** Paper behind paywall (try with proxy)
- **404 Not Found:** PDF URL not available
- **Timeout:** Network issues (re-run to resume)

---

## Part 5: Generating BibTeX Bibliography

### Basic BibTeX Generation

```bash
findpapers bibtex climate_ai_search.json references.bib --selected
```

Creates `references.bib` with entries like:

```bibtex
@article{Smith2023,
  title={Deep Learning for Climate Change Prediction: A Survey},
  author={Smith, John and Johnson, Alice and Williams, Bob},
  journal={IEEE Transactions on Neural Networks},
  year={2023},
  volume={34},
  number={5},
  pages={1234--1256},
  doi={10.1109/TNNLS.2023.12345}
}
```

### BibTeX with Categories Filter

Generate bibliography for specific categories:

```bash
findpapers bibtex climate_ai_search.json references_empirical.bib \
  --selected \
  --categories "Study Type:Empirical"
```

### Including Findpapers Citation

Add Findpapers itself to your bibliography:

```bash
findpapers bibtex climate_ai_search.json references.bib --selected --findpapers
```

This adds:

```bibtex
@misc{grosman2020findpapers,
  title={{Findpapers: A tool for helping researchers who are looking for related works}},
  author={Grosman, Jonatas},
  howpublished={\url{https://github.com/jonatasgrosman/findpapers}},
  year={2020}
}
```

---

## Part 6: Complete Workflow Example

Let's put it all together with a real-world example:

### Step 1: Prepare Your Environment

```bash
# Activate your environment
conda activate autosearch

# Set API keys (if available)
export SCOPUS_TOKEN="your-key"
export IEEE_TOKEN="your-key"

# Create project directory
mkdir climate_ai_review
cd climate_ai_review
```

### Step 2: Create Query File

**query.txt:**
```
([artificial intelligence] OR [AI] OR [machine learning] OR [deep learning])
AND
([climate change] OR [global warming])
AND
([predict*] OR [forecast*] OR [model*])
AND NOT
[review]
```

### Step 3: Execute Search

```bash
findpapers search results.json \
  --query-file query.txt \
  --since 2020-01-01 \
  --until 2024-12-31 \
  --databases "scopus,ieee,acm,arxiv,pubmed" \
  --publication-types "journal,conference proceedings" \
  --limit-db 100 \
  --token-scopus "$SCOPUS_TOKEN" \
  --token-ieee "$IEEE_TOKEN" \
  -v
```

### Step 4: First Screening (Titles)

```bash
findpapers refine results.json -v
```
- Review all titles
- Select potentially relevant papers
- Remove clearly irrelevant ones

### Step 5: Second Screening (Abstracts)

```bash
findpapers refine results.json \
  --selected \
  --abstract \
  --extra-info \
  --highlights "predict,model,accuracy,climate,temperature" \
  -v
```

### Step 6: Categorization

```bash
findpapers refine results.json \
  --selected \
  --abstract \
  --extra-info \
  --categories "Study Type:Empirical,Theoretical,Review,Methodological" \
  --categories "AI Method:CNN,RNN,LSTM,GAN,Transformer,Ensemble,Other" \
  --categories "Climate Focus:Temperature,Precipitation,Extreme Events,Sea Level,Other" \
  -v
```

### Step 7: Download Papers

```bash
findpapers download results.json ./papers/ \
  --selected \
  --proxy "http://proxy.university.edu:8080" \
  -v
```

### Step 8: Generate Bibliography

```bash
# All selected papers
findpapers bibtex results.json all_references.bib --selected --findpapers

# Empirical studies only
findpapers bibtex results.json empirical_refs.bib \
  --selected \
  --categories "Study Type:Empirical"

# By AI method
findpapers bibtex results.json lstm_refs.bib \
  --selected \
  --categories "AI Method:LSTM"
```

### Step 9: Create Summary Report

```bash
# List all selected papers with details
findpapers refine results.json \
  --selected \
  --abstract \
  --extra-info \
  --list > selected_papers_summary.txt
```

---

## Part 7: Tips & Best Practices

### Query Construction Tips

1. **Start broad, refine iteratively**
   ```bash
   # First try: broad query
   findpapers search test1.json --query "[AI] AND [climate]" --limit 20
   
   # Check results, then refine
   findpapers search test2.json \
     --query "([AI] OR [ML]) AND [climate change] AND [predict*]" \
     --limit 50
   ```

2. **Use wildcards wisely**
   - `[predict*]` captures: predict, prediction, predictions, predictive, predicting
   - `[climat*]` captures: climate, climatic, climatology
   - Don't overuse – can return too many irrelevant results

3. **Balance specificity vs. comprehensiveness**
   - Too specific: `[LSTM] AND [temperature prediction] AND [China]` (might miss relevant papers)
   - Too broad: `[AI] AND [climate]` (too many irrelevant results)
   - Good: `([deep learning] OR [neural network]) AND [climate] AND [predict*]`

### Search Strategy Tips

1. **Test your query first**
   ```bash
   findpapers search test.json --query "..." --limit 20
   ```

2. **Use database limits to ensure coverage**
   ```bash
   --limit-db 100  # Get up to 100 from each database
   ```

3. **Filter by publication type**
   ```bash
   --publication-types "journal,conference proceedings"
   # Excludes books, magazines, other
   ```

4. **Set appropriate date ranges**
   ```bash
   --since 2020-01-01 --until 2024-12-31
   ```

### Refinement Tips

1. **Use multiple passes**
   - Pass 1: Quick title screening
   - Pass 2: Abstract review
   - Pass 3: Categorization

2. **Create meaningful categories**
   ```bash
   --categories "Contribution:Dataset,Algorithm,Tool,Survey,Benchmark"
   --categories "Quality:High,Medium,Low"
   --categories "Relevance:Core,Related,Background"
   ```

3. **Use highlights effectively**
   ```bash
   --highlights "method,propose,novel,result,improve,accuracy,dataset"
   ```

### Download Tips

1. **Check download.log for failures**
   ```bash
   grep "❌" papers/download.log
   ```

2. **Use institutional proxy when possible**
   - Increases success rate significantly
   - Contact your librarian for proxy details

3. **Download in batches**
   - Download by category to organize papers
   - Easier to manage than one giant folder

### Data Management Tips

1. **Version control your query files**
   ```bash
   git add query.txt
   git commit -m "Updated query to exclude reviews"
   ```

2. **Backup your results.json file**
   - Contains all your screening decisions
   - Time-consuming to recreate if lost

3. **Document your process**
   - Save command history
   - Create README with methodology
   - Track inclusion/exclusion criteria

---

## Part 8: Troubleshooting

### Common Issues & Solutions

::::{grid} 1 1 1 2
:gutter: 2

:::{grid-item-card} ❌ "Invalid query syntax"
**Problem:** Query doesn't follow rules

**Solution:**
- Check brackets around terms
- Verify operators are UPPERCASE
- Ensure whitespace around operators
- Validate wildcard usage
:::

:::{grid-item-card} ❌ "No results found"
**Problem:** Query too specific or database issues

**Solution:**
- Broaden your query
- Check date ranges
- Try fewer databases
- Verify API keys if using Scopus/IEEE
:::

:::{grid-item-card} ❌ "API key invalid"
**Problem:** Authentication failed

**Solution:**
```bash
# Check key is set
echo $SCOPUS_TOKEN
# Re-export if needed
export SCOPUS_TOKEN="your-key"
```
:::

:::{grid-item-card} ❌ "Download failed (403)"
**Problem:** Papers behind paywall

**Solution:**
- Use institutional proxy
- Try from campus network
- Check if open access version exists
:::

::::

### Getting Help

- 📖 Check [official documentation](https://github.com/jonatasgrosman/findpapers)
- 🐛 Report bugs on [GitHub Issues](https://github.com/jonatasgrosman/findpapers/issues)
- 💬 Ask questions in [Discussions](https://github.com/jonatasgrosman/findpapers/discussions)

---

## Part 9: Practice Exercises

Try these exercises to solidify your learning:

### Exercise 1: Basic Search
**Task:** Find papers on "quantum computing" published in 2023

<details>
<summary>Solution</summary>

```bash
findpapers search quantum2023.json \
  --query "[quantum computing]" \
  --since 2023-01-01 \
  --until 2023-12-31 \
  --limit 50
```
</details>

### Exercise 2: Complex Query
**Task:** Find papers on machine learning in healthcare, excluding reviews

<details>
<summary>Solution</summary>

```bash
findpapers search ml_health.json \
  --query "([machine learning] OR [deep learning]) AND ([healthcare] OR [medical] OR [clinical]) AND NOT [review]" \
  --limit 100
```
</details>

### Exercise 3: Complete Workflow
**Task:** Perform a mini systematic review on any topic of your choice

Steps:
1. Create a research question
2. Build a search query
3. Execute search
4. Refine results
5. Categorize papers
6. Download top 10 papers
7. Generate BibTeX

---

## Part 10: Programmatic Usage (Python API)

Beyond the command-line interface, Findpapers can be used **programmatically** in Python scripts for complete automation and integration into larger workflows.

### Why Use the Python API?

- 🔄 **Full automation**: Run searches without manual intervention
- 📊 **Integration**: Combine with data analysis pipelines
- 🤖 **Batch processing**: Process multiple queries or projects
- 📝 **Documentation**: Self-documenting reproducible workflows
- 🔧 **Customization**: Fine-grained control over parameters

### Basic Programmatic Example

Here's a complete example for a **quick demonstration** - a focused search on AI applications in mental health:

```python
"""
Automated Literature Search: AI in Mental Health
A quick demonstration of programmatic Findpapers usage
"""

import findpapers
import datetime
from pathlib import Path

# Configuration
project_dir = Path("./mental_health_ai_demo")
project_dir.mkdir(exist_ok=True)

search_file = project_dir / "search_results.json"
output_dir = project_dir / "papers"
bibtex_file = project_dir / "references.bib"

# Research question: AI applications in anxiety and depression diagnosis
query = (
    "([artificial intelligence] OR [machine learning] OR [deep learning]) "
    "AND ([anxiety] OR [depression] OR [mental health]) "
    "AND ([diagnosis] OR [detection] OR [screening]) "
    "AND NOT [review]"
)

# Time range: Recent papers only (last 3 years)
since = datetime.date(2021, 1, 1)
until = datetime.date(2024, 12, 31)

# Limit results for quick demo
limit_per_database = 5  # Small number for demonstration
databases = ["pubmed", "arxiv"]  # Focus on relevant databases

# Publication types
publication_types = ["journal", "conference proceedings"]

# API tokens (optional - set to None if not available)
scopus_api_token = None  # Replace with your token if available
ieee_api_token = None    # Replace with your token if available

# Proxy (optional - for institutional access)
proxy = None  # "http://username:password@proxy.university.edu:8080"

# Categories for organization
categories = {
    "AI Method": [
        "Machine Learning", "Deep Learning", "Neural Networks", 
        "NLP", "Computer Vision", "Other"
    ],
    "Mental Health Condition": [
        "Depression", "Anxiety", "Both", "General Mental Health"
    ],
    "Study Type": [
        "Clinical Trial", "Observational", "Methodology", "Application"
    ],
    "Quality": [
        "High", "Medium", "Low"
    ]
}

# Keywords to highlight during refinement
highlights = [
    "diagnos", "detect", "accuracy", "AUC", "sensitivity", 
    "specificity", "machine learning", "deep learning", 
    "neural network", "performance", "model"
]

# Verbose output
verbose = True

print("=" * 60)
print("AUTOMATED LITERATURE SEARCH DEMO")
print("=" * 60)
print(f"Research Question: AI in Mental Health Diagnosis")
print(f"Date Range: {since} to {until}")
print(f"Databases: {', '.join(databases)}")
print(f"Max papers per database: {limit_per_database}")
print("=" * 60)
print()

# Step 1: Search
print("🔍 Step 1: Searching databases...")
print("-" * 60)
try:
    findpapers.search(
        outputpath=str(search_file),
        query=query,
        since=since,
        until=until,
        limit=None,  # No total limit
        limit_per_database=limit_per_database,
        databases=databases,
        publication_types=publication_types,
        scopus_api_token=scopus_api_token,
        ieee_api_token=ieee_api_token,
        verbose=verbose
    )
    print("✅ Search completed!")
except Exception as e:
    print(f"❌ Search failed: {e}")
    exit(1)

print()
print("=" * 60)
print("📊 Search results saved to:", search_file)
print("=" * 60)
print()

# Step 2: Interactive Refinement
print("🎨 Step 2: Refining results...")
print("-" * 60)
print("Opening interactive refinement interface...")
print("Actions available:")
print("  - [s] Select paper")
print("  - [r] Remove paper")
print("  - [n] Next paper")
print("  - [p] Previous paper")
print("  - [q] Quit and save")
print("-" * 60)
print()

try:
    findpapers.refine(
        search_path=str(search_file),
        categories=categories,
        highlights=highlights,
        show_abstract=True,
        show_extra_info=True,
        only_selected_papers=False,
        verbose=verbose
    )
    print("✅ Refinement completed!")
except Exception as e:
    print(f"⚠️ Refinement interrupted or completed: {e}")

print()

# Step 3: Download selected papers
print("📥 Step 3: Downloading full-text papers...")
print("-" * 60)
try:
    findpapers.download(
        search_path=str(search_file),
        output_directory=str(output_dir),
        only_selected_papers=True,
        proxy=proxy,
        verbose=verbose
    )
    print(f"✅ Papers downloaded to: {output_dir}")
except Exception as e:
    print(f"⚠️ Download completed with issues: {e}")

print()

# Step 4: Generate BibTeX
print("📚 Step 4: Generating BibTeX bibliography...")
print("-" * 60)
try:
    findpapers.generate_bibtex(
        search_path=str(search_file),
        outputpath=str(bibtex_file),
        only_selected_papers=True,
        add_findpapers_citation=True,
        verbose=verbose
    )
    print(f"✅ BibTeX file created: {bibtex_file}")
except Exception as e:
    print(f"❌ BibTeX generation failed: {e}")

print()
print("=" * 60)
print("🎉 DEMO COMPLETE!")
print("=" * 60)
print()
print("📁 Output files:")
print(f"  - Search results: {search_file}")
print(f"  - Downloaded papers: {output_dir}/")
print(f"  - Bibliography: {bibtex_file}")
print()
print("Next steps:")
print("  1. Review selected papers in the output directory")
print("  2. Import BibTeX into your reference manager")
print("  3. Modify the script for your research question")
print()
print("Happy researching! 🔬📚")
```

### Running the Script

Save the script as `demo_search.py` and run it:

```bash
# Activate your environment
conda activate autosearch

# Run the demo
python demo_search.py
```

### Expected Output

```
============================================================
AUTOMATED LITERATURE SEARCH DEMO
============================================================
Research Question: AI in Mental Health Diagnosis
Date Range: 2021-01-01 to 2024-12-31
Databases: pubmed, arxiv
Max papers per database: 5
============================================================

🔍 Step 1: Searching databases...
------------------------------------------------------------
Searching papers...
- PubMed: Found 5 papers
- arXiv: Found 5 papers

Removing duplicates...
Total unique papers: 9 (1 duplicate removed)

✅ Search completed!

============================================================
📊 Search results saved to: mental_health_ai_demo/search_results.json
============================================================

🎨 Step 2: Refining results...
[Interactive refinement interface opens]
...
```

### Advanced Usage: Multiple Queries

For comparing different research angles:

```python
"""
Batch processing: Compare different AI methods in mental health
"""

import findpapers
import datetime
from pathlib import Path

queries = {
    "traditional_ml": (
        "[machine learning] AND NOT [deep learning] "
        "AND ([depression] OR [anxiety]) AND [diagnosis]"
    ),
    "deep_learning": (
        "[deep learning] AND ([depression] OR [anxiety]) AND [diagnosis]"
    ),
    "nlp_approach": (
        "[natural language processing] AND [mental health] AND [text analysis]"
    )
}

base_dir = Path("./comparative_study")
base_dir.mkdir(exist_ok=True)

for name, query in queries.items():
    print(f"\n{'='*60}")
    print(f"Processing: {name}")
    print(f"{'='*60}\n")
    
    search_file = base_dir / f"{name}_results.json"
    
    findpapers.search(
        outputpath=str(search_file),
        query=query,
        since=datetime.date(2020, 1, 1),
        until=datetime.date(2024, 12, 31),
        limit_per_database=10,
        databases=["pubmed", "arxiv"],
        verbose=True
    )
    
    print(f"✅ {name}: Results saved to {search_file}\n")

print("\n🎉 All searches completed!")
print("Review results in:", base_dir)
```

### Integration with Data Analysis

Combine with pandas for analysis:

```python
"""
Analyze search results programmatically
"""

import json
import pandas as pd
from pathlib import Path

# Load search results
search_file = Path("mental_health_ai_demo/search_results.json")

with open(search_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract papers to DataFrame
papers = data.get('papers', [])
df = pd.DataFrame([
    {
        'title': p.get('title'),
        'year': p.get('publication_year'),
        'authors': ', '.join([a.get('name', '') for a in p.get('authors', [])[:3]]),
        'database': ', '.join(p.get('databases', [])),
        'selected': p.get('selected', False),
        'citations': p.get('citations'),
        'doi': p.get('doi')
    }
    for p in papers
])

# Analyze
print("=" * 60)
print("SEARCH RESULTS ANALYSIS")
print("=" * 60)
print(f"\nTotal papers found: {len(df)}")
print(f"Selected papers: {df['selected'].sum()}")
print(f"\nPapers by year:")
print(df['year'].value_counts().sort_index())
print(f"\nPapers by database:")
print(df['database'].value_counts())
print(f"\nMost cited papers:")
print(df.nlargest(5, 'citations')[['title', 'year', 'citations']])

# Export for further analysis
df.to_csv('search_analysis.csv', index=False)
print(f"\n✅ Analysis exported to: search_analysis.csv")
```

### Benefits of Programmatic Approach

::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item-card} 🔄 Reproducibility
Your entire search process is documented in code, making it easy to:
- Reproduce results exactly
- Share with collaborators
- Version control your methods
:::

:::{grid-item-card} ⚡ Efficiency
Automate repetitive tasks:
- Multiple related searches
- Batch processing
- Scheduled updates
:::

:::{grid-item-card} 📊 Integration
Seamlessly combine with:
- Data analysis (pandas)
- Visualization (matplotlib)
- Statistical tests
- Report generation
:::

:::{grid-item-card} 🎯 Customization
Fine-tune every aspect:
- Custom filtering logic
- Automated categorization
- Quality thresholds
- Custom output formats
:::

::::

### Best Practices

1. **Start with command-line** to understand the workflow
2. **Create modular scripts** for different stages
3. **Version control** your search scripts
4. **Document parameters** in comments
5. **Log all outputs** for debugging
6. **Test with small limits** before full searches
7. **Handle errors gracefully** with try-except blocks

### Common Use Cases

| Use Case | Approach |
|----------|----------|
| **Single focused search** | Command-line (fastest) |
| **Multiple related searches** | Python script with loop |
| **Weekly literature monitoring** | Scheduled Python script |
| **Integration with analysis** | Python with pandas/matplotlib |
| **Team collaboration** | Shared Python scripts + version control |
| **Large-scale study** | Python with parallel processing |

---

## Next Steps

🎉 **Congratulations!** You now know how to use Findpapers both via command-line and programmatically!

**What's next?**
- 📊 Explore [Additional Tools](../AMSR/paperscraper/0_Introduction) for specialized searches
- 🔄 Learn about [Complete Workflow](../AMSR/workflow/0_end_to_end) for end-to-end systematic reviews
- 📈 Create visualizations from your search results
- 🐍 Adapt the Python examples to your research question

:::{admonition} Pro Tip
:class: tip
The programmatic approach is especially valuable for reproducible research. Save your search scripts alongside your data analysis code in a Git repository!
:::

---

## Summary

You learned:
- ✅ How to construct complex search queries
- ✅ How to execute multi-database searches
- ✅ How to refine and categorize results interactively
- ✅ How to download papers with proxy support
- ✅ How to generate BibTeX bibliographies
- ✅ Best practices for systematic reviews

**Key Commands:**
```bash
# Search
findpapers search results.json --query-file query.txt --since 2020-01-01

# Refine
findpapers refine results.json --abstract --categories "Type:..."

# Download
findpapers download results.json ./papers/ --selected --proxy "..."

# BibTeX
findpapers bibtex results.json refs.bib --selected --findpapers
```

Happy researching! 🚀
