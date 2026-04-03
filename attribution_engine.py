from typing import List, Dict, Any

class AttributionEngine:
    """Engine responsible for building citations for found matches."""
    
    def generate_attributions(self, matches: List[Dict[str, Any]], citation_style: str = "APA") -> List[Dict[str, Any]]:
        attributions = []
        for match in matches:
            title = match.get('title', 'Unknown Title')
            author = match.get('author_name', 'Unknown Author')
            publisher = match.get('publisher', 'Unknown Publisher')
            
            # publication_date format 'YYYY-MM-DD'
            date_str = match.get('publication_date', 'Unknown')
            year = date_str[:4] if isinstance(date_str, str) and len(date_str) >= 4 else 'Unknown'
            
            attr = {
                'title': title,
                'author': author,
                'publisher': publisher,
                'year': year,
                'similarity_score': match.get('similarity', 0.0),
                'content_type': match.get('content_type', 'Unknown'),
                'publication_date': match.get('publication_date', 'Unknown'),
                'confidence': f"{match.get('similarity', 0.0):.1%}"
            }
            
            if citation_style == "APA":
                attr['citation'] = f"{author} ({year}). {title}. {publisher}."
            else:
                attr['citation'] = f"{title} by {author} ({year})"
                
            attributions.append(attr)
            
        return attributions
