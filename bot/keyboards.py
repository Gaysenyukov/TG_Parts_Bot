from telegram import ReplyKeyboardMarkup

def main_keyboard():
    return ReplyKeyboardMarkup(
        [["Поиск товаров Grass"]],
        resize_keyboard=True
    )