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

# <i class="fa-solid fa-database"></i> Data curation


Data curation is the process of creating, organizing, and maintaining data sets so that people seeking information can access and use them. Curation involves collecting, structuring, indexing, and cataloging data for users within an organization, group, or the general public. In this session, we will ensure that we have the scientific computing skills necessary to **clean**, **explore**, **summarize**, and **visualize** data efficiently using the tools you were introduced to last semester: the `pandas`, `numpy`, and `matplotlib` libraries.

## Datasets

In this session, we will use the **Child Numeracy Skills** and the **Yeatman** datasets:

### Child Numeracy Skills
The dataset contains responses from a classroom-based arithmetic assessment. 
The dataset captures performance across multiple addition and subtraction tasks, allowing for the analysis of numerical ability in children.

#### Variables

- `addit1` to `addit8`: Scores for **eight addition problems**, assessing mental arithmetic and computation speed.
- `subtr1` to `subtr8`: Scores for **eight subtraction problems**, similarly targeting subtraction skills.
- `class`: Indicates the **class group** the child belongs to (useful for group comparisons or multilevel modeling).
- `time`: Represents the **total time taken** (in seconds) to complete the task, serving as a measure of processing speed or efficiency.

#### Usage

This dataset is well-suited for:
- Exploratory data analysis
- Item-level psychometric modeling
- Group comparisons (e.g., by class)
- Linking accuracy with processing time

### Yeatman dataset

This dataset contains demographic and cognitive profile data for 77 participants involved in a diffusion MRI study. Each row represents an individual subject and includes attributes relevant for analysis of structural brain connectivity.

#### Columns

- `subjectID`: Unique identifier for each participant.
- `Age`: Participant's age in years.
- `Gender`: Categorical variable indicating biological sex (Male/Female).
- `Handedness`: Preferred hand for tasks (e.g., 'Right', 'Left'). Some entries are missing.
- `IQ`: Composite intelligence quotient score.
- `IQ_Matrix`: Score on a matrix reasoning task (non-verbal IQ component).
- `IQ_Vocab`: Score on a vocabulary test (verbal IQ component).

#### Notes

- Some variables contain missing data, especially `Handedness`, `IQ`, `IQ_Matrix`, and `IQ_Vocab`.
