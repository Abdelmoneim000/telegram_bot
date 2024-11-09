from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMemberUpdated
from telegram.ext import CallbackContext
from .database import db
from .premium import admin_required

@admin_required
async def add_premium_commands(update: Update, context: CallbackContext):
    message = f"Premium commands:\n" \
              f"━━━━━━━━━━━━━\n"
    
    for command in db.get_premium_commands():
        message += f"<code>/{command['command']} - {command['description']}</code>\n"

    message += "━━━━━━━━━━━━━\n" \
               f"Instructions: How to Handle Premium Commands\n" \
               f"━━━━━━━━━━━━━\n" \
               f"1. /addcommand <command_name> <command_description>\n" \
               f"2. /deletecommand <command_name>\n" \
               f"3. /editcommand <command_name> <new_command_description>\n"

    keyboard = [
        [
            InlineKeyboardButton(text="Back", callback_data="back_start"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(message, reply_markup=reply_markup)

@admin_required
async def admin_portal(update: Update, context: CallbackContext):
    message = f"Admin Portal:\n" \
              f"━━━━━━━━━━━━━\n" \
              f"1. /addadmin <username>\n" \
              f"2. /removeadmin <username>\n" \
              f"3. /listadmins\n" \
              f"━━━━━━━━━━━━━\n" \
              f"4. /authorizegroup <group_id>\n" \
              f"5. /unauthorizegroup <group_id>\n" \
              f"━━━━━━━━━━━━━\n" \
              f"6. /authorizeuser <username>\n" \
              f"7. /unauthorizeuser <username>\n" \
              f"━━━━━━━━━━━━━\n" \
              f"8. /banuser <username>\n" \
              f"9. /unbanuser <username>\n" \
              
    keyboard = [
        [
            InlineKeyboardButton(text="Back", callback_data="back_start"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(message, reply_markup=reply_markup)
