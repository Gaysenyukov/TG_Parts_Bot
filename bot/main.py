import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import token
from api import AbcpClient
from services import SearchService
from bot.handlers import start, text_router

def main():
    login = os.environ.get("USERLOGIN")
    password = os.environ.get("USERPASS")

    client = AbcpClient(login, password)
    service = SearchService(client)

    app = Application.builder().token(token).build()
    app.bot_data["search_service"] = service

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_router))

    app.run_polling()

if __name__ == "__main__":
    main()
