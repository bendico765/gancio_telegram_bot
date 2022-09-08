# gancio_telegram_bot

``gancio_telegram_bot`` is a bot which allows to interact with a specified Gancio instance.
[Gancio](https://gancio.org/) is a shared agenda for local communities, a project which wants to provide
a self-hosted solution to host and organize events.  

![](https://github.com/bendico765/gancio_telegram_bot/blob/master/assets/bot_overview.gif?raw=true)

## Installation
To install the latest version of the bot just download (or clone) the current project,
open a terminal and run the following commands:
```shell
pip install -r requirements.txt
pip install .
```
Alternatively, use pip:
```shell
pip install gancio_telegram_bot
```
It's also possible to create a docker image and run the application in a container; see [Docker usage](#docker). 

### Dependencies
At the moment I have tested the bot only on _python == 3.10.4_  
The bot requires the dependencies specified in _requirements.txt_ and I haven't still tested
other versions.

## Usage
### Configuration file (.env)
The bot relies on environment variables for its configuration; some parameters are strictly required 
(e.g. AUTH_TOKEN, INSTANCE_URL), while others just allow to personalize the bot appearance.

| Parameter                     | Function                                                                                             |
|-------------------------------|------------------------------------------------------------------------------------------------------|
| AUTH_TOKEN                    | Telegram bot authentication token                                                                    |
| INSTANCE_URL                  | Url of the gancio instance from which fetch the events                                               |
| SHOW_EVENT_URL                | Set to "True" if each event must be accompanied by its url on the Gancio instance (default is False) |
| MENU_ELEMENTS                 | Number of events to show in a single message (default is 3)                                          |
| CACHE_NAME                    | Path to the database used for caching (default disable the cache mechanism)                          |
| HTTP_CACHE_EXPIRATION_SECONDS | How many seconds the cache lasts (default is 10 minutes)                                             |

### Command line interface
```shell
python3 -m gancio_telegram_bot
```

### Docker
```shell
docker compose up -d
```

## Visualisation
The package comes up with some functions to allow the parsing of the
logfile and the visualisation of statistics related to the usage of the bot.

![](https://github.com/bendico765/gancio_telegram_bot/blob/master/assets/visualisation_example.png?raw=true)

## Todolist
- Better define which versions of python and dependency packages are compatible.
- Create some tests.
- Allow to define more fine-grained queries for the events (e.g. display just the events in a specific date).
- Make more visualisation plots.