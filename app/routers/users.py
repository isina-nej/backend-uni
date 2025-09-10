# app/routers/users.py
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_

from app.database import get_db
from app.models.user import User, Role, Permission, UserRole, UserPermission
from app.schemas.user import (
    UserCreate, UserUpdate, UserResponse, UserLogin, TokenResponse,
    RefreshTokenRequest, ChangePasswordRequest, UserProfileResponse,
    RoleCreate, RoleUpdate, RoleResponse,
    PermissionCreate, PermissionUpdate, PermissionResponse,
    UserRoleAssignment, UserRoleResponse,
    UserPermissionAssignment, UserPermissionResponse,
    RolePermissionAssignment, RolePermissionResponse
)
from app.core.auth import (
    authenticate_user, create_user_session, get_current_user,
    refresh_access_token, logout_user
)
from app.core.security import hash_password, verify_password
from app.dependencies import get_pagination, get_search_filters

router = APIRouter()

# Authentication endpoints
@router.post("/auth/login", response_model=TokenResponse)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """Authenticate user and return access token"""
    user = await authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create user session
    session = await create_user_session(db, user)

    return TokenResponse(
        access_token=session.session_token,
        refresh_token=session.refresh_token,
        expires_in=30 * 60,  # 30 minutes
        user=UserResponse.from_orm(user)
    )

