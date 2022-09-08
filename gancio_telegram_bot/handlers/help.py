from telegram import Update
from telegram.ext import ContextTypes


__all__ = ["help"]


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await context.bot.send_message(
		chat_id=update.effective_chat.id,
		text="Fatto con \u2764 da @bendico765"
	)
