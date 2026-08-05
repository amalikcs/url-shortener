from datetime import datetime
from pydantic import BaseModel, HttpUrl


class URLCreate(BaseModel):
    original_url: HttpUrl


class URLResponse(BaseModel):
    original_url: HttpUrl
    short_code: str

    class Config:
        from_attributes = True


class URLInfo(BaseModel):
    id: int
    original_url: HttpUrl
    short_code: str
    created_at: datetime

    class Config:
        from_attributes = True
