"""
Quick Demo: arXiv-Only Search (PDFs WILL Download!)
This demo uses arXiv database which always has downloadable PDFs.
Perfect for demonstrating the complete end-to-end workflow.
"""

import findpapers
import datetime
from pathlib import Path

def main():
    """Run a complete demo using arXiv (guaranteed PDF downloads!)."""
    
    print("=" * 80)
    print("FINDPAPERS DEMO: arXiv Search (PDFs WILL Download!)")
    print("=" * 80)
    print()
    
    # Configuration
    project_dir = Path("./arxiv_demo")
    project_dir.mkdir(exist_ok=True)
    
    search_file = project_dir / "search_results.json"
    download_dir = project_dir / "papers"
    bibtex_file = project_dir / "references.bib"
    
    # Search parameters
    query = (
        "([machine learning] OR [deep learning] OR [neural network*] OR [artificial intelligence]) "
        "AND ([mental health] OR [depression] OR [anxiety] OR [psychiatric])"
    )
    
    databases = ["arxiv"]  # ONLY arXiv - all papers have PDFs!
    
    print("📋 SEARCH CONFIGURATION")
    print("-" * 80)
    print(f"Query: {query}")
    print(f"Databases: {databases}")
    print(f"Date range: 2022-2024")
    print(f"Limit per database: 10 papers")
    print()
    
    # Step 1: Search
    print("🔍 STEP 1: Searching arXiv...")
    print("-" * 80)
    
    findpapers.search(
        search_file=str(search_file),
        query=query,
        since=datetime.date(2022, 1, 1),
        until=datetime.date(2024, 12, 31),
        limit_per_database=10,
        databases=databases,
        verbose=True
    )
    
    print()
    print("✅ Search complete!")
    print(f"   Results saved to: {search_file}")
    print()
    
    # Step 2: Refine (with categories)
    print("📝 STEP 2: Refining results...")
    print("-" * 80)
    
    # Define categories for organizing papers
    categories = {
        "AI Method": [
            "CNN", "RNN", "Transformer", "LSTM", "SVM", 
            "Random Forest", "XGBoost", "Deep Learning"
        ],
        "Mental Health Condition": [
            "Depression", "Anxiety", "PTSD", "Bipolar", 
            "Schizophrenia", "Stress"
        ],
        "Data Type": [
            "EEG", "fMRI", "Text", "Speech", "Wearable", 
            "Clinical Records", "Social Media"
        ],
        "Study Type": [
            "Classification", "Prediction", "Detection", 
            "Diagnosis", "Treatment", "Review"
        ]
    }
    
    # Highlight important keywords
    highlights = [
        "state-of-the-art",
        "benchmark",
        "novel",
        "clinical trial",
        "real-world",
        "interpretable",
        "explainable"
    ]
    
    findpapers.refine(
        search_file=str(search_file),
        categories=categories,
        highlights=highlights,
        verbose=True
    )
    
    print()
    print("✅ Refinement complete!")
    print("   Papers categorized and ready for review")
    print()
    
    # Step 3: Download PDFs
    print("📥 STEP 3: Downloading PDFs...")
    print("-" * 80)
    print("⚠️  NOTE: This will download ALL selected papers from arXiv")
    print("   arXiv papers are ALWAYS downloadable (open access)!")
    print()
    
    user_input = input("Continue with download? [y/N]: ")
    
    if user_input.lower() in ['y', 'yes']:
        download_dir.mkdir(exist_ok=True)
        
        findpapers.download(
            search_file=str(search_file),
            papers_directory=str(download_dir),
            selected_only=True,
            verbose=True
        )
        
        print()
        print("✅ Download complete!")
        print(f"   PDFs saved to: {download_dir}")
        
        # Count downloaded PDFs
        pdf_files = list(download_dir.glob("*.pdf"))
        print(f"   Total PDFs downloaded: {len(pdf_files)}")
        print()
    else:
        print("⏭️  Skipping download step")
        print()
    
    # Step 4: Generate BibTeX
    print("📚 STEP 4: Generating BibTeX...")
    print("-" * 80)
    
    findpapers.generate_bibtex(
        search_file=str(search_file),
        bibtex_file=str(bibtex_file),
        selected_only=True,
        verbose=True
    )
    
    print()
    print("✅ BibTeX generation complete!")
    print(f"   References saved to: {bibtex_file}")
    print()
    
    # Final summary
    print("=" * 80)
    print("DEMO COMPLETE! 🎉")
    print("=" * 80)
    print()
    print("📊 RESULTS:")
    print(f"   Search results: {search_file}")
    print(f"   Downloaded PDFs: {download_dir}")
    print(f"   BibTeX file: {bibtex_file}")
    print()
    print("💡 WHY THIS WORKED:")
    print("   ✅ arXiv is a preprint repository")
    print("   ✅ All papers are freely available")
    print("   ✅ Direct PDF download links provided")
    print("   ✅ No paywalls or institutional access needed!")
    print()
    print("🔬 COMPARING TO PUBMED:")
    print("   ❌ PubMed is a metadata-only database")
    print("   ❌ Does not provide PDF download links")
    print("   ❌ Papers are often behind journal paywalls")
    print("   ✅ Good for finding papers, but not downloading")
    print()
    print("📖 NEXT STEPS:")
    print("   1. Open the downloaded PDFs in: " + str(download_dir))
    print("   2. Import references.bib into your reference manager")
    print("   3. Start your literature review!")
    print()
    print("🎯 FOR YOUR MEETING:")
    print("   This demo shows the COMPLETE workflow including PDF downloads!")
    print("   Much better than PubMed-only demo with failed downloads.")
    print()

if __name__ == "__main__":
    main()
