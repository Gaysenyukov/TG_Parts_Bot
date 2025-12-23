import aiohttp
from urllib.parse import quote_plus
from utils.normalizers import clean_product_name
import logging

logger = logging.getLogger(__name__)


class AbcpClient:
    BASE_URL = "https://id42133.public.api.abcp.ru/search/articles/"

    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password

    async def search(self, article: str, brand: str) -> dict | None:
        url = (
            f"{self.BASE_URL}"
            f"?userlogin={self.login}"
            f"&userpsw={self.password}"
            f"&number={quote_plus(article)}"
            f"&brand={quote_plus(brand)}"
        )

        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()

                    if not data:
                        logger.info("API вернул пустой результат для article=%s brand=%s", article, brand)
                        return None

                    item = data[0]
                    return {
                        "name": clean_product_name(item.get("description", "")),
                        "price": float(item.get("price", 0)),
                        "delivery_min": item.get("deliveryPeriod"),
                        "delivery_max": item.get("deliveryPeriodMax"),
                    }


        except Exception:
            logger.exception("ABCP API error while requesting %s", url)
            raise