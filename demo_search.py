"""
Findpapers Demo Script - AI in Mental Health Diagnosis
======================================================

A quick demonstration of automated literature search using Findpapers.
This script searches for recent papers on AI applications in mental health diagnosis.

Author: Leonardo Zaggia
Date: 2025-10-20
"""

import findpapers
import datetime
from pathlib import Path

def main():
    """Run a quick literature search demonstration."""
    
    # ========================================================================
    # CONFIGURATION
    # ========================================================================
    
    # Project setup
    project_name = "mental_health_ai_demo"
    project_dir = Path(f"./{project_name}")
    project_dir.mkdir(exist_ok=True)
    
    # File paths
    search_file = project_dir / "search_results.json"
    output_dir = project_dir / "papers"
    bibtex_file = project_dir / "references.bib"
    
    # Research question: AI applications in anxiety and depression diagnosis
    # This is a focused query to return a manageable number of papers for demo
    query = (
        "([artificial intelligence] OR [machine learning] OR [deep learning]) "
        "AND ([anxiety] OR [depression] OR [mental health]) "
        "AND ([diagnosis] OR [detection] OR [screening]) "
        "AND NOT [review]"
    )
    
    # Time range: Last 3 years only for recent, relevant papers
    since = datetime.date(2022, 1, 1)
    until = datetime.date(2025, 10, 15)
    
    # Limit for quick demonstration (adjust as needed)
    limit_per_database = 5  # Small number to keep demo quick
    
    # Focus on most relevant databases for this topic
    databases = ["pubmed", "arxiv"]
    
    # Publication types
    publication_types = ["journal", "conference proceedings"]
    
    # API tokens (optional - replace with your own if available)
    # Leave as None to use databases that don't require authentication
    scopus_api_token = None  # Replace: "YOUR_SCOPUS_TOKEN"
    ieee_api_token = None    # Replace: "YOUR_IEEE_TOKEN"
    
    # Proxy configuration (optional - for institutional access)
    proxy = None  # Example: "http://username:password@proxy.university.edu:8080"
    
    # Categories for organizing papers during refinement
    categories = {
        "AI Method": [
            "Machine Learning", 
            "Deep Learning", 
            "Neural Networks", 
            "NLP", 
            "Computer Vision", 
            "Other"
        ],
        "Mental Health Condition": [
            "Depression", 
            "Anxiety", 
            "Both", 
            "General Mental Health"
        ],
        "Study Type": [
            "Clinical Trial", 
            "Observational", 
            "Methodology", 
            "Application"
        ],
        "Data Source": [
            "Clinical", 
            "EHR", 
            "Social Media", 
            "Wearable", 
            "Neuroimaging",
            "Other"
        ],
        "Quality": [
            "High", 
            "Medium", 
            "Low"
        ]
    }
    
    # Keywords to highlight in abstracts during refinement
    highlights = [
        "diagnos", "detect", "accuracy", "AUC", "ROC",
        "sensitivity", "specificity", "precision", "recall",
        "machine learning", "deep learning", "neural network",
        "performance", "model", "algorithm", "prediction"
    ]
    
    # Enable verbose output for detailed progress
    verbose = True
    
    # ========================================================================
    # DEMO EXECUTION
    # ========================================================================
    
    print_header("AUTOMATED LITERATURE SEARCH DEMO")
    print(f"Research Topic: AI in Mental Health Diagnosis")
    print(f"Date Range: {since} to {until}")
    print(f"Databases: {', '.join(databases)}")
    print(f"Max papers per database: {limit_per_database}")
    print_separator()
    print()
    
    # ------------------------------------------------------------------------
    # STEP 1: Search
    # ------------------------------------------------------------------------
    print_step("1", "SEARCHING DATABASES")
    print(f"Query: {query[:80]}...")
    print_separator()
    
    try:
        findpapers.search(
            outputpath=str(search_file),
            query=query,
            since=since,
            until=until,
            limit=None,  # No overall limit, just per-database limit
            limit_per_database=limit_per_database,
            databases=databases,
            publication_types=publication_types,
            scopus_api_token=scopus_api_token,
            ieee_api_token=ieee_api_token,
            verbose=verbose
        )
        print()
        print("✅ Search completed successfully!")
        print(f"📁 Results saved to: {search_file}")
        
    except Exception as e:
        print(f"\n❌ Search failed: {e}")
        print("Please check your query and try again.")
        return 1
    
    print()
    input("Press Enter to continue to refinement...")
    print()
    
    # ------------------------------------------------------------------------
    # STEP 2: Refine
    # ------------------------------------------------------------------------
    print_step("2", "REFINING RESULTS (INTERACTIVE)")
    print("Instructions:")
    print("  • [s] = Select paper (mark as relevant)")
    print("  • [r] = Remove paper (mark as irrelevant)")
    print("  • [n] = Next paper (skip for now)")
    print("  • [p] = Previous paper (go back)")
    print("  • [q] = Quit and save (finish refinement)")
    print()
    print("Categories will be shown for classification.")
    print("Keywords will be highlighted in the abstract.")
    print_separator()
    print()
    input("Press Enter to start interactive refinement...")
    print()
    
    try:
        findpapers.refine(
            search_path=str(search_file),
            categories=categories,
            highlights=highlights,
            show_abstract=True,
            show_extra_info=True,
            only_selected_papers=False,
            verbose=verbose
        )
        print()
        print("✅ Refinement completed!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Refinement interrupted by user.")
        print("Your progress has been saved.")
    except Exception as e:
        print(f"\n⚠️ Refinement issue: {e}")
    
    print()
    input("Press Enter to continue to download...")
    print()
    
    # ------------------------------------------------------------------------
    # STEP 3: Download
    # ------------------------------------------------------------------------
    print_step("3", "DOWNLOADING SELECTED PAPERS")
    print(f"Target directory: {output_dir}")
    print_separator()
    
    try:
        findpapers.download(
            search_path=str(search_file),
            output_directory=str(output_dir),
            only_selected_papers=True,
            proxy=proxy,
            verbose=verbose
        )
        print()
        print(f"✅ Download process completed!")
        print(f"📁 Papers saved to: {output_dir}/")
        print(f"📋 Check {output_dir}/download.log for details")
        
    except Exception as e:
        print(f"\n⚠️ Download completed with issues: {e}")
        print("Check the download log for failed papers.")
    
    print()
    
    # ------------------------------------------------------------------------
    # STEP 4: Generate BibTeX
    # ------------------------------------------------------------------------
    print_step("4", "GENERATING BIBTEX BIBLIOGRAPHY")
    print(f"Output file: {bibtex_file}")
    print_separator()
    
    try:
        findpapers.generate_bibtex(
            search_path=str(search_file),
            outputpath=str(bibtex_file),
            only_selected_papers=True,
            add_findpapers_citation=True,
            verbose=verbose
        )
        print()
        print(f"✅ BibTeX file created successfully!")
        print(f"📁 Bibliography: {bibtex_file}")
        
    except Exception as e:
        print(f"\n❌ BibTeX generation failed: {e}")
        return 1
    
    print()
    
    # ------------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------------
    print_header("DEMO COMPLETED SUCCESSFULLY! 🎉")
    print()
    print("📂 Output Files:")
    print(f"  • Search results:    {search_file}")
    print(f"  • Downloaded PDFs:   {output_dir}/")
    print(f"  • Bibliography:      {bibtex_file}")
    print()
    print("🎯 Next Steps:")
    print("  1. Review selected papers in the output directory")
    print("  2. Import BibTeX file into your reference manager")
    print("  3. Modify this script for your own research question")
    print("  4. Explore the complete tutorial in the book")
    print()
    print("📚 Documentation:")
    print("  • Tutorial: findpapers/1_demo_findpapers.md")
    print("  • Workflow: book/AMSR/workflow/0_end_to_end.md")
    print()
    print_separator()
    print()
    print("Thank you for using Findpapers! Happy researching! 🔬📖")
    print()
    
    return 0


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def print_header(text):
    """Print a formatted header."""
    width = 70
    print()
    print("=" * width)
    print(f"  {text}")
    print("=" * width)


def print_separator():
    """Print a separator line."""
    print("-" * 70)


def print_step(number, title):
    """Print a step header."""
    print()
    print("=" * 70)
    print(f"  STEP {number}: {title}")
    print("=" * 70)


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    try:
        exit_code = main()
        exit(exit_code if exit_code else 0)
    except KeyboardInterrupt:
        print("\n\n❌ Demo interrupted by user. Exiting...")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        print("Please check your environment and try again.")
        exit(1)
