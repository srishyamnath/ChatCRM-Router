import json
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from utils.tenant_loader import get_tenant_config
from crm.crm_router import send_to_crm

# Map your bot token → tenant_id
BOT_TOKEN_TENANT_MAP = {
    "8016794857:AAEZjR8E-Zz9R454XaAUTE8xDaTIZgiKNTE": "lifecode_india"
}

def extract_lead_data(message_text: str) -> dict:
    name_match = re.search(r"my name is ([\w\s]+)", message_text, re.I)
    email_match = re.search(r"[\w\.-]+@[\w\.-]+", message_text)
    phone_match = re.search(r"\d{10}", message_text)

    return {
        "name": name_match.group(1).strip() if name_match else "Unknown",
        "email": email_match.group(0) if email_match else "unknown@example.com",
        "phone": phone_match.group(0) if phone_match else "0000000000",
        "message": message_text
    }

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    chat_id = update.effective_chat.id

    # Get bot token and map to tenant
    bot_token = context.bot.token
    tenant_id = BOT_TOKEN_TENANT_MAP.get(bot_token)

    if not tenant_id:
        await context.bot.send_message(chat_id=chat_id, text="❌ Unauthorized bot.")
        return

    tenant_config = get_tenant_config(tenant_id)
    lead_data = extract_lead_data(message_text)

    # Send to CRM
    send_to_crm(lead_data, tenant_config)

    # Reply to user
    welcome_msg = tenant_config["branding"].get("welcome_message", "Hello!")
    name = lead_data.get("name", "there")
    reply = f"""
{welcome_msg}

Thank you, {name}! Your information has been received and a ticket has been created in our system. Our team will be in touch shortly.
"""

    await context.bot.send_message(chat_id=chat_id, text=reply)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Please introduce yourself so we can assist you.")

def main():
    # Use the first token from the map to initialize the bot
    bot_token = list(BOT_TOKEN_TENANT_MAP.keys())[0]
    app = ApplicationBuilder().token(bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
