# app/routers/academic.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.dependencies import get_pagination, get_search_filters, get_current_user

router = APIRouter()

# Placeholder for academic endpoints
# These will be implemented based on the academic models from MAIN_MODELS.md

@router.get("/")
async def get_academic_entities(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    pagination: dict = Depends(get_pagination),
    search_filters: dict = Depends(get_search_filters)
):
    """Get list of academic entities (faculties, departments, courses, etc.)"""
    return {"message": "Academic entities endpoint - To be implemented"}

@router.get("/faculties")
async def get_faculties(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of faculties"""
    return {"message": "Faculties endpoint - To be implemented"}

@router.get("/departments")
async def get_departments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of departments"""
    return {"message": "Departments endpoint - To be implemented"}

@router.get("/courses")
async def get_courses(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of courses"""
    return {"message": "Courses endpoint - To be implemented"}

@router.get("/students")
async def get_students(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of students"""
    return {"message": "Students endpoint - To be implemented"}

@router.get("/enrollments")
async def get_enrollments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of course enrollments"""
    return {"message": "Enrollments endpoint - To be implemented"}
