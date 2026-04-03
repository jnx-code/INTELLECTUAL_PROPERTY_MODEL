"""
Main system integration module for the AI Copyright Detection System.
"""

import os
from typing import Optional, Tuple, List
import pandas as pd

from config import CONFIG
from dataset_generator import CopyrightedContentGenerator, create_dataset
from embedding_engine import EmbeddingEngine
from vector_store import CopyrightVectorStore
from copyright_detector import CopyrightDetector, DetectionResult
from attribution_engine import AttributionEngine
from legal_compliance import LegalComplianceModule
from report_generator import ReportGenerator, CopyrightReport


class CopyrightDetectionSystem:
    """
    Main integration class for the AI Copyright Detection System.
    
    Coordinates all components to provide comprehensive copyright
    detection, attribution, and compliance assessment.
    """
    
    def __init__(self, data_dir: str = "./data"):
        """
        Initialize the copyright detection system.
        
        Args:
            data_dir: Directory for storing system data.
        """
        self.data_dir = data_dir
        self.embedding_engine: Optional[EmbeddingEngine] = None
        self.vector_store: Optional[CopyrightVectorStore] = None
        self.detector: Optional[CopyrightDetector] = None
        self.attribution_engine: Optional[AttributionEngine] = None
        self.compliance_module: Optional[LegalComplianceModule] = None
        self.report_generator: Optional[ReportGenerator] = None
        self.dataset: Optional[pd.DataFrame] = None
        self._initialized = False
    
    def initialize(self, force_rebuild: bool = False):
        """
        Initialize all system components.
        
        Args:
            force_rebuild: If True, rebuild the vector store even if it exists.
        """
        print("=" * 60)
        print("INITIALIZING AI COPYRIGHT DETECTION SYSTEM")
        print("=" * 60)
        
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize embedding engine
        print("\n[1/6] Loading embedding model...")
        self.embedding_engine = EmbeddingEngine()
        
        # Initialize vector store
        print("\n[2/6] Setting up vector store...")
        self.vector_store = CopyrightVectorStore(
            dimension=self.embedding_engine.get_embedding_dimension()
        )
        
        # Check for existing data or generate new
        vector_store_path = os.path.join(self.data_dir, "vector_store")
        
        if os.path.exists(vector_store_path) and not force_rebuild:
            print("\n[3/6] Loading existing vector store and model...")
            self.vector_store.load(vector_store_path)
            model_path = os.path.join(self.data_dir, "embedding_model.pkl")
            self.embedding_engine.load(model_path)
        else:
            print("\n[3/6] Generating synthetic dataset...")
            self.dataset, self.test_queries = create_dataset()
            
            print(f"  Generated {len(self.dataset)} copyrighted content records")
            
            print("\n[4/6] Generating ML embeddings...")
            contents = self.dataset["content"].tolist()
            self.embedding_engine.train(contents)
            embeddings = self.embedding_engine.generate_embeddings(contents)
            
            print("\n[5/6] Indexing content in vector store...")
            self.vector_store.add_from_dataframe(self.dataset, embeddings)
            
            # Save for future use
            self.vector_store.save(vector_store_path)
            
            # Save ML Model
            model_path = os.path.join(self.data_dir, "embedding_model.pkl")
            self.embedding_engine.save(model_path)
            
            # Save dataset
            dataset_path = os.path.join(self.data_dir, "dataset.csv")
            self.dataset.to_csv(dataset_path, index=False)
        
        # Initialize remaining components
        print("\n[6/6] Initializing detection components...")
        self.detector = CopyrightDetector(self.vector_store, self.embedding_engine)
        self.attribution_engine = AttributionEngine()
        self.compliance_module = LegalComplianceModule()
        self.report_generator = ReportGenerator()
        
        self._initialized = True
        
        print("\n" + "=" * 60)
        print("SYSTEM INITIALIZED SUCCESSFULLY")
        print("=" * 60)
        print(f"\nIndexed works: {self.vector_store.get_stats()['total_vectors']}")
        print(f"Embedding dimension: {self.embedding_engine.get_embedding_dimension()}")
    
    def analyze(
        self,
        text: str,
        top_k: int = None,
        use_purpose: str = "general",
        citation_style: str = "APA"
    ) -> CopyrightReport:
        """
        Perform complete copyright analysis on text.
        
        Args:
            text: Text to analyze.
            top_k: Maximum number of matches to return.
            use_purpose: Intended use purpose for fair use analysis.
            citation_style: Citation format style.
            
        Returns:
            Complete CopyrightReport with all analysis results.
        """
        if not self._initialized:
            raise RuntimeError("System not initialized. Call initialize() first.")
        
        # Detect potential matches
        detection_result = self.detector.detect(text, top_k=top_k)
        
        # Generate comprehensive report
        report = self.report_generator.generate(
            detection_result,
            use_purpose=use_purpose,
            citation_style=citation_style
        )
        
        return report
    
    def quick_check(self, text: str) -> Tuple[bool, str, float]:
        """
        Perform quick copyright check.
        
        Args:
            text: Text to check.
            
        Returns:
            Tuple of (has_issues, risk_level, similarity_score).
        """
        if not self._initialized:
            raise RuntimeError("System not initialized. Call initialize() first.")
        
        return self.detector.quick_check(text)
    
    def batch_analyze(
        self,
        texts: List[str],
        top_k: int = 3
    ) -> List[Tuple[str, bool, str, float]]:
        """
        Analyze multiple texts.
        
        Args:
            texts: List of texts to analyze.
            top_k: Maximum matches per text.
            
        Returns:
            List of (text_preview, has_issues, risk_level, similarity) tuples.
        """
        if not self._initialized:
            raise RuntimeError("System not initialized. Call initialize() first.")
        
        results = []
        for text in texts:
            has_issues, risk_level, similarity = self.detector.quick_check(text)
            preview = text[:100] + "..." if len(text) > 100 else text
            results.append((preview, has_issues, risk_level, similarity))
        
        return results
    
    def get_formatted_report(
        self,
        text: str,
        format_type: str = "text"
    ) -> str:
        """
        Get formatted report for text.
        
        Args:
            text: Text to analyze.
            format_type: "text" or "json".
            
        Returns:
            Formatted report string.
        """
        report = self.analyze(text)
        
        if format_type == "json":
            return self.report_generator.format_report_json(report)
        else:
            return self.report_generator.format_report_text(report)


