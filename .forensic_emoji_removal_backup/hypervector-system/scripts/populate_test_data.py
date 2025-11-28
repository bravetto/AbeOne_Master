#!/usr/bin/env python3
"""
Populate Test Data

Script to populate vector store with test vectors.
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.hypervector.storage import HyperVectorStorage
from src.hypervector.utils import generate_random_vector


def main():
    parser = argparse.ArgumentParser(description="Populate HyperVector store with test data")
    parser.add_argument(
        "--count",
        type=int,
        default=100,
        help="Number of vectors to generate (default: 100)"
    )
    parser.add_argument(
        "--dimension",
        type=int,
        default=1024,
        help="Vector dimension (default: 1024)"
    )
    parser.add_argument(
        "--storage-path",
        type=str,
        default=".hypervector",
        help="Storage path (default: .hypervector)"
    )
    
    args = parser.parse_args()
    
    print(f"🔥 Populating HyperVector store...")
    print(f"   Count: {args.count}")
    print(f"   Dimension: {args.dimension}")
    print(f"   Storage Path: {args.storage_path}")
    
    try:
        storage = HyperVectorStorage(
            dimension=args.dimension,
            capacity=10000,
            storage_path=args.storage_path
        )
        
        print(f"\n📊 Generating {args.count} vectors...")
        for i in range(args.count):
            vector = generate_random_vector(args.dimension)
            metadata = {
                "index": i,
                "name": f"test_vector_{i}",
                "category": "test"
            }
            vector_id = storage.add_vector(vector, metadata)
            
            if (i + 1) % 10 == 0:
                print(f"   Generated {i + 1}/{args.count} vectors...")
        
        stats = storage.get_stats()
        print(f"\n✅ Test data populated successfully!")
        print(f"   Total vectors: {stats['count']}")
        
    except Exception as e:
        print(f"\n❌ Error populating data: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

