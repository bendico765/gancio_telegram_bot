from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from gancio_telegram_bot import utils, config
import gancio_requests
import logging

__all__ = ["show_calendar"]


async def show_calendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
	"""
	Shows the events in the calendar
	"""
	logging.info(f"{update.message.from_user.username} fetches calendar")

	# we need to request the events from the start of the current day
	response = await gancio_requests.request.get_events(
		config.instance_url,
		params={"start": utils.get_current_day_timestamp()},
		cache=config.cache
	)

	if response["status"] != 200:
		await utils.send_connection_error_message(update.message, context)
	else:
		calendar = response["json_content"]
		if len(calendar) == 0:
			await update.message.reply_text("Non ci sono eventi in calendario!")
		else:
			if len(calendar) > config.elements_in_menu:
				markup = InlineKeyboardMarkup(
					[
						[
							InlineKeyboardButton(
								text="2>",
								callback_data="events_page_2"
							)
						]
					]
				)
			else:
				markup = None

			reply_message = utils.events_to_html_format(
				calendar[:config.elements_in_menu],
				config.instance_url if config.show_event_url else None
			)
			await context.bot.send_message(
				update.effective_chat.id,
				text=reply_message,
				parse_mode="html",
				disable_web_page_preview=True,
				reply_markup=markup
			)
