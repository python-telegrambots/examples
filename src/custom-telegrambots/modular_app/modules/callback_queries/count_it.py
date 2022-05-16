from telegrambots.custom import abstracts, CallbackQueryContext
from telegrambots.custom.helpers import InlineButtonBuilder


class CountIt(abstracts.CallbackQueryHandler):
    def __init__(self) -> None:
        super().__init__(
            "count_it", continue_after=["start_message"], allow_continue_after_self=True
        )

    async def _process(self, context: CallbackQueryContext) -> None:
        if (count := context.try_get_data("count", int)) is not None:
            context["count"] = count + 1

            await context.edit_reply_markup(
                InlineButtonBuilder(
                    lambda x: x.with_callback_data(str(context["count"]), "count")
                )(),
            )

            context.continue_with.self_shared_keys()
