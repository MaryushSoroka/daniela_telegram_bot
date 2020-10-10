from telegram import Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
import requests
import re


def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url


def bop(update, context):
    url = get_url()
    update
    context
    chat_id = bot.message.chat.id
    bot.send_photo(chat_id=chat_id, photo=url)


def main():
    updater = Updater('1227978888:AAHkkmUt6YBjR8aE3n8XSsHKuBuDAIWxNQs')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop', bop))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