@router.post("/auth/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """Refresh access token using refresh token"""
    access_token = await refresh_access_token(refresh_data.refresh_token, db)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    # Get user from token
    from app.core.auth import get_current_user
    user = await get_current_user(access_token)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_data.refresh_token,
        expires_in=30 * 60,
        user=UserResponse.from_orm(user)
    )

@router.post("/auth/logout")
async def logout(
    token: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Logout user by invalidating session"""
    success = await logout_user(token, db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid session"
        )

    return {"message": "Successfully logged out"}

# User management endpoints
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new user"""
    # Check if user already exists
    existing_user = await db.execute(
        select(User).where(
            or_(User.email == user_data.email, User.username == user_data.username)
        )
    )
    existing_user = existing_user.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists"
        )

    # Create user
    user = User(**user_data.dict(exclude={'password'}))
    user.created_by = current_user.id
    user.updated_by = current_user.id

    db.add(user)
    await db.flush()

    # Create password
    from app.models.user import UserPassword
    password = UserPassword(
        user_id=user.id,
        password_hash=hash_password(user_data.password),
        last_changed=datetime.utcnow()
    )
    db.add(password)

    await db.commit()
    await db.refresh(user)

    return UserResponse.from_orm(user)

@router.get("/", response_model=List[UserResponse])
async def get_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    pagination: dict = Depends(get_pagination),
    search_filters: dict = Depends(get_search_filters),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    role_id: Optional[int] = Query(None, description="Filter by role ID")
):
    """Get list of users with pagination and filtering"""
    query = select(User)

    # Apply filters
    if is_active is not None:
        query = query.where(User.is_active == is_active)

    if role_id:
        query = query.join(UserRole).where(
            and_(UserRole.role_id == role_id, UserRole.is_active == True)
        )

    # Apply search
    if search_filters.get("search"):
        search_term = f"%{search_filters['search']}%"
        query = query.where(
            or_(
                User.email.ilike(search_term),
                User.first_name.ilike(search_term),
                User.last_name.ilike(search_term),
                User.username.ilike(search_term)
            )
        )

    # Apply sorting
    if search_filters.get("sort_by"):
        sort_column = getattr(User, search_filters["sort_by"], None)
        if sort_column:
            if search_filters["sort_order"] == "desc":
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())

    # Apply pagination
    query = query.offset(pagination["skip"]).limit(pagination["limit"])

    result = await db.execute(query)
    users = result.scalars().all()

    return [UserResponse.from_orm(user) for user in users]

@router.get("/profile", response_model=UserProfileResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user profile with roles and permissions"""
    # Get user roles
    roles_query = select(UserRole).where(
        and_(UserRole.user_id == current_user.id, UserRole.is_active == True)
    ).options(
        # Include role details
    )

    roles_result = await db.execute(roles_query)
    user_roles = roles_result.scalars().all()

    # Get user permissions
    permissions_query = select(UserPermission).where(
        and_(UserPermission.user_id == current_user.id, UserPermission.is_active == True)
    )

    permissions_result = await db.execute(permissions_query)
    user_permissions = permissions_result.scalars().all()

    # Create response
    response = UserProfileResponse.from_orm(current_user)
    response.roles = [UserRoleResponse.from_orm(role) for role in user_roles]
    response.permissions = [UserPermissionResponse.from_orm(perm) for perm in user_permissions]

    return response

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user by ID"""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse.from_orm(user)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user information"""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check if email/username is already taken by another user
    if user_data.email or user_data.username:
        existing_query = select(User).where(User.id != user_id)
        if user_data.email:
            existing_query = existing_query.where(User.email == user_data.email)
        if user_data.username:
            existing_query = existing_query.where(User.username == user_data.username)

        existing_user = await db.execute(existing_query)
        existing_user = existing_user.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or username already taken"
            )

    # Update user
    for field, value in user_data.dict(exclude_unset=True).items():
        if hasattr(user, field):
            setattr(user, field, value)

    user.updated_by = current_user.id
    user.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(user)

    return UserResponse.from_orm(user)

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Soft delete user (deactivate)"""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.is_active = False
    user.updated_by = current_user.id
    user.updated_at = datetime.utcnow()

    await db.commit()

    return {"message": "User deactivated successfully"}

@router.post("/{user_id}/change-password")
async def change_password(
    user_id: int,
    password_data: ChangePasswordRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Change user password"""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Verify current password
    user_password = await db.execute(
        select(UserPassword)
        .where(UserPassword.user_id == user_id)
        .where(UserPassword.is_active == True)
    )
    user_password = user_password.scalar_one_or_none()

    if not user_password or not verify_password(password_data.current_password, user_password.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    # Update password
    user_password.is_active = False
    user_password.expires_at = datetime.utcnow()

    new_password = UserPassword(
        user_id=user_id,
        password_hash=hash_password(password_data.new_password),
        last_changed=datetime.utcnow()
    )

    db.add(new_password)
    await db.commit()

    return {"message": "Password changed successfully"}

# Role management endpoints
@router.post("/roles/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new role"""
    # Check if role code already exists
    existing_role = await db.execute(
        select(Role).where(Role.code == role_data.code)
    )
    existing_role = existing_role.scalar_one_or_none()

    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role with this code already exists"
        )

    role = Role(**role_data.dict())
    role.created_by = current_user.id
    role.updated_by = current_user.id

    db.add(role)
    await db.commit()
    await db.refresh(role)

    return RoleResponse.from_orm(role)

@router.get("/roles/", response_model=List[RoleResponse])
async def get_roles(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    pagination: dict = Depends(get_pagination),
    search_filters: dict = Depends(get_search_filters)
):
    """Get list of roles"""
    query = select(Role)

    # Apply search
    if search_filters.get("search"):
        search_term = f"%{search_filters['search']}%"
        query = query.where(
            or_(
                Role.name.ilike(search_term),
                Role.name_fa.ilike(search_term),
                Role.code.ilike(search_term)
            )
        )

    # Apply sorting
    if search_filters.get("sort_by"):
        sort_column = getattr(Role, search_filters["sort_by"], None)
        if sort_column:
            if search_filters["sort_order"] == "desc":
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())

    # Apply pagination
    query = query.offset(pagination["skip"]).limit(pagination["limit"])

    result = await db.execute(query)
    roles = result.scalars().all()

    return [RoleResponse.from_orm(role) for role in roles]

@router.get("/roles/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get role by ID"""
    role = await db.get(Role, role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )

    return RoleResponse.from_orm(role)

@router.put("/roles/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    role_data: RoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update role information"""
    role = await db.get(Role, role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )

    # Check if new code conflicts with existing role
    if role_data.code and role_data.code != role.code:
        existing_role = await db.execute(
            select(Role).where(Role.code == role_data.code)
        )
        existing_role = existing_role.scalar_one_or_none()

        if existing_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role code already exists"
            )

    # Update role
    for field, value in role_data.dict(exclude_unset=True).items():
        if hasattr(role, field):
            setattr(role, field, value)

    role.updated_by = current_user.id
    role.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(role)

    return RoleResponse.from_orm(role)

@router.delete("/roles/{role_id}")
async def delete_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete role"""
    role = await db.get(Role, role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )

    if role.is_system:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete system role"
        )

    await db.delete(role)
    await db.commit()

    return {"message": "Role deleted successfully"}

# User-Role assignment endpoints
@router.post("/users/{user_id}/roles", response_model=UserRoleResponse)
async def assign_role_to_user(
    user_id: int,
    role_assignment: UserRoleAssignment,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Assign role to user"""
    # Check if user exists
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check if role exists
    role = await db.get(Role, role_assignment.role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )

    # Check if assignment already exists
    existing_assignment = await db.execute(
        select(UserRole).where(
            and_(
                UserRole.user_id == user_id,
                UserRole.role_id == role_assignment.role_id
            )
        )
    )
    existing_assignment = existing_assignment.scalar_one_or_none()

    if existing_assignment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role already assigned to user"
        )

    # Create assignment
    user_role = UserRole(
        user_id=user_id,
        role_id=role_assignment.role_id,
        assigned_by=current_user.id,
        expires_at=role_assignment.expires_at
    )

    db.add(user_role)
    await db.commit()
    await db.refresh(user_role)

    return UserRoleResponse.from_orm(user_role)

