# <i class="fa-solid fa-clipboard-check"></i> Reporting & Validation

Automation changes *how* you search and screen, not *what* a systematic review has to report. This page shows how to turn a Review Buddy run into a method you can describe, reproduce and defend.

Three documents set the bar:

- **PRISMA 2020** {cite}`Page2021PRISMA` - the reporting guideline: a 27-item checklist and the flow diagram. PRISMA tells you what to *report*; it does not prescribe how to *conduct* the review, and no tool is "PRISMA-compliant" by itself - your report is.
- **PRISMA-S** {cite}`Rethlefsen2021PRISMAS` - the PRISMA extension for reporting literature **searches**: databases, full search strings, limits, dates, deduplication.
- **The 2025 position statement on AI in evidence synthesis** by Cochrane, the Campbell Collaboration, JBI and the Collaboration for Environmental Evidence {cite}`Flemyng2025RAISE`, which endorses the RAISE recommendations: the review team stays **accountable** for every AI-assisted decision, AI is used under **human oversight**, and any AI use that makes or suggests judgements is **reported transparently**.

For reporting AI-assisted screening in detail, independent authors have also proposed the **PRISMA-trAIce** checklist {cite}`Holst2025PRISMAtrAIce` (it is not an official PRISMA extension).

---

## 1. Record the Search (PRISMA-S)

Everything that defines a Review Buddy search is in two small text files. Keep them, with the date, next to your results:

