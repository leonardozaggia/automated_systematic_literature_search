# ✅ PROGRAMMATIC USAGE ADDED - Meeting Ready!

## 🎉 What's New

I've added a **complete programmatic usage section** to your Findpapers tutorial, perfect for demonstrating during your meeting!

## 📍 Where to Find It

**In the Book:**
- File: `findpapers/1_demo_findpapers.md`
- Section: **Part 10: Programmatic Usage (Python API)**
- Located right before the "Next Steps" section

**Standalone Demo Script:**
- File: `demo_search.py`
- Ready to run: `python demo_search.py`
- Complete with helpful output and progress tracking

## 🎯 What the New Section Covers

### 1. **Why Use Python API**
- Full automation benefits
- Integration with data pipelines
- Batch processing capabilities
- Reproducibility advantages

### 2. **Complete Demo Example**
**Research Question:** AI in Mental Health Diagnosis  
**Configuration:**
- Focused query (anxiety, depression, AI diagnosis)
- Recent papers only (2021-2024)
- Limited results (5 per database) for quick demo
- PubMed + arXiv (no API keys needed)

### 3. **Four Complete Steps**
```python
# Step 1: Search
findpapers.search(...)

# Step 2: Refine (interactive)
findpapers.refine(...)

# Step 3: Download
findpapers.download(...)

# Step 4: Generate BibTeX
findpapers.generate_bibtex(...)
```

### 4. **Advanced Examples**
- **Batch processing**: Multiple queries comparison
- **Data analysis integration**: Using pandas to analyze results
- **Workflow automation**: Complete pipelines

### 5. **Best Practices**
- Modular scripts
- Error handling
- Version control
- Documentation

## 🚀 Demo Script Features

The `demo_search.py` script includes:

✅ **Clear configuration section** - Easy to modify  
✅ **Step-by-step execution** - With prompts between steps  
✅ **Helpful output** - Progress indicators and summaries  
✅ **Error handling** - Graceful failures with helpful messages  
✅ **Complete documentation** - Comments throughout  
✅ **Professional formatting** - Headers, separators, emojis  

### Demo Parameters (Optimized for Quick Demo)

```python
# Research topic
query = "([AI] OR [ML] OR [DL]) AND ([anxiety] OR [depression]) 
         AND [diagnosis] AND NOT [review]"

# Date range
since = 2021-01-01
until = 2024-12-31

# Papers
limit_per_database = 5  # ~10 papers total after deduplication

# Databases  
databases = ["pubmed", "arxiv"]  # No API keys required!

# Duration
~5-10 minutes total
```

## 📖 Quick Start for Your Meeting

### Option 1: Run the Demo Script (Recommended)

```bash
# Activate environment
conda activate autosearch

# Run demo
python demo_search.py
```

**What happens:**
1. Searches for ~10 recent papers on AI in mental health
2. Opens interactive refinement interface
3. Downloads selected papers
4. Generates BibTeX bibliography

**Output:**
```
mental_health_ai_demo/
├── search_results.json
├── references.bib
└── papers/
    └── [PDFs]
```

### Option 2: Show the Code (If Time is Limited)

Just open `demo_search.py` and walk through:
- Configuration section (lines 20-100)
- Four main steps (lines 120-250)
- Helper functions (lines 260+)

### Option 3: Show the Tutorial Section

Open the book and navigate to:
`findpapers/1_demo_findpapers.md` → Part 10

## 🎤 Meeting Presentation Tips

### 1. **Introduction (2 min)**
"Findpapers can be used both from command-line AND programmatically via Python API for complete automation..."

### 2. **Show the Code (3 min)**
Open `demo_search.py` and highlight:
- Simple configuration
- 4-line main workflow
- Professional output

### 3. **Run the Demo (5-7 min)**
```bash
python demo_search.py
```
- Let it search (shows database progress)
- Do 1-2 refinements interactively
- Show the generated files

### 4. **Benefits Discussion (2 min)**
- Reproducibility (code + results)
- Automation (batch processing)
- Integration (analysis pipelines)
- Collaboration (shared scripts)

