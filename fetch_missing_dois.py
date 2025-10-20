"""
Fetch missing DOIs from PubMed API
This script enriches your search results with missing DOI information
"""
import json
import time
from pathlib import Path
import urllib.request
import xml.etree.ElementTree as ET

def fetch_doi_from_pubmed(pmid):
    """
    Fetch DOI for a PubMed article using the PubMed API.
    
    Args:
        pmid: PubMed ID (e.g., "39011768")
    
    Returns:
        DOI string or None if not found
    """
    try:
        # PubMed E-utilities API
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&retmode=xml"
        
        with urllib.request.urlopen(url, timeout=10) as response:
            xml_data = response.read()
        
        # Parse XML
        root = ET.fromstring(xml_data)
        
        # Find DOI in the XML structure
        # DOIs are usually in ArticleIdList with IdType="doi"
        for article_id in root.findall('.//ArticleId[@IdType="doi"]'):
            doi = article_id.text
            if doi:
                return doi.strip()
        
        return None
        
    except Exception as e:
        print(f"   ⚠️  Error fetching DOI for PMID {pmid}: {e}")
        return None

def enrich_search_results_with_dois(search_file, output_file=None):
    """
    Add missing DOIs to search results by querying PubMed API.
    
    Args:
        search_file: Path to search_results.json
        output_file: Path to save enriched results (default: overwrites original)
    """
    if output_file is None:
        output_file = search_file
    
    # Read search results
    print(f"📖 Reading: {search_file}")
    with open(search_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    papers = data['papers']
    
    print(f"📊 Found {len(papers)} papers")
    
    # Count papers with missing DOIs
    missing_doi_papers = [p for p in papers if not p.get('doi') and p.get('pubmed_id')]
    
    print(f"🔍 Papers with missing DOI (but have PubMed ID): {len(missing_doi_papers)}")
    
    if not missing_doi_papers:
        print("✅ All papers already have DOIs or lack PubMed IDs!")
        return
    
    print("\n🌐 Fetching missing DOIs from PubMed API...")
    print("   (This may take a few seconds...)\n")
    
    added_count = 0
    failed_count = 0
    
    for i, paper in enumerate(missing_doi_papers, 1):
        pmid = paper['pubmed_id']
        title = paper.get('title', 'Unknown')[:50]
        
        print(f"[{i}/{len(missing_doi_papers)}] {title}...")
        print(f"   PubMed ID: {pmid}")
        
        # Fetch DOI
        doi = fetch_doi_from_pubmed(pmid)
        
        if doi:
            paper['doi'] = doi
            added_count += 1
            print(f"   ✅ Found DOI: {doi}")
        else:
            failed_count += 1
            print(f"   ❌ DOI not found in PubMed")
        
        # Be respectful to the API - add delay
        time.sleep(0.5)  # 500ms delay between requests
        print()
    
    # Save enriched results
    print(f"💾 Saving enriched results to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"✅ DOIs added: {added_count}")
    print(f"❌ DOIs not found: {failed_count}")
    print(f"📁 Enriched file: {output_file}")
    
    if added_count > 0:
        print("\n💡 NEXT STEPS:")
        print("   1. Re-run: python extract_paper_links.py")
        print("      (Now with DOI links!)")
        print("   2. Re-generate BibTeX:")
        print("      findpapers generate-bibtex mental_health_ai_demo/search_results.json --selected")
        print("      (Now with DOI fields!)")

def main():
    """Main function to enrich search results with DOIs."""
    
    search_file = "mental_health_ai_demo/search_results.json"
    
    if not Path(search_file).exists():
        print(f"❌ Error: {search_file} not found!")
        print("   Make sure you've run demo_search.py first")
        return
    
    # Create backup
    backup_file = search_file.replace('.json', '_backup.json')
    print(f"📦 Creating backup: {backup_file}")
    
    with open(search_file, 'r') as f:
        data = f.read()
    with open(backup_file, 'w') as f:
        f.write(data)
    
    # Enrich with DOIs
    enrich_search_results_with_dois(search_file)

if __name__ == "__main__":
    main()