| What to report | Where it is |
|---|---|
| Databases searched | `search.sources` in `config.yaml` |
| Full search string | `query.txt` (or `search.query`) |
| Limits: years, fields | `search.year_from`, `search.year_to`, `search.pubmed_field` (`tiab` = PubMed Title/Abstract). Scopus is always searched in title/abstract/keywords (`TITLE-ABS-KEY`) |
| Date of the search | The day you ran step 1 - write it down |
| Software and version | `git rev-parse HEAD` in the `review_buddy` folder |
| Records per database | The step 1 output: `<Source>: Added N papers` |
| Deduplication method | DOI or normalised title, PubMed record preferred ([details](https://github.com/leonardozaggia/review_buddy/blob/main/docs/DEDUPLICATION.md)) |

The easiest way to keep the numbers is to save the console output of every run:

```bash
python main.py --ai > run_2026-10-06.log 2>&1
```

On Windows, enable Python's UTF-8 mode first (`$env:PYTHONUTF8 = "1"` in PowerShell, `set PYTHONUTF8=1` in cmd) so that every step writes the `✓`/`⚠` symbols to the file correctly.

:::{admonition} The same query is adapted per database
:class: note
PRISMA-S asks for the search string *as run* in each database. Review Buddy sends one query and each searcher adapts it (field scoping, `NOT` rewriting, wildcard removal on arXiv). The step 1 log shows the translated query for each source (e.g. `Searching arXiv with query: ...`) - quote those in your appendix.
:::

---

## 2. Fill the PRISMA 2020 Flow Diagram

Most boxes in the identification and screening part of the PRISMA 2020 flow diagram can be read straight from Review Buddy's outputs:

```{mermaid}
graph TD
    A["Records identified from databases<br>step 1 log: 'Source: Added N papers'"] --> B["Duplicates removed<br>sum of per-source counts minus unique records"]
    A --> C["Removed for other reasons<br>'Post-filter: Removed N papers outside year range'<br>'... with no publication date'"]
    A --> D["Records screened<br>papers loaded by step 2"]
    D --> E["Records excluded / marked ineligible by automation tools<br>filtered_out/ or filtered_out_ai/"]
    D --> F["Reports sought for retrieval<br>kept papers passed to step 3"]
    F --> G["Reports not retrieved<br>pdfs/failed_downloads.csv"]
    F --> H["Reports assessed for eligibility<br>your full-text review"]

    style A fill:#e1f5ff
    style D fill:#fff4e1
    style F fill:#fff4e1
    style H fill:#e8f5e9
```

| PRISMA 2020 box | Review Buddy source |
|---|---|
| Records identified, per database | Step 1 log, `<Source>: Added N papers` for each source |
| Duplicate records removed | Sum of the per-source counts − unique records before the year filter |
| Records removed for other reasons | Step 1 log, `Post-filter: Removed N papers outside year range` and `... with no publication date` |
| Records marked as ineligible by automation tools | Step 2 summary, `Breakdown by filter` (and the CSVs in `filtered_out/` or `filtered_out_ai/`) - **if no human checked those exclusions** |
| Records screened / excluded | Your own title/abstract screening of the kept papers (`papers_filtered*.csv`) |
| Reports sought for retrieval | Papers in the bibliography given to step 3 |
| Reports not retrieved | Rows in `results/pdfs/failed_downloads.csv` that you couldn't obtain by hand either |
| Reports assessed / excluded with reasons / included | Your full-text review - outside the tool |

Where automated exclusions go depends on your method. If the keyword or AI filter removes records **with no human check**, report them as *records marked as ineligible by automation tools*. If people re-screen those exclusions, they are part of the screening step, and you report the human decisions.

---

## 3. Validate the Screening

Automated exclusion is the step where a review can silently lose relevant studies. A false exclusion costs more than a false inclusion: a borderline paper you keep gets a human look later, but one you exclude is never seen again. Validate before you trust a filter.

### Keyword filter

- Read every `results/filtered_out/<filter>.csv`, or a random sample of each if they are large.
- Look for meaning-blind matches. Two real examples: `rat` removed a robotics study with autistic children because the abstract abbreviates *robot-assisted therapy* as "RAT", and `bmi` (if you add it to `bci`) matches *body mass index*.
- Report the keyword lists in full - they are part of your eligibility criteria.

### AI filter

1. **Fix the setup before screening.** Write the model and its tag (`gemma3:4b`), the prompts, `invert`, `confidence_threshold` and `temperature` into your protocol, before you look at the results. Changing prompts until the output "looks right" is the screening equivalent of tuning a search until it finds the papers you already know.
2. **Hand-label a sample and measure agreement.** `scripts/benchmark_ollama_models.py` scores models against hand-assigned labels and reports per-filter agreement, JSON reliability and speed:
   ```bash
   # build the sample locally from your own bibliography
   python scripts/benchmark_ollama_models.py --rebuild-sample results/references.bib \
       --gold scripts/benchmark_data/gold_labels.json --sample sample.json
   # score one or more models
   python scripts/benchmark_ollama_models.py --models gemma3:4b gpt-oss:20b \
       --sample sample.json --gold scripts/benchmark_data/gold_labels.json --out bench.json
   ```
   The script ships with the filter set and the 48 gold labels of the developer's own review (neonatal fMRI). To measure *your* filters, replace its filter definitions and gold labels with your own.
3. **Check the exclusions, not only the agreement.** Draw a random sample from `results/filtered_out_ai/` and screen it by hand. Report how many you checked and how many were wrongly excluded.
4. **Read every paper in `manual_review_ai.csv`.** These are the low-confidence calls and failed model calls. They are kept, so they need a human decision.
5. **Report it.** Give the tool and version, the model, the prompts, the threshold, the human-checking strategy (all exclusions, a sample, or only the flagged papers) and the agreement you measured.

:::{admonition} Screening is a filter, not a reviewer
:class: important
Even the best model in the developer's benchmark (0.971 agreement) disagrees with a human on about 1 paper in 34. The standard for screening in intervention reviews remains two independent human reviewers {cite}`Higgins2024Handbook`; describe the AI filter as what it is - a tool that reduces the workload of human screening, under human oversight.
:::

---

## 4. Known Blind Spots

Report these where they apply - each one can bias which studies reach your synthesis:

| Behaviour | Effect | What to do |
|---|---|---|
| The year filter removes papers **with no publication date** | Some records disappear before screening | Report the count from the step 1 log |
| Papers **without an abstract** are excluded (`no_abstract`, always on in AI mode) | Letters, conference papers and some older records are never screened | Screen `filtered_out*/no_abstract.csv` by hand if they matter for your question |
| `non_english` removes non-English papers | Language restriction is a known source of bias | State it as an eligibility criterion |
| Google Scholar is unreliable; arXiv mishandles complex queries | Per-source counts can be misleading | Report per-source counts and the translated queries |
| Downloads fail more often for paywalled publishers | Full-text availability is not random | Report *reports not retrieved* and try to obtain them by hand |

---

## 5. Responsible Use

- **Accountability and oversight**: the review team, not the tool, is responsible for every inclusion and exclusion {cite}`Flemyng2025RAISE`.
- **Confidentiality**: the AI filter runs on a local Ollama model, so abstracts and your criteria never leave your machine.
- **Access rights**: the downloader only retrieves what your network is entitled to. Check publishers' terms of service before automating a browser at scale, and treat the Sci-Hub option (off by default) as a decision under your local law.

Full references are listed on the [References](../references) page.
