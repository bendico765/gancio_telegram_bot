import gancio_requests
from gancio_telegram_bot import config, utils, handlers
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from math import ceil
from itertools import islice


__all__ = ["page_turn"]


def get_menu_markup(requested_page: int, number_available_pages: int) -> InlineKeyboardMarkup:
	"""
	Creates a new keyboard layout to navigate the calendar events

	:param requested_page: index of the calendar page requested by the user
	:param number_available_pages: total number of calendar pages available
	:return: the new layout of the message
	"""
	if number_available_pages == 1:
		markup = None
	elif number_available_pages == 2:
		if requested_page == 1:
			markup = InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton(text="2>", callback_data="events_page_2")
					]
				]
			)
		else:
			markup = InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton(text="<1", callback_data="events_page_1")
					]
				]
			)
	elif number_available_pages == 3:
		if requested_page == 1:
			markup = InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton(text="2>", callback_data="events_page_2")
					]
				]
			)
		elif requested_page == 2:
			markup = InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("<1", callback_data="events_page_1"),
						InlineKeyboardButton("3>", callback_data="events_page_3")
					]
				]
			)
		else:
			markup = InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("<<1", callback_data="events_page_1"),
						InlineKeyboardButton("<2", callback_data="events_page_2")
					]
				]
			)
	else:
		if requested_page == 1:
			markup = InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton(text="2>", callback_data="events_page_2")
					]
				]
			)
		elif requested_page == 2:
			markup = InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("<1", callback_data="events_page_1"),
						InlineKeyboardButton("3>", callback_data="events_page_3")
					]
				]
			)
		elif requested_page == number_available_pages:
			second_last_page = number_available_pages - 1
			markup = InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton(f"<<1", callback_data=f"events_page_1"),
						InlineKeyboardButton(f"<{second_last_page}", callback_data=f"events_page_{second_last_page}")
					]
				]
			)
		else:  # 2 < requested_page < number_available_pages
			previous_page = requested_page - 1
			next_page = requested_page + 1
			markup = InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("<<1", callback_data="events_page_1"),
						InlineKeyboardButton(f"<{previous_page}", callback_data=f"events_page_{previous_page}"),
						InlineKeyboardButton(f"{next_page}>", callback_data=f"events_page_{next_page}")
					]
				]
			)

	return markup


async def page_turn(update: Update, context: ContextTypes.DEFAULT_TYPE):
	"""
	Edits the calendar message every time the user requests a new page
	"""
	requested_page = int(update.callback_query.data.split("_")[-1])
	message_to_change = update.callback_query.message

	# get new events
	response = await gancio_requests.request.get_events(
		config.instance_url,
		params={"start": utils.get_current_day_timestamp()},
		cache=config.cache
	)

	if response["status"] != 200:
		await utils.send_connection_error_message(message_to_change, context)
	else:
		calendar = response["json_content"]
		if len(calendar) == 0:
			await message_to_change.reply_text(
				text="Il calendario è troppo vecchio e al momento non ci sono nuovi eventi!"
			)
		else:
			# get new events page
			iterator = iter(calendar)
			number_available_pages = ceil(len(calendar) / config.elements_in_menu)
			events_groups = [list(islice(iterator, config.elements_in_menu)) for _ in range(number_available_pages)]

			# check if requested page still exists
			if not (requested_page - 1 < number_available_pages):
				await message_to_change.reply_text(
					text="Le informazioni di questo calendario sono vecchie, mando il calendario aggiornato"
				)
				await handlers.show_calendar(update, context)
				return

			new_text = utils.events_to_html_format(
				events_groups[requested_page - 1],
				config.instance_url if config.show_event_url else None
			)

			markup = get_menu_markup(requested_page, number_available_pages)

			await context.bot.edit_message_text(
				new_text,
				chat_id=update.effective_chat.id,
				message_id=message_to_change.message_id,
				disable_web_page_preview=True,
				reply_markup=markup,
				parse_mode="html"
			)
