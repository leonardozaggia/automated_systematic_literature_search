"""
Extract DOIs from search results and generate access links
This script helps you access papers when Findpapers download fails
"""
import json
from pathlib import Path
import csv

def extract_dois_and_links(search_file):
    """Extract DOIs from Findpapers results and generate access links."""
    
    with open(search_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    selected_papers = [p for p in data['papers'] if p.get('selected', False)]
    
    print("=" * 80)
    print("SELECTED PAPERS WITH ACCESS LINKS")
    print("=" * 80)
    print()
    
    access_data = []
    
    for i, paper in enumerate(selected_papers, 1):
        title = paper.get('title', 'No title')
        doi = paper.get('doi')
        pmid = paper.get('pubmed_id')
        year = paper.get('publication_year', 'N/A')
        
        print(f"{i}. {title[:70]}...")
        print(f"   Year: {year}")
        print(f"   Journal: {paper.get('publication', {}).get('title', 'N/A')}")
        
        links = {}
        
        # DOI link (most reliable)
        if doi:
            doi_link = f"https://doi.org/{doi}"
            print(f"   📄 DOI: {doi_link}")
            links['DOI'] = doi_link
        else:
            print(f"   ⚠️  DOI: Not available - will try to find it")
            links['DOI'] = "Missing"
        
        # PubMed link
        if pmid:
            pmid_link = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            print(f"   🔬 PubMed: {pmid_link}")
            links['PubMed'] = pmid_link
        
        # Sci-Hub (use cautiously - check your institution's policies)
        if doi:
            scihub_link = f"https://sci-hub.se/{doi}"
            print(f"   🔓 Sci-Hub: {scihub_link}")
            links['SciHub'] = scihub_link
        
        # Google Scholar search (can find DOI if missing!)
        clean_title = title.replace(' ', '+').replace('"', '%22')
        scholar_link = f"https://scholar.google.com/scholar?q={clean_title}"
        print(f"   🔍 Google Scholar: {scholar_link}")
        links['GoogleScholar'] = scholar_link
        
        # Recommendation if DOI missing
        if not doi:
            print(f"   💡 Tip: Use Google Scholar link above to find DOI")
        
        print()
        
        access_data.append({
            'Number': i,
            'Title': title,
            'Year': year,
            'DOI': doi or 'Missing',
            'PubMed_ID': pmid or 'N/A',
            'DOI_Link': links.get('DOI', 'N/A'),
            'PubMed_Link': links.get('PubMed', 'N/A'),
            'SciHub_Link': links.get('SciHub', 'N/A'),
            'GoogleScholar_Link': scholar_link
        })
    
    return selected_papers, access_data

def save_to_csv(access_data, output_file='paper_access_links.csv'):
    """Save access links to CSV file."""
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        if access_data:
            writer = csv.DictWriter(f, fieldnames=access_data[0].keys())
            writer.writeheader()
            writer.writerows(access_data)
    
    print(f"✅ Access links exported to: {output_file}")
    print(f"   Open in Excel to easily access all papers!")

def main():
    """Main function to extract and export paper access links."""
    
    search_file = "mental_health_ai_demo/search_results.json"
    
    if not Path(search_file).exists():
        print(f"❌ Error: {search_file} not found!")
        print("   Make sure you've run demo_search.py first")
        return
    
    papers, access_data = extract_dois_and_links(search_file)
    
    if not access_data:
        print("⚠️  No selected papers found!")
        print("   Run demo_search.py and select some papers first")
        return
    
    # Save to CSV
    save_to_csv(access_data)
    
    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total selected papers: {len(access_data)}")
    
    missing_doi = sum(1 for p in papers if not p.get('doi'))
    if missing_doi > 0:
        print(f"⚠️  Papers with missing DOI: {missing_doi}")
        print("   → Use PubMed link to find DOI manually")
        print("   → Use Google Scholar link to search for the paper")
    
    with_pmid = sum(1 for p in papers if p.get('pubmed_id'))
    print(f"✅ Papers with PubMed ID: {with_pmid}")
    
    print("\n💡 NEXT STEPS:")
    print("   1. Open paper_access_links.csv in Excel")
    print("   2. Click on the links to access papers")
    print("   3. For missing DOIs:")
    print("      - Go to PubMed link")
    print("      - Look for DOI on the paper page")
    print("      - Or search Google Scholar")
    print("   4. Download PDFs through your institution's access")

if __name__ == "__main__":
    main()