@router.delete("/users/{user_id}/roles/{role_id}")
async def remove_role_from_user(
    user_id: int,
    role_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove role from user"""
    # Find assignment
    assignment = await db.execute(
        select(UserRole).where(
            and_(
                UserRole.user_id == user_id,
                UserRole.role_id == role_id,
                UserRole.is_active == True
            )
        )
    )
    assignment = assignment.scalar_one_or_none()

    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role assignment not found"
        )

    assignment.is_active = False
    await db.commit()

    return {"message": "Role removed from user successfully"}

# Permission management endpoints
@router.post("/permissions/", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
async def create_permission(
    permission_data: PermissionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new permission"""
    # Check if permission code already exists
    existing_permission = await db.execute(
        select(Permission).where(Permission.code == permission_data.code)
    )
    existing_permission = existing_permission.scalar_one_or_none()

    if existing_permission:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission with this code already exists"
        )

    permission = Permission(**permission_data.dict())
    permission.created_by = current_user.id
    permission.updated_by = current_user.id

    db.add(permission)
    await db.commit()
    await db.refresh(permission)

    return PermissionResponse.from_orm(permission)

@router.get("/permissions/", response_model=List[PermissionResponse])
async def get_permissions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    pagination: dict = Depends(get_pagination),
    search_filters: dict = Depends(get_search_filters)
):
    """Get list of permissions"""
    query = select(Permission)

    # Apply search
    if search_filters.get("search"):
        search_term = f"%{search_filters['search']}%"
        query = query.where(
            or_(
                Permission.name.ilike(search_term),
                Permission.name_fa.ilike(search_term),
                Permission.code.ilike(search_term)
            )
        )

    # Apply sorting
    if search_filters.get("sort_by"):
        sort_column = getattr(Permission, search_filters["sort_by"], None)
        if sort_column:
            if search_filters["sort_order"] == "desc":
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())

    # Apply pagination
    query = query.offset(pagination["skip"]).limit(pagination["limit"])

    result = await db.execute(query)
    permissions = result.scalars().all()

    return [PermissionResponse.from_orm(permission) for permission in permissions]

@router.get("/permissions/{permission_id}", response_model=PermissionResponse)
async def get_permission(
    permission_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get permission by ID"""
    permission = await db.get(Permission, permission_id)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )

    return PermissionResponse.from_orm(permission)

@router.put("/permissions/{permission_id}", response_model=PermissionResponse)
async def update_permission(
    permission_id: int,
    permission_data: PermissionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update permission information"""
    permission = await db.get(Permission, permission_id)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )

    # Check if new code conflicts with existing permission
    if permission_data.code and permission_data.code != permission.code:
        existing_permission = await db.execute(
            select(Permission).where(Permission.code == permission_data.code)
        )
        existing_permission = existing_permission.scalar_one_or_none()

        if existing_permission:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Permission code already exists"
            )

    # Update permission
    for field, value in permission_data.dict(exclude_unset=True).items():
        if hasattr(permission, field):
            setattr(permission, field, value)

    permission.updated_by = current_user.id
    permission.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(permission)

    return PermissionResponse.from_orm(permission)

@router.delete("/permissions/{permission_id}")
async def delete_permission(
    permission_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete permission"""
    permission = await db.get(Permission, permission_id)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )

    if permission.is_system:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete system permission"
        )

    await db.delete(permission)
    await db.commit()

    return {"message": "Permission deleted successfully"}
