# Findpapers Limitations & Workarounds

## 🔍 Understanding the Issues

### Issue 1: Download Failures ("Empty URL list")

**Why this happens:**
- Papers are in databases without direct PDF links (PubMed is a metadata-only database)
- Papers are behind paywalls
- Findpapers uses heuristics to find PDF URLs - doesn't work for all publishers
- Some journals have complex download systems

**From your log:**
All 5 papers failed because PubMed only provides metadata, not PDF links. These are journal articles that require:
- Journal subscription
- Institutional access
- Individual purchase
- Or finding via DOI

### Issue 2: Missing DOIs in BibTeX

**Why this happens:**
- Findpapers relies on what the database provides
- PubMed sometimes doesn't include DOI in the API response
- The data might be incomplete in the source

**Your BibTeX entries are missing:**
- `doi = {...}` field
- Sometimes `url = {...}` field

---

## 💡 Workarounds & Solutions

### Solution 1: Use DOI to Access Papers

Create a helper script to find papers using their DOIs:

```python
"""
Extract DOIs from search results and generate access links
"""
import json
from pathlib import Path

def extract_dois_and_links(search_file):
    """Extract DOIs from Findpapers results and generate access links."""
    
    with open(search_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    selected_papers = [p for p in data['papers'] if p.get('selected', False)]
    
    print("=" * 70)
    print("SELECTED PAPERS WITH ACCESS LINKS")
    print("=" * 70)
    print()
    
    for i, paper in enumerate(selected_papers, 1):
        title = paper.get('title', 'No title')
        doi = paper.get('doi')
        pmid = paper.get('pubmed_id')
        
        print(f"{i}. {title[:60]}...")
        print(f"   Year: {paper.get('publication_year')}")
        
        # DOI link (most reliable)
        if doi:
            print(f"   📄 DOI: https://doi.org/{doi}")
        
        # PubMed link
        if pmid:
            print(f"   🔬 PubMed: https://pubmed.ncbi.nlm.nih.gov/{pmid}/")
        
        # Sci-Hub (use cautiously - check your institution's policies)
        if doi:
            print(f"   🔓 Sci-Hub: https://sci-hub.se/{doi}")
        
        # Google Scholar search
        clean_title = title.replace(' ', '+')
        print(f"   🔍 Google Scholar: https://scholar.google.com/scholar?q={clean_title}")
        
        print()
    
    return selected_papers

if __name__ == "__main__":
    search_file = "mental_health_ai_demo/search_results.json"
    papers = extract_dois_and_links(search_file)
    
    # Export to CSV for easy access
    import csv
    with open('paper_access_links.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'DOI', 'DOI_Link', 'PubMed_Link', 'Year'])
        for p in papers:
            doi = p.get('doi', '')
            pmid = p.get('pubmed_id', '')
            writer.writerow([
                p.get('title', ''),
                doi,
                f"https://doi.org/{doi}" if doi else '',
                f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else '',
                p.get('publication_year', '')
            ])
    
    print("✅ Access links exported to: paper_access_links.csv")
```

Save as `extract_paper_links.py` and run:
```bash
python extract_paper_links.py
```

### Solution 2: Manual Download via Institution

Most universities provide access through:

**A. Library Portal**
1. Go to your university library website
2. Search by DOI or title
3. Download PDF directly

**B. Institutional Proxy**
Configure your browser with institutional proxy:
```python
# In demo_search.py, add your proxy
proxy = "http://username:password@proxy.university.edu:8080"
```

**C. VPN**
- Connect to university VPN
- Access journal websites directly
- DOIs will resolve to full-text

### Solution 3: Use Unpaywall API

Unpaywall finds legal open-access versions:

```python
"""
Check Unpaywall for open-access versions
"""
import requests
import json

def check_unpaywall(doi, email="your.email@university.edu"):
    """Check if paper is available via open access."""
    url = f"https://api.unpaywall.org/v2/{doi}?email={email}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            
            if data.get('is_oa'):
                print(f"✅ Open Access: {data['best_oa_location']['url']}")
                return data['best_oa_location']['url']
            else:
                print("❌ Not freely available")
                return None
    except:
        print("⚠️ Could not check Unpaywall")
        return None

# Example usage
def check_all_papers_unpaywall(search_file):
    """Check all selected papers for OA versions."""
    with open(search_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    selected = [p for p in data['papers'] if p.get('selected', False)]
    
    print("Checking for open-access versions...\n")
    
    oa_links = []
    for paper in selected:
        doi = paper.get('doi')
        if doi:
            print(f"Checking: {paper['title'][:50]}...")
            url = check_unpaywall(doi)
            if url:
                oa_links.append({'title': paper['title'], 'url': url})
            print()
    
    return oa_links

if __name__ == "__main__":
    oa_papers = check_all_papers_unpaywall("mental_health_ai_demo/search_results.json")
    print(f"\n✅ Found {len(oa_papers)} open-access papers")
```

### Solution 4: Enhance BibTeX with Missing DOIs

