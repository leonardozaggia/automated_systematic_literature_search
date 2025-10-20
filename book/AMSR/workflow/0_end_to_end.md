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

# <i class="fa-solid fa-diagram-project"></i> Complete Systematic Review Workflow

This chapter presents a comprehensive, step-by-step workflow for conducting an automated systematic literature review or metanalysis from start to finish.

## Overview: The PRISMA-Aligned Workflow

Our automated workflow follows the PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses) guidelines while leveraging automation tools to enhance efficiency and reproducibility.

```{mermaid}
graph TB
    A[Phase 1: Planning] --> B[Phase 2: Search]
    B --> C[Phase 3: Screening]
    C --> D[Phase 4: Data Extraction]
    D --> E[Phase 5: Analysis]
    E --> F[Phase 6: Reporting]
    
    A1[Define research question<br/>Develop protocol<br/>Register study] --> A
    B1[Build search query<br/>Execute multi-database search<br/>Remove duplicates] --> B
    C1[Title/abstract screening<br/>Full-text screening<br/>Apply inclusion criteria] --> C
    D1[Extract study characteristics<br/>Extract outcome data<br/>Assess quality] --> D
    E1[Synthesize findings<br/>Perform metanalysis<br/>Assess bias] --> E
    F1[Write manuscript<br/>Create PRISMA diagram<br/>Publish results] --> F
    
    style A fill:#e3f2fd
    style B fill:#fff3e0
    style C fill:#ffe0b2
    style D fill:#c8e6c9
    style E fill:#b2dfdb
    style F fill:#f8bbd0
```

---

## Phase 1: Planning & Protocol Development

### Step 1.1: Define Your Research Question

Use the **PICO framework** (for intervention studies) or **PEO framework** (for observational studies):

#### PICO Framework
- **P**opulation: Who are you studying?
- **I**ntervention: What is being tested?
- **C**omparison: What is it compared to?
- **O**utcome: What are you measuring?

#### Example Research Questions

| Framework | Question |
|-----------|----------|
| **PICO** | In patients with depression (**P**), does cognitive behavioral therapy (**I**) compared to medication (**C**) lead to better symptom reduction (**O**)? |
| **PEO** | In university students (**P**), what is the effect of social media use (**E**) on mental health outcomes (**O**)? |

### Step 1.2: Develop a Protocol

Create a protocol document specifying:

**Essential Elements:**
1. Research objectives
2. Inclusion/exclusion criteria
3. Search strategy
4. Databases to search
5. Screening process
6. Data extraction plan
7. Quality assessment method
8. Analysis plan

**Template Protocol Structure:**

```markdown
# Systematic Review Protocol

## 1. Title
[Your review title]

## 2. Research Question
PICO: P=__, I=__, C=__, O=__

## 3. Objectives
- Primary objective: 
- Secondary objectives:

## 4. Inclusion Criteria
- Population: 
- Study design: 
- Publication type: 
- Language: 
- Date range: 

## 5. Exclusion Criteria
- 
- 

## 6. Search Strategy
Databases: ACM, IEEE, Scopus, PubMed, arXiv
Query: [detailed search string]

## 7. Screening Process
- Level 1: Title/abstract screening by 2 reviewers
- Level 2: Full-text screening by 2 reviewers
- Conflict resolution: Discussion or 3rd reviewer

## 8. Data Extraction
Variables to extract:
- Study characteristics: 
- Participant characteristics: 
- Outcomes: 
- Effect sizes: 

## 9. Quality Assessment
Tool: [e.g., Cochrane Risk of Bias Tool, Newcastle-Ottawa Scale]

## 10. Analysis Plan
- Narrative synthesis
- Meta-analysis (if appropriate)
- Subgroup analyses: 
```

### Step 1.3: Register Your Protocol (Optional but Recommended)

Register your protocol in:
- **PROSPERO** (health/medical reviews): https://www.crd.york.ac.uk/prospero/
- **Open Science Framework (OSF)**: https://osf.io/

