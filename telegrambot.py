import telebot
from dop import keys, TOKEN
from extensions import CryptoConverter, ApiException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help (message: telebot.types.Message):
    # text = "text"
    text = 'Чтобы начать работу введите комманду боту в следующем формате:\ <Валюта конвертирования> \
<В какую валюту конвертировать> \
<Количество конвертируемой валюты> \n Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values (message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
           raise ApiException('Слишком много параметров')


        quote, base, amount = values
        total_base = CryptoConverter.convert(quote.lower(), base.lower(), amount)
        text = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)
    except ApiException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')


bot.polling()
