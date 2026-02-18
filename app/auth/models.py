from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Literal

Role = Literal["user", "guardian", "admin"]

class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    birth_date: datetime
    gender: Literal["male", "female"]
    password: str = Field(min_length=8)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserPublic(BaseModel):
    user_number: int
    email: str
    role: Role
    guardian_rank: Optional[int] = None
    username: Optional[str] = None
    username_updated_at: Optional[datetime] = None
    is_active: bool = True

class UserInternal(UserPublic):
    password_hash: str


class TwoFAVerifyRequest(BaseModel):
    code: str = Field(..., min_length=6, max_length=6)


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(min_length=8)


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)
    new_password_confirm: str = Field(min_length=8)


class UsernameState(BaseModel):
    username: Optional[str] = None
    can_update: bool
    cooldown_until: Optional[datetime] = None
    cooldown_remaining_days: int = 0
    profile_url: str


class UsernameAvailabilityOut(BaseModel):
    username: str
    available: bool
    detail: Optional[str] = None


class UsernameUpdateRequest(BaseModel):
    username: str = Field(min_length=4, max_length=30)


class UsernameUpdateResponse(BaseModel):
    updated: bool
    state: UsernameState
