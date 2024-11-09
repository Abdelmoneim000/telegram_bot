from telegram import Update
from telegram.ext import CallbackContext

async def close(update: Update, context: CallbackContext):
    goodbye_message = (
        "<i><b>Good bye!</b></i> 🌩\n"
        "━━━━━━━━━━━━━━━━━\n"
        "<i><b>Enjoy my use.</b></i>"
    )
    await update.callback_query.edit_message_text(text=goodbye_message, parse_mode="HTML")
