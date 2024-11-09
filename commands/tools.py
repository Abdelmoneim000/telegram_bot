from telegram import Update
from telegram.ext import ContextTypes
from .show import show_tools

async def tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_tools(update, 0)
