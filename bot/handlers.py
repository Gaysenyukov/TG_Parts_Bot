from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards import main_keyboard
from services.search import SearchService

GRASS_BRAND = "Grass"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Нажми кнопку для поиска товаров Grass",
        reply_markup=main_keyboard()
    )

async def text_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    service: SearchService = context.bot_data["search_service"]

    if text == "Поиск товаров Grass":
        context.user_data["await_article"] = True
        await update.message.reply_text("Введите артикул товара Grass:")
        return

    if context.user_data.get("await_article"):
        context.user_data["await_article"] = False
        await update.message.reply_text("🔎 Ищу товар, подожди...")
        result = await service.search(text, GRASS_BRAND)
        await update.message.reply_text(result)
        return

    await update.message.reply_text("Нажмите кнопку «Поиск товаров Grass».")