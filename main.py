import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url


def bop(update, context):
    url = get_url()
    chat_id = update.message.chat.id
    context.bot.send_photo(chat_id=chat_id, photo=url)


def start(update: Update, context: CallbackContext):
    bot = context.bot
    chat_id = update.effective_chat.id

    bot.send_message(chat_id,
                     "Принцесса Даниэла очень хотела порадовать своего принца. Она приготовила ему такой чудесный "
                     "подарок, а в королевстве ни одной кареты до вечера. «Какой кошмар!» - Даниэла была в гневе. "
                     "«Как это так, я Принцесса! Для мена всегда должны быть кареты». Она расплакалась, "
                     "еще никогда ее планы не рушились так сильно.")
    bot.send_message(chat_id,
                     """Услышав рыдания принцессы, ее верный друг поросенок тут же прибежал к ней. 
-Что случилось, Даниээла? – впопыхах спросил поросенок. 
-В целом королевстве нет ни одной кареты, которая бы смогла отвезти этот чудесный подарок графу Ярославу. 
-Давай я отнесу, - гордо предложил поросенок.
-А ты сможешь? Не устанешь? – спросила Даниэла. На ее лице уже появилась милая улыбка.
-Раз предлагаю – смогу! Давай сюда подарок и адрес. 
Принцесса вручила поросенку коробку и бумажку с адресом. 
-Спасибо огромное! Будь осторожнее сказала она. - Даниэла обняла поросенка и он побежал.""")
    bot.send_message(chat_id,
                     "Добежав до королевского сада, поросенок увидел, что он потерял открытку. Он уж было хотел "
                     "вернуться назад, чтобы ее искать, но к нему подлетела птичка, которая сказала, что открытку "
                     "украла овечка-клептоманка и что она побежала вперед по другой прямой дороге. \n\nЗадачка: "
                     "Овечка бежит по прямой дороге со скоростью 4 м/с. Поросенок н будет бежать за овечкой "
                     "всегда, двигаясь по направлению к ней. Поросенок начнет бежать за овечкой прямо от "
                     "королевского сада, который находится в 600 м от дороги, где бежит овечка. С какой скоростью "
                     "нужно будет бежать за овечкой, чтобы добраться до нее за 100 секунд?")


def check(update: Update, context: CallbackContext):
    bot = context.bot
    text = update.message.text
    bot.send_message(update.effective_chat.id, text[::-1])


def main():
    updater = Updater('1227978888:AAHkkmUt6YBjR8aE3n8XSsHKuBuDAIWxNQs')
    dp = updater.dispatcher
    mh = MessageHandler(Filters.all, check)
    dp.add_handler(CommandHandler('bop', bop))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(mh)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
