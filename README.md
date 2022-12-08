# data_collection_bot

## Description

This is a telegram bot for collecting urls and xpaths for scrapping to the database.
Small scrapper for mean prices included.

It accepts xls files of this type:

name, url, xpath

## Getting started


### Dependencies

* Python 3.11
* python-telegram-bot 20.0a4
* aiohttp = 3.8.3

### Installing

Clone repository and install dependencies

```
poetry install
```

And activate venv:

```
poetry shell
```

Make .env file with bot token:

```
TOKEN=your bot token
```

Creata a database:

```
python data_handler/database/create_db.py
```

Start the bot:

```
python bot.py
```