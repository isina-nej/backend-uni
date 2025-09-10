# app/schemas/user.py
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class Theme(str, Enum):
    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"

class Language(str, Enum):
    FA = "fa"
    EN = "en"

class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: Optional[str] = None
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    national_id: Optional[str] = Field(None, regex=r'^\d{10}$')
    phone: Optional[str] = None
    mobile: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = Field(None, max_length=500)
    date_of_birth: Optional[datetime] = None
    gender: Optional[Gender] = None
    employee_id: Optional[str] = None
    hire_date: Optional[datetime] = None
    termination_date: Optional[datetime] = None
    student_id: Optional[str] = None
    academic_year: Optional[str] = None
    semester: Optional[str] = None
    language: Language = Language.FA
    timezone: str = "Asia/Tehran"
    theme: Theme = Theme.LIGHT
    metadata: Optional[Dict[str, Any]] = None

class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8)

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

class UserUpdate(BaseModel):
    """Schema for updating user information"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    national_id: Optional[str] = Field(None, regex=r'^\d{10}$')
    phone: Optional[str] = None
    mobile: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = Field(None, max_length=500)
    date_of_birth: Optional[datetime] = None
    gender: Optional[Gender] = None
    employee_id: Optional[str] = None
    hire_date: Optional[datetime] = None
    termination_date: Optional[datetime] = None
    student_id: Optional[str] = None
    academic_year: Optional[str] = None
    semester: Optional[str] = None
    language: Optional[Language] = None
    timezone: Optional[str] = None
    theme: Optional[Theme] = None
    metadata: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None

class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    is_active: bool
    is_verified: bool
    is_staff: bool
    is_superuser: bool
    email_verified_at: Optional[datetime]
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int]
    updated_by: Optional[int]
    version: int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str
    remember_me: bool = False

class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse

class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request"""
    refresh_token: str

class ChangePasswordRequest(BaseModel):
    """Schema for changing password"""
    current_password: str
    new_password: str = Field(..., min_length=8)

    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

# Role schemas
class RoleBase(BaseModel):
    """Base role schema"""
    name: str = Field(..., min_length=1, max_length=100)
    name_fa: Optional[str] = Field(None, max_length=100)
    code: str = Field(..., min_length=1, max_length=50, regex=r'^[A-Z_]+$')
    description: Optional[str] = Field(None, max_length=500)
    priority: int = 0

class RoleCreate(RoleBase):
    """Schema for creating a new role"""
    pass

class RoleUpdate(BaseModel):
    """Schema for updating role information"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    name_fa: Optional[str] = Field(None, max_length=100)
    code: Optional[str] = Field(None, min_length=1, max_length=50, regex=r'^[A-Z_]+$')
    description: Optional[str] = Field(None, max_length=500)
    priority: Optional[int] = None
    is_active: Optional[bool] = None

class RoleResponse(RoleBase):
    """Schema for role response"""
    id: int
    is_system: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int]
    updated_by: Optional[int]
    version: int

    class Config:
        orm_mode = True

# Permission schemas
class PermissionBase(BaseModel):
    """Base permission schema"""
    name: str = Field(..., min_length=1, max_length=100)
    name_fa: Optional[str] = Field(None, max_length=100)
    code: str = Field(..., min_length=1, max_length=100, regex=r'^[a-z_]+\.[a-z_]+$')
    description: Optional[str] = Field(None, max_length=500)
    resource_type: str = Field(..., min_length=1, max_length=50)
    action: str = Field(..., min_length=1, max_length=50)

class PermissionCreate(PermissionBase):
    """Schema for creating a new permission"""
    pass

class PermissionUpdate(BaseModel):
    """Schema for updating permission information"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    name_fa: Optional[str] = Field(None, max_length=100)
    code: Optional[str] = Field(None, min_length=1, max_length=100, regex=r'^[a-z_]+\.[a-z_]+$')
    description: Optional[str] = Field(None, max_length=500)
    resource_type: Optional[str] = Field(None, min_length=1, max_length=50)
    action: Optional[str] = Field(None, min_length=1, max_length=50)

class PermissionResponse(PermissionBase):
    """Schema for permission response"""
    id: int
    is_system: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int]
    updated_by: Optional[int]
    version: int

    class Config:
        orm_mode = True

# User role assignment schemas
class UserRoleAssignment(BaseModel):
    """Schema for assigning role to user"""
    user_id: int
    role_id: int
    expires_at: Optional[datetime] = None

class UserRoleResponse(BaseModel):
    """Schema for user role response"""
    id: int
    user_id: int
    role_id: int
    role: RoleResponse
    is_active: bool
    assigned_by: Optional[int]
    assigned_at: datetime
    expires_at: Optional[datetime]

    class Config:
        orm_mode = True

# User permission assignment schemas
class UserPermissionAssignment(BaseModel):
    """Schema for assigning permission to user"""
    user_id: int
    permission_id: int
    expires_at: Optional[datetime] = None

class UserPermissionResponse(BaseModel):
    """Schema for user permission response"""
    id: int
    user_id: int
    permission_id: int
    permission: PermissionResponse
    is_active: bool
    granted_by: Optional[int]
    granted_at: datetime
    expires_at: Optional[datetime]

    class Config:
        orm_mode = True

# Role permission assignment schemas
class RolePermissionAssignment(BaseModel):
    """Schema for assigning permission to role"""
    role_id: int
    permission_id: int

class RolePermissionResponse(BaseModel):
    """Schema for role permission response"""
    id: int
    role_id: int
    permission_id: int
    permission: PermissionResponse
    is_active: bool
    granted_by: Optional[int]
    granted_at: datetime

    class Config:
        orm_mode = True

# User profile response with roles and permissions
class UserProfileResponse(UserResponse):
    """Schema for user profile with roles and permissions"""
    roles: List[UserRoleResponse] = []
    permissions: List[UserPermissionResponse] = []

    class Config:
        orm_mode = True
