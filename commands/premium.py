from telegram import Update
from functools import wraps
from telegram.ext import ContextTypes
from commands.database import db
import sqlite3

DB_PATH = "database.db"



def admin_required(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        # Check if it's a callback query or a message
        if update.callback_query:
            user_id = update.callback_query.from_user.id  # Get the user ID from the callback query
        elif update.message:
            user_id = update.message.from_user.id  # Get the user ID from the message
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Unable to identify user.")
            return  # Exit if neither is present

        if not db.is_admin(user_id):  # Check if the user is an admin
            await context.bot.send_message(chat_id=update.effective_chat.id, text="You do not have permission to use this command.")
            return  # Exit if the user is not an admin
        
        return await func(update, context, *args, **kwargs)  # Call the original function
    return wrapper

@admin_required
async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /addadmin <username>")
        return
    username = str(context.args[0])
    db.add_admin(username)
    await update.message.reply_text("Admin added successfully")

@admin_required
async def remove_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /removeadmin <username>")
        return
    username = str(context.args[0])
    user = db.get_user_by_username(username)
    if not user or user[3] == 0:
        await update.message.reply_text("User not found or is not an admin.")
        return
    if db.is_owner(user[1]):
        await update.message.reply_text("You cannot remove the owner.")
        return
    db.remove_admin(username)
    await update.message.reply_text("Admin removed successfully")

@admin_required
async def list_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admins = db.get_admins()
    message = "Admins:\n"
    for admin in admins:
        message += f"@{admin['username']}\n"
    await update.message.reply_text(message)

@admin_required
async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args is None or len(context.args) < 2:
        message = "Usage: /addcommand <command_name> <command_description>"
        await update.message.reply_text(message)
        return
    command = context.args[0]
    description = " ".join(context.args[1:])
    db.add_premium_command(command, description)
    await update.message.reply_text(f"Added command: /{command} - {description}")

@admin_required
async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /deletecommand <command>")
        return
    command = context.args[0]
    db.delete_premium_command(command)
    await update.message.reply_text(f"Deleted command: /{command}")

@admin_required
async def edit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /editcommand <command> <new_description>")
        return
    command = context.args[0]
    description = " ".join(context.args[1:])
    if db.update_premium_command(command, description):
        await update.message.reply_text(f"Updated command: /{command} - {description}")
    else:
        await update.message.reply_text(f"Command not found: /{command}")

@admin_required
async def list_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = db.get_premium_commands()
    message = "Premium commands:\n"
    for command in commands:
        message += f"/{command['command']} - {command['description']}\n"
    await update.message.reply_text(message)

@admin_required
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /broadcast <message>")
        return
    
    message = " ".join(context.args)
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Fetch usernames instead of user_ids
    cursor.execute("SELECT user_id FROM authorized_users")
    user_ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    if not user_ids:
        await update.message.reply_text("No authorized users found.")
        return
    
    for user_id in user_ids:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            print(f"Could not send message to {user_id}: {e}")

@admin_required
async def authorize_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if not context.args:
        await update.message.reply_text("Usage: /authorizeuser <username>")
        return
    username = str(context.args[0])
    user = db.get_user_by_username(username)
    if not user:
        await update.message.reply_text("User not found.")
        return
    db.authorize_user(user[1], user[2])
    await update.message.reply_text(f"Authorized user: {username}")

@admin_required
async def unauthorize_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /unauthorizeuser <username>")
        return
    username = int(context.args[0])
    db.unauthorize_user(username)
    await update.message.reply_text(f"Unauthorized user: {username}")

@admin_required
async def authorize_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /authorize_group <group_id>")
        return
    group_id = int(context.args[0])
    db.authorize_group(group_id)
    await update.message.reply_text(f"Authorized group: {group_id}")

@admin_required
async def unauthorize_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /unauthorize_group <group_id>")
        return
    group_id = int(context.args[0])
    db.unauthorize_group(group_id)
    await update.message.reply_text(f"Unauthorized group: {group_id}")

@admin_required
async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /ban_user <username>")
        return
    username = int(context.args[0])
    db.ban_user(username)
    await update.message.reply_text(f"Banned user: {username}")

@admin_required
async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /unban_user <username>")
        return
    username = int(context.args[0])
    db.unban_user(username)
    await update.message.reply_text(f"Unbanned user: {username}")
