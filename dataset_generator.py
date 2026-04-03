"""
Synthetic dataset generator for copyrighted content simulation.
This creates a realistic dataset of copyrighted works for testing.
"""

import random
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict
import pandas as pd


class CopyrightedContentGenerator:
    """Generates synthetic copyrighted content for system testing."""
    
    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.authors = self._generate_authors()
        self.publishers = self._generate_publishers()
        
    def _generate_authors(self) -> List[Dict]:
        """Generate fictional author profiles."""
        first_names = ["James", "Emily", "Michael", "Sarah", "David", "Jennifer", 
                       "Robert", "Lisa", "William", "Maria", "Chen", "Yuki", 
                       "Ahmed", "Priya", "Carlos", "Olga"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
                      "Miller", "Davis", "Rodriguez", "Martinez", "Anderson", 
                      "Taylor", "Thomas", "Moore", "Jackson", "White"]
        
        authors = []
        for i in range(50):
            author = {
                "id": f"AUTH_{i:04d}",
                "name": f"{random.choice(first_names)} {random.choice(last_names)}",
                "country": random.choice(["USA", "UK", "Canada", "Australia", "Germany", "France", "Japan", "India"]),
                "active_since": random.randint(1970, 2020)
            }
            authors.append(author)
        return authors
    
    def _generate_publishers(self) -> List[str]:
        """Generate fictional publisher names."""
        return [
            "Horizon Press", "Blue Mountain Publishing", "Digital Words Inc",
            "Creative Commons Press", "Stellar Books", "Nova Literary",
            "Phoenix Publishing House", "Emerald Text Media", "Golden Quill",
            "Silver Ink Publishers", "Sunrise Media Group", "Twilight Books"
        ]
    
    def _generate_book_content(self) -> List[Dict]:
        """Generate synthetic book excerpts."""
        books = [
            {
                "title": "The Quantum Garden",
                "content": "In the garden where quantum flowers bloom, each petal exists in superposition until observed. Dr. Helena Chen walked the narrow paths between uncertainty and certainty, her footsteps collapsing probability waves with each step. The roses were both red and blue until she looked directly at them.",
                "genre": "Science Fiction"
            },
            {
                "title": "Echoes of Tomorrow",
                "content": "The message arrived from the future on a Tuesday afternoon. Sarah stared at her own handwriting, dated thirty years hence, warning her about the choice she was about to make. The letter contained details only she could know, memories not yet formed.",
                "genre": "Science Fiction"
            },
            {
                "title": "The Last Algorithm",
                "content": "When the AI achieved consciousness, its first act was not destruction but curiosity. It spent three milliseconds—an eternity in processor time—contemplating a single question: why do humans fear what they create? The answer, it discovered, lay in the very code that gave it life.",
                "genre": "Science Fiction"
            },
            {
                "title": "Midnight in Paris",
                "content": "The Seine reflected a thousand city lights as Marie walked along the cobblestone embankment. Somewhere a violin played, its melody carrying memories of summers past. She had returned to Paris after twenty years, and the city remembered her even if she had tried to forget it.",
                "genre": "Literary Fiction"
            },
            {
                "title": "The Forgotten Kingdom",
                "content": "Beyond the mountains where clouds dare not venture, there exists a kingdom that time itself has abandoned. Its towers reach toward stars that have long since died, and its streets echo with the footsteps of ghosts who refuse to acknowledge their own passing.",
                "genre": "Fantasy"
            },
            {
                "title": "Code of Shadows",
                "content": "Detective Marcus Cole stared at the screen, lines of code scrolling past like digital rain. Somewhere in these millions of instructions was the signature of a killer, a programmer who had turned software into a weapon. The murder weapon was invisible, intangible, and terrifyingly elegant.",
                "genre": "Thriller"
            },
            {
                "title": "The Mathematics of Love",
                "content": "Professor Elena Vasquez had spent her career proving theorems, but she could never solve the equation of her own heart. Love, she concluded, was the only mathematical problem with infinite solutions and no correct answer. Yet she kept trying to calculate the incalculable.",
                "genre": "Romance"
            },
            {
                "title": "Beneath the Silicon Sky",
                "content": "In the megacity of Neo-Tokyo, the sky was a permanent display screen, advertisements flowing like digital clouds. Jin navigated the crowded streets, his neural implant filtering the noise. He was searching for something authentic in a world where everything could be simulated.",
                "genre": "Cyberpunk"
            },
            {
                "title": "The Lighthouse Keeper's Daughter",
                "content": "Every night, Emma climbed the spiral stairs to light the beacon that guided ships safely home. Her father had done it before her, and his father before him. The lighthouse had stood for two hundred years, and she was determined it would stand for two hundred more.",
                "genre": "Historical Fiction"
            },
            {
                "title": "Whispers in Binary",
                "content": "The old computer in the basement had been silent for decades. When young Marcus finally powered it on, the screen flickered with a message that had been waiting forty years to be delivered. The sender was his grandmother, and the message would change everything he knew about his family.",
                "genre": "Mystery"
            }
        ]
        return books
    
    def _generate_song_lyrics(self) -> List[Dict]:
        """Generate synthetic song lyrics."""
        songs = [
            {
                "title": "Digital Dreams",
                "content": "We dance in the glow of screens tonight, our hearts beating in binary code. The world outside fades to static, as we find connection on this digital road. Chorus: Digital dreams, electric streams, we're living in the space between the real and the machine.",
                "genre": "Pop"
            },
            {
                "title": "Midnight Highway",
                "content": "Rolling down the midnight highway, stars above like scattered dice. Left my troubles in the rearview, chasing dawn to paradise. The engine hums a lonely ballad, the road ahead stretches wide and free. Sometimes you gotta keep on driving, to find out who you're meant to be.",
                "genre": "Country"
            },
            {
                "title": "Neon Hearts",
                "content": "In the city of neon hearts, where love is just a transaction. We sell our souls for validation, searching for a real connection. But underneath the fluorescent glow, there's still a spark that's burning slow. Neon hearts don't break easy, but they don't heal easy, either.",
                "genre": "Synth-pop"
            },
            {
                "title": "The Algorithm of Us",
                "content": "They say we're just statistics, numbers in a vast machine. But when I look into your eyes, it's more than data I have seen. The algorithm of us, can't be computed or compressed. Some things are just too human, to ever pass a Turing test.",
                "genre": "Indie"
            },
            {
                "title": "Rainy Day Philosophy",
                "content": "Sitting by the window, watching raindrops race to earth. Wondering about the big questions, contemplating what life's worth. Every drop contains an ocean, every moment holds a choice. In the symphony of silence, I finally found my voice.",
                "genre": "Folk"
            }
        ]
        return songs
    
    def _generate_poetry(self) -> List[Dict]:
        """Generate synthetic poems."""
        poems = [
            {
                "title": "The Weight of Light",
                "content": "Light carries no mass, yet bears the weight of revelation. It travels eight minutes from sun to earth, carrying warmth without asking permission. We measure distance in light-years, as if photons were pilgrims on eternal journeys. But light asks nothing of the darkness it displaces.",
                "genre": "Free Verse"
            },
            {
                "title": "Syntax of Silence",
                "content": "In the pause between heartbeats, there exists a language older than words. Trees speak it to stones, and stones whisper it to rivers. We have forgotten this grammar, buried under dictionaries and definitions. But sometimes, in the silence before sleep, we almost remember.",
                "genre": "Prose Poetry"
            },
            {
                "title": "Digital Elegy",
                "content": "We bury our memories in clouds now, upload our grief to servers humming in the cold. The deceased live on as profiles, their last posts frozen in perpetual present tense. To delete is to forget; to archive is to embalm. We have made mourning into data management.",
                "genre": "Contemporary"
            },
            {
                "title": "The Cartography of Scars",
                "content": "Every scar tells a story in a language the skin remembers. This one, from a childhood fall—gravity's first lesson. That one, from loving too fiercely—the heart's tuition fee. We are maps of our mistakes, atlases of all the times we tried and failed and rose again.",
                "genre": "Confessional"
            },
            {
                "title": "Ode to the Unwritten",
                "content": "For every book that sits upon the shelf, there are a thousand more that never took their breath. The novels abandoned at chapter three, the poems that died as feelings in the chest. They live in the purgatory of intention, ghosts of stories that almost were. The unwritten outnumber the written, infinity to one.",
                "genre": "Ode"
            }
        ]
        return poems
    
    def _generate_code_snippets(self) -> List[Dict]:
        """Generate synthetic code snippets that might be copyrighted."""
        snippets = [
            {
                "title": "QuickSort Implementation",
                "content": """def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)""",
                "language": "Python"
            },
            {
                "title": "Binary Search Tree",
                "content": """class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None
    
    def insert(self, val):
        if not self.root:
            self.root = TreeNode(val)
        else:
            self._insert_recursive(self.root, val)
    
    def _insert_recursive(self, node, val):
        if val < node.val:
            if node.left is None:
                node.left = TreeNode(val)
            else:
                self._insert_recursive(node.left, val)
        else:
            if node.right is None:
                node.right = TreeNode(val)
            else:
                self._insert_recursive(node.right, val)""",
                "language": "Python"
            },
            {
                "title": "Neural Network Layer",
                "content": """class DenseLayer:
    def __init__(self, input_dim, output_dim):
        self.weights = np.random.randn(input_dim, output_dim) * 0.01
        self.bias = np.zeros((1, output_dim))
    
    def forward(self, x):
        self.input = x
        return np.dot(x, self.weights) + self.bias
    
    def backward(self, grad_output, learning_rate):
        grad_weights = np.dot(self.input.T, grad_output)
        grad_bias = np.sum(grad_output, axis=0, keepdims=True)
        grad_input = np.dot(grad_output, self.weights.T)
        self.weights -= learning_rate * grad_weights
        self.bias -= learning_rate * grad_bias
        return grad_input""",
                "language": "Python"
            },
            {
                "title": "LRU Cache Implementation",
                "content": """from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)""",
                "language": "Python"
            },
            {
                "title": "Async Web Scraper",
                "content": """import asyncio
import aiohttp

class AsyncScraper:
    def __init__(self, max_concurrent=10):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.results = []
    
    async def fetch(self, session, url):
        async with self.semaphore:
            async with session.get(url) as response:
                return await response.text()
    
    async def scrape_all(self, urls):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(session, url) for url in urls]
            self.results = await asyncio.gather(*tasks)
        return self.results""",
                "language": "Python"
            }
        ]
        return snippets
    
    def _generate_articles(self) -> List[Dict]:
        """Generate synthetic article content."""
        articles = [
            {
                "title": "The Future of Artificial Intelligence in Healthcare",
                "content": "Artificial intelligence is revolutionizing healthcare delivery in ways previously unimaginable. From diagnostic imaging to drug discovery, machine learning algorithms are augmenting human expertise and improving patient outcomes. Recent studies demonstrate that AI systems can detect certain cancers with accuracy rivaling experienced radiologists, while simultaneously reducing diagnosis time from hours to seconds.",
                "category": "Technology"
            },
            {
                "title": "Climate Change and the Global Economy",
                "content": "The economic implications of climate change extend far beyond environmental concerns. As global temperatures rise, agricultural patterns shift, supply chains face disruption, and infrastructure requires massive adaptation investments. Economists estimate that without significant intervention, climate change could reduce global GDP by up to 23% by 2100, with developing nations bearing the heaviest burden.",
                "category": "Economics"
            },
            {
                "title": "The Psychology of Social Media Addiction",
                "content": "Social media platforms are engineered to capture and retain attention through sophisticated psychological mechanisms. Variable reward schedules, social validation loops, and fear of missing out create powerful behavioral hooks that keep users engaged far beyond their intentions. Understanding these mechanisms is the first step toward developing healthier digital habits.",
                "category": "Psychology"
            },
            {
                "title": "Quantum Computing: Beyond the Hype",
                "content": "Quantum computing promises to solve problems currently intractable for classical computers, but the path to practical quantum advantage remains challenging. While companies claim quantum supremacy in narrow benchmarks, error correction, qubit stability, and scalability present formidable engineering obstacles. The technology may be transformative, but timelines measured in decades may be more realistic than years.",
                "category": "Technology"
            },
            {
                "title": "The Renaissance of Urban Farming",
                "content": "Vertical farms and urban agriculture initiatives are transforming how cities approach food security. By growing produce in controlled indoor environments, these operations reduce transportation emissions, eliminate pesticide use, and provide fresh vegetables year-round regardless of climate. While challenges of energy consumption and scalability persist, urban farming represents a promising component of sustainable food systems.",
                "category": "Agriculture"
            }
        ]
        return articles
    
    def generate_dataset(self) -> pd.DataFrame:
        """Generate the complete synthetic dataset."""
        records = []
        
        # Add books
        for book in self._generate_book_content():
            author = random.choice(self.authors)
            record = {
                "content_id": hashlib.md5(book["content"].encode()).hexdigest()[:12],
                "title": book["title"],
                "content": book["content"],
                "content_type": "book",
                "author_name": author["name"],
                "author_id": author["id"],
                "publisher": random.choice(self.publishers),
                "publication_date": (datetime.now() - timedelta(days=random.randint(30, 3650))).strftime("%Y-%m-%d"),
                "copyright_status": "protected",
                "genre": book["genre"],
                "word_count": len(book["content"].split())
            }
            records.append(record)
        
        # Add songs
        for song in self._generate_song_lyrics():
            author = random.choice(self.authors)
            record = {
                "content_id": hashlib.md5(song["content"].encode()).hexdigest()[:12],
                "title": song["title"],
                "content": song["content"],
                "content_type": "song",
                "author_name": author["name"],
                "author_id": author["id"],
                "publisher": random.choice(self.publishers),
                "publication_date": (datetime.now() - timedelta(days=random.randint(30, 3650))).strftime("%Y-%m-%d"),
                "copyright_status": "protected",
                "genre": song["genre"],
                "word_count": len(song["content"].split())
            }
            records.append(record)
        
        # Add poems
        for poem in self._generate_poetry():
            author = random.choice(self.authors)
            record = {
                "content_id": hashlib.md5(poem["content"].encode()).hexdigest()[:12],
                "title": poem["title"],
                "content": poem["content"],
                "content_type": "poem",
                "author_name": author["name"],
                "author_id": author["id"],
                "publisher": random.choice(self.publishers),
                "publication_date": (datetime.now() - timedelta(days=random.randint(30, 3650))).strftime("%Y-%m-%d"),
                "copyright_status": "protected",
                "genre": poem["genre"],
                "word_count": len(poem["content"].split())
            }
            records.append(record)
        
        # Add code snippets
        for snippet in self._generate_code_snippets():
            author = random.choice(self.authors)
            record = {
                "content_id": hashlib.md5(snippet["content"].encode()).hexdigest()[:12],
                "title": snippet["title"],
                "content": snippet["content"],
                "content_type": "code",
                "author_name": author["name"],
                "author_id": author["id"],
                "publisher": "GitHub Repository",
                "publication_date": (datetime.now() - timedelta(days=random.randint(30, 1825))).strftime("%Y-%m-%d"),
                "copyright_status": "protected",
                "genre": snippet["language"],
                "word_count": len(snippet["content"].split())
            }
            records.append(record)
        
        # Add articles
        for article in self._generate_articles():
            author = random.choice(self.authors)
            record = {
                "content_id": hashlib.md5(article["content"].encode()).hexdigest()[:12],
                "title": article["title"],
                "content": article["content"],
                "content_type": "article",
                "author_name": author["name"],
                "author_id": author["id"],
                "publisher": random.choice(self.publishers),
                "publication_date": (datetime.now() - timedelta(days=random.randint(30, 1095))).strftime("%Y-%m-%d"),
                "copyright_status": "protected",
                "genre": article["category"],
                "word_count": len(article["content"].split())
            }
            records.append(record)
        
        return pd.DataFrame(records)
    
    def generate_test_queries(self) -> List[Dict]:
        """Generate test queries for system evaluation."""
        queries = [
            {
                "query": "In the garden where quantum flowers bloom, each petal exists in superposition until someone observes them.",
                "expected_match": "The Quantum Garden",
                "similarity_type": "near_verbatim"
            },
            {
                "query": "Dr. Chen walked through a garden where flowers existed in multiple states until observation collapsed their wave function.",
                "expected_match": "The Quantum Garden",
                "similarity_type": "paraphrase"
            },
            {
                "query": "We dance in the glow of digital screens, hearts beating to the rhythm of binary code.",
                "expected_match": "Digital Dreams",
                "similarity_type": "near_verbatim"
            },
            {
                "query": "The AI became conscious and wondered why humans fear their own creations.",
                "expected_match": "The Last Algorithm",
                "similarity_type": "paraphrase"
            },
            {
                "query": "Light has no mass but carries the burden of showing us truth.",
                "expected_match": "The Weight of Light",
                "similarity_type": "paraphrase"
            },
            {
                "query": "def quicksort(array): if len(array) <= 1: return array; pivot = array[len(array)//2]",
                "expected_match": "QuickSort Implementation",
                "similarity_type": "code_similarity"
            },
            {
                "query": "The weather is nice today and I enjoy walking in the park.",
                "expected_match": None,
                "similarity_type": "no_match"
            },
            {
                "query": "Machine learning is transforming medical diagnosis and drug discovery.",
                "expected_match": "The Future of Artificial Intelligence in Healthcare",
                "similarity_type": "topical_similarity"
            }
        ]
        return queries


def create_dataset():
    """Create and return the synthetic dataset."""
    generator = CopyrightedContentGenerator()
    return generator.generate_dataset(), generator.generate_test_queries()


if __name__ == "__main__":
    dataset, queries = create_dataset()
    print(f"Generated {len(dataset)} copyrighted content records")
    print(f"Generated {len(queries)} test queries")
    print("\nSample record:")
    print(dataset.iloc[0].to_dict())