def main():
    """Main entry point for testing the system."""
    # Initialize system
    system = CopyrightDetectionSystem()
    system.initialize()
    
    # Test queries
    test_texts = [
        # Near-verbatim match
        "In the garden where quantum flowers bloom, each petal exists in superposition until observed.",
        
        # Paraphrase
        "Dr. Chen walked through a garden where flowers existed in multiple states until observation collapsed their wave function.",
        
        # Song lyrics similarity
        "We dance in the glow of digital screens, hearts beating to the rhythm of binary code.",
        
        # Code similarity
        "def quicksort(arr): if len(arr) <= 1: return arr; pivot = arr[len(arr)//2]",
        
        # No match expected
        "The weather today is sunny with a chance of rain in the afternoon.",
    ]
    
    print("\n" + "=" * 70)
    print("RUNNING TEST ANALYSES")
    print("=" * 70)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{'─' * 70}")
        print(f"TEST {i}: {text[:60]}...")
        print("─" * 70)
        
        report = system.analyze(text)
        
        print(f"Risk Level: {report.detection_summary['risk_level']}")
        print(f"Highest Similarity: {report.detection_summary['highest_similarity']:.2%}")
        print(f"Matches Found: {report.detection_summary['matches_found']}")
        print(f"Compliance Status: {report.compliance_assessment['status']}")
        print(f"Recommendation: {report.overall_recommendation[:100]}...")
        
        if report.attributions:
            print(f"\nTop Match: {report.attributions[0]['title']}")
            print(f"  Author: {report.attributions[0]['author']}")
            print(f"  Citation: {report.attributions[0]['citation']}")
    
    # Generate full report for first test
    print("\n" + "=" * 70)
    print("FULL REPORT EXAMPLE")
    print("=" * 70)
    
    full_report = system.get_formatted_report(test_texts[0])
    print(full_report)
    
    return system


if __name__ == "__main__":
    main()
