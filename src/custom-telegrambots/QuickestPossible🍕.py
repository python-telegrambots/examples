from telegrambots.custom import TelegramBot, MessageContext, filters as flts


bot = TelegramBot("BOT_TOKEN")
dp = bot.dispatcher

dp.add_default_exception_handler()


@dp.add.handlers.via_decorator.message(
    flts.messages.Regex("^/start") & flts.messages.private
)
async def starting(context: MessageContext):
    await context.reply_text("Started")


if __name__ == "__main__":
    dp.unlimited("message")
