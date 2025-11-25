#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CDF Genius Indexer - Multi-dimensional indexing and scoring
AI-friendly structure with semantic analysis
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class CDFGeniusIndexer:
    """Multi-dimensional genius indexing for CDF documents."""
    
    def __init__(self):
        self.technical_keywords = [
            'api', 'function', 'class', 'method', 'algorithm', 'code', 'programming',
            'python', 'javascript', 'typescript', 'react', 'node', 'database', 'sql',
            'architecture', 'system', 'design', 'implementation', 'framework', 'library'
        ]
        
        self.creative_keywords = [
            'design', 'creative', 'art', 'visual', 'aesthetic', 'beautiful', 'elegant',
            'inspiration', 'idea', 'concept', 'vision', 'story', 'narrative', 'brand',
            'color', 'typography', 'layout', 'composition', 'style', 'theme'
        ]
        
        self.strategic_keywords = [
            'strategy', 'plan', 'goal', 'objective', 'vision', 'mission', 'roadmap',
            'business', 'market', 'competition', 'growth', 'scaling', 'metrics', 'kpi',
            'analysis', 'insight', 'decision', 'priority', 'impact', 'value', 'roi'
        ]
    
    def analyze_content(self, content: str) -> Dict[str, float]:
        """Analyze content and return genius scores."""
        content_lower = content.lower()
        
        # Technical score
        technical_matches = sum(1 for keyword in self.technical_keywords if keyword in content_lower)
        technical_score = min(technical_matches / 10.0, 1.0)
        
        # Creative score
        creative_matches = sum(1 for keyword in self.creative_keywords if keyword in content_lower)
        creative_score = min(creative_matches / 10.0, 1.0)
        
        # Strategic score
        strategic_matches = sum(1 for keyword in self.strategic_keywords if keyword in content_lower)
        strategic_score = min(strategic_matches / 10.0, 1.0)
        
        return {
            "technical": round(technical_score, 2),
            "creative": round(creative_score, 2),
            "strategic": round(strategic_score, 2)
        }
    
    def index_document(self, cdf_path: Path) -> Dict[str, Any]:
        """Index a CDF document with genius scores."""
        content = cdf_path.read_text(encoding='utf-8')
        
        # Extract metadata
        metadata = {}
        if 'METADATA:' in content:
            metadata_start = content.find('METADATA:')
            metadata_lines = content[metadata_start:].split('\n')[:10]
            for line in metadata_lines:
                if ':' in line and not line.startswith('METADATA'):
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
        
        # Analyze content
        genius_scores = self.analyze_content(content)
        
        # Extract patterns
        patterns = self.extract_patterns(content)
        
        return {
            "cdf_id": f"{cdf_path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "path": str(cdf_path),
            "metadata": metadata,
            "genius_index": genius_scores,
            "patterns": patterns,
            "indexed_at": datetime.now().isoformat()
        }
    
    def extract_patterns(self, content: str) -> List[str]:
        """Extract patterns from content."""
        patterns = []
        
        # Code blocks
        if '```' in content or 'CODE BLOCK' in content:
            patterns.append("code")
        
        # Lists
        if re.search(r'^\s*[-*]\s+', content, re.MULTILINE):
            patterns.append("lists")
        
        # Headers
        if re.search(r'^#{1,6}\s+', content, re.MULTILINE):
            patterns.append("structured")
        
        # Links
        if 'http' in content or 'www.' in content:
            patterns.append("linked")
        
        # Tables (if we add support)
        if '|' in content and content.count('|') > 5:
            patterns.append("tabular")
        
        return patterns
    
    def create_index(self, cdf_directory: Path) -> Dict[str, Any]:
        """Create index of all CDF files in directory."""
        index = {
            "index_version": "1.0",
            "created_at": datetime.now().isoformat(),
            "documents": []
        }
        
        for cdf_file in cdf_directory.glob("*.cdf"):
            doc_index = self.index_document(cdf_file)
            index["documents"].append(doc_index)
        
        return index
    
    def save_index(self, index: Dict[str, Any], output_path: Path):
        """Save index to JSON file."""
        output_path.write_text(
            json.dumps(index, indent=2),
            encoding='utf-8'
        )
        print(f"✅ Index saved to: {output_path}")


if __name__ == "__main__":
    import sys
    
    indexer = CDFGeniusIndexer()
    
    if len(sys.argv) < 2:
        print("Usage: python cdf_genius_indexer.py <cdf_file.cdf> [output.json]")
        print("   or: python cdf_genius_indexer.py <directory> [output.json]")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    
    if input_path.is_file():
        # Index single file
        doc_index = indexer.index_document(input_path)
        output_path = output_path or input_path.with_suffix('.index.json')
        output_path.write_text(
            json.dumps(doc_index, indent=2),
            encoding='utf-8'
        )
        print(f"✅ Indexed: {input_path}")
        print(f"   Technical: {doc_index['genius_index']['technical']}")
        print(f"   Creative: {doc_index['genius_index']['creative']}")
        print(f"   Strategic: {doc_index['genius_index']['strategic']}")
    
    elif input_path.is_dir():
        # Index directory
        index = indexer.create_index(input_path)
        output_path = output_path or input_path / "cdf_index.json"
        indexer.save_index(index, output_path)
        print(f"✅ Indexed {len(index['documents'])} documents")
    
    else:
        print(f"❌ Path not found: {input_path}")
        sys.exit(1)

