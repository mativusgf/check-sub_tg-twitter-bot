import telebot
from telebot import types

bot = telebot.TeleBot("5903865521:AAEJgx6RIYItxfetJm-2eUyOSIZ0gvznlmU")

@bot.message_handler(commands=["start"])
def start(message):
    channel_link = "https://t.me/checktingest"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard = types.KeyboardButton(text="Подтвердить")
    markup.add(keyboard)
    chat_id = message.chat.id
    user = message.chat.first_name
    bot.send_message(chat_id, f"Привет {user} чтобы пользоваться ботом подпишись на канал\n"
                     f"{channel_link}", reply_markup=markup)

@bot.message_handler(content_types=["text"])
def text(message):
    user = message.chat.first_name
    if message.chat.type == 'private':
        if message.text == 'Подтвердить':
            status = ['creator', 'administrator', 'member']
            for stat in status:
                if stat == bot.get_chat_member(chat_id="@checktingest", user_id=message.from_user.id).status:
                    bot.send_message(message.chat.id, f"Доступ открыт {user}")
                    break

            else:
                bot.send_message(message.chat.id, f"{user} Не пытайтесь нас на*бать :)")

bot.polling(none_stop=True)