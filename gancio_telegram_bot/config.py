import os
from dotenv import load_dotenv
from aiohttp_client_cache import SQLiteBackend


load_dotenv()
token = os.getenv("AUTH_TOKEN")
instance_url = os.getenv("INSTANCE_URL")
show_event_url = os.getenv("SHOW_EVENT_URL") == "True"
elements_in_menu = int(os.getenv("MENU_ELEMENTS")) if os.getenv("MENU_ELEMENTS") is not None else 3

if os.getenv("CACHE_NAME") is not None:
	if os.getenv("HTTP_CACHE_EXPIRATION_SECONDS") is not None:
		cache = SQLiteBackend(
			cache_name=os.getenv("CACHE_NAME"),
			expire_after=int(os.getenv("HTTP_CACHE_EXPIRATION_SECONDS"))
		)
	else:
		cache = SQLiteBackend(
			cache_name=os.getenv("CACHE_NAME"),
			expire_after=600
		)
else:
	cache = None
