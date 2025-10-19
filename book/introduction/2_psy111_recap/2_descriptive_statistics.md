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

# 2.2 Statistics
Descriptive statistics summarize and describe dataset characteristics, and are great to give an overview of your data to whomever is approaching your work.
You could calculate these statistics by hand, but `pandas` already offers methods to call them directly from your `df_c`.

```{code-cell} ipython3
:tags: [remove-input]
import pandas as pd
df_c = pd.read_csv("./data/child_num_skills.csv")  
df_y = pd.read_csv("./data/subjects.csv") 
```

## 2.1 Measures of Central Tendency

```{code-cell}
mean = df_c["addit1"].mean()     # Arithmetic mean
median = df_c["addit1"].median() # Middle value

print(f"Mean: {mean}")
print(f"median: {median}")
```

## 2.2 Measures of Dispersion

```{code-cell}
std_dev = df_y["IQ_Vocab"].std()   # Standard deviation
variance = df_y["IQ_Vocab"].var()  # Variance
quantiles = df_y["IQ_Vocab"].quantile([0.25, 0.5, 0.75])  # Quartiles

print(f"Standard deviation: {std_dev}")
print(f"Variance: {variance}")
print("Quantiles: ")
print(quantiles)

```

## 2.3 `.describe()` method
Alternatively, `pandas` offer us a convenient way to get a first statistical summary. The `count` column will tell you how many values were used for the calculations in each column.

```{code-cell}
df_subset = df_c.iloc[:, :5]   # subset only the first 5 columns
df_subset.describe()
```

## 2.4 Mode, correlation, contingency tables

```{code-cell}
# MODE
mode_value = df_c["class"].mode()    # Most frequent value(s)
print("Mode:", mode_value.tolist())  # We use .tolist() to prettify the output
print()

# CORRELATION MATRIX
correlation_matrix = df_c.iloc[:, :5].corr()
print("Correlation Matrix:")
print(correlation_matrix)
print()

# CONTINGENCY TABLE (CROSS-TABULATION)
contingency_table = pd.crosstab(df_y["Gender"], df_y["Handedness"])
print("Contingency Table:")
print(contingency_table)
```

A **contingency table** summarizes the relationship between two categorical variables. It is useful for understanding frequency distributions across groups (e.g., how handedness varies by gender).

### Other Useful Descriptive Statistics to Consider

- **Skewness and Kurtosis**: Insight into the shape of distributions.
- **Range and IQR (Interquartile Range)**: For detecting outliers.
- **Z-scores**: Standardized scores help identify outliers or compare variables on a common scale.
- **Value counts**: Great for summarizing categorical variables.

```{code-cell}
# SKEWNESS AND KURTOSIS
skewness = df_c["addit1"].skew()
kurtosis = df_c["addit1"].kurt()
print(f"Skewness: {skewness}")
print(f"Kurtosis: {kurtosis}")
```

**Skewness** measures the asymmetry of the distribution. A skewness close to 0 indicates a symmetric distribution.  
**Kurtosis** indicates the "tailedness" of the distribution—higher values mean more extreme outliers.

---

```{code-cell}
# RANGE AND IQR
range_value = df_y["IQ_Matrix"].max() - df_y["IQ_Matrix"].min()
iqr = df_y["IQ_Matrix"].quantile(0.75) - df_y["IQ_Matrix"].quantile(0.25)
print(f"Range: {range_value}")
print(f"IQR (Interquartile Range): {iqr}")
```

**Range** shows the spread between the highest and lowest values.  
**IQR** (Interquartile Range) captures the middle 50% of the data and is robust to outliers.

---

```{code-cell}
# VALUE COUNTS
value_counts = df_y["Gender"].value_counts()
print("Value Counts for 'Gender':")
print(value_counts)
```

**Value counts** show the frequency of each category in a categorical column—ideal for understanding group sizes.

---

```{code-cell}
# Z-SCORES
from scipy.stats import zscore
z_scores = zscore(df_c["addit1"].dropna())
print("Z-scores (first 5):", z_scores[:5])
```

**Z-scores** standardize values relative to the mean and standard deviation, helping identify how far a value is from the average.
