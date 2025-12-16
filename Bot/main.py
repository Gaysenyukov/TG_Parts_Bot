import aiohttp
import asyncio
from config import token
import os
import telegram

'''Токен бота, логин и пароль к хосту хранится в переменных окружения'''

url_login = os.environ.get('USERLOGIN')
url_pass = os.environ.get('USERPASS')

article_number = 'DT-0169'
brand = 'Detail'

url: str = f'https://id42133.public.api.abcp.ru/search/articles/?userlogin={url_login}&userpsw={url_pass}&number={article_number
}&brand={brand}'  #хост API

async def get_data(url: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                name = data[0].get("description")
                price = data[0].get("price")
                delivery_min = data[0].get("deliveryPeriod")
                delivery_max = data[0].get("deliveryPeriodMax")
                result = (
                    f"Товар: {name}\n"
                    f"Цена: {float(price) * 1.15} ₽\n"
                    f"Срок поставки: {delivery_min}–{delivery_max} час."
                )

                return result
    except Exception as e:
        return f"Ошибка при получении данных: {type(e).__name__} — {e}"

""" Секция с ботом"""

async def main():
    bot = telegram.Bot(token)
    async with bot:
        result = await get_data(url)
        await bot.send_message(text = result, chat_id=403566169)

    result = await get_data(url)
    print(result)

asyncio.run(main())