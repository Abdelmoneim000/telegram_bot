from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import sqlite3

items_per_page = 5

async def show_page(update: Update, page: int):
    """Show page of items"""
    query = update.callback_query
    await query.answer()

    # Open a new connection for each command
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        offset = (page - 1) * items_per_page

        # Get total items and calculate total pages
        cursor.execute('SELECT COUNT(*) FROM gateways')
        total_items = cursor.fetchone()[0]
        total_pages = (total_items // items_per_page) + (1 if total_items % items_per_page > 0 else 0)

        # Fetch items for the current page
        cursor.execute('''
            SELECT name, format, condition, comment, type, amount
            FROM gateways
            LIMIT ? OFFSET ?
        ''', (items_per_page, offset))
        page_items = cursor.fetchall()

    # Create header
    header = (
        "<a href='tg://resolve?domain=Onyxcheck_bot'>[ϟ]</a> Onyx gateways online | "
        f"<code>Charge Gateways P: {page}/{total_pages}</code>\n"
        "━━━━━━━━━━━━\n"
    )

    # Format each gateway's details with invisible link
    message = header
    for i, gateway in enumerate(page_items):
        name, format_, condition, comment, type_, amount = gateway
        message += (
            f"<a href='tg://resolve?domain=Onyxcheck_bot'>[ϟ]</a> Name: <code>{name}</code>\n"
            f"<a href='tg://resolve?domain=Onyxcheck_bot'>[ϟ]</a> Format: <code>{format_}</code> | "
            f"<a href='tg://resolve?domain=Onyxcheck_bot'>[ϟ]</a> Amount: <code>{amount}</code>\n"
            f"<a href='tg://resolve?domain=Onyxcheck_bot'>[ϟ]</a> Condition: <code>{condition}</code> | "
            f"<a href='tg://resolve?domain=Onyxcheck_bot'>[ϟ]</a> Comment: <code>{comment}</code>\n"
            f"<a href='tg://resolve?domain=Onyxcheck_bot'>[ϟ]</a> Type: <code>{type_}</code>\n"
        )
        if i < len(page_items) - 1:
            message += "\n"
    message += "━━━━━━━━━━━━"

    keyboard = []

    button_row = []

    if page == 0:
        button_row.append(InlineKeyboardButton("Back", callback_data="home_gateways"))

    # Previous button
    if page > 0:
        button_row.append(InlineKeyboardButton("Back", callback_data=f"page_{page - 1}"))

    # Next button
    if page < total_pages - 1:
        button_row.append(InlineKeyboardButton("Next", callback_data=f"page_{page + 1}"))

    if button_row:
        keyboard.append(button_row)

    keyboard.append([InlineKeyboardButton("Home", callback_data="home_gateways")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.edit_message_text(message, parse_mode="HTML", reply_markup=reply_markup)

async def show_information(update: Update, page: int):
    query = update.callback_query
    await query.answer()

    message = (
        "Onyx Credits and info! 🌩\n"
        "━━━━━━━━━━━━\n"
        "Channels:\n"
        "Onyx Updates: @onyxcheckbot\n"
        "Onyx References channel: @onyxcheckbot\n"
        "Onyx Free Users: @freeusersdev\n"
        "━━━━━━━━━━━━━━━━━\n"
        "Onyx Information:\n"
        "━━━━━\n"
        "Dev: @littleconditions ✅\n"
        "Dev Note: Hi guys, this is the new version of Onyx, made with speed and good checking experience in mind!\n"
        "━━━━━\n"
        "Hunters:\n"
        "@None | 000000000 ✅\n"
        "━━━━━━━━━━━━━━━━━\n"
        "Onyx Updates:\n"
        "Version: 3.2.0 [✅]\n"
        "Update: 25/10/2023 22:06 p.m (GMT-5) [✅]\n"
        "━━━━━━━━━━━━━━━━━\n"
        "Report problems to: @onyx_apis"
    )
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data="back_start"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.edit_message_text(message, reply_markup=reply_markup)

async def show_tools(update: Update, page: int):
    query = update.callback_query
    await query.answer()

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        offset = (page - 1) * items_per_page

        # Get total items and calculate total pages
        cursor.execute('SELECT COUNT(*) FROM gateways')
        total_items = cursor.fetchone()[0]
        total_pages = (total_items // items_per_page) + (1 if total_items % items_per_page > 0 else 0)

        # Fetch items for the current page
        cursor.execute('SELECT name, format, condition FROM gateways LIMIT ? OFFSET ?', (items_per_page, offset))
        gateways = cursor.fetchall()

    # Format the response message
    message = f"Onyx Tools / Page {page if page > 0 else 1}\n━━━━━━━━━━━━\n"
    for name, format_str, condition in gateways:
        message += f"{name}:\nFormat: <code>{format_str}</code>\nCondition: <code>{condition}</code>\n━━━━━━━━━━━━\n"

    keyboard = []

    button_row = []

    if page == 0:
        button_row.append(InlineKeyboardButton("Back", callback_data="back_start"))

    # Previous button
    if page > 0:
        button_row.append(InlineKeyboardButton("Back", callback_data=f"toolspage_{page - 1}"))

    # Next button
    if page < total_pages - 1:
        button_row.append(InlineKeyboardButton("Next", callback_data=f"toolspage_{page + 1}"))

    if button_row:
        keyboard.append(button_row)

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.edit_message_text(message, parse_mode="HTML", reply_markup=reply_markup)
