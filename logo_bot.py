import telebot
from tg_api import bot_key
from telebot import types

token = bot_key()
bot = telebot.TeleBot(token)


one_age = ['а', 'е', 'о', 'м', 'б', 'к', 'г']
one_age_fin = ', '.join(one_age)

two_age = ['а', 'е', 'о', 'и', 'м', 'м мягкий', 'б', 'б мягкий', 'к', 'к мягкий', 'г', 'г мягкий', 'п', 'т',
           'т мягкий', 'д', 'д мягкий', 'н', 'н мягкий']
two_age_fin = ', '.join(two_age)

three_age = two_age + ['в', 'в мягкий', 'ф', 'ф мягкий', 'ы', 'э', 'х', 'х мягкий', 'с мягкий', 'з мягкий']
three_age_fin = ', '.join(three_age)

four_age = three_age + ['c', 'з', 'у', 'ш', 'ж', 'ч', 'щ']
four_age_fin = ', '.join(four_age)

five_age = four_age + ['р', 'р мягкий', 'л', 'л мягкий', 'правильно произносить и дифференцировать в речи все звуки']
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
        bot.send_message(chat_id=message.chat.id, text='В данном возрасте ваш ребенок должен  говорить следующие звуки:'
                                                       ' {}'.format(value))


def check_age(message):
    for c in age:
        if c in message.text.lower():
            return True
    return False


def check_age_value(text):
    age_values = {'1': one_age_fin, '2': two_age_fin, '3': three_age_fin,'4': four_age_fin, '5': five_age_fin
                  }
    for age, value in age_values.items():
        if age in text.lower():
            return age, value
    return None, None


@bot.message_handler(func=check_age)
def handle_age(message):
    age, value = check_age_value(message.text)
    if age:
        bot.send_message(chat_id=message.chat.id, text='В данном возрасте ваш ребенок должен  говорить следующие звуки:'
                                                       ' {}'.format(value))
    else:
        bot.send_message(chat_id=message.chat.id, text='Укажите возвраст вашего ребенка')


@bot.message_handler(commands=['start', 'help'])
def handle_message(message):
    keyboard = create_keyboard()
    bot.send_message(chat_id=message.chat.id, text='Сколько полных лет вашему ребенку?',  reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in new_age)
def handle_message(message):
    bot.send_message(chat_id=message.chat.id, text='В данном возрасте ваш ребенок должен правильно произносить и дифференцировать в речи все звуки')


if __name__ == '__main__':
    bot.polling(none_stop=True)