```python
"""
Fix missing DOIs in BibTeX file
"""
import json
import re

def add_dois_to_bibtex(search_file, bibtex_file, output_file="references_fixed.bib"):
    """Add missing DOI fields to BibTeX entries."""
    
    # Load search results to get DOIs
    with open(search_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create DOI lookup by title
    doi_lookup = {}
    for paper in data['papers']:
        if paper.get('doi'):
            # Normalize title for matching
            title = paper['title'].lower().strip()
            doi_lookup[title] = paper['doi']
    
    # Read BibTeX file
    with open(bibtex_file, 'r', encoding='utf-8') as f:
        bibtex_content = f.read()
    
    # Find all entries
    entries = re.split(r'(@\w+{[^}]+,)', bibtex_content)
    
    fixed_content = ""
    added_count = 0
    
    for part in entries:
        if part.startswith('@'):
            # Extract title from this entry
            title_match = re.search(r'title\s*=\s*{([^}]+)}', part, re.IGNORECASE)
            if title_match:
                title = title_match.group(1).lower().strip()
                # Remove trailing periods and extra spaces
                title = re.sub(r'\.$', '', title).strip()
                
                # Check if DOI already exists
                has_doi = re.search(r'doi\s*=', part, re.IGNORECASE)
                
                if not has_doi and title in doi_lookup:
                    # Find the closing brace
                    last_brace = part.rfind('}')
                    if last_brace != -1:
                        # Insert DOI before closing brace
                        doi = doi_lookup[title]
                        part = part[:last_brace] + f",\n    doi = {{{doi}}}\n" + part[last_brace:]
                        added_count += 1
        
        fixed_content += part
    
    # Write fixed BibTeX
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"✅ Added {added_count} missing DOI fields")
    print(f"✅ Fixed BibTeX saved to: {output_file}")
    
    return added_count

if __name__ == "__main__":
    add_dois_to_bibtex(
        "mental_health_ai_demo/search_results.json",
        "mental_health_ai_demo/references.bib",
        "mental_health_ai_demo/references_fixed.bib"
    )
```

### Solution 5: Use Alternative Databases

Modify your demo to include databases with better PDF access:

```python
# In demo_search.py, change databases:
databases = [
    "arxiv",        # Always has PDFs!
    "biorxiv",      # Preprints with PDFs
    "medrxiv",      # Medical preprints with PDFs
    "pubmed"        # For completeness, but no PDFs
]
```

**arXiv papers always downloadable!** They're preprints with open access.

### Solution 6: Automate with Selenium

For advanced users - automate browser downloads:

```python
"""
Automated download using Selenium (requires institutional access)
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def download_via_doi(doi, download_dir="./papers"):
    """Attempt to download paper via DOI using browser automation."""
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
    })
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # Navigate to DOI
        driver.get(f"https://doi.org/{doi}")
        time.sleep(3)
        
        # Try to find PDF link (varies by publisher)
        pdf_patterns = [
            "//a[contains(@href, '.pdf')]",
            "//a[contains(text(), 'PDF')]",
            "//a[contains(@class, 'pdf')]",
        ]
        
        for pattern in pdf_patterns:
            try:
                pdf_link = driver.find_element(By.XPATH, pattern)
                pdf_link.click()
                print(f"✅ Downloading: {doi}")
                time.sleep(5)  # Wait for download
                return True
            except:
                continue
        
        print(f"❌ Could not find PDF link for: {doi}")
        return False
        
    finally:
        driver.quit()

# Note: Requires institutional access/VPN
```

---

## 🎯 Recommended Workflow for Your Meeting

Since downloads failed, here's the **best approach for demonstration**:

### Option A: Use arXiv Instead

```python
# Modify demo_search.py
databases = ["arxiv"]  # Only arXiv - all papers downloadable!

query = (
    "([machine learning] OR [deep learning] OR [neural network*]) "
    "AND ([mental health] OR [depression] OR [anxiety])"
)
```

**Why:** arXiv papers ALWAYS have PDFs available!

### Option B: Show the Workaround

During your demo:

1. **Show the download failure** (it's honest!)
2. **Explain why** (PubMed is metadata-only)
3. **Show the workaround:**
   ```bash
   python extract_paper_links.py
   ```
4. **Open one DOI link** in browser to show how to access

This actually makes for a **better demo** - shows real-world challenges and solutions!

### Option C: Pre-download Sample Papers

1. Use arXiv papers (always work)
2. Or manually download 2-3 PDFs via your institution
3. Place in `mental_health_ai_demo/papers/` before demo
4. Show "these were successfully downloaded"

---

## 📝 Add to Your Tutorial

I can add a new section to the tutorial explaining these limitations and workarounds. Would you like me to create:

1. **"Part 11: Handling Download Limitations"** in the tutorial
2. **Helper scripts** for the workarounds above
3. **Updated demo script** that uses arXiv (guaranteed downloads)

---

## 🔧 Quick Fix for Your Demo

**Immediate solution for your meeting:**

```python
# Create this script: quick_arxiv_demo.py

import findpapers
import datetime
from pathlib import Path

# Use arXiv only - guaranteed PDFs!
project_dir = Path("./arxiv_demo")
project_dir.mkdir(exist_ok=True)

findpapers.search(
    search_file=str(project_dir / "results.json"),
    query="([machine learning] OR [deep learning]) AND ([mental health] OR [depression])",
    since=datetime.date(2022, 1, 1),
    until=datetime.date(2024, 12, 31),
    limit_per_database=5,
    databases=["arxiv"],  # Only arXiv!
    verbose=True
)

print("\n✅ Search complete! arXiv papers have downloadable PDFs.")
print("Run: findpapers download arxiv_demo/results.json ./arxiv_papers/ --selected")
```

This will **actually download PDFs** successfully! 🎉

---

Would you like me to:
1. Create these helper scripts?
2. Update your demo to use arXiv?
3. Add a comprehensive section about limitations to the tutorial?
