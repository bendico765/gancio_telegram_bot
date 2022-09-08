import logging
from gancio_telegram_bot import config, handlers, callbacks
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler


logging.basicConfig(
	filename='logfile.log',
	format="%(asctime)s %(levelname)s %(message)s",
	datefmt="%Y-%m-%d %H:%M:%S",
	encoding='utf-8',
	level=logging.INFO
)


if __name__ == "__main__":
	application = ApplicationBuilder().token(config.token).build()

	application.add_handlers(
		[
			CommandHandler(["start", "aiuto"], handlers.help),
			CommandHandler("calendario", handlers.show_calendar)
		]
	)

	application.add_handler(CallbackQueryHandler(callbacks.page_turn))

	application.run_polling()
