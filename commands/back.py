from telegram import Update
from telegram.ext import ContextTypes

async def back(update: Update, context: ContextTypes.DEFAULT_TYPE, callback_func):
    """Handle the back button."""
    await callback_func(update, context)
