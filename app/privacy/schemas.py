from __future__ import annotations

from pydantic import BaseModel


class PublicProfilePrivacyOut(BaseModel):
    public_profile_show_public_wishes: bool = True
    public_profile_show_fulfilled_wishes: bool = True
    public_profile_show_calendar: bool = True
    public_profile_show_oracle: bool = True


class PublicProfilePrivacyUpdateRequest(BaseModel):
    public_profile_show_public_wishes: bool | None = None
    public_profile_show_fulfilled_wishes: bool | None = None
    public_profile_show_calendar: bool | None = None
    public_profile_show_oracle: bool | None = None

