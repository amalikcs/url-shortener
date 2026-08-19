import secrets
import string
import logging

from app.repositories.url_repository import URLRepository
from app.models.urls import URLMapping

logger = logging.getLogger(__name__)

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
            logger.warning(f"URL already exists: {original_url}, returning existing short code: {existing_url.short_code}")
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
                url_mapping = self.repository.create(
                    original_url=original_url,
                    short_code=short_code
                )
                logger.info(f"Created new URL mapping: {url_mapping.short_code} for original URL: {url_mapping.original_url}")
                return url_mapping

            # Code already exists → try again
            attempt += 1

        # Could not generate a unique code
        logger.error(f"Failed to generate a unique short code for original URL: {original_url} after {self.MAX_ATTEMPTS} attempts")
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

    def get_all_urls(self) -> list[URLMapping]:
        urls = self.repository.get_all_urls()
        logger.info("Fetching all URL mappings")
        return urls

    def get_original_url(self, short_code: str) -> str:

        url_mapping = self.repository.get_by_short_code(short_code)

        if not url_mapping:
            logger.warning(f"Short code '{short_code}' not found for original URL: {url_mapping.original_url if url_mapping else 'Unknown'}")
            raise ValueError(
                f"Short code '{short_code}' not found"
            )
        logger.info(f"Redirecting short code '{short_code}' to original URL: {url_mapping.original_url}")
        try:
            self.repository.increment_click_count(url_mapping)
            logger.info(f"Incremented click count for short code '{short_code}'")
        except Exception as e:
             logger.error(
            f"Failed to increment click count for "
            f"short code '{short_code}': {e}"
        )
        return url_mapping.original_url

    def get_url_stats(self, short_code: str) -> URLMapping:
        url_mapping = self.repository.get_by_short_code(short_code)
        if not url_mapping:
            logger.warning(f"Short code '{short_code}' not found for original URL: {url_mapping.original_url if url_mapping else 'Unknown'}")
            raise ValueError(
                    f"Short code '{short_code}' not found"
                )
        logger.info(f"Fetching stats for short code '{short_code}'")
        return url_mapping

   