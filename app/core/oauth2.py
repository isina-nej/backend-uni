# app/core/oauth2.py
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.config import settings

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Import here to avoid circular imports
from app.models.user import User, UserSession
from app.core.security import verify_token

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get current authenticated user from token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    # Get user from database
    async with get_db() as db:
        user = await db.get(User, int(user_id))
        if user is None:
            raise credentials_exception

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )

        return user

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

async def get_current_admin_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Get current admin user"""
    # Check if user has admin role
    async with get_db() as db:
        from app.models.user import UserRole, Role
        admin_role = await db.execute(
            select(Role).where(Role.code == "ADMIN")
        )
        admin_role = admin_role.scalar_one_or_none()

        if not admin_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin role not found"
            )

        user_role = await db.execute(
            select(UserRole).where(
                UserRole.user_id == current_user.id,
                UserRole.role_id == admin_role.id,
                UserRole.is_active == True
            )
        )
        user_role = user_role.scalar_one_or_none()

        if not user_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )

    return current_user

async def get_current_superuser(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Get current superuser"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Superuser access required"
        )
    return current_user

async def get_optional_current_user(
    token: Optional[str] = Depends(oauth2_scheme)
) -> Optional[User]:
    """Get current user if authenticated, None otherwise"""
    if not token:
        return None

    try:
        return await get_current_user(token)
    except HTTPException:
        return None

# Permission-based dependencies
def require_permission(permission_code: str):
    """Create a dependency that requires specific permission"""
    async def permission_dependency(
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db)
    ) -> User:
        # Check direct permissions
        from app.models.user import UserPermission, Permission
        user_perm = await db.execute(
            select(UserPermission).join(Permission).where(
                UserPermission.user_id == current_user.id,
                Permission.code == permission_code,
                UserPermission.is_active == True
            )
        )
        user_perm = user_perm.scalar_one_or_none()

        if user_perm:
            return current_user

        # Check role permissions
        from app.models.user import UserRole, RolePermission
        role_perm = await db.execute(
            select(RolePermission).join(UserRole).join(Permission).where(
                UserRole.user_id == current_user.id,
                Permission.code == permission_code,
                UserRole.is_active == True,
                RolePermission.is_active == True
            )
        )
        role_perm = role_perm.scalar_one_or_none()

        if role_perm:
            return current_user

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission required: {permission_code}"
        )

    return permission_dependency

def require_any_permission(*permission_codes: str):
    """Create a dependency that requires any of the specified permissions"""
    async def permission_dependency(
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db)
    ) -> User:
        for permission_code in permission_codes:
            try:
                # Check direct permissions
                from app.models.user import UserPermission, Permission
                user_perm = await db.execute(
                    select(UserPermission).join(Permission).where(
                        UserPermission.user_id == current_user.id,
                        Permission.code == permission_code,
                        UserPermission.is_active == True
                    )
                )
                user_perm = user_perm.scalar_one_or_none()

                if user_perm:
                    return current_user

                # Check role permissions
                from app.models.user import UserRole, RolePermission
                role_perm = await db.execute(
                    select(RolePermission).join(UserRole).join(Permission).where(
                        UserRole.user_id == current_user.id,
                        Permission.code == permission_code,
                        UserRole.is_active == True,
                        RolePermission.is_active == True
                    )
                )
                role_perm = role_perm.scalar_one_or_none()

                if role_perm:
                    return current_user
            except:
                continue

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"One of these permissions required: {', '.join(permission_codes)}"
        )

    return permission_dependency

def require_all_permissions(*permission_codes: str):
    """Create a dependency that requires all of the specified permissions"""
    async def permission_dependency(
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db)
    ) -> User:
        for permission_code in permission_codes:
            has_permission = False

            # Check direct permissions
            from app.models.user import UserPermission, Permission
            user_perm = await db.execute(
                select(UserPermission).join(Permission).where(
                    UserPermission.user_id == current_user.id,
                    Permission.code == permission_code,
                    UserPermission.is_active == True
                )
            )
            user_perm = user_perm.scalar_one_or_none()

            if user_perm:
                has_permission = True
            else:
                # Check role permissions
                from app.models.user import UserRole, RolePermission
                role_perm = await db.execute(
                    select(RolePermission).join(UserRole).join(Permission).where(
                        UserRole.user_id == current_user.id,
                        Permission.code == permission_code,
                        UserRole.is_active == True,
                        RolePermission.is_active == True
                    )
                )
                role_perm = role_perm.scalar_one_or_none()

                if role_perm:
                    has_permission = True

            if not has_permission:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"All permissions required: {', '.join(permission_codes)}"
                )

        return current_user

    return permission_dependency

def require_role(role_code: str):
    """Create a dependency that requires specific role"""
    async def role_dependency(
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db)
    ) -> User:
        from app.models.user import UserRole, Role
        user_role = await db.execute(
            select(UserRole).join(Role).where(
                UserRole.user_id == current_user.id,
                Role.code == role_code,
                UserRole.is_active == True
            )
        )
        user_role = user_role.scalar_one_or_none()

        if not user_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role required: {role_code}"
            )

        return current_user

    return role_dependency
