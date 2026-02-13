# 📊 Info-Extractor

Extract information from papers in a structured way for systematic analysis and data synthesis.

## Overview

Info-Extractor is a tool designed to systematically extract and organize information from academic papers. It enables researchers to convert unstructured paper content into structured data formats, facilitating quantitative analysis, meta-analysis, and systematic reviews.

## Key Features

:::{admonition} Coming Soon
:class: note
This section is under development. Check back soon for detailed documentation on Info-Extractor's features and usage instructions.
:::

### Main Capabilities

- **Structured Data Extraction**: Extract key information into predefined fields
- **Custom Templates**: Define your own extraction schemas
- **Batch Processing**: Process multiple papers simultaneously
- **Quality Control**: Built-in validation and consistency checks
- **Export Formats**: CSV, Excel, JSON, and database-ready outputs

## Typical Workflow

```{mermaid}
graph LR
    A[Complete Paper Set] --> B[Define Schema]
    B --> C[Extract Data]
    C --> D[Validate Results]
    D --> E[Export Data]
    E --> F[Analysis/Meta-analysis]
    
    style A fill:#e8f5e9
    style B fill:#fff3e0
    style C fill:#e3f2fd
    style D fill:#fce4ec
    style E fill:#f3e5f5
    style F fill:#f1f8e9
```

## Common Extraction Fields

Info-Extractor can be configured to extract various types of information:

### Study Characteristics
- Publication year, authors, journal
- Study design and methodology
- Sample size and demographics
- Geographic location

### Research Findings
- Primary outcomes and measures
- Statistical results (p-values, effect sizes, confidence intervals)
- Key findings and conclusions
- Limitations

### Quality Assessment
- Risk of bias indicators
- Study quality scores
- Funding sources
- Conflicts of interest

## Use Cases

Info-Extractor is ideal for:

- **Systematic Reviews**: Extract data for PRISMA-compliant reviews
- **Meta-Analysis**: Gather statistical data for quantitative synthesis
- **Scoping Reviews**: Map research characteristics across fields
- **Evidence Synthesis**: Compile findings from multiple studies
- **Quality Assessment**: Systematically evaluate study quality

## Integration with Other Tools

| Tool | Purpose | Info-Extractor Role |
|------|---------|---------------------|
| Review Buddy | Paper Collection | Provides papers to extract from |
| Elicit | AI Screening | Complements with structured extraction |
| Excel/R/Python | Statistical Analysis | Receives structured data for analysis |

## Getting Started

Documentation for Info-Extractor installation and detailed usage will be added soon.

---

:::{admonition} Best Practices
:class: tip
Define your extraction schema **before** starting the extraction process. This ensures consistency across all papers and reduces the need for re-extraction.
:::

:::{admonition} Quality Control
:class: warning
Always validate extracted data through double-checking or inter-rater reliability assessments, especially for critical meta-analysis inputs.
:::
