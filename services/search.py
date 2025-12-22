from api.abcp import AbcpClient
from utils import normalize_article

class SearchService:
    def __init__(self, client: AbcpClient, markup: float = 1.15):
        self.client = client
        self.markup = markup

    async def search(self, article: str, brand: str) -> str:
        normalized = normalize_article(article)
        product = await self.client.search(normalized, brand)

        if not product:
            return "Товар не найден"

        price = round(product["price"] * self.markup, 2)

        return (
            f"Товар: {product['name']}\n"
            f"Цена: {price} ₽\n"
            f"Срок поставки: "
            f"{product['delivery_min']}–{product['delivery_max']} час."
        )
