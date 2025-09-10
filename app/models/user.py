# app/models/user.py
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base

class User(Base):
    """User model for authentication and profile management"""

    __tablename__ = "users"

    # Basic information
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    national_id = Column(String(20), unique=True, nullable=True, index=True)
    phone = Column(String(20), nullable=True)
    mobile = Column(String(20), nullable=True)

    # Profile information
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    gender = Column(String(20), nullable=True)  # male, female, other

    # Employment information
    employee_id = Column(String(50), unique=True, nullable=True, index=True)
    hire_date = Column(DateTime, nullable=True)
    termination_date = Column(DateTime, nullable=True)

    # Academic information (for students and staff)
    student_id = Column(String(50), unique=True, nullable=True, index=True)
    academic_year = Column(String(20), nullable=True)
    semester = Column(String(20), nullable=True)

    # Status and flags
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_staff = Column(Boolean, default=False, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    email_verified_at = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)

    # Preferences and settings
    language = Column(String(10), default="fa", nullable=False)
    timezone = Column(String(50), default="Asia/Tehran", nullable=False)
    theme = Column(String(20), default="light", nullable=False)

    # Metadata
    metadata = Column(JSON, nullable=True)  # Additional custom fields

    # Relationships
    passwords = relationship("UserPassword", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    permissions = relationship("UserPermission", back_populates="user", cascade="all, delete-orphan")

    # University relationships (will be defined in university models)
    # university_id = Column(Integer, ForeignKey("universities.id"), nullable=True)
    # faculty_id = Column(Integer, ForeignKey("faculties.id"), nullable=True)
    # department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.first_name} {self.last_name})>"

    @property
    def full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"

    @property
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.is_active and self.is_verified

    def get_permissions(self) -> list:
        """Get all user permissions"""
        permissions = []
        # Direct permissions
        for perm in self.permissions:
            if perm.is_active:
                permissions.append(perm.permission)
        # Role permissions
        for role_rel in self.roles:
            if role_rel.is_active:
                for role_perm in role_rel.role.permissions:
                    if role_perm.is_active:
                        permissions.append(role_perm.permission)
        return list(set(permissions))  # Remove duplicates

    def has_permission(self, permission_code: str) -> bool:
        """Check if user has specific permission"""
        permissions = self.get_permissions()
        return any(perm.code == permission_code for perm in permissions)

    def has_role(self, role_code: str) -> bool:
        """Check if user has specific role"""
        return any(role_rel.role.code == role_code for role_rel in self.roles if role_rel.is_active)

class UserPassword(Base):
    """User password model for secure password storage"""

    __tablename__ = "user_passwords"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    salt = Column(String(255), nullable=True)
    algorithm = Column(String(50), default="bcrypt", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    last_changed = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="passwords")

    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'is_active', name='unique_active_password'),
    )

    def __repr__(self):
        return f"<UserPassword(user_id={self.user_id}, active={self.is_active})>"

class UserSession(Base):
    """User session model for managing user sessions"""

    __tablename__ = "user_sessions"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    session_token = Column(String(500), unique=True, nullable=False, index=True)
    refresh_token = Column(String(500), unique=True, nullable=False, index=True)
    device_info = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)  # IPv6 support
    user_agent = Column(Text, nullable=True)
    status = Column(String(20), default="active", nullable=False)  # active, expired, logged_out
    login_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_activity = Column(DateTime, default=datetime.utcnow, nullable=False)
    expiry_time = Column(DateTime, nullable=False)
    authentication_method = Column(String(50), default="password", nullable=False)

    # Relationships
    user = relationship("User", back_populates="sessions")

    def __repr__(self):
        return f"<UserSession(user_id={self.user_id}, status={self.status})>"

    @property
    def is_expired(self) -> bool:
        """Check if session is expired"""
        return datetime.utcnow() > self.expiry_time

    @property
    def is_active(self) -> bool:
        """Check if session is active"""
        return self.status == "active" and not self.is_expired

class Role(Base):
    """Role model for role-based access control"""

    __tablename__ = "roles"

    name = Column(String(100), nullable=False)
    name_fa = Column(String(100), nullable=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    is_system = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    priority = Column(Integer, default=0, nullable=False)  # Higher priority = more permissions

    # Relationships
    users = relationship("UserRole", back_populates="role", cascade="all, delete-orphan")
    permissions = relationship("RolePermission", back_populates="role", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Role(id={self.id}, code={self.code}, name={self.name})>"

class Permission(Base):
    """Permission model for granular access control"""

    __tablename__ = "permissions"

    name = Column(String(100), nullable=False)
    name_fa = Column(String(100), nullable=True)
    code = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    resource_type = Column(String(50), nullable=False)  # user, university, financial, etc.
    action = Column(String(50), nullable=False)  # create, read, update, delete
    is_system = Column(Boolean, default=False, nullable=False)

    # Relationships
    roles = relationship("RolePermission", back_populates="permission", cascade="all, delete-orphan")
    users = relationship("UserPermission", back_populates="permission", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Permission(id={self.id}, code={self.code}, resource={self.resource_type})>"

class UserRole(Base):
    """Many-to-many relationship between users and roles"""

    __tablename__ = "user_roles"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    assigned_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    assigned_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="roles", foreign_keys=[user_id])
    role = relationship("Role", back_populates="users")
    assigner = relationship("User", foreign_keys=[assigned_by])

    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'role_id', name='unique_user_role'),
    )

    def __repr__(self):
        return f"<UserRole(user_id={self.user_id}, role_id={self.role_id})>"

class UserPermission(Base):
    """Direct user permissions (bypassing roles)"""

    __tablename__ = "user_permissions"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    granted_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    granted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="permissions", foreign_keys=[user_id])
    permission = relationship("Permission", back_populates="users")
    granter = relationship("User", foreign_keys=[granted_by])

    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'permission_id', name='unique_user_permission'),
    )

    def __repr__(self):
        return f"<UserPermission(user_id={self.user_id}, permission_id={self.permission_id})>"

class RolePermission(Base):
    """Many-to-many relationship between roles and permissions"""

    __tablename__ = "role_permissions"

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, index=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    granted_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    granted_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")
    granter = relationship("User", foreign_keys=[granted_by])

    # Constraints
    __table_args__ = (
        UniqueConstraint('role_id', 'permission_id', name='unique_role_permission'),
    )

    def __repr__(self):
        return f"<RolePermission(role_id={self.role_id}, permission_id={self.permission_id})>"
