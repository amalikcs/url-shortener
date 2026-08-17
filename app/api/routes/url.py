from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.url import URLCreate, URLResponse
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
    