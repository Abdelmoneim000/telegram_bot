from telegram.ext import CommandHandler, CallbackQueryHandler, Application
from config import api_token
from commands import start, button, add_command, delete_command, edit_command,broadcast, authorize_user, unauthorize_user, authorize_group, unauthorize_group, ban_user, unban_user, add_admin, remove_admin, list_commands
from commands.database import db
# from commands.handlers import handle_chat_member_update

# db.insert_gateways()

application = Application.builder().token(api_token).build()

# Add handlers for commands and button responses
application.add_handler(CommandHandler('start', start))

# Admin commands
application.add_handler(CommandHandler('addadmin', add_admin))
application.add_handler(CommandHandler('removeadmin', remove_admin))
application.add_handler(CommandHandler('listcommands', list_commands))

 # Premium command management
application.add_handler(CommandHandler("addcommand", add_command))
application.add_handler(CommandHandler("deletecommand", delete_command))
application.add_handler(CommandHandler("editcommand", edit_command))

# Broadcast command
application.add_handler(CommandHandler("broadcast", broadcast))

# Authorization and ban commands
application.add_handler(CommandHandler("authorizeuser", authorize_user))
application.add_handler(CommandHandler("unauthorizeuser", unauthorize_user))
application.add_handler(CommandHandler("authorizegroup", authorize_group))
application.add_handler(CommandHandler("unauthorizegroup", unauthorize_group))
application.add_handler(CommandHandler("banuser", ban_user))
application.add_handler(CommandHandler("unbanuser", unban_user))

# Buttons
application.add_handler(CallbackQueryHandler(button))

# application.add_handler(ChatMemberHandler(handle_chat_member_update, ChatMemberHandler.CHAT_MEMBER))

application.run_polling()
