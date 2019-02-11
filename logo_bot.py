import telebot
from tg_api import bot_key
from telebot import types

token = bot_key()
bot = telebot.TeleBot(token)


one_age = ['гласные звуки: [а] [е] [о]', 'а также согласные твердые звуки: [б] [г] [к] [м]']
one_age_fin = ', '.join(one_age)

two_age = ['гласные звуки: [а] [е] [и] [о]',
           'согласные твердые звуки: [б] [г] [д] [к] [м] [н] [п] [т]',
           'а также согласные мягкие звуки: [б] [г] [д] [к] [м] [н] [т]']
two_age_fin = ', '.join(two_age)

three_age = ['гласные звуки: [а] [е] [и] [о] [ы] [э]',
             'согласные твердые звуки: [б] [в] [г] [д] [к] [м] [н] [п] [т] [ф] [х]',
             'а также согласные мягкие звуки: [б] [в] [г] [д] [з] [к] [м] [н] [п] [c] [т] [ф] [х]']
three_age_fin = ','.join(three_age)

four_age = ['гласные звуки: [а] [е] [и] [о] [у] [ы] [э]',
            'согласные твердые звуки: [б] [в] [г] [д] [ж] [з] [к] [м] [н] [п] [c] [т] [ф] [х] [ч] [ш] [щ]',
            'а также согласные мягкие звуки: [б] [в] [г] [д] [з] [к] [м] [н] [п] [c] [т] [ф] [х]']
four_age_fin = ', '.join(four_age)

five_age = ['гласные звуки: [а] [е] [и] [о] [у] [ы] [э]',
            'согласные твердые звуки: [б] [в] [г] [д] [ж] [з] [к] [л] [м] [н] [п] [р] [c] [т] [ф] [х] [ч] [ш] [щ]',
            'а также согласные мягкие звуки: [б] [в] [г] [д] [з] [к] [л] [м] [н] [п] [р] [c] [т] [ф] [х]']
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


if __name__ == '__main__':
    bot.polling(none_stop=True)
