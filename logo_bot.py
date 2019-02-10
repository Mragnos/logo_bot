import telebot
from tg_api import bot_key


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

five_age = four_age + ['р', 'р мягкий', 'л', 'л мягкий', 'правильно произносить и дифференцировать в речи все звуки'
                                                         'родного языка']
five_age_fin = ', '.join(five_age)
#six_plus = 'вау'

age = ['1', '2', '3', '4', '5']


def check_age(message):
    for c in age:
        if c in message.text.lower():
            return True
    return False


def check_age_value(text):
    age_values = {'1': one_age_fin, '2': two_age_fin, '3': three_age_fin, '4': four_age_fin, '5': five_age_fin}
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


@bot.message_handler()
def handle_message(message):
    bot.send_message(chat_id=message.chat.id, text='Сколько полных лет вашему ребенку?')


if __name__ == '__main__':
    bot.polling(none_stop=True)
