import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date, timedelta, datetime


_all_ = [
	"plot_week_calendar_usage"
]


def _parse_line(line: str) -> dict:
	try:
		line = line[0:-1] # delete newline
		tokens = line.split(" ")

		return {
			"datetime": datetime.strptime(tokens[0] + " " + tokens[1], "%Y-%m-%d %H:%M:%S"),
			"level": tokens[2],
			"message": " ".join(tokens[3:])
		}
	except Exception:
		return {}


def plot_week_calendar_usage(filename: str):
	last_seven_days = [str(date.today() - timedelta(days=i)) for i in range(7)]
	last_seven_days.reverse()
	number_requests = [0 for _ in range(7)]

	with open(filename, "r") as f:
		for line in f:
			parsed_line = _parse_line(line)
			if parsed_line == {}:
				continue # a parsing error occured

			line_date = parsed_line["datetime"].date()
			if str(line_date) in last_seven_days:
				i = last_seven_days.index(str(line_date))
				number_requests[i] += 1

	df = pd.DataFrame(
		data = {
			"Day": last_seven_days,
			"Calendar requests": number_requests
		}
	)

	sns.barplot(x="Day", y="Calendar requests", data=df)
	plt.show()
