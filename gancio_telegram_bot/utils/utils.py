from telegram import Update, Message
from telegram.ext import ContextTypes
from datetime import datetime, date
from math import floor

__all__ = [
	"send_connection_error_message",
	"get_current_day_timestamp",
	"events_to_html_format"
]


def hlink(text: str, url: str) -> str:
	"""
	Given a text and an url, returns a html formatted hyperlink

	:param text: Text of the hyperlink
	:param url: Url which the hyperlink refers to
	:return: the html formatted hyperlink
	"""
	return f"<a href='{url}'>{text}</a>"


async def send_connection_error_message(message: Message, context: ContextTypes.DEFAULT_TYPE):
	"""
	Displays the error message to the user

	:param message: message command sent by the user which caused the error
	:param context: context of the message
	"""
	await context.bot.sendPhoto(
		chat_id=message.chat.id,
		photo=open("./assets/error_occurred.jpeg", "rb"),
		caption="Si è verificato un errore, ma niente paura! Le nostre tecniche e i nostri tecnici sono già a lavoro per risolverlo",
		reply_to_message_id=message.message_id
	)


def get_current_day_timestamp() -> int:
	"""
	Gets current day (starting from 00:00:00) timestamp
	"""
	current_day = date.today()
	return floor(datetime(
		year=current_day.year,
		month=current_day.month,
		day=current_day.day
	).timestamp())


def events_to_html_format(events: list, instance_url: str) -> str:
	"""
	Given a list of events (dict), returns a html formatted message displaying them

	:param events: list of events fetched from the gancio instance
	:param instance_url: optional, the instance from whom the events belong to.
	If specified the event link is displayed in the message, otherwise not.
	:return: the html formatted string containing the events' description
	"""
	reply_message = ""
	for event in events:
		title = event["title"]
		slug = event["slug"]
		is_multidate = event["multidate"]
		start_datetime = datetime.fromtimestamp(event["start_datetime"]).strftime("%d/%m/%Y %H:%M")
		place_name = event["place"]["name"]
		address = event["place"]["address"]

		event_message = f"{title}\n\U0001F4CD {place_name} - {address}\n\U0001F550 {start_datetime}\n"

		"""
		if instance_url is not None:
			event_link = hlink("Approfondisci", f"{instance_url}/event/{slug}")
			event_message = f"{title}\n\U0001F4CD {place_name} - {address}\n\U0001F550 {start_datetime}\n{event_link}\n"
		else:
			event_message = f"{title}\n\U0001F4CD {place_name} - {address}\n\U0001F550 {start_datetime}\n"
		"""

		if is_multidate:
			event_message += "(Questo evento si compone di più date)\n"

		if instance_url is not None:
			event_link = hlink("Approfondisci", f"{instance_url}/event/{slug}")
			event_message += event_link + "\n"

		reply_message += event_message + "\n"
	return reply_message
