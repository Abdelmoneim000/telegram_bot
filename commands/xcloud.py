from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def xcloud(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(text="Home", callback_data="back_start"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.edit_message_text(
        "XCloud is a cloud gaming service that allows you to play Xbox games on multiple devices.", parse_mode="HTML", reply_markup=reply_markup
    )
