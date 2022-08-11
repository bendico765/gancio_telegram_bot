import os
import asyncio
import gancio_requests
import utils
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.async_telebot import AsyncTeleBot
from telebot.formatting import hlink
from dotenv import load_dotenv
from itertools import islice
from aiohttp_client_cache import SQLiteBackend
from math import ceil

load_dotenv()
token = os.getenv("AUTH_TOKEN")
instance_url = os.getenv("INSTANCE_URL")
elements_in_menu = int(os.getenv("MENU_ELEMENTS"))
error_occurred_image_path = "./assets/error_occurred.jpeg"
cache = SQLiteBackend(
	cache_name=os.getenv("CACHE_NAME"),
	expire_after=int(os.getenv("HTTP_CACHE_EXPIRATION_SECONDS"))
)
bot = AsyncTeleBot(token)


def get_menu_markup(requested_page: int, number_available_pages: int) -> InlineKeyboardMarkup:
	markup = InlineKeyboardMarkup()

	if number_available_pages == 1:
		markup = None
	elif number_available_pages == 2:
		if requested_page == 1:
			markup.row_width = 1
			markup.add(
				InlineKeyboardButton("2>", callback_data="events_page_2")
			)
		else:
			markup.row_width = 1
			markup.add(
				InlineKeyboardButton("<1", callback_data="events_page_1")
			)
	elif number_available_pages == 3:
		if requested_page == 1:
			markup.row_width = 1
			markup.add(
				InlineKeyboardButton("2>", callback_data="events_page_2")
			)
		elif requested_page == 2:
			markup.row_width = 2
			markup.add(
				InlineKeyboardButton("<1", callback_data="events_page_1"),
				InlineKeyboardButton("3>", callback_data="events_page_3")
			)
		else:
			markup.row_width = 2
			markup.add(
				InlineKeyboardButton("<<1", callback_data="events_page_1"),
				InlineKeyboardButton("<2", callback_data="events_page_2")
			)
	else:
		if requested_page == 1:
			markup.row_width = 1
			markup.add(
				InlineKeyboardButton("2>", callback_data="events_page_2")
			)
		elif requested_page == 2:
			markup.row_width = 2
			markup.add(
				InlineKeyboardButton("<1", callback_data="events_page_1"),
				InlineKeyboardButton("3>", callback_data="events_page_3")
			)
		elif requested_page == number_available_pages:
			markup.row_width = 2
			second_last_page = number_available_pages - 1
			markup.add(
				InlineKeyboardButton(f"<<1", callback_data=f"events_page_1"),
				InlineKeyboardButton(f"<{second_last_page}", callback_data=f"events_page_{second_last_page}")
			)
		else:  # 2 < requested_page < number_available_pages
			markup.row_width = 3
			previous_page = requested_page - 1
			next_page = requested_page + 1
			markup.add(
				InlineKeyboardButton("<<1", callback_data="events_page_1"),
				InlineKeyboardButton(f"<{previous_page}", callback_data=f"events_page_{previous_page}"),
				InlineKeyboardButton(f"{next_page}>", callback_data=f"events_page_{next_page}")
			)

	return markup


async def send_connection_error_message(message):
	await bot.send_photo(
		chat_id=message.chat.id,
		photo=open(error_occurred_image_path, "rb"),
		caption="Si è verificato un errore, ma niente paura! Le nostre tecniche e i nostri tecnici sono già a lavoro per risolverlo",
		reply_to_message_id=message.message_id
	)


@bot.message_handler(commands=['aiuto'])
async def help(message):
	eigenlab_reference = "Fatto con \u2764 da " + hlink("EigenLab", "https://eigenlab.org/")
	await bot.reply_to(message, eigenlab_reference, parse_mode="html")


@bot.callback_query_handler(func=lambda call: "events_page" in call.data)
async def page_turn_handler(callback_query):
	requested_page = int(callback_query.data.split("_")[-1])
	message_to_change = callback_query.message

	# get new events
	response = await gancio_requests.requests.get_events(
		instance_url,
		params={"start": utils.get_current_day_timestamp()},
		cache=cache
	)
	if response["status"] != 200:
		await send_connection_error_message(message_to_change)
	else:
		calendar = response["json_content"]
		if len(calendar) == 0:
			await bot.reply_to(
				message_to_change,
				"Il calendario è troppo vecchio e al momento non ci sono nuovi eventi!"
			)
		else:
			# get new events page
			iterator = iter(calendar)
			number_available_pages = ceil(len(calendar) / elements_in_menu)
			events_groups = [list(islice(iterator, elements_in_menu)) for _ in range(number_available_pages)]

			# check if requested page still exists
			if not (requested_page - 1 < number_available_pages):
				new_msg = await bot.reply_to(
					message_to_change,
					"Le informazioni di questo calendario sono vecchie, mando il calendario aggiornato "
				)
				await show_calendar(new_msg)
				return

			new_text = utils.events_to_html_format(instance_url, events_groups[requested_page - 1])

			# aggiungere casi ultima pagina e ritorno alla prima pagina
			markup = get_menu_markup(requested_page, number_available_pages)

			await bot.edit_message_text(
				new_text,
				chat_id=message_to_change.chat.id,
				message_id=message_to_change.message_id,
				disable_web_page_preview=True,
				reply_markup=markup,
				parse_mode="html"
			)


@bot.message_handler(commands=['calendario'])
async def show_calendar(message):
	# we need to request the events from the start of the current day
	response = await gancio_requests.requests.get_events(
		instance_url,
		params={"start": utils.get_current_day_timestamp()},
		cache=cache
	)

	if response["status"] != 200:
		await send_connection_error_message(message)
	else:
		calendar = response["json_content"]
		if len(calendar) == 0:
			await bot.reply_to(message, "Non ci sono eventi in calendario!")
		else:
			if len(calendar) > elements_in_menu:
				markup = InlineKeyboardMarkup()
				markup.row_width = 1
				markup.add(
					InlineKeyboardButton("2>", callback_data="events_page_2")
				)
			else:
				markup = None

			reply_message = utils.events_to_html_format(instance_url, calendar[:elements_in_menu])
			await bot.reply_to(
				message,
				reply_message,
				disable_web_page_preview=True,
				reply_markup=markup,
				parse_mode="html"
			)


if __name__ == "__main__":
	asyncio.run(bot.infinity_polling())
