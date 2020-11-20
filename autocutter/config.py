import json
from pathlib import Path
from tempfile import TemporaryDirectory

try:
    with open('config.json') as file:
        config = json.load(file)
    TOKEN = config['token']
except:
    raise FileNotFoundError("Você deve criar um arquivo config.json com o token de um bot do telegram.")

try:
    DB_PATH = Path(config['db_path'])
except:
    DB_PATH = Path().cwd() / 'database.db'

tempdir = TemporaryDirectory()
TEMP_PATH = Path(tempdir.name)