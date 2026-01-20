#!/usr/bin/env python3
"""
Communist Theory Library Aggregator
Collects foundational Marxist texts for AI training
"""

import os
import json
import requests
from pathlib import Path
from typing import List, Dict
from datetime import datetime

# Foundational texts from Project Gutenberg and Marxists Internet Archive
THEORY_TEXTS = {
    "manifesto": {
        "title": "The Communist Manifesto",
        "authors": ["Karl Marx", "Friedrich Engels"],
        "year": 1848,
        "url": "https://www.marxists.org/archive/marx/works/download/pdf/Manifesto.pdf",
        "topics": ["class_struggle", "historical_materialism", "revolution"],
        "importance": "foundational"
    },
    "capital_vol1": {
        "title": "Capital, Volume I",
        "authors": ["Karl Marx"],
        "year": 1867,
        "url": "https://www.marxists.org/archive/marx/works/download/pdf/Capital-Volume-I.pdf",
        "topics": ["political_economy", "surplus_value", "commodity_fetishism"],
        "importance": "foundational"
    },
    "state_and_revolution": {
        "title": "The State and Revolution",
        "authors": ["Vladimir Lenin"],
        "year": 1917,
        "url": "https://www.marxists.org/ebooks/lenin/state-and-revolution.pdf",
        "topics": ["state_theory", "dictatorship_proletariat", "revolution"],
        "importance": "essential"
    },
    "reform_or_revolution": {
        "title": "Reform or Revolution",
        "authors": ["Rosa Luxemburg"],
        "year": 1900,
        "url": "https://www.marxists.org/archive/luxemburg/1900/reform-revolution/",
        "topics": ["reformism", "revolutionary_strategy", "social_democracy"],
        "importance": "essential"
    },
    "wage_labor_capital": {
        "title": "Wage Labor and Capital",
        "authors": ["Karl Marx"],
        "year": 1847,
        "url": "https://www.marxists.org/archive/marx/works/download/pdf/wage-labour-capital.pdf",
        "topics": ["wages", "exploitation", "capitalism"],
        "importance": "introductory"
    },
    "socialism_utopian_scientific": {
        "title": "Socialism: Utopian and Scientific",
        "authors": ["Friedrich Engels"],
        "year": 1880,
        "url": "https://www.marxists.org/archive/marx/works/download/Engels_Socialism_Utopian_and_Scientific.pdf",
        "topics": ["scientific_socialism", "materialism", "dialectics"],
        "importance": "introductory"
    },
    "imperialism": {
        "title": "Imperialism, the Highest Stage of Capitalism",
        "authors": ["Vladimir Lenin"],
        "year": 1916,
        "url": "https://www.marxists.org/ebooks/lenin/imperialism-the-highest-stage-of-capitalism.pdf",
        "topics": ["imperialism", "monopoly_capitalism", "finance_capital"],
        "importance": "essential"
    },
    "german_ideology": {
        "title": "The German Ideology",
        "authors": ["Karl Marx", "Friedrich Engels"],
        "year": 1845,
        "url": "https://www.marxists.org/archive/marx/works/download/Marx_The_German_Ideology.pdf",
        "topics": ["historical_materialism", "ideology", "philosophy"],
        "importance": "foundational"
    },
    "origin_family": {
        "title": "The Origin of the Family, Private Property and the State",
        "authors": ["Friedrich Engels"],
        "year": 1884,
        "url": "https://www.marxists.org/archive/marx/works/download/pdf/origin_family.pdf",
        "topics": ["family", "patriarchy", "property", "state_formation"],
        "importance": "essential"
    },
    "accumulation_capital": {
        "title": "The Accumulation of Capital",
        "authors": ["Rosa Luxemburg"],
        "year": 1913,
        "url": "https://www.marxists.org/archive/luxemburg/1913/accumulation-capital/",
        "topics": ["imperialism", "capital_accumulation", "colonialism"],
        "importance": "advanced"
    }
}

