import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

users = dict()

answers = ["", "1", "2", "1234"]
messages = [["Первый блок с задачей про овечку", "ответ 1"],
            ["Второй блок с еще какой-то задачей", "ответ 2"],
            ["еще один блок, поиграем в быки и коровы", "ответ 1234"],
            ["Последний блок"]]


def bop(update, context):
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    chat_id = update.message.chat.id
    context.bot.send_photo(chat_id=chat_id, photo=url)


def start(update: Update, context: CallbackContext):
    bot = context.bot
    chat_id = update.effective_chat.id

    if chat_id not in users:
        users[chat_id] = 0

    bot.send_message(chat_id, "Начнем?")


def restart(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    users[chat_id] = 0
    start(update, context)


#     bot.send_message(chat_id,
#                      "Принцесса Даниэла очень хотела порадовать своего принца. Она приготовила ему такой чудесный "
#                      "подарок, а в королевстве ни одной кареты до вечера. «Какой кошмар!» - Даниэла была в гневе. "
#                      "«Как это так, я Принцесса! Для мена всегда должны быть кареты». Она расплакалась, "
#                      "еще никогда ее планы не рушились так сильно.")
#     bot.send_message(chat_id,
#                      """Услышав рыдания принцессы, ее верный друг поросенок тут же прибежал к ней.
# -Что случилось, Даниээла? – впопыхах спросил поросенок.
# -В целом королевстве нет ни одной кареты, которая бы смогла отвезти этот чудесный подарок графу Ярославу.
# -Давай я отнесу, - гордо предложил поросенок.
# -А ты сможешь? Не устанешь? – спросила Даниэла. На ее лице уже появилась милая улыбка.
# -Раз предлагаю – смогу! Давай сюда подарок и адрес.
# Принцесса вручила поросенку коробку и бумажку с адресом.
# -Спасибо огромное! Будь осторожнее сказала она. - Даниэла обняла поросенка и он побежал.""")
#     bot.send_message(chat_id,
#                      "Добежав до королевского сада, поросенок увидел, что он потерял открытку. Он уж было хотел "
#                      "вернуться назад, чтобы ее искать, но к нему подлетела птичка, которая сказала, что открытку "
#                      "украла овечка-клептоманка и что она побежала вперед по другой прямой дороге. \n\nЗадачка: "
#                      "Овечка бежит по прямой дороге со скоростью 4 м/с. Поросенок н будет бежать за овечкой "
#                      "всегда, двигаясь по направлению к ней. Поросенок начнет бежать за овечкой прямо от "
#                      "королевского сада, который находится в 600 м от дороги, где бежит овечка. С какой скоростью "
#                      "нужно будет бежать за овечкой, чтобы добраться до нее за 100 секунд?")

def bullsAndCows(ans, guess):

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

    return "Быки: {}\nКоровы: {}".format(bull, cow)


def reply(update: Update, context: CallbackContext):
    bot = context.bot
    chat_id = update.effective_chat.id
    text = update.message.text

    step = users[chat_id]

    def nextLevel():
        for str in messages[step]:
            bot.send_message(chat_id, str)
        users[chat_id] += 1

    if step < len(answers):
        ans = answers[step]

        if step == 3:
            message = bullsAndCows(ans, text)
            if message == "":
                nextLevel()
            else:
                bot.send_message(chat_id, message)
        else:
            if (ans == "") or (ans == text):
                nextLevel()
            else:
                bot.send_message(chat_id, "Пробуй еще")
    else:
        bot.send_message(chat_id, "а всё уже :( кинь команду /restart чтобы начать заново")


def main():
    updater = Updater('1227978888:AAHkkmUt6YBjR8aE3n8XSsHKuBuDAIWxNQs')
    dp = updater.dispatcher
    mh = MessageHandler(Filters.all, reply)
    dp.add_handler(CommandHandler('bop', bop))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('restart', restart))
    dp.add_handler(mh)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
