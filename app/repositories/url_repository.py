from sqlalchemy.orm import Session
from app.models.urls import URLMapping


class URLRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, original_url: str, short_code: str) -> URLMapping:
        url_mapping = URLMapping(original_url=original_url, short_code=short_code)
        try:
            self.db.add(url_mapping)
            self.db.commit()
            self.db.refresh(url_mapping)

            return url_mapping
        except Exception:
            self.db.rollback()
            raise

    def get_by_short_code(self, short_code: str) -> URLMapping | None:
        return self.db.query(URLMapping) \
                .filter(URLMapping.short_code == short_code) \
                .first()

    def get_by_original_url(self, original_url: str) -> URLMapping | None:
        return self.db.query(URLMapping) \
                .filter(URLMapping.original_url == original_url) \
                .first()

    def increment_click_count(self, url_mapping: URLMapping) -> URLMapping:

        url_mapping.click_count += 1
        try:
            self.db.commit()
            self.db.refresh(url_mapping)
        except Exception:
            self.db.rollback()
            raise
        return url_mapping