:::{admonition} Why Register?
:class: tip
Registration increases transparency, reduces publication bias, and demonstrates rigorous methodology.
:::

---

## Phase 2: Literature Search

### Step 2.1: Build Your Search Query

Based on your PICO/PEO elements, construct a comprehensive search query.

**Example: AI in Mental Health Diagnosis**

**PICO Elements:**
- P: Mental health patients
- I: Artificial intelligence / machine learning
- C: (not applicable for this example)
- O: Diagnosis accuracy

**Query Construction:**

```text
# Population terms
([mental health] OR [psychiatric] OR [depression] OR [anxiety] OR [schizophrenia] OR [bipolar])

AND

# Intervention terms  
([artificial intelligence] OR [AI] OR [machine learning] OR [ML] OR [deep learning] OR [neural network*])

AND

# Outcome terms
([diagnos*] OR [detect*] OR [predict*] OR [classify] OR [accuracy])

AND NOT

# Exclusion terms
([review] OR [survey] OR [editorial])
```

**Save to file:** `search_query.txt`

### Step 2.2: Execute Multi-Database Search

```bash
# Create project directory
mkdir mental_health_ai_review
cd mental_health_ai_review

# Activate environment
conda activate autosearch

# Set API keys
export SCOPUS_TOKEN="your-scopus-key"
export IEEE_TOKEN="your-ieee-key"

# Execute search
findpapers search results.json \
  --query-file search_query.txt \
  --since 2015-01-01 \
  --until 2024-12-31 \
  --databases "scopus,ieee,acm,pubmed,arxiv" \
  --publication-types "journal,conference proceedings" \
  --limit-db 200 \
  --token-scopus "$SCOPUS_TOKEN" \
  --token-ieee "$IEEE_TOKEN" \
  -v
```

### Step 2.3: Document Search Results

Create a search log:

```bash
# Create search documentation
cat > search_log.md << 'EOF'
# Literature Search Log

## Search Date
2024-10-19

## Databases Searched
- Scopus (with API key)
- IEEE Xplore (with API key)
- ACM Digital Library
- PubMed
- arXiv

## Search Results
- Total records retrieved: [X]
- Duplicates removed: [Y]
- Unique records: [Z]

## Date Range
2015-01-01 to 2024-12-31

## Query
[paste your full query here]
EOF
```

---

## Phase 3: Screening

### Step 3.1: Title and Abstract Screening

**First Pass - Quick Screening:**

```bash
# Screen all papers - title only
findpapers refine results.json -v
```

**Actions:**
- `s` = Select if potentially relevant
- `r` = Remove if clearly irrelevant
- `n` = Unsure, review later

**Inclusion/Exclusion Criteria:**

Include if:
- ✅ Uses AI/ML for mental health diagnosis
- ✅ Reports diagnostic accuracy or performance
- ✅ Published 2015-2024
- ✅ Peer-reviewed journal or conference

Exclude if:
- ❌ Not about mental health
- ❌ Not about diagnosis/detection
- ❌ Review article or editorial
- ❌ Not using AI/ML methods

### Step 3.2: Abstract Screening

**Second Pass - Detailed Screening:**

```bash
# Review selected papers with abstracts
findpapers refine results.json \
  --selected \
  --abstract \
  --extra-info \
  --highlights "diagnos,predict,accuracy,AUC,sensitivity,specificity,machine learning,deep learning" \
  -v
```

**Tips:**
- Read abstract carefully
- Check publication venue (avoid predatory journals)
- Note any uncertainty for full-text review
- Look for key methodological details

### Step 3.3: Full-Text Screening

**Download selected papers:**

```bash
# Download PDFs
findpapers download results.json ./papers/ \
  --selected \
  --proxy "http://proxy.university.edu:8080" \
  -v
```

