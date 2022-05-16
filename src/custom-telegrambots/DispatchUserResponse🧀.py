from telegrambots.custom import MessageContext, TelegramBot
from telegrambots.custom import message_filters as mf


bot = TelegramBot("BOT_TOKEN")
dp = bot.dispatcher

dp.add_default_exception_handler()


@dp.add.handlers.via_decorator.message(mf.Regex("^/start") & mf.private)
async def starting(context: MessageContext):
    await context.reply_text("What's your name?")

    if context.sender:

        @context.continue_with.this.text_input_from(context.sender.id)
        async def _(context: MessageContext):
            await context.reply_text(f"You said, {context.text}!")


if __name__ == "__main__":
    dp.unlimited()