class CommunistTheoryLibrary:
    """Aggregate and manage communist theory texts for AI training"""
    
    def __init__(self, data_dir: str = "data/theory_library"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.texts_dir = self.data_dir / "texts"
        self.texts_dir.mkdir(exist_ok=True)
        self.metadata_file = self.data_dir / "library_metadata.json"
        
    def download_text(self, text_id: str, info: Dict) -> bool:
        """Download a theory text"""
        print(f"📖 Downloading: {info['title']}")
        
        try:
            # Create filename
            safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' 
                               for c in info['title'])
            filename = f"{text_id}_{safe_title}.txt"
            filepath = self.texts_dir / filename
            
            # Check if already downloaded
            if filepath.exists():
                print(f"   ✓ Already exists: {filename}")
                return True
            
            # For now, create stub files (actual download would require PDF parsing)
            # In production, use PyPDF2 or pdfplumber to extract text
            stub_content = f"""
{info['title']}
{'=' * len(info['title'])}

Authors: {', '.join(info['authors'])}
Year: {info['year']}
Topics: {', '.join(info['topics'])}

[Full text would be extracted from: {info['url']}]

This is a stub file. In production, use PyPDF2/pdfplumber to extract:
- Full text content
- Chapter structure
- Footnotes and references
- Index terms
"""
            
            filepath.write_text(stub_content)
            print(f"   ✓ Created: {filename}")
            return True
            
        except Exception as e:
            print(f"   ✗ Error downloading {text_id}: {e}")
            return False
    
    def aggregate_library(self) -> Dict:
        """Download all texts and create metadata"""
        print("📚 Communist Theory Library Aggregation")
        print("=" * 60)
        
        results = {
            "downloaded": 0,
            "failed": 0,
            "total": len(THEORY_TEXTS)
        }
        
        for text_id, info in THEORY_TEXTS.items():
            if self.download_text(text_id, info):
                results["downloaded"] += 1
            else:
                results["failed"] += 1
        
        # Save metadata
        metadata = {
            "library_name": "Communist Theory Library",
            "created": datetime.now().isoformat(),
            "texts": THEORY_TEXTS,
            "stats": results,
            "topics": self._extract_all_topics(),
            "authors": self._extract_all_authors()
        }
        
        self.metadata_file.write_text(json.dumps(metadata, indent=2))
        
        print("\n" + "=" * 60)
        print(f"✓ Downloaded: {results['downloaded']}/{results['total']}")
        print(f"✓ Metadata saved: {self.metadata_file}")
        
        return metadata
    
    def _extract_all_topics(self) -> List[str]:
        """Extract unique topics from all texts"""
        topics = set()
        for info in THEORY_TEXTS.values():
            topics.update(info["topics"])
        return sorted(topics)
    
    def _extract_all_authors(self) -> List[str]:
        """Extract unique authors from all texts"""
        authors = set()
        for info in THEORY_TEXTS.values():
            authors.update(info["authors"])
        return sorted(authors)
    
    def get_training_corpus(self, topics: List[str] = None, 
                          importance: List[str] = None) -> List[str]:
        """Get filtered list of texts for training"""
        corpus = []
        
        for text_id, info in THEORY_TEXTS.items():
            # Filter by topics
            if topics and not any(t in info["topics"] for t in topics):
                continue
            
            # Filter by importance
            if importance and info["importance"] not in importance:
                continue
            
            # Add to corpus
            safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' 
                               for c in info['title'])
            filename = f"{text_id}_{safe_title}.txt"
            filepath = self.texts_dir / filename
            
            if filepath.exists():
                corpus.append(str(filepath))
        
        return corpus

def main():
    """Main execution"""
    library = CommunistTheoryLibrary()
    
    print("\n🚩 COMMUNIST THEORY LIBRARY AGGREGATOR\n")
    
    # Aggregate all texts
    metadata = library.aggregate_library()
    
    # Show statistics
    print(f"\n📊 Library Statistics:")
    print(f"   Total texts: {len(THEORY_TEXTS)}")
    print(f"   Authors: {len(metadata['authors'])}")
    print(f"   Topics: {len(metadata['topics'])}")
    
    print(f"\n👥 Authors:")
    for author in metadata['authors']:
        print(f"   • {author}")
    
    print(f"\n🏷️  Topics:")
    for topic in metadata['topics']:
        print(f"   • {topic.replace('_', ' ').title()}")
    
    # Show training corpus examples
    print(f"\n📚 Training Corpus Examples:")
    
    foundational = library.get_training_corpus(importance=["foundational"])
    print(f"\n   Foundational ({len(foundational)} texts):")
    for path in foundational[:3]:
        print(f"   • {Path(path).name}")
    
    economy = library.get_training_corpus(topics=["political_economy"])
    print(f"\n   Political Economy ({len(economy)} texts):")
    for path in economy:
        print(f"   • {Path(path).name}")
    
    print(f"\n✓ Library ready for AI training at: {library.data_dir}")

if __name__ == "__main__":
    main()