### 5. **Advanced Examples (2 min)**
Show in tutorial:
- Batch processing multiple queries
- Integration with pandas/matplotlib
- Scheduled literature monitoring

## 📊 Key Talking Points

### For Researchers
- "Your entire search methodology documented in code"
- "Run weekly to monitor new publications"
- "Share exact search parameters with collaborators"

### For Technical Audience
- "Full Python API with all command-line features"
- "Integrate with pandas, matplotlib, numpy"
- "Scriptable, testable, version-controllable"

### For Beginners
- "Start with command-line, graduate to Python"
- "Copy-paste examples provided"
- "Step-by-step tutorial included"

## 📁 Files Created

```
automated_systematic_literature_search/
├── demo_search.py              # ⭐ Ready-to-run demo script
├── DEMO_README.md              # Instructions for demo
│
└── findpapers/
    └── 1_demo_findpapers.md    # ⭐ Updated with Part 10
```

## 🔧 Customization Options

### For Different Research Topics

Edit `demo_search.py` line 40:
```python
query = "[YOUR TOPIC] AND [YOUR FOCUS] AND NOT [EXCLUDE]"
```

### For More/Fewer Papers

Edit line 53:
```python
limit_per_database = 10  # Adjust as needed
```

### For Different Databases

Edit line 56:
```python
databases = ["scopus", "ieee", "acm", "pubmed", "arxiv"]
```

### For Your API Keys

Edit lines 65-66:
```python
scopus_api_token = "YOUR_TOKEN_HERE"
ieee_api_token = "YOUR_TOKEN_HERE"
```

## ✅ Pre-Meeting Checklist

- [ ] Environment activated: `conda activate autosearch`
- [ ] Findpapers installed: `findpapers version`
- [ ] Demo script tested: `python demo_search.py` (run once to familiarize)
- [ ] Book built: `jupyter-book build .`
- [ ] Browser ready with `_build/html/index.html` open
- [ ] Editor ready with `demo_search.py` open
- [ ] Terminal ready in project directory

## 🎯 Demo Flow (10-minute version)

**1. Show the problem (1 min)**
- Traditional manual searching is slow
- Hard to reproduce
- Error-prone

**2. Introduce the solution (1 min)**
- Findpapers Python API
- Programmatic automation
- Complete reproducibility

**3. Walk through code (3 min)**
- Open `demo_search.py`
- Show configuration
- Show 4-step process

**4. Run live demo (5 min)**
- Execute script
- Show search progress
- Do 2-3 refinements
- Show outputs

**5. Wrap up (1 min)**
- Point to full tutorial
- Mention book
- Q&A

## 🌟 Success Metrics

After your demo, attendees should understand:
- ✅ Findpapers has both CLI and Python API
- ✅ Python API enables complete automation
- ✅ Workflows are reproducible and shareable
- ✅ Integration with analysis tools is seamless
- ✅ Your book provides complete tutorials

## 📚 Resources to Share

After the meeting, share:
1. **Book URL**: https://leonardozaggia.github.io/automated_systematic_literature_search/
2. **Demo script**: `demo_search.py`
3. **Tutorial section**: Part 10 in Findpapers chapter
4. **Original repository**: https://github.com/jonatasgrosman/findpapers

## 🚀 You're Ready!

Everything is prepared for an impressive demonstration:

✅ Complete programmatic usage section in book  
✅ Professional demo script ready to run  
✅ Clear documentation and examples  
✅ Focused on mental health AI (relevant & interesting)  
✅ Quick execution (~10 papers for speed)  
✅ No API keys needed (PubMed + arXiv)  

**The demo will show:**
- Powerful automation capabilities
- Professional code quality
- Practical real-world application
- Complete reproducibility
- Your comprehensive tutorial book

Good luck with your meeting! 🎉📚🔬

---

**Quick Test:**
```bash
python demo_search.py
```

If it runs without errors and shows search progress, you're ready to go! 🚀
