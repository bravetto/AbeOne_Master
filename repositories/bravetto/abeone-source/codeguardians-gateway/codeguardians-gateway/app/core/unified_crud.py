"""
Unified CRUD Operations - Convergent Emergence

EEAaO: Everything Everywhere All at Once
- Single source of truth for CRUD operations
- Elegant convergence of patterns
- 20% code reduction through unification
- Natural flow like water to ocean
"""

from typing import TypeVar, Type, List, Optional, Dict, Any, Generic
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import selectinload
from pydantic import BaseModel

from app.core.database import get_db
from app.core.models import Base
from app.core.error_exporter import get_error_exporter
from app.utils.logging import get_logger

logger = get_logger(__name__)

T = TypeVar('T', bound=Base)
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)
ResponseSchema = TypeVar('ResponseSchema', bound=BaseModel)


class UnifiedCRUD(Generic[T, CreateSchema, UpdateSchema, ResponseSchema]):
    """
    Unified CRUD operations - convergent emergence of all patterns.
    
    EEAaO: Single elegant solution for all CRUD needs
    Water flow: Natural, simple, powerful
    """
    
    def __init__(
        self,
        model: Type[T],
        create_schema: Type[CreateSchema],
        update_schema: Type[UpdateSchema],
        response_schema: Type[ResponseSchema],
        router: APIRouter,
        prefix: str = "",
        tags: List[str] = None,
        dependencies: List = None,
        relationships: List[str] = None
    ):
        self.model = model
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.response_schema = response_schema
        self.router = router
        self.prefix = prefix
        self.tags = tags or []
        self.dependencies = dependencies or []
        self.relationships = relationships or []
        self.error_exporter = get_error_exporter()
        
        # Register routes - convergent emergence
        self._register_routes()
    
    def _register_routes(self):
        """Register all CRUD routes - elegant convergence."""
        base_path = f"{self.prefix}" if self.prefix else ""
        
        # List - with pagination and filtering
        @self.router.get(
            f"{base_path}/",
            response_model=Dict[str, Any],
            summary=f"List {self.model.__name__}s",
            tags=self.tags,
            dependencies=self.dependencies
        )
        async def list_items(
            skip: int = Query(0, ge=0),
            limit: int = Query(100, ge=1, le=1000),
            filters: Optional[str] = Query(None),
            db: AsyncSession = Depends(get_db)
        ):
            """List items with pagination and filtering."""
            try:
                query = select(self.model)
                
                # Apply filters if provided
                if filters:
                    query = self._apply_filters(query, filters)
                
                # Count total
                count_query = select(func.count()).select_from(query.subquery())
                total = (await db.execute(count_query)).scalar() or 0
                
                # Apply pagination
                query = query.offset(skip).limit(limit)
                
                # Load relationships if specified
                if self.relationships:
                    for rel in self.relationships:
                        query = query.options(selectinload(getattr(self.model, rel)))
                
                result = await db.execute(query)
                items = result.scalars().all()
                
                return {
                    "items": [self._to_response(item) for item in items],
                    "total": total,
                    "skip": skip,
                    "limit": limit
                }
            except Exception as e:
                self.error_exporter.export_error(
                    e,
                    context={"operation": "list_items", "model": self.model.__name__},
                    error_code="LIST_ERROR"
                )
                raise HTTPException(status_code=500, detail=str(e))
        
        # Get by ID
        @self.router.get(
            f"{base_path}/{{item_id}}",
            response_model=ResponseSchema,
            summary=f"Get {self.model.__name__} by ID",
            tags=self.tags,
            dependencies=self.dependencies
        )
        async def get_item(
            item_id: int,
            db: AsyncSession = Depends(get_db)
        ):
            """Get item by ID."""
            try:
                query = select(self.model).where(self.model.id == item_id)
                
                # Load relationships
                if self.relationships:
                    for rel in self.relationships:
                        query = query.options(selectinload(getattr(self.model, rel)))
                
                result = await db.execute(query)
                item = result.scalar_one_or_none()
                
                if not item:
                    raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
                
                return self._to_response(item)
            except HTTPException:
                raise
            except Exception as e:
                self.error_exporter.export_error(
                    e,
                    context={"operation": "get_item", "model": self.model.__name__, "item_id": item_id},
                    error_code="GET_ERROR"
                )
                raise HTTPException(status_code=500, detail=str(e))
        
        # Create
        @self.router.post(
            f"{base_path}/",
            response_model=ResponseSchema,
            status_code=201,
            summary=f"Create {self.model.__name__}",
            tags=self.tags,
            dependencies=self.dependencies
        )
        async def create_item(
            item_data: CreateSchema,
            db: AsyncSession = Depends(get_db)
        ):
            """Create new item."""
            try:
                item_dict = item_data.dict(exclude_unset=True)
                item = self.model(**item_dict)
                db.add(item)
                await db.commit()
                await db.refresh(item)
                
                return self._to_response(item)
            except Exception as e:
                await db.rollback()
                self.error_exporter.export_error(
                    e,
                    context={"operation": "create_item", "model": self.model.__name__},
                    error_code="CREATE_ERROR"
                )
                raise HTTPException(status_code=500, detail=str(e))
        
        # Update
        @self.router.patch(
            f"{base_path}/{{item_id}}",
            response_model=ResponseSchema,
            summary=f"Update {self.model.__name__}",
            tags=self.tags,
            dependencies=self.dependencies
        )
        async def update_item(
            item_id: int,
            item_data: UpdateSchema,
            db: AsyncSession = Depends(get_db)
        ):
            """Update item."""
            try:
                result = await db.execute(
                    select(self.model).where(self.model.id == item_id)
                )
                item = result.scalar_one_or_none()
                
                if not item:
                    raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
                
                update_data = item_data.dict(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(item, key, value)
                
                await db.commit()
                await db.refresh(item)
                
                return self._to_response(item)
            except HTTPException:
                raise
            except Exception as e:
                await db.rollback()
                self.error_exporter.export_error(
                    e,
                    context={"operation": "update_item", "model": self.model.__name__, "item_id": item_id},
                    error_code="UPDATE_ERROR"
                )
                raise HTTPException(status_code=500, detail=str(e))
        
        # Delete
        @self.router.delete(
            f"{base_path}/{{item_id}}",
            status_code=204,
            summary=f"Delete {self.model.__name__}",
            tags=self.tags,
            dependencies=self.dependencies
        )
        async def delete_item(
            item_id: int,
            db: AsyncSession = Depends(get_db)
        ):
            """Delete item."""
            try:
                result = await db.execute(
                    select(self.model).where(self.model.id == item_id)
                )
                item = result.scalar_one_or_none()
                
                if not item:
                    raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
                
                await db.delete(item)
                await db.commit()
                
                return None
            except HTTPException:
                raise
            except Exception as e:
                await db.rollback()
                self.error_exporter.export_error(
                    e,
                    context={"operation": "delete_item", "model": self.model.__name__, "item_id": item_id},
                    error_code="DELETE_ERROR"
                )
                raise HTTPException(status_code=500, detail=str(e))
    
    def _apply_filters(self, query, filters: str):
        """Apply filters to query - elegant parsing."""
        # Simple filter format: "field1:value1,field2:value2"
        # Can be extended for more complex filtering
        filter_pairs = filters.split(',')
        for pair in filter_pairs:
            if ':' in pair:
                field, value = pair.split(':', 1)
                if hasattr(self.model, field):
                    query = query.where(getattr(self.model, field) == value)
        return query
    
    def _to_response(self, item: T) -> Dict[str, Any]:
        """Convert model to response schema - elegant transformation."""
        return self.response_schema.from_orm(item).dict()


def create_unified_crud(
    model: Type[T],
    create_schema: Type[CreateSchema],
    update_schema: Type[UpdateSchema],
    response_schema: Type[ResponseSchema],
    router: APIRouter,
    prefix: str = "",
    tags: List[str] = None,
    dependencies: List = None,
    relationships: List[str] = None
) -> UnifiedCRUD:
    """
    Create unified CRUD operations - water flow to ocean.
    
    EEAaO: Convergent emergence of all CRUD patterns
    """
    return UnifiedCRUD(
        model=model,
        create_schema=create_schema,
        update_schema=update_schema,
        response_schema=response_schema,
        router=router,
        prefix=prefix,
        tags=tags,
        dependencies=dependencies,
        relationships=relationships
    )

