# app/utils/pagination.py
from typing import Generic, TypeVar, List, Optional, Dict, Any
from pydantic import BaseModel
from fastapi import Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')

class PaginationParams(BaseModel):
    """Parameters for pagination"""
    page: int = Query(1, ge=1, description="Page number")
    size: int = Query(10, ge=1, le=100, description="Items per page")
    sort_by: Optional[str] = Query(None, description="Sort field")
    sort_order: str = Query("asc", regex="^(asc|desc)$", description="Sort order")

    @property
    def skip(self) -> int:
        """Calculate skip value for database query"""
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        """Get limit value for database query"""
        return self.size

class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response model"""
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_prev: bool

    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        page: int,
        size: int
    ) -> "PaginatedResponse[T]":
        """Create paginated response"""
        pages = (total + size - 1) // size  # Ceiling division
        has_next = page < pages
        has_prev = page > 1

        return cls(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages,
            has_next=has_next,
            has_prev=has_prev
        )

async def paginate_query(
    db: AsyncSession,
    query: select,
    pagination: PaginationParams
) -> PaginatedResponse:
    """Execute paginated query"""
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Apply sorting if specified
    if pagination.sort_by:
        sort_column = getattr(query.column_descriptions[0]['entity'], pagination.sort_by, None)
        if sort_column is not None:
            if pagination.sort_order == "desc":
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())

    # Apply pagination
    query = query.offset(pagination.skip).limit(pagination.limit)

    # Execute query
    result = await db.execute(query)
    items = result.scalars().all()

    return PaginatedResponse.create(
        items=items,
        total=total,
        page=pagination.page,
        size=pagination.size
    )

class SearchParams(BaseModel):
    """Parameters for search and filtering"""
    q: Optional[str] = Query(None, description="Search query")
    filters: Optional[Dict[str, Any]] = Query(None, description="Additional filters")

def apply_search_filters(
    query: select,
    search_params: SearchParams,
    search_fields: List[str]
) -> select:
    """Apply search filters to query"""
    if search_params.q:
        search_conditions = []
        for field in search_fields:
            # This is a simplified version - in practice you'd want more sophisticated search
            search_conditions.append(getattr(query.column_descriptions[0]['entity'], field).ilike(f"%{search_params.q}%"))
        if search_conditions:
            query = query.where(or_(*search_conditions))

    return query

# Common pagination dependencies
def get_pagination_params(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    sort_by: Optional[str] = Query(None, description="Sort field"),
    sort_order: str = Query("asc", regex="^(asc|desc)$", description="Sort order")
) -> PaginationParams:
    """Get pagination parameters"""
    return PaginationParams(
        page=page,
        size=size,
        sort_by=sort_by,
        sort_order=sort_order
    )

def get_search_params(
    q: Optional[str] = Query(None, description="Search query")
) -> SearchParams:
    """Get search parameters"""
    return SearchParams(q=q)
