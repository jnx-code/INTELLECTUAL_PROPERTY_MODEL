from config import CONFIG, RISK
from dataclasses import dataclass
from typing import Dict, Any, List, Tuple

@dataclass
class DetectionResult:
    text: str
    matches: List[Dict[str, Any]]
    highest_similarity: float
    risk_level: str

class CopyrightDetector:
    """Core detection logic matching queries against the vector store."""
    
    def __init__(self, vector_store, embedding_engine):
        self.vector_store = vector_store
        self.embedding_engine = embedding_engine
        
    def detect(self, text: str, top_k: int = None) -> DetectionResult:
        if top_k is None:
            top_k = CONFIG.top_k_results
            
        query_embedding = self.embedding_engine.generate_embeddings([text])[0]
        matches = self.vector_store.search(query_embedding, top_k=top_k)
        
        if not matches:
            return DetectionResult(text, [], 0.0, RISK.NONE)
            
        highest_sim = matches[0]['similarity']
        
        if highest_sim >= CONFIG.high_risk_threshold:
            risk = RISK.HIGH
        elif highest_sim >= CONFIG.medium_risk_threshold:
            risk = RISK.MEDIUM
        elif highest_sim >= CONFIG.low_risk_threshold:
            risk = RISK.LOW
        else:
            risk = RISK.NONE
            
        return DetectionResult(text, matches, highest_sim, risk)
        
    def quick_check(self, text: str) -> Tuple[bool, str, float]:
        result = self.detect(text, top_k=1)
        has_issues = result.risk_level in [RISK.HIGH, RISK.MEDIUM, RISK.LOW]
        return has_issues, result.risk_level, result.highest_similarity
