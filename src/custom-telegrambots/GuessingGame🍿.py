import random
from typing import cast

from telegrambots.custom import MessageContext, TelegramBot
from telegrambots.custom import message_filters as mf


bot = TelegramBot("BOT_TOKEN")
dp = bot.dispatcher

dp.add_default_exception_handler()  # prints exceptions occurred inside handlers.


@dp.add.handlers.via_decorator.message(mf.Regex("^/guess") & mf.private)
async def starting(context: MessageContext):
    await context.reply_text("Ok, let's start guessing.")
    random_number = random.randint(0, 100)
    await context.reply_text(
        "Now, send me your guesses (0 ~ 100). this's your first guess, come'on"
    )

    if context.sender:

        # By default, continue_with will make parent context's data to be available inside child context
        # These're are available in _'s context.
        context["random_number"] = random_number
        context["tries"] = 0

        @context.continue_with.this.text_input_from(
            context.sender.id,
            other_continue_with=[
                "_"
            ],  # Allows following handler to be continued with itself. ( in additional to the parent handler ( `starting` ))
        )
        async def _(context: MessageContext):
            if not context.sender:
                return

            maximum_tries = 5
            text = cast(str, context.update.text)
            finished = False
            random_number: int = context["random_number"]  # Custom data are here

            try:
                guess = int(text)

                if guess == random_number:
                    await context.reply_text(
                        "You got it! The number was {}".format(random_number)
                    )
                    finished = True
                elif guess > random_number:
                    await context.reply_text("Too high, try again")
                elif guess < random_number:
                    await context.reply_text("Too low, try again")

            except ValueError:
                await context.reply_text("Please send a number.")

            if not finished:
                if context["tries"] == maximum_tries:
                    finished = True
                    await context.reply_text(
                        f"You have reached the maximum number of tries. The number was {random_number}."
                    )
                    return

                context["tries"] += 1
                await context.reply_text(
                    "Try again, You have {} tries left.".format(
                        maximum_tries - context["tries"] + 1
                    )
                )
                context.continue_with.self_shared_keys()  # Use kays we used for this handler.


if __name__ == "__main__":
    dp.unlimited()
