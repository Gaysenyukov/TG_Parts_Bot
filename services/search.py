from api import AbcpClient
from utils import normalize_article

import logging

logger = logging.getLogger(__name__)

class SearchService:
    def __init__(self, client: AbcpClient, markup: float = 1.15):
        self.client = client
        self.markup = markup

    async def search(self, article: str, brand: str) -> str:
        logger.info("Search request: article=%s brand=%s", article, brand)

        normalized = normalize_article(article)
        logger.debug("Normalized article: %s", normalized)

        try:
            product = await self.client.search(normalized, brand)
        except Exception:
            logger.exception("Search failed due to API error")
            return "Сервис временно недоступен. Попробуйте позже."

        if not product:
            logger.warning("Product not found")
            return "Товар не найден"

        logger.info("Product found")

        price = round(product["price"] * self.markup, 2)

        return (
            f"Товар: {product['name']}\n"
            f"Цена: {price} ₽\n"
            f"Срок поставки: "
            f"{product['delivery_min']}–{product['delivery_max']} час."
        )