**Manual full-text review:**
- Open each PDF
- Apply full inclusion/exclusion criteria
- Check for all required information
- Update selection in Findpapers

```bash
# After reading PDFs, update selections
findpapers refine results.json --selected -v
# Remove papers that don't meet criteria after full read
```

### Step 3.4: Create PRISMA Flow Diagram Data

Track your numbers for the PRISMA diagram:

```python
# prisma_flow.py
prisma_data = {
    "identification": {
        "records_identified": 847,
        "records_from_databases": {
            "Scopus": 312,
            "IEEE": 198,
            "ACM": 145,
            "PubMed": 156,
            "arXiv": 36
        }
    },
    "screening": {
        "records_screened": 847,
        "records_excluded": 612,
        "reasons": {
            "Not about mental health": 234,
            "Not about diagnosis": 198,
            "Review/editorial": 98,
            "Wrong methodology": 82
        }
    },
    "eligibility": {
        "full_text_assessed": 235,
        "full_text_excluded": 127,
        "reasons": {
            "No diagnostic accuracy": 56,
            "Insufficient data": 38,
            "Duplicate data": 21,
            "Poor quality": 12
        }
    },
    "included": {
        "studies_included": 108
    }
}
```

---

## Phase 4: Data Extraction

### Step 4.1: Categorize Studies

```bash
# Categorize final selected papers
findpapers refine results.json \
  --selected \
  --abstract \
  --extra-info \
  --categories "Study Design:RCT,Cohort,Case-Control,Cross-Sectional,Other" \
  --categories "AI Method:SVM,Random Forest,Neural Network,Deep Learning,Ensemble,Other" \
  --categories "Mental Health Condition:Depression,Anxiety,Schizophrenia,Bipolar,Multiple,Other" \
  --categories "Data Type:Clinical,Neuroimaging,EEG,Text,Social Media,Multiple" \
  --categories "Sample Size:<100,100-500,500-1000,>1000" \
  --categories "Quality:High,Medium,Low" \
  -v
```

### Step 4.2: Extract Study Characteristics

Create a data extraction spreadsheet:

```python
# data_extraction.py
import pandas as pd
import json

# Load findpapers results
with open('results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Create DataFrame for selected papers
papers = [p for p in data['papers'] if p.get('selected')]

extraction_data = []
for paper in papers:
    extraction_data.append({
        'Study_ID': paper.get('id'),
        'Authors': ', '.join([a.get('name', '') for a in paper.get('authors', [])]),
        'Year': paper.get('publication_year'),
        'Title': paper.get('title'),
        'DOI': paper.get('doi'),
        # Add your extraction fields
        'Study_Design': '',
        'Sample_Size': '',
        'AI_Method': '',
        'Mental_Health_Condition': '',
        'Data_Type': '',
        'Accuracy': '',
        'Sensitivity': '',
        'Specificity': '',
        'AUC': '',
        'Quality_Score': '',
        'Notes': ''
    })

df = pd.DataFrame(extraction_data)
df.to_csv('data_extraction_template.csv', index=False)
print(f"Created extraction template for {len(df)} papers")
```

### Step 4.3: Quality Assessment

Choose an appropriate quality assessment tool:

**For Diagnostic Accuracy Studies:**
- **QUADAS-2** (Quality Assessment of Diagnostic Accuracy Studies)

**For Observational Studies:**
- **Newcastle-Ottawa Scale**

**For RCTs:**
- **Cochrane Risk of Bias Tool**

**Example: Simple Quality Checklist**

```markdown
## Quality Assessment Criteria

For each study, assess:

1. **Selection Bias**
   - [ ] Representative sample?
   - [ ] Clear inclusion/exclusion criteria?

2. **Performance**
   - [ ] Clear description of AI method?
   - [ ] Appropriate validation method?
   - [ ] Train/test split or cross-validation?

3. **Detection Bias**
   - [ ] Blinded assessment?
   - [ ] Objective outcome measures?

4. **Reporting**
   - [ ] Complete reporting of results?
   - [ ] Adequate statistical analysis?

Score: High quality (7-8), Medium (5-6), Low (<5)
```

---

## Phase 5: Analysis and Synthesis

### Step 5.1: Descriptive Statistics

```python
# analysis.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load extracted data
df = pd.read_csv('data_extraction_complete.csv')

# Descriptive statistics
print("=== Study Characteristics ===")
print(f"Total studies: {len(df)}")
print(f"\nYear distribution:")
print(df['Year'].value_counts().sort_index())

print(f"\nAI Methods:")
print(df['AI_Method'].value_counts())

print(f"\nMental Health Conditions:")
print(df['Mental_Health_Condition'].value_counts())

# Visualizations
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Publications over time
df['Year'].value_counts().sort_index().plot(kind='bar', ax=axes[0,0])
axes[0,0].set_title('Publications by Year')
axes[0,0].set_xlabel('Year')
axes[0,0].set_ylabel('Number of Studies')

# AI methods
df['AI_Method'].value_counts().plot(kind='pie', ax=axes[0,1], autopct='%1.1f%%')
axes[0,1].set_title('AI Methods Used')

# Mental health conditions
df['Mental_Health_Condition'].value_counts().plot(kind='barh', ax=axes[1,0])
axes[1,0].set_title('Mental Health Conditions Studied')

# Sample sizes
df['Sample_Size'].value_counts().plot(kind='bar', ax=axes[1,1])
axes[1,1].set_title('Sample Size Distribution')

plt.tight_layout()
plt.savefig('descriptive_analysis.png', dpi=300)
print("\nFigure saved: descriptive_analysis.png")
```

### Step 5.2: Meta-Analysis (if appropriate)

```python
# meta_analysis.py
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('data_extraction_complete.csv')

# Filter studies with required data
meta_df = df[df['AUC'].notna()].copy()
meta_df['AUC'] = pd.to_numeric(meta_df['AUC'])

print(f"Studies included in meta-analysis: {len(meta_df)}")

# Calculate pooled effect size (simplified example)
# For a proper meta-analysis, use specialized packages like metafor (R) or meta (Python)

# Summary statistics
mean_auc = meta_df['AUC'].mean()
std_auc = meta_df['AUC'].std()
se_auc = std_auc / np.sqrt(len(meta_df))

print(f"\n=== Meta-Analysis Results ===")
print(f"Pooled AUC: {mean_auc:.3f} (95% CI: {mean_auc - 1.96*se_auc:.3f} - {mean_auc + 1.96*se_auc:.3f})")

# Forest plot (simplified)
fig, ax = plt.subplots(figsize=(10, len(meta_df)*0.4))

y_positions = range(len(meta_df))
ax.scatter(meta_df['AUC'], y_positions, s=100, alpha=0.6)

# Add study labels
for i, (idx, row) in enumerate(meta_df.iterrows()):
    ax.text(-0.05, i, f"{row['Authors'].split(',')[0]} ({row['Year']})", 
            ha='right', va='center', fontsize=8)

# Add pooled estimate
ax.axvline(mean_auc, color='red', linestyle='--', linewidth=2, label='Pooled Estimate')
ax.scatter([mean_auc], [-1], color='red', s=200, marker='D')

ax.set_ylim(-2, len(meta_df))
ax.set_xlim(0.5, 1.0)
ax.set_xlabel('AUC')
ax.set_title('Forest Plot: Diagnostic Accuracy (AUC)')
ax.grid(axis='x', alpha=0.3)
ax.legend()

plt.tight_layout()
plt.savefig('forest_plot.png', dpi=300, bbox_inches='tight')
print("\nForest plot saved: forest_plot.png")
```

### Step 5.3: Subgroup Analysis

```python
# subgroup_analysis.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data_extraction_complete.csv')
df['AUC'] = pd.to_numeric(df['AUC'], errors='coerce')

# Subgroup by AI method
print("=== Subgroup Analysis: AI Method ===")
subgroup_ai = df.groupby('AI_Method')['AUC'].agg(['mean', 'std', 'count'])
print(subgroup_ai)

# Subgroup by mental health condition
print("\n=== Subgroup Analysis: Mental Health Condition ===")
subgroup_mh = df.groupby('Mental_Health_Condition')['AUC'].agg(['mean', 'std', 'count'])
print(subgroup_mh)

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Box plot by AI method
df.boxplot(column='AUC', by='AI_Method', ax=axes[0])
axes[0].set_title('AUC by AI Method')
axes[0].set_xlabel('AI Method')
axes[0].set_ylabel('AUC')

# Box plot by condition
df.boxplot(column='AUC', by='Mental_Health_Condition', ax=axes[1])
axes[1].set_title('AUC by Mental Health Condition')
axes[1].set_xlabel('Condition')
axes[1].set_ylabel('AUC')

plt.suptitle('')
plt.tight_layout()
plt.savefig('subgroup_analysis.png', dpi=300)
print("\nSubgroup analysis figure saved")
```

---

## Phase 6: Reporting

### Step 6.1: Generate Bibliography

```bash
# Generate BibTeX for all included studies
findpapers bibtex results.json included_studies.bib --selected --findpapers

# Generate separate BibTeX files by category
findpapers bibtex results.json neural_network_studies.bib \
  --selected \
  --categories "AI Method:Neural Network"

findpapers bibtex results.json depression_studies.bib \
  --selected \
  --categories "Mental Health Condition:Depression"
```

### Step 6.2: Create PRISMA Flow Diagram

Use the data collected in Phase 3:

```python
# create_prisma_diagram.py
# This creates a simple text representation
# For publication, use tools like draw.io or dedicated PRISMA diagram generators

prisma_text = """
┌─────────────────────────────────────────────┐
│         IDENTIFICATION                       │
│                                             │
│  Records identified through                 │
│  database searching (n = 847)               │
│    - Scopus: 312                           │
│    - IEEE: 198                             │
│    - ACM: 145                              │
│    - PubMed: 156                           │
│    - arXiv: 36                             │
│                                             │
│  Duplicates removed (n = 189)              │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         SCREENING                           │
│                                             │
│  Records screened (n = 658)                │
│                                             │
│  Records excluded (n = 423)                │
│    - Not about mental health: 234          │
│    - Not about diagnosis: 98               │
│    - Review/editorial: 91                  │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         ELIGIBILITY                         │
│                                             │
│  Full-text articles assessed (n = 235)     │
│                                             │
│  Full-text excluded (n = 127)              │
│    - No diagnostic accuracy: 56            │
│    - Insufficient data: 38                 │
│    - Duplicate data: 21                    │
│    - Poor quality: 12                      │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         INCLUDED                            │
│                                             │
│  Studies included in                        │
│  qualitative synthesis (n = 108)           │
│                                             │
│  Studies included in                        │
│  quantitative synthesis (n = 95)           │
└─────────────────────────────────────────────┘
"""

print(prisma_text)

with open('prisma_flow.txt', 'w') as f:
    f.write(prisma_text)

print("PRISMA flow diagram saved to: prisma_flow.txt")
print("\nFor publication-ready diagrams, use:")
print("- http://prisma.thetacollaborative.ca/ (PRISMA diagram generator)")
print("- https://www.draw.io/ (manual creation)")
```

### Step 6.3: Write Results Section

Template structure:

