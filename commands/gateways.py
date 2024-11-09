from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from .show import show_page

async def gateways(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = f"<b>Welcome to Onyx / Onyx gateways Online</b>\n" \
              f"━━━━━━━━━━━━\n" \
              f"<b>Gates CMDS:</b>  <code>100 Api Gates!</code> ✅\n" \
              f"━━━━━━━━━━━━\n" \
              f"<b>Gates auth:</b> <code>31</code>     |    <b>Gates Charge:</b> <code>37</code>\n" \
              f"<b>Gates CCN (Auth & Charge):</b> <code>28</code>  |    <b>Gates Mass Checking:</b> <code>4</code>\n" \
              f"━━━━━━━━━━━━\n" \
              f"<b>Select the type of gate you want for your use!</b>\n"

    keyboard = [
        [
            InlineKeyboardButton(text="Auth", callback_data="auth"),
            InlineKeyboardButton(text="Charge", callback_data="charge"),
            InlineKeyboardButton(text="CCN Gates", callback_data="ccn_gates"),
        ],
        [
            InlineKeyboardButton(text="Mass Checking", callback_data="mass_checking"),
            InlineKeyboardButton(text="Back", callback_data="back_start"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(message, parse_mode="HTML", reply_markup=reply_markup)

async def auth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_page(update, 0)

async def charge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_page(update, 0)

async def ccn_gates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_page(update, 0)

async def mass_checking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_page(update, 0)
