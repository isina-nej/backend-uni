# app/core/auth.py
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User, UserSession
from app.config import settings
from app.core.security import verify_token, generate_token, generate_refresh_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
    """Authenticate user with email and password"""
    from app.core.security import verify_password

    user = await db.execute(
        select(User).where(User.email == email).where(User.is_active == True)
    )
    user = user.scalar_one_or_none()

    if not user:
        return None

    # Get active password
    user_password = await db.execute(
        select(UserPassword)
        .where(UserPassword.user_id == user.id)
        .where(UserPassword.is_active == True)
    )
    user_password = user_password.scalar_one_or_none()

    if not user_password or not verify_password(password, user_password.password_hash):
        return None

    return user

async def create_user_session(
    db: AsyncSession,
    user: User,
    device_info: Optional[dict] = None,
    ip_address: str = None,
    user_agent: str = None
) -> UserSession:
    """Create a new user session"""
    from app.core.security import generate_token, generate_refresh_token

    # Generate tokens
    access_token = generate_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    refresh_token = generate_refresh_token()

    # Create session
    session = UserSession(
        user_id=user.id,
        session_token=access_token,
        refresh_token=refresh_token,
        device_info=device_info,
        ip_address=ip_address,
        user_agent=user_agent,
        status="active",
        login_time=datetime.utcnow(),
        last_activity=datetime.utcnow(),
        expiry_time=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        authentication_method="password"
    )

    db.add(session)
    await db.commit()
    await db.refresh(session)

    return session

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
    async with async_session() as db:
        user = await db.get(User, int(user_id))
        if user is None:
            raise credentials_exception

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )

        return user

async def get_current_user_optional(request) -> Optional[User]:
    """Get current user if authenticated, None otherwise"""
    try:
        authorization = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            return None

        token = authorization.split(" ")[1]
        return await get_current_user(token)
    except:
        return None

async def refresh_access_token(refresh_token: str, db: AsyncSession) -> Optional[str]:
    """Refresh access token using refresh token"""
    # Find session with refresh token
    session = await db.execute(
        select(UserSession)
        .where(UserSession.refresh_token == refresh_token)
        .where(UserSession.status == "active")
        .where(UserSession.expiry_time > datetime.utcnow())
    )
    session = session.scalar_one_or_none()

    if not session:
        return None

    # Generate new access token
    access_token = generate_token(
        data={"sub": str(session.user_id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Update session
    session.session_token = access_token
    session.last_activity = datetime.utcnow()
    await db.commit()

    return access_token

async def logout_user(token: str, db: AsyncSession) -> bool:
    """Logout user by invalidating session"""
    # Find and invalidate session
    session = await db.execute(
        select(UserSession)
        .where(UserSession.session_token == token)
        .where(UserSession.status == "active")
    )
    session = session.scalar_one_or_none()

    if session:
        session.status = "logged_out"
        session.last_activity = datetime.utcnow()
        await db.commit()
        return True

    return False

async def validate_session(token: str, db: AsyncSession) -> Optional[UserSession]:
    """Validate user session"""
    session = await db.execute(
        select(UserSession)
        .where(UserSession.session_token == token)
        .where(UserSession.status == "active")
        .where(UserSession.expiry_time > datetime.utcnow())
    )
    session = session.scalar_one_or_none()

    if session:
        # Update last activity
        session.last_activity = datetime.utcnow()
        await db.commit()
        return session

    return None
