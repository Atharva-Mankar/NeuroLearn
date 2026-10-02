"""Pydantic schemas for authentication endpoints."""

from pydantic import BaseModel, Field, validator
from typing import Optional
import re


class SignupRequest(BaseModel):
    """Request model for user signup."""
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: str = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password")

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Name must not be empty')
        return v.strip()

    @validator('email')
    def email_must_be_valid(cls, v):
        if not v or not v.strip():
            raise ValueError('Email is required')
        email = v.strip().lower()
        # Basic email validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError('Invalid email format')
        return email

    @validator('password')
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class SignupResponse(BaseModel):
    """Response model for successful signup."""
    message: str = Field(default="Account created successfully")
    user: dict = Field(..., description="Created user information (without password)")


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str