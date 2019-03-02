import telebot
from tg_api import bot_key
from telebot import types
import os
from flask import Flask, request


token = bot_key()
bot = telebot.TeleBot(token)


one_age = ['гласные звуки: [а] [у] [о]', 'а также согласные твердые звуки: [м] [б] [к] [г]']
one_age_fin = ', '.join(one_age)

two_age = ['гласные звуки: [а] [у] [о] [и]',
           'согласные твердые звуки:  [к] [г] [м] [п] [б] [т] [д] [н]',
           'а также согласные мягкие звуки: [к] [г] [м] [п] [б] [т] [д] [н]']
two_age_fin = ', '.join(two_age)

three_age = ['гласные звуки: [а] [у] [и] [о] [ы] [э]',
             'согласные твердые звуки: [к] [г] [м] [п] [б] [т] [д] [н] [в] [ф] [х]',
             'а также согласные мягкие звуки: [к] [г] [м] [п] [б] [т] [д] [н] [в] [ф] [х] [з] [c] [й]']
three_age_fin = ','.join(three_age)

four_age = ['гласные звуки: [а] [у] [и] [о] [ы] [э]',
            'согласные твердые звуки: [к] [г] [м] [п] [б] [т] [д] [н] [в] [ф] [х] [с] [з] [ц] [ш] [ж]',
            'а также согласные мягкие звуки: [к] [г] [м] [п] [б] [т] [д] [н] [в] [ф] [х] [з] [c] [й] [ч] [щ]']
four_age_fin = ', '.join(four_age)

five_age = ['гласные звуки: [а] [у] [и] [о] [ы] [э]',
            'согласные твердые звуки: [к] [г] [м] [п] [б] [т] [д] [н] [в] [ф] [х] [с] [з] [ц] [ш] [ж] [р] [л]',
            'а также согласные мягкие звуки: [к] [г] [м] [п] [б] [т] [д] [н] [в] [ф] [х] [з] [c] [й] [ч] [щ] [р] [л]']
five_age_fin = ', '.join(five_age)


age = ['1', '2', '3', '4', '5', '6+']

new_age = [str(i).zfill(1) for i in range(6, 99)]


def create_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    buttons = [types.InlineKeyboardButton(text=c, callback_data=c) for c in age]
    keyboard.add(*buttons)
    return keyboard


@bot.callback_query_handler(func=lambda x: True)
def callback_handler(callback_query):
    message = callback_query.message
    text = callback_query.data
    age, value = check_age_value(text)
    if age:
        bot.send_message(chat_id=message.chat.id, text='В данном возрасте ваш ребенок должен правильно произносить'
                                                       ' {}'.format(value))


def check_age(message):
    for c in age:
        if c in message.text.lower():
            return True
    return False


def check_age_value(text):
    age_values = {'1': one_age_fin, '2': two_age_fin, '3': three_age_fin, '4': four_age_fin, '5': five_age_fin,
                  '6+': ' и дифференцировать в речи все звуки родного языка'}
    for age, value in age_values.items():
        if age in text.lower():
            return age, value
    return None, None


@bot.message_handler(func=check_age)
def handle_age(message):
    age, value = check_age_value(message.text)
    if age:
        bot.send_message(chat_id=message.chat.id, text='В данном возрасте ваш ребенок должен правильно произносить'
                                                       ' {}'.format(value))
    else:
        bot.send_message(chat_id=message.chat.id, text='Укажите возвраст вашего ребенка')


@bot.message_handler(commands=['start', 'help'])
def handle_message(message):
    keyboard = create_keyboard()
    bot.send_message(chat_id=message.chat.id, text='Сколько полных лет вашему ребенку?',  reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in new_age)
def handle_message(message):
    bot.send_message(chat_id=message.chat.id, text='В данном возрасте ваш ребенок должен правильно произносить и'
                                                   '  дифференцировать в речи все звуки родного языка')


@bot.message_handler()
def handle_message(message):
    bot.send_message(chat_id=message.chat.id, text='Сколько полных лет вашему ребенку?')


server = Flask(__name__)


@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://ratesbot.herokuapp.com/bot")
    return "?", 200


server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
