"""
HyperVector SDK Client

Python client for HyperVector API.
"""

import requests
from typing import List, Dict, Any, Optional, Tuple
from urllib.parse import urljoin

from .exceptions import (
    HyperVectorAPIError,
    HyperVectorNotFoundError,
    HyperVectorValidationError
)


class HyperVectorClient:
    """
    Python SDK client for HyperVector API.
    
    Example:
        ```python
        client = HyperVectorClient(api_url="http://localhost:8000")
        vector_id = client.add_vector([0.1] * 1024, {"name": "test"})
        results = client.search([0.1] * 1024, top_k=10)
        ```
    """
    
    def __init__(
        self,
        api_url: str = "http://localhost:8000",
        timeout: int = 30
    ):
        """
        Initialize SDK client.
        
        Args:
            api_url: API base URL
            timeout: Request timeout in seconds
        """
        self.api_url = api_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
    
    def _request(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make API request.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            json_data: Optional JSON data
            params: Optional query parameters
        
        Returns:
            Response JSON
        
        Raises:
            HyperVectorAPIError: On API error
        """
        url = urljoin(self.api_url, endpoint)
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=json_data,
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 404:
                raise HyperVectorNotFoundError(
                    f"Resource not found: {endpoint}",
                    status_code=404
                )
            
            response.raise_for_status()
            
            if response.status_code == 204:  # No content
                return {}
            
            return response.json()
        
        except requests.exceptions.RequestException as e:
            if isinstance(e, HyperVectorNotFoundError):
                raise
            
            raise HyperVectorAPIError(
                f"API request failed: {str(e)}",
                status_code=getattr(e.response, 'status_code', None)
            )
    
    def add_vector(
        self,
        vector: List[float],
        metadata: Optional[Dict[str, Any]] = None,
        vector_id: Optional[str] = None
    ) -> str:
        """
        Add a new vector.
        
        Args:
            vector: Vector as list of floats
            metadata: Optional metadata dictionary
            vector_id: Optional custom vector ID
        
        Returns:
            Vector ID
        
        Raises:
            HyperVectorValidationError: On validation error
            HyperVectorAPIError: On API error
        """
        if not vector:
            raise HyperVectorValidationError("Vector cannot be empty")
        
        data = {
            "vector": vector,
            "metadata": metadata or {}
        }
        
        if vector_id:
            data["vector_id"] = vector_id
        
        try:
            response = self._request("POST", "/api/v1/vectors", json_data=data)
            return response["vector_id"]
        except HyperVectorAPIError as e:
            if e.status_code == 400:
                raise HyperVectorValidationError(str(e))
            raise
    
    def get_vector(self, vector_id: str) -> Dict[str, Any]:
        """
        Get vector by ID.
        
        Args:
            vector_id: Vector ID
        
        Returns:
            Vector record with metadata
        
        Raises:
            HyperVectorNotFoundError: If vector not found
            HyperVectorAPIError: On API error
        """
        return self._request("GET", f"/api/v1/vectors/{vector_id}")
    
    def update_vector(
        self,
        vector_id: str,
        vector: Optional[List[float]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Update vector and/or metadata.
        
        Args:
            vector_id: Vector ID
            vector: Optional new vector
            metadata: Optional new metadata (merged)
        
        Returns:
            Updated vector record
        
        Raises:
            HyperVectorNotFoundError: If vector not found
            HyperVectorAPIError: On API error
        """
        data = {}
        if vector is not None:
            data["vector"] = vector
        if metadata is not None:
            data["metadata"] = metadata
        
        return self._request("PUT", f"/api/v1/vectors/{vector_id}", json_data=data)
    
    def delete_vector(self, vector_id: str) -> bool:
        """
        Delete vector by ID.
        
        Args:
            vector_id: Vector ID
        
        Returns:
            True if deleted
        
        Raises:
            HyperVectorNotFoundError: If vector not found
            HyperVectorAPIError: On API error
        """
        try:
            self._request("DELETE", f"/api/v1/vectors/{vector_id}")
            return True
        except HyperVectorNotFoundError:
            return False
    
    def search(
        self,
        query_vector: List[float],
        top_k: int = 10,
        min_score: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors.
        
        Args:
            query_vector: Query vector
            top_k: Number of results (default: 10)
            min_score: Minimum similarity score (default: 0.0)
        
        Returns:
            List of search results with vector_id, score, and metadata
        
        Raises:
            HyperVectorValidationError: On validation error
            HyperVectorAPIError: On API error
        """
        if not query_vector:
            raise HyperVectorValidationError("Query vector cannot be empty")
        
        data = {
            "query_vector": query_vector,
            "top_k": top_k,
            "min_score": min_score
        }
        
        try:
            response = self._request("POST", "/api/v1/vectors/search", json_data=data)
            return response["results"]
        except HyperVectorAPIError as e:
            if e.status_code == 400:
                raise HyperVectorValidationError(str(e))
            raise
    
    def list_vectors(self, limit: Optional[int] = None) -> List[str]:
        """
        List all vector IDs.
        
        Args:
            limit: Optional limit on number of IDs
        
        Returns:
            List of vector IDs
        
        Raises:
            HyperVectorAPIError: On API error
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        
        return self._request("GET", "/api/v1/vectors", params=params)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get system statistics.
        
        Returns:
            Statistics dictionary
        
        Raises:
            HyperVectorAPIError: On API error
        """
        return self._request("GET", "/api/v1/vectors/stats")
    
    def health_check(self) -> Dict[str, str]:
        """
        Check API health.
        
        Returns:
            Health status dictionary
        
        Raises:
            HyperVectorAPIError: On API error
        """
        return self._request("GET", "/api/v1/health")
    
    def batch_add_vectors(
        self,
        vectors: List[Tuple[List[float], Optional[Dict[str, Any]]]]
    ) -> List[str]:
        """
        Add multiple vectors in batch.
        
        Args:
            vectors: List of (vector, metadata) tuples
        
        Returns:
            List of vector IDs
        
        Raises:
            HyperVectorAPIError: On API error
        """
        vector_ids = []
        for vector, metadata in vectors:
            vector_id = self.add_vector(vector, metadata)
            vector_ids.append(vector_id)
        return vector_ids