```markdown
# Results

## Study Selection
The literature search identified 847 records across five databases 
(Scopus: 312, IEEE: 198, ACM: 145, PubMed: 156, arXiv: 36). After 
removing 189 duplicates, 658 unique records were screened. Title and 
abstract screening excluded 423 records. Full-text screening of 235 
articles resulted in 108 studies meeting inclusion criteria for 
qualitative synthesis, with 95 providing sufficient data for meta-analysis.

## Study Characteristics
The included studies were published between 2015 and 2024, with a notable 
increase in publications after 2019 (n = 87, 80.6%). Studies investigated 
various mental health conditions: depression (n = 45, 41.7%), anxiety 
(n = 28, 25.9%), schizophrenia (n = 18, 16.7%), and bipolar disorder 
(n = 17, 15.7%). Sample sizes ranged from 52 to 15,234 participants 
(median = 456).

## AI Methods
Deep learning approaches were most common (n = 48, 44.4%), followed by 
support vector machines (n = 23, 21.3%), random forests (n = 19, 17.6%), 
and ensemble methods (n = 18, 16.7%). Data sources included clinical 
assessments (n = 52), neuroimaging (n = 31), electronic health records 
(n = 15), and social media data (n = 10).

## Diagnostic Accuracy
Meta-analysis of 95 studies reporting AUC values yielded a pooled AUC of 
0.876 (95% CI: 0.852-0.900), indicating good diagnostic performance. 
Substantial heterogeneity was observed (I² = 87.3%, p < 0.001).

### Subgroup Analysis
Diagnostic accuracy varied by AI method: deep learning (AUC = 0.901), 
ensemble methods (AUC = 0.887), SVM (AUC = 0.856), and random forests 
(AUC = 0.841). Accuracy also differed by condition: depression (AUC = 0.892), 
anxiety (AUC = 0.871), bipolar disorder (AUC = 0.863), and schizophrenia 
(AUC = 0.854).

## Quality Assessment
Using QUADAS-2, 42 studies (38.9%) were rated as high quality, 51 (47.2%) 
as medium quality, and 15 (13.9%) as low quality. Common methodological 
concerns included small sample sizes (n = 38), lack of external validation 
(n = 45), and inadequate reporting of model details (n = 28).
```

### Step 6.4: Create Supplementary Materials

```python
# create_supplementary_materials.py
import pandas as pd

# Load data
df = pd.read_csv('data_extraction_complete.csv')

# Create supplementary tables

# Table S1: Characteristics of included studies
table_s1 = df[['Study_ID', 'Authors', 'Year', 'Title', 'Study_Design', 
               'Sample_Size', 'Mental_Health_Condition']].copy()
table_s1.to_csv('supplementary_table_s1_characteristics.csv', index=False)

# Table S2: AI methods and performance
table_s2 = df[['Study_ID', 'Authors', 'Year', 'AI_Method', 'Data_Type',
               'Accuracy', 'Sensitivity', 'Specificity', 'AUC']].copy()
table_s2.to_csv('supplementary_table_s2_performance.csv', index=False)

# Table S3: Quality assessment
table_s3 = df[['Study_ID', 'Authors', 'Year', 'Quality_Score', 'Quality']].copy()
table_s3.to_csv('supplementary_table_s3_quality.csv', index=False)

print("Supplementary materials created:")
print("- supplementary_table_s1_characteristics.csv")
print("- supplementary_table_s2_performance.csv")
print("- supplementary_table_s3_quality.csv")

# Create list of included studies for appendix
with open('supplementary_appendix_included_studies.txt', 'w', encoding='utf-8') as f:
    f.write("# Appendix: List of Included Studies\n\n")
    for idx, row in df.sort_values(['Year', 'Authors']).iterrows():
        f.write(f"{row['Authors']} ({row['Year']}). {row['Title']}. ")
        f.write(f"DOI: {row['DOI']}\n\n")

print("- supplementary_appendix_included_studies.txt")
```

---

## Phase 7: Reproducibility Package

Create a complete reproducibility package:

### Project Structure

