import requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

from resources import *

users = dict()

answers = ["", "", "8", "bag", "", "", "5777", "7308"]
messages = [(img1, [str1]),
            (img2, [str2]),
            (img3, [str3]),
            (img4, [str4]),
            (img5, [str5]),
            (img6, [str6]),
            (None, [str7]),
            (None, [str8]),
            (img9, [str9])]


# def bop(update, context):
#     contents = requests.get('https://random.dog/woof.json').json()
#     url = contents['url']
#     chat_id = update.message.chat.id
#     context.bot.send_photo(chat_id=chat_id, photo=url)
def start(update: Update, context: CallbackContext):
    bot = context.bot
    chat_id = update.effective_chat.id

    users[chat_id] = -1

    print('{name}: /start;'.format(name=update.effective_chat.first_name))
    nextLevel(bot, chat_id)


def next(update: Update, context: CallbackContext):
    bot = context.bot
    chat_id = update.effective_chat.id

    try:
        step = users[chat_id]
    except KeyError:
        start(update, context)
        return

    if step >= len(answers):
        msg = bot.send_message(chat_id, "а всё уже :( кинь команду /start чтобы начать заново")
        print('{name}: /next; ans: {msg}'.format(name=update.effective_chat.first_name, msg=msg.text))
        return

    if answers[step] == "":
        print('{name}: /next;'.format(name=update.effective_chat.first_name))
        nextLevel(bot, chat_id)
    else:
        msg = bot.send_message(chat_id, "Сначала разгадай загадку!")
        print('{name}: /next; ans: {msg}'.format(name=update.effective_chat.first_name, msg=msg.text))


def restart(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    users[chat_id] = 0
    start(update, context)


def nextLevel(bot, chat_id):
    users[chat_id] += 1

    img, strList = messages[users[chat_id]]

    if img is not None:
        msg = bot.send_photo(chat_id, img)
        print('img')

        # print(msg.photo[-1].file_id)

    for str in strList:

        keyboardMarkup = InlineKeyboardMarkup.from_button(InlineKeyboardButton('Следующая страничка', callback_data='u'))

        msg = bot.send_message(chat_id, str, reply_markup=keyboardMarkup)
        print(str)

    # for str in messages[users[chat_id]]:
    #     bot.send_message(chat_id, str)


def bullsAndCows(ans, guess):
    try:
        int(guess)
    except ValueError:
        return "Ящик открывается четырьмя цифрами"

    if len(guess.replace(' ', '')) != 4:
        return "Ящик открывается четырьмя цифрами"

    if len(list(guess)) != len(set(guess)):
        return "Цифры не должны повторяться"

    if ans == guess:
        return ""

    cow = 0
    bullCow = 0

    for i in range(0, 4):
        if ans[i] == guess[i]:
            cow += 1

    for i in guess:
        if i in ans:
            bullCow += 1

    bull = bullCow - cow

    return "Быки: {}\nКоровы: {}".format(cow, bull)


def reply(update: Update, context: CallbackContext):
    bot = context.bot
    chat_id = update.effective_chat.id
    text = update.message.text

    try:
        step = users[chat_id]
    except KeyError:
        start(update, context)
        return

    if step >= len(answers):
        msg = bot.send_message(chat_id, "а всё уже :( кинь команду /start чтобы начать заново")
        print('{name}: {text}; ans: {msg}'.format(name=update.effective_chat.first_name, msg=msg.text, text=text))
        return

    ans = answers[step]

    if step == 7:
        message = bullsAndCows(ans, text)
        if message == "":
            bot.send_message(chat_id, 'Загляни за кроватку')
            print('{name}: {text}; ans: Загляни за кроватку'.format(name=update.effective_chat.first_name, text=text))
            nextLevel(bot, chat_id)
        else:
            bot.send_message(chat_id, message)
            print('{name}: {text}; ans: {msg}'.format(name=update.effective_chat.first_name, msg=message, text=text))
    else:
        if (ans == "") or (ans == text.lower()):
            print('{name}: {text};'.format(name=update.effective_chat.first_name, text=text))
            nextLevel(bot, chat_id)
        else:
            bot.send_message(chat_id, "Пробуй еще")
            print('{name}: {text}; ans: пробуй еще'.format(name=update.effective_chat.first_name, text=text))


def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    next(update, context)


def main():
    updater = Updater('1317680111:AAHyis9cLcA1phN4ILjhfPI6vPY9Bnwd6mw')
    dp = updater.dispatcher
    mh = MessageHandler(Filters.all, reply)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('restart', restart))
    dp.add_handler(CommandHandler('next', next))
    dp.add_handler(mh)
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
