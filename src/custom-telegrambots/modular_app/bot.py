from pathlib import Path
from telegrambots.custom import TelegramBot


bot = TelegramBot("2015323878:AAEng0bPfJuAAOAPKgcuhrSDo-K0Jqh24fA")
dp = bot.dispatcher

dp.add_default_exception_handler()

dp.add.handlers.locate(
    Path("modules")
)  # This will search for all modules that contains handlers in the modules folder.


if __name__ == "__main__":
    dp.unlimited()
