from telegram import Update
from telegram.ext import ContextTypes
from .show import show_information

async def information(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_information(update, 0)