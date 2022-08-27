from telebot.formatting import hlink
from datetime import datetime, date
from math import floor

__all__ = [
	"get_current_day_timestamp",
	"events_to_html_format"
]


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


def events_to_html_format(instance_url: str, events: list) -> str:
	"""
	Given a list of events (dict), returns a html formatted message displaying them
	"""
	reply_message = ""
	for event in events:
		# event_id = event["id"]
		title = event["title"]
		slug = event["slug"]
		is_multidate = event["multidate"]
		start_datetime = datetime.fromtimestamp(event["start_datetime"]).strftime("%d/%m/%Y %H:%M")
		place_name = event["place"]["name"]
		address = event["place"]["address"]
		#event_link = hlink("Approfondisci", f"{instance_url}/event/{slug}")
		# event_link = f"/event_{event_id}"
		#event_message = f"{title}\n\U0001F4CD {place_name} - {address}\n\U0001F550 {start_datetime}\n{event_link}"
		event_message = f"{title}\n\U0001F4CD {place_name} - {address}\n\U0001F550 {start_datetime}\n"
		if is_multidate:
			event_message += "(Questo evento si compone di più date)\n"
		reply_message += event_message + "\n"
	return reply_message
