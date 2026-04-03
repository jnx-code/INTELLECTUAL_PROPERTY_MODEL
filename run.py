#!/usr/bin/env python3
"""
Entry point script for running the AI Copyright Detection System.

Usage:
    python run.py --mode cli      # Run command-line demo
    python run.py --mode api      # Run REST API server
    python run.py --mode app      # Run Streamlit web app
    python run.py --mode test     # Run system tests
"""

import argparse
import sys
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def run_cli():
    """Run the command-line interface demo."""
    print("Running CLI Demo...")
    from main import main
    main()


def run_api():
    """Run the FastAPI server."""
    print("Starting API Server...")
    print("API documentation will be available at: [localhost](http://localhost:8000/docs)")
    from api import run_api
    run_api(host="0.0.0.0", port=8000)


def run_app():
    """Run the Streamlit web application."""
    print("Starting Streamlit Web Application...")
    print("Open your browser to: [localhost](http://localhost:8501)")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])


def run_tests():
    """Run system tests."""
    print("Running System Tests...")
    print("=" * 60)
    
    from main import CopyrightDetectionSystem
    
    # Initialize system
    print("\n[TEST 1] System Initialization")
    system = CopyrightDetectionSystem()
    system.initialize()
    print("✓ System initialized successfully")
    
    # Test detection
    print("\n[TEST 2] Copyright Detection")
    test_text = "In the garden where quantum flowers bloom, each petal exists in superposition."
    report = system.analyze(test_text)
    assert report.detection_summary["matches_found"] > 0, "Should find matches"
    assert report.detection_summary["risk_level"] in ["HIGH", "MEDIUM", "LOW", "NONE"], "Invalid risk level"
    print(f"✓ Detection working (found {report.detection_summary['matches_found']} matches)")
    
    # Test quick check
    print("\n[TEST 3] Quick Check")
    has_issues, risk_level, similarity = system.quick_check(test_text)
    assert isinstance(has_issues, bool), "has_issues should be boolean"
    assert isinstance(similarity, float), "similarity should be float"
    print(f"✓ Quick check working (issues: {has_issues}, similarity: {similarity:.2%})")
    
    # Test no-match scenario
    print("\n[TEST 4] No-Match Scenario")
    safe_text = "The weather is nice today and I enjoy walking in the park with my dog."
    safe_report = system.analyze(safe_text)
    assert safe_report.detection_summary["highest_similarity"] < 0.7, "Should have low similarity"
    print(f"✓ No-match scenario working (similarity: {safe_report.detection_summary['highest_similarity']:.2%})")
    
    # Test batch processing
    print("\n[TEST 5] Batch Processing")
    batch_texts = [
        "Test text one about quantum physics",
        "Test text two about machine learning",
        "Test text three about natural language"
    ]
    batch_results = system.batch_analyze(batch_texts)
    assert len(batch_results) == len(batch_texts), "Should process all texts"
    print(f"✓ Batch processing working ({len(batch_results)} texts processed)")
    
    # Test report generation
    print("\n[TEST 6] Report Generation")
    text_report = system.get_formatted_report(test_text, format_type="text")
    json_report = system.get_formatted_report(test_text, format_type="json")
    assert len(text_report) > 0, "Text report should not be empty"
    assert len(json_report) > 0, "JSON report should not be empty"
    print("✓ Report generation working")
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="AI Copyright Detection System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run.py --mode cli      Run command-line demo
    python run.py --mode api      Start REST API server
    python run.py --mode app      Start Streamlit web app
    python run.py --mode test     Run system tests
        """
    )
    
    parser.add_argument(
        "--mode",
        choices=["cli", "api", "app", "test"],
        default="cli",
        help="Execution mode (default: cli)"
    )
    
    args = parser.parse_args()
    
    if args.mode == "cli":
        run_cli()
    elif args.mode == "api":
        run_api()
    elif args.mode == "app":
        run_app()
    elif args.mode == "test":
        run_tests()


if __name__ == "__main__":
    main()
