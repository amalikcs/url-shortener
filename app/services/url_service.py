import secrets
import string

from app.repositories.url_repository import URLRepository
from app.models.urls import URLMapping


class URLService:

    MAX_ATTEMPTS = 5

    def __init__(self, repository: URLRepository):
        self.repository = repository

    def create_url(self, original_url: str):

        # 1. Check if the original URL already exists
        existing_url = self.repository.get_by_original_url(
            original_url
        )

        if existing_url:
            return existing_url

        # 2. Generate a unique short code
        attempt = 0

        while attempt < self.MAX_ATTEMPTS:

            short_code = self.generate_short_code()

            existing_code = self.repository.get_by_short_code(
                short_code
            )

            # Code is available
            if not existing_code:
                return self.repository.create(
                    original_url=original_url,
                    short_code=short_code
                )

            # Code already exists → try again
            attempt += 1

        # Could not generate a unique code
        raise RuntimeError(
            "Unable to generate a unique short code"
        )

    @staticmethod
    def generate_short_code(length: int = 6) -> str:

        characters = string.ascii_letters + string.digits

        result = ""

        for _ in range(length):
            character = secrets.choice(characters)
            result += character

        return result

    def get_original_url(self, short_code: str) -> str:

        url_mapping = self.repository.get_by_short_code(short_code)

        if not url_mapping:
            raise ValueError(
                f"Short code '{short_code}' not found"
            )
        try:
            self.repository.increment_click_count(url_mapping)
        except Exception:
            pass
        return url_mapping.original_url

    def get_url_stats(self, short_code: str) -> URLMapping:
        url_mapping = self.repository.get_by_short_code(short_code)
        if not url_mapping:
            raise ValueError(
                    f"Short code '{short_code}' not found"
                )
        return url_mapping

   