# app/core/security.py
import bcrypt
import secrets
from datetime import datetime, timedelta
from typing import Optional
import jwt
import logging

from app.config import settings
from app.database import async_session
from app.models.user import User, UserPassword, Role, UserRole

logger = logging.getLogger(__name__)

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

def generate_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Generate JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def generate_refresh_token() -> str:
    """Generate a secure refresh token"""
    return secrets.token_urlsafe(32)

def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

async def create_initial_admin():
    """Create initial admin user if not exists"""
    async with async_session() as db:
        # Check if admin user exists
        admin_user = await db.execute(
            select(User).where(User.email == "admin@university.edu")
        )
        admin_user = admin_user.scalar_one_or_none()

        if admin_user is None:
            # Create admin user
            admin_user = User(
                email="admin@university.edu",
                first_name="System",
                last_name="Administrator",
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(admin_user)
            await db.flush()

            # Create admin password
            admin_password = UserPassword(
                user_id=admin_user.id,
                password_hash=hash_password("admin123"),
                is_active=True,
                created_at=datetime.utcnow()
            )
            db.add(admin_password)

            # Create admin role if not exists
            admin_role = await db.execute(
                select(Role).where(Role.code == "ADMIN")
            )
            admin_role = admin_role.scalar_one_or_none()

            if admin_role is None:
                admin_role = Role(
                    name="Administrator",
                    name_fa="مدیر سیستم",
                    code="ADMIN",
                    description="System administrator with full access",
                    is_system=True,
                    is_active=True,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(admin_role)
                await db.flush()

            # Assign admin role to user
            user_role = UserRole(
                user_id=admin_user.id,
                role_id=admin_role.id,
                is_active=True,
                created_at=datetime.utcnow()
            )
            db.add(user_role)

            await db.commit()
            logger.info("Initial admin user created successfully")

def generate_secure_password(length: int = 12) -> str:
    """Generate a secure random password"""
    import string
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent XSS"""
    import html
    return html.escape(text.strip())

def validate_email_format(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password_strength(password: str) -> dict:
    """Validate password strength"""
    result = {
        "is_valid": True,
        "errors": [],
        "strength": "weak"
    }

    if len(password) < 8:
        result["errors"].append("Password must be at least 8 characters long")
        result["is_valid"] = False

    if not any(c.isupper() for c in password):
        result["errors"].append("Password must contain at least one uppercase letter")
        result["is_valid"] = False

    if not any(c.islower() for c in password):
        result["errors"].append("Password must contain at least one lowercase letter")
        result["is_valid"] = False

    if not any(c.isdigit() for c in password):
        result["errors"].append("Password must contain at least one digit")
        result["is_valid"] = False

    # Calculate strength
    strength_score = 0
    if len(password) >= 8:
        strength_score += 1
    if any(c.isupper() for c in password):
        strength_score += 1
    if any(c.islower() for c in password):
        strength_score += 1
    if any(c.isdigit() for c in password):
        strength_score += 1
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        strength_score += 1

    if strength_score >= 4:
        result["strength"] = "strong"
    elif strength_score >= 3:
        result["strength"] = "medium"

    return result
