#!/usr/bin/env python3
"""
Initialize HyperVector Store

Script to initialize vector storage with specified dimensions and capacity.
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.hypervector.storage import HyperVectorStorage


def main():
    parser = argparse.ArgumentParser(description="Initialize HyperVector store")
    parser.add_argument(
        "--dimension",
        type=int,
        default=1024,
        help="Vector dimension (default: 1024)"
    )
    parser.add_argument(
        "--capacity",
        type=int,
        default=10000,
        help="Maximum capacity (default: 10000)"
    )
    parser.add_argument(
        "--storage-path",
        type=str,
        default=".hypervector",
        help="Storage path (default: .hypervector)"
    )
    
    args = parser.parse_args()
    
    print(f"🔥 Initializing HyperVector store...")
    print(f"   Dimension: {args.dimension}")
    print(f"   Capacity: {args.capacity}")
    print(f"   Storage Path: {args.storage_path}")
    
    try:
        storage = HyperVectorStorage(
            dimension=args.dimension,
            capacity=args.capacity,
            storage_path=args.storage_path
        )
        
        stats = storage.get_stats()
        print(f"\n✅ Store initialized successfully!")
        print(f"   Current count: {stats['count']}")
        print(f"   Capacity: {stats['capacity']}")
        print(f"   Dimension: {stats['dimension']}")
        
    except Exception as e:
        print(f"\n❌ Error initializing store: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

