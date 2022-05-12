import random
from typing import Any, Mapping, Optional

from telegrambots.custom import (
    CallbackQueryContext,
    ContextTemplate,
    ContinueWithInfo,
    KeyBuilder,
    MessageContext,
    TelegramBot,
)
from telegrambots.custom import callback_query_filters as cf
from telegrambots.custom import message_filters as mf
from telegrambots.custom.helpers import InlineButtonBuilder


bot = TelegramBot("BOT_TOKEN")
dp = bot.dispatcher

dp.add_default_exception_handler()


def my_continue_with(
    context: ContextTemplate, user_id: int, message_id: int, **kwargs: Any
):
    keys = (
        KeyBuilder.for_callback_query()
        .from_user(user_id)
        .from_message(message_id)
        .build()
    )
    return context.continue_with.many(
        ContinueWithInfo.with_callback_query("gimme_food", keys, **kwargs),
    )


my_keyboard = InlineButtonBuilder(lambda b: b.with_callback_data("🌭🍕🍔🍟", "gimme"))()

fast_foods = ("🌭", "🍕", "🍔", "🍟")


def foods_selector(mapping: Mapping[str, Any]):
    return {k: mapping[k] for k in mapping if k in fast_foods}


def random_fastfood():
    return random.choice(fast_foods)


def get_ate_count(**fast_foods: int):
    return (
        "Let us just eat some fast food! ...\n\n"
        "🍟 - {🍟}\n🍔 - {🍔}\n🍕 - {🍕}\n🌭 - {🌭}".format(**fast_foods)
    )


def check_capacity(maximum: int = 5, **fast_foods: int) -> Optional[str]:
    if sum(x for x in fast_foods.values()) >= maximum:
        sort_it = sorted(fast_foods.items(), key=lambda x: x[1], reverse=True)
        return sort_it[0][0]
    return None


@dp.add.handlers.via_decorator.message(mf.Regex("^/start") & mf.private)
async def starting(context: MessageContext):
    my_fastfoods = {"🌭": 0, "🍕": 0, "🍔": 0, "🍟": 0}

    message = await context.reply_text(
        get_ate_count(**my_fastfoods), reply_markup=my_keyboard
    )

    if context.update.from_user:
        my_continue_with(
            context, context.update.from_user.id, message.message_id, **my_fastfoods
        )


@dp.add.handlers.via_decorator.callback_query(
    cf.regex("^gimme$"), continue_after=["starting", "gimme_food"]
)
async def gimme_food(context: CallbackQueryContext):
    if context.update.from_user and context.update.message:
        maximum = check_capacity(**foods_selector(context))
        if maximum is not None:
            await context.answer("Looks like it's your maximum capacity.")
            await context.edit_reply_markup()
            await context.bot.send_message(context.update.from_user.id, maximum)
            return

        fast_food = random_fastfood()
        await context.answer(f"Time to eat some {fast_food}!")
        context[fast_food] += 1

        await context.edit_text(
            get_ate_count(**foods_selector(context)), reply_markup=my_keyboard
        )

        my_continue_with(
            context,
            context.update.from_user.id,
            context.update.message.message_id,
            **context,
        )


if __name__ == "__main__":
    dp.unlimited()
