import dataclasses
from typing import Optional
from telegrambots.custom import TelegramBot, MessageContext, message_filters as mf


@dataclasses.dataclass(repr=True)
class Inforamation:
    id: int
    name: str
    favorite_color: Optional[str] = None
    preferred_lunch: Optional[str] = None
    preferred_dinner: Optional[str] = None
    has_a_dog: Optional[bool] = None
    has_a_cat: Optional[bool] = None
    dog_name: Optional[str] = None
    cat_name: Optional[str] = None


bot = TelegramBot("5373053513:AAFjuooGr532lOILaylmG9RjO4XIawLxNzU")
dp = bot.dispatcher


@dp.add.handlers.via_decorator.message(mf.Regex("^/start") & mf.private)
async def start(context: MessageContext):
    if context.sender:
        await context.reply_text(
            f"Hello, {context.sender.first_name}!\n" "Can i know you more? 🤔"
        )

        context["info"] = Inforamation(context.sender.id, context.sender.first_name)

        await context.reply_text("What's your favorite color?")

        context.continue_with.message_from(context.sender.id, "favorite_color")


@dp.add.handlers.via_decorator.message(mf.text_message, continue_after=["start"])
async def favorite_color(context: MessageContext):
    context["info"].favorite_color = context.text
    await context.reply_text("What's your preferred lunch?")
    context.continue_with.message_from(context["info"].id, "preferred_lunch")


@dp.add.handlers.via_decorator.message(
    mf.text_message, continue_after=["favorite_color"]
)
async def preferred_lunch(context: MessageContext):
    context["info"].preferred_lunch = context.text
    await context.reply_text("What's your preferred dinner?")
    context.continue_with.message_from(context["info"].id, "preferred_dinner")


@dp.add.handlers.via_decorator.message(
    mf.text_message, continue_after=["preferred_lunch"]
)
async def preferred_dinner(context: MessageContext):
    context["info"].preferred_dinner = context.text
    await context.reply_text("Do you have a dog?")
    context.continue_with.message_from(context["info"].id, "has_a_dog")


@dp.add.handlers.via_decorator.message(
    mf.text_message, continue_after=["preferred_dinner"]
)
async def has_a_dog(context: MessageContext):
    context["info"].has_a_dog = context.text.lower() == "yes"
    if context["info"].has_a_dog:
        await context.reply_text("What's your dog's name?")
        context.continue_with.message_from(context["info"].id, "dog_name")
    else:
        await context.reply_text("Do you have a cat?")
        context.continue_with.message_from(context["info"].id, "has_a_cat")


@dp.add.handlers.via_decorator.message(mf.text_message, continue_after=["has_a_dog"])
async def dog_name(context: MessageContext):
    context["info"].dog_name = context.text
    await context.reply_text("Do you have a cat?")
    context.continue_with.message_from(context["info"].id, "has_a_cat")


@dp.add.handlers.via_decorator.message(mf.text_message, continue_after=["has_a_dog"])
async def has_a_cat(context: MessageContext):
    context["info"].has_a_cat = context.text.lower() == "yes"
    if context["info"].has_a_cat:
        await context.reply_text("What's your cat's name?")
        context.continue_with.message_from(context["info"].id, "cat_name")
    else:
        await context.reply_text("I'm done! Thank you for your information!")
        await context.reply_text(str(context["info"]))


@dp.add.handlers.via_decorator.message(mf.text_message, continue_after=["has_a_cat"])
async def cat_name(context: MessageContext):
    context["info"].cat_name = context.text
    await context.reply_text("I'm done! Thank you for your information!")
    await context.reply_text(str(context["info"]))


if __name__ == "__main__":
    dp.unlimited()
