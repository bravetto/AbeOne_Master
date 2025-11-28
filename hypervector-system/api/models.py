"""
API Models

Pydantic models for request/response validation.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator


class VectorRequest(BaseModel):
    """Request model for adding/updating vectors."""
    vector: List[float] = Field(..., description="Vector as list of floats")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Optional metadata")
    vector_id: Optional[str] = Field(None, description="Optional custom vector ID")
    
    @validator('vector')
    def validate_vector(cls, v):
        if not v:
            raise ValueError("Vector cannot be empty")
        if not all(isinstance(x, (int, float)) for x in v):
            raise ValueError("Vector must contain only numbers")
        return v


class VectorResponse(BaseModel):
    """Response model for vector operations."""
    vector_id: str
    vector: Optional[List[float]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class SearchRequest(BaseModel):
    """Request model for vector search."""
    query_vector: List[float] = Field(..., description="Query vector")
    top_k: int = Field(10, ge=1, le=100, description="Number of results")
    min_score: float = Field(0.0, ge=0.0, le=1.0, description="Minimum similarity score")
    
    @validator('query_vector')
    def validate_query_vector(cls, v):
        if not v:
            raise ValueError("Query vector cannot be empty")
        if not all(isinstance(x, (int, float)) for x in v):
            raise ValueError("Query vector must contain only numbers")
        return v


class SearchResult(BaseModel):
    """Single search result."""
    vector_id: str
    score: float
    metadata: Optional[Dict[str, Any]] = None


class SearchResponse(BaseModel):
    """Response model for search operations."""
    results: List[SearchResult]
    count: int


class UpdateRequest(BaseModel):
    """Request model for updating vectors."""
    vector: Optional[List[float]] = Field(None, description="New vector")
    metadata: Optional[Dict[str, Any]] = Field(None, description="New metadata (merged)")


class StatsResponse(BaseModel):
    """Response model for system statistics."""
    count: int
    capacity: int
    dimension: int
    storage_path: str
    faiss_available: bool


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    version: str

