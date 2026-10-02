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


class LoginRequest(BaseModel):
    """Request model for user login."""
    email: str = Field(..., description="User's email address")
    password: str = Field(..., min_length=1, description="User's password")

    @validator('email')
    def email_must_be_valid(cls, v):
        if not v or not v.strip():
            raise ValueError('Email is required')
        email = v.strip().lower()
        # Same validation as signup so both endpoints agree on what an email is
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError('Invalid email format')
        return email

    @validator('password')
    def password_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('Password is required')
        return v


class SignupResponse(BaseModel):
    """Response model for successful signup."""
    message: str = Field(default="Account created successfully")
    user: dict = Field(..., description="Created user information (without password)")


class LoginResponse(BaseModel):
    """Response model for successful login.

    Carries only safe user fields. password and password_hash are deliberately
    absent so they cannot be leaked by response serialization.
    """
    id: int = Field(..., description="User ID")
    name: str = Field(..., description="User's name")
    email: str = Field(..., description="User's normalized email address")


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


class ProfileResponse(BaseModel):
    """Response model for the signed-in user's own profile.

    Carries only safe fields. password and password_hash are deliberately
    absent so they cannot be leaked by response serialization.
    """
    id: int = Field(..., description="User ID")
    name: str = Field(..., description="User's current display name")
    email: str = Field(..., description="User's email address (the login identifier)")
    created_at: str = Field(..., description="ISO timestamp of when the account was created")


class UpdateProfileRequest(BaseModel):
    """Request model for editing the signed-in user's own profile.

    Only ``name`` is editable. ``email`` is the login identifier and is
    deliberately not changeable here: changing it would require re-verifying
    ownership of the new address, which this phase does not do.
    """
    name: str = Field(..., min_length=1, max_length=100, description="New display name")

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Name must not be empty')
        return v.strip()