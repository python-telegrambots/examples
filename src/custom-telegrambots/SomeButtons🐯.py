from telegrambots.custom import (
    CallbackQueryContext,
    MessageContext,
    TelegramBot,
)
from telegrambots.custom import callback_query_filters as cf, message_filters as mf
from telegrambots.custom.helpers import InlineButtonBuilder


bot = TelegramBot("BOT_TOKEN")
dp = bot.dispatcher

dp.add_default_exception_handler()


@dp.add.handlers.via_decorator.message(mf.Regex("^/start") & mf.private)
async def starting(context: MessageContext):

    # ---- Here is button builder ----
    buttons = (
        InlineButtonBuilder()
        .append_button(
            lambda b: b.with_callback_data("(1, 1)", "(1, 1)")
        )  # Add button to first row
        .append_row()  # Add a new row
        .append_many_buttons(  # Add many buttons to newly added row
            lambda b: b.with_callback_data("(2, 1)", "(2, 1)"),
            lambda b: b.with_callback_data("(2, 2)", "(2, 2)"),
            lambda b: b.with_callback_data("(2, 3)", "(2, 3)"),
        )
        .append_row(
            lambda b: b.with_callback_data("(3, 1)", "(3, 1)")
        )  # Add a new row with a button in it
    ).build()

    message = await context.reply_text("Try click me!", reply_markup=buttons)

    if context.update.from_user:

        @context.continue_with.this.callback_query_same_message_form(
            message.message_id,
            context.update.from_user.id,
            cf.any_callback,
            allow_continue_after_self=True,
        )
        async def _(context: CallbackQueryContext):
            await context.answer(f"You clicked on {context.data}!", show_alert=True)
            context.continue_with.self_shared_keys()


if __name__ == "__main__":
    dp.unlimited()
