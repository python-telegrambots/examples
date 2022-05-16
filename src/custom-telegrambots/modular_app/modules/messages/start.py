from telegrambots.custom import abstracts, message_filters as mf, MessageContext
from telegrambots.custom.helpers import InlineButtonBuilder


class Start(abstracts.MessageHandler):
    def __init__(self):
        super().__init__("start_message", mf.Regex("^/start") & mf.private)

    async def _process(self, context: MessageContext) -> None:
        message = await context.reply_text(
            "Welcome to counter, click button below.",
            reply_markup=InlineButtonBuilder(
                lambda x: x.with_callback_data("0", "count")
            )(),  # or .build()
        )

        context["count"] = 0

        context.continue_with.callback_query_same_message(
            "count_it", message.message_id
        )
