# app/dependencies.py
from typing import Optional, List, Dict, Any
from fastapi import Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, and_
import jwt

from app.database import get_db
from app.config import settings
from app.models.user import User, UserSession
from app.core.security import verify_token

# Database dependency
async def get_database(db: AsyncSession = Depends(get_db)):
    """Database session dependency"""
    return db

# Authentication dependencies
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = await db.get(User, int(user_id))
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    return user

async def get_current_user_optional(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """Get current user if authenticated, None otherwise"""
    try:
        return await get_current_user(request, db)
    except:
        return None

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

# Permission dependencies
async def require_permission(permission_code: str):
    """Check if user has specific permission"""
    def permission_checker(
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db)
    ):
        # Check user permissions
        user_permissions = await db.execute(
            select(UserPermission)
            .where(UserPermission.user_id == current_user.id)
            .where(UserPermission.is_active == True)
        )
        user_permissions = user_permissions.scalars().all()

        # Check role permissions
        user_roles = await db.execute(
            select(UserRole)
            .where(UserRole.user_id == current_user.id)
            .where(UserRole.is_active == True)
        )
        user_roles = user_roles.scalars().all()

        role_permissions = []
        for role in user_roles:
            role_perms = await db.execute(
                select(RolePermission)
                .where(RolePermission.role_id == role.role_id)
                .where(RolePermission.is_active == True)
            )
            role_permissions.extend(role_perms.scalars().all())

        # Check if user has the required permission
        all_permissions = user_permissions + role_permissions
        for perm in all_permissions:
            if perm.permission.code == permission_code:
                return current_user

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission denied: {permission_code}"
        )

    return permission_checker

# Pagination dependency
def get_pagination(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page")
) -> dict:
    """Pagination parameters"""
    return {
        "page": page,
        "size": size,
        "skip": (page - 1) * size,
        "limit": size
    }

# Search dependency
def get_search_filters(
    search: Optional[str] = Query(None, description="Search query"),
    sort_by: Optional[str] = Query(None, description="Sort field"),
    sort_order: str = Query("asc", regex="^(asc|desc)$", description="Sort order")
) -> dict:
    """Search and sort parameters"""
    return {
        "search": search,
        "sort_by": sort_by,
        "sort_order": sort_order
    }

# Common query builders
def apply_search_filters(query, search_fields: List[str], search: str):
    """Apply search filters to query"""
    if search:
        search_conditions = []
        for field in search_fields:
            search_conditions.append(getattr(Model, field).ilike(f"%{search}%"))
        query = query.where(or_(*search_conditions))
    return query

def apply_sorting(query, sort_by: str, sort_order: str, default_sort: str = "id"):
    """Apply sorting to query"""
    if sort_by:
        sort_column = getattr(Model, sort_by, None)
        if sort_column is not None:
            if sort_order == "desc":
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())
        else:
            # Default sorting
            default_column = getattr(Model, default_sort)
            query = query.order_by(default_column.asc())
    else:
        # Default sorting
        default_column = getattr(Model, default_sort)
        query = query.order_by(default_column.asc())

    return query
