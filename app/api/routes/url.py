from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.url import URLCreate, URLResponse, URLStatsResponse
from app.db.db import get_db

from app.repositories.url_repository import URLRepository
from app.services.url_service import URLService

router = APIRouter(prefix="/urls", tags=["urls"])

@router.get("/")
def get_urls():
    return {"message": "List of URLs"}


@router.post("/", response_model=URLResponse, status_code=201)
def create_url(url: URLCreate, 
               db: Session = Depends(get_db)):
    
    repository = URLRepository(db)
    service = URLService(repository)

    return service.create_url(original_url=str(url.original_url))

@router.get("/short/{short_code}")
def get_original_url(short_code: str,
                     db: Session = Depends(get_db)):

    repository = URLRepository(db)
    service = URLService(repository)

    original_url = service.get_original_url(short_code=short_code)

    return {"original_url": original_url}

@router.get("/stats/{short_code}", response_model=URLStatsResponse)
def get_url_stats(short_code: str,
                  db: Session = Depends(get_db)):

    repository = URLRepository(db)
    service = URLService(repository)

    try:
        url_mapping = service.get_url_stats(short_code=short_code)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return URLStatsResponse(
        short_code=url_mapping.short_code,
        click_count=url_mapping.click_count,
        original_url=url_mapping.original_url,
        created_at=url_mapping.created_at
    )

@router.get("/{short_code}")
def redirect_to_original_url(short_code: str,
                     db: Session = Depends(get_db)):

    repository = URLRepository(db)
    service = URLService(repository)

    try:
        original_url = service.get_original_url(short_code=short_code)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return RedirectResponse(url=original_url, status_code=302)

