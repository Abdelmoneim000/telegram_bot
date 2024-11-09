from telegram import Update
from telegram.ext import ContextTypes
from .close import close
from .gateways import gateways, auth, charge, ccn_gates, mass_checking
from .tools import tools
from .information import information
from .xcloud import xcloud
from .back import back
from .start import start
from .show import show_page, show_tools
from .handlers import add_premium_commands, admin_portal

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "add_premium_commands":
        await add_premium_commands(update, context)
    elif query.data == "admin_portal":
        await admin_portal(update, context)
    elif query.data == "close":
        await close(update, context)
    elif query.data == "back_start":
        await back(update, context, start)
    elif query.data == "home_gateways":
        await gateways(update, context)
    elif query.data == "gateways":
        await gateways(update, context)
    elif query.data == "auth":
        await auth(update, context)
    elif query.data == "charge":
        await charge(update, context)
    elif query.data == "ccn_gates":
        await ccn_gates(update, context)
    elif query.data == "mass_checking":
        await mass_checking(update, context)
    elif query.data == "tools":
        await tools(update, context)
    elif query.data == "information":
        await information(update, context)
    elif query.data == "xcloud":
        await xcloud(update, context)

    elif query.data.startswith("page_"):
        page = int(query.data.split("_")[1])  # Extract the page number from the callback data
        await show_page(update, page)

    elif query.data.startswith("toolspage_"):
        page = int(query.data.split("_")[1])  # Extract the page number from the callback data
        await show_tools(update, page)
