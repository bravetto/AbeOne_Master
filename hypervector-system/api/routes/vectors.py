"""
Vector API Routes

Endpoints for vector operations.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List

from ..models import (
    VectorRequest,
    VectorResponse,
    SearchRequest,
    SearchResponse,
    SearchResult,
    UpdateRequest,
    StatsResponse
)
from ...src.hypervector.storage import HyperVectorStorage

router = APIRouter(prefix="/api/v1/vectors", tags=["vectors"])

# Global storage instance (initialized in main.py)
storage: HyperVectorStorage = None


def set_storage(storage_instance: HyperVectorStorage):
    """Set storage instance."""
    global storage
    storage = storage_instance


@router.post("", response_model=VectorResponse, status_code=status.HTTP_201_CREATED)
async def add_vector(request: VectorRequest):
    """
    Add a new vector.
    
    - **vector**: Vector as list of floats
    - **metadata**: Optional metadata dictionary
    - **vector_id**: Optional custom vector ID
    """
    if storage is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Storage not initialized"
        )
    
    try:
        vector_id = storage.add_vector(
            vector=request.vector,
            metadata=request.metadata,
            vector_id=request.vector_id
        )
        
        record = storage.get_vector(vector_id)
        return VectorResponse(
            vector_id=record.vector_id,
            vector=record.vector,
            metadata=record.metadata,
            created_at=record.created_at,
            updated_at=record.updated_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=str(e)
        )


@router.get("/{vector_id}", response_model=VectorResponse)
async def get_vector(vector_id: str):
    """
    Get vector by ID.
    
    - **vector_id**: Vector ID
    """
    if storage is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Storage not initialized"
        )
    
    record = storage.get_vector(vector_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vector {vector_id} not found"
        )
    
    return VectorResponse(
        vector_id=record.vector_id,
        vector=record.vector,
        metadata=record.metadata,
        created_at=record.created_at,
        updated_at=record.updated_at
    )


@router.put("/{vector_id}", response_model=VectorResponse)
async def update_vector(vector_id: str, request: UpdateRequest):
    """
    Update vector and/or metadata.
    
    - **vector_id**: Vector ID
    - **vector**: Optional new vector
    - **metadata**: Optional new metadata (merged with existing)
    """
    if storage is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Storage not initialized"
        )
    
    success = storage.update_vector(
        vector_id=vector_id,
        vector=request.vector,
        metadata=request.metadata
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vector {vector_id} not found"
        )
    
    record = storage.get_vector(vector_id)
    return VectorResponse(
        vector_id=record.vector_id,
        vector=record.vector,
        metadata=record.metadata,
        created_at=record.created_at,
        updated_at=record.updated_at
    )


@router.delete("/{vector_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vector(vector_id: str):
    """
    Delete vector by ID.
    
    - **vector_id**: Vector ID
    """
    if storage is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Storage not initialized"
        )
    
    success = storage.delete_vector(vector_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vector {vector_id} not found"
        )


@router.post("/search", response_model=SearchResponse)
async def search_vectors(request: SearchRequest):
    """
    Search for similar vectors.
    
    - **query_vector**: Query vector
    - **top_k**: Number of results (1-100)
    - **min_score**: Minimum similarity score (0.0-1.0)
    """
    if storage is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Storage not initialized"
        )
    
    try:
        results = storage.search(
            query_vector=request.query_vector,
            top_k=request.top_k,
            min_score=request.min_score
        )
        
        # Fetch metadata for results
        search_results = []
        for vector_id, score in results:
            record = storage.get_vector(vector_id)
            search_results.append(SearchResult(
                vector_id=vector_id,
                score=score,
                metadata=record.metadata if record else None
            ))
        
        return SearchResponse(
            results=search_results,
            count=len(search_results)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("", response_model=List[str])
async def list_vectors(limit: int = 100):
    """
    List all vector IDs.
    
    - **limit**: Maximum number of IDs to return
    """
    if storage is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Storage not initialized"
        )
    
    return storage.list_vectors(limit=limit)


@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get system statistics."""
    if storage is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Storage not initialized"
        )
    
    stats = storage.get_stats()
    return StatsResponse(**stats)

