import logging 
from telegram.ext import Updater

from commands import HANDLERS
from config import TOKEN

logging.basicConfig()

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    for handler in HANDLERS:
        dp.add_handler(handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()