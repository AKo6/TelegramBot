import telebot
from config import keys, TOKEN
from extensions import ConvertionException, BotConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = f"Приветствую {message.chat.username},\n"\
                     'Я умею конвертировать одну валюту в другую.\n'\
                     'Чтобы узнать как, напишите: /help\n'\
                     'Чтобы узнать какие валюты доступны напишите: /values.'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать укажите название любой из доступных валют и количество переводимой валюты.\n' \
           'Пример: Доллар Рубль 1 \n'\
    'Важно: Название валют должно начинаться с большой буквы.\n'\
           'Для просмотра доступных валют напишите:/values'

    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Неправильное количество параметров')

        quote, base, amount = values
        total_base = BotConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка {message.chat.username},\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)