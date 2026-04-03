import numpy as np
import pandas as pd
import json
import os
from typing import Dict, List, Any

class CopyrightVectorStore:
    """Vector database for copyrighted content."""
    
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.vectors = None
        self.metadata = []
        
    def load(self, path: str):
        vectors_path = os.path.join(path, "vectors.npy")
        metadata_path = os.path.join(path, "metadata.json")
        if os.path.exists(vectors_path) and os.path.exists(metadata_path):
            self.vectors = np.load(vectors_path)
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
                
    def add_from_dataframe(self, dataset: pd.DataFrame, embeddings: np.ndarray):
        self.vectors = embeddings
        # Replace NaN with None for json serialization
        dataset = dataset.replace({np.nan: None})
        self.metadata = dataset.to_dict('records')
        
    def save(self, path: str):
        os.makedirs(path, exist_ok=True)
        if self.vectors is not None:
            np.save(os.path.join(path, "vectors.npy"), self.vectors)
        if self.metadata:
            with open(os.path.join(path, "metadata.json"), 'w') as f:
                json.dump(self.metadata, f)
                
    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_vectors": len(self.metadata) if self.metadata else 0,
            "dimension": self.dimension
        }
        
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        if self.vectors is None or len(self.metadata) == 0:
            return []
            
        # Cosine similarity (vectors are assumed to be normalized)
        similarities = np.dot(self.vectors, query_embedding)
        
        # Get top k indices using argsort and reversing logic
        # For a single query_embedding against multiple stored vectors
        if len(self.metadata) < top_k:
            top_k = len(self.metadata)
            
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            res = self.metadata[idx].copy()
            res['similarity'] = float(similarities[idx])
            results.append(res)
            
        return results