```
mental_health_ai_review/
├── protocol/
│   └── protocol.md
├── search/
│   ├── search_query.txt
│   ├── search_log.md
│   └── results.json
├── screening/
│   └── screening_decisions.json
├── extraction/
│   ├── data_extraction_template.csv
│   └── data_extraction_complete.csv
├── analysis/
│   ├── descriptive_analysis.py
│   ├── meta_analysis.py
│   ├── subgroup_analysis.py
│   └── figures/
│       ├── descriptive_analysis.png
│       ├── forest_plot.png
│       └── subgroup_analysis.png
├── papers/
│   └── [downloaded PDFs]
├── bibliography/
│   ├── included_studies.bib
│   └── [category-specific .bib files]
├── manuscript/
│   ├── manuscript.md
│   └── supplementary_materials/
└── README.md
```

### Create README

```markdown
# Systematic Review: AI in Mental Health Diagnosis

## Overview
This repository contains all materials for conducting and reproducing our 
systematic review on artificial intelligence applications in mental health 
diagnosis.

## Contents
- `protocol/`: Study protocol and registration
- `search/`: Search strategies and results
- `screening/`: Screening decisions and PRISMA flow
- `extraction/`: Data extraction forms and data
- `analysis/`: Analysis scripts and outputs
- `papers/`: Downloaded full-text articles
- `bibliography/`: Reference lists
- `manuscript/`: Final manuscript and supplements

## Reproducibility

### Prerequisites
```bash
conda create -n review_env python=3.10
conda activate review_env
pip install findpapers pandas matplotlib seaborn scipy
```

### Reproduce the Search
```bash
cd search/
findpapers search results.json --query-file search_query.txt ...
```

### Reproduce the Analysis
```bash
cd analysis/
python descriptive_analysis.py
python meta_analysis.py
python subgroup_analysis.py
```

## Citation
[Your citation here]

## License
CC-BY-4.0

## Contact
[Your email]
```

---

## Checklist: Complete Workflow

Use this checklist to ensure you've completed all steps:

### Planning Phase
- [ ] Research question defined (PICO/PEO)
- [ ] Protocol developed
- [ ] Protocol registered (if applicable)
- [ ] Inclusion/exclusion criteria clear
- [ ] Search strategy planned

### Search Phase
- [ ] Search query constructed and tested
- [ ] Multi-database search executed
- [ ] Search results documented
- [ ] Duplicates removed
- [ ] Results saved and backed up

### Screening Phase
- [ ] Title screening completed
- [ ] Abstract screening completed
- [ ] Full-text screening completed
- [ ] Screening documented (PRISMA flow)
- [ ] Inter-rater reliability assessed (if multiple reviewers)

### Extraction Phase
- [ ] Data extraction form created
- [ ] Study characteristics extracted
- [ ] Outcome data extracted
- [ ] Quality assessment completed
- [ ] Data verified and cleaned

### Analysis Phase
- [ ] Descriptive statistics calculated
- [ ] Meta-analysis performed (if appropriate)
- [ ] Subgroup analyses conducted
- [ ] Sensitivity analyses performed
- [ ] Publication bias assessed

### Reporting Phase
- [ ] PRISMA checklist completed
- [ ] PRISMA flow diagram created
- [ ] Results section written
- [ ] Bibliography generated
- [ ] Supplementary materials prepared
- [ ] Reproducibility package created

---

## Summary

This chapter provided a complete workflow for conducting automated systematic reviews:

1. **Planning**: Define research question, develop protocol
2. **Search**: Build queries, execute multi-database searches
3. **Screening**: Screen titles, abstracts, and full texts
4. **Extraction**: Extract data and assess quality
5. **Analysis**: Synthesize findings and perform meta-analysis
6. **Reporting**: Write manuscript and create reproducibility package

By following this workflow and leveraging automation tools like Findpapers, you can conduct rigorous, transparent, and reproducible systematic reviews efficiently.

---

:::{admonition} Next Steps
:class: tip
- Explore specific analysis techniques in the [Analysis Examples](../analysis/) section
- Learn about advanced querying in [Advanced Topics](../advanced/)
- Check out [Real-World Examples](../examples/) for inspiration
:::
