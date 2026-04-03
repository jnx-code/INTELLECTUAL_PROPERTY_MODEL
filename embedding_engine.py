import numpy as np
import os
import pickle
from typing import List, Union
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline

class EmbeddingEngine:
    """Generates embeddings for content using a trainable TF-IDF and SVD dimensional reduction."""
    
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.pipeline = make_pipeline(
            TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2)),
            TruncatedSVD(n_components=dimension, random_state=42)
        )
        self.is_trained = False
        
    def get_embedding_dimension(self) -> int:
        return self.dimension
        
    def train(self, contents: List[str]):
        """Fits the underlying ML model onto a corpus of text."""
        print(f"Training Model on {len(contents)} examples...")
        # SVD n_components can't be > n_samples-1
        max_dim = max(1, len(contents) - 1)
        if max_dim < self.dimension:
            self.pipeline.steps[1][1].n_components = max_dim
            self.dimension = max_dim
            
        self.pipeline.fit(contents)
        self.is_trained = True
        print(f"Training Complete. Resolved Dimensions: {self.dimension}")
        
    def save(self, path: str):
        if self.is_trained:
            os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
            with open(path, 'wb') as f:
                pickle.dump((self.pipeline, self.dimension), f)
            
    def load(self, path: str):
        if os.path.exists(path):
            with open(path, 'rb') as f:
                self.pipeline, self.dimension = pickle.load(f)
            self.is_trained = True
            
    def generate_embeddings(self, contents: Union[str, List[str]]) -> np.ndarray:
        if isinstance(contents, str):
            contents = [contents]
            
        if not self.is_trained:
            self.train(contents)
            
        embeddings = self.pipeline.transform(contents)
        
        # Normalizing vectors to unit length to ensure exact cosine-similarity bounds (0-1) length
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        embeddings = np.divide(embeddings, norms, out=np.zeros_like(embeddings), where=norms!=0)
        return embeddings
