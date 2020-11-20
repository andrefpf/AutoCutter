import json
import pathlib

with open('config.json') as file:
    config = json.load(file)

TOKEN = config['token']

try:
    DB_PATH = pathlib.Path(config['db_path'])
except:
    DB_PATH = pathlib.Path().cwd() / 'database.db'
