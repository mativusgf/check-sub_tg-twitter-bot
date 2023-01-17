import telebot
from telebot import types
import tweepy
import config

bot = telebot.TeleBot("5903865521:AAEJgx6RIYItxfetJm-2eUyOSIZ0gvznlmU")


class User:
    def __init__(self, username):
        self.telegram_username = username
        self.twitter_username = None
        self.telegram_subscription = False
        self.twitter_subscription = False


user_dict = {}


@bot.message_handler(commands=["start"])
def start(message):
    telegram_channel_link = "https://t.me/checktingest"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    telegram_button = types.KeyboardButton(text="Подписался на Telegram канал")
    markup.add(telegram_button)

    chat_id = message.chat.id
    user = message.chat.first_name
    bot.send_message(chat_id, f"Привет, {user}! Чтобы пользоваться ботом тебе нужно подписаться на:\n"
                              f"1) Telegram канал\n"
                              f"2) Twitter аккаунт\n")
    msg = bot.send_message(chat_id, f"Сначала подпишись на Telegram канал\n"
                                    f"{telegram_channel_link}", reply_markup=markup)

    bot.register_next_step_handler(msg, check_telegram)


@bot.message_handler(content_types=["text"])
def check_telegram(message):
    chat_id = message.chat.id

    status = ['creator', 'administrator', 'member']

    twitter_channel_link = "https://twitter.com/merouseer"

    try:
        username = message.chat.username
        person = User(username)
        user_dict[chat_id] = person
        for stat in status:
            if stat == bot.get_chat_member(chat_id, user_id=message.from_user.id).status:
                person.telegram_subscription = True
                bot.send_message(message.chat.id, f"Вы подписаны на наш Telegram канал!")
                bot.send_message(chat_id, f"А теперь подпишитесь на нас в Twitter!\n"
                                          f"{twitter_channel_link}")
                msg = bot.send_message(chat_id, f"Введите ваш никнейм в Twitter без знака @")
                bot.register_next_step_handler(msg, check_twitter)
    except Exception as e:
        bot.send_message(chat_id, f"Что-то пошло не так!")


@bot.message_handler(content_types=["text"])
def check_twitter(message):
    chat_id = message.chat.id
    client = tweepy.Client(bearer_token=config.BEARER_TOKEN)
    twitter_users = client.get_users_followers(id=config.USER_ID)
    try:
        username_twitter = message.text
        person = user_dict[chat_id]
        person.twitter_username = username_twitter
        for user in twitter_users.data:
            if username_twitter == user.username:
                person.twitter_subscription = True
                break
            else:
                person.twitter_subscription = False
        if person.twitter_subscription:
            bot.send_message(message.chat.id, f"Вы подписаны на наш Twitter!")
            bot.send_message(message.chat.id, f"Верификация прошла успешно!")
        else:
            # bot.send_message(message.chat.id, f"Вы не подписаны на наш Twitter аккаунт!")
            raise Exception("Вы не подписаны на наш Twitter аккаунт!")
    except Exception as e:
        bot.send_message(chat_id, f"Что-то пошло не так!")

    # bot.send_message(chat_id, f"А теперь подпишитесь на нас в Twitter!\n"
    #                           f"{twitter_link}")
    # bot.send_message(chat_id, f"Введите ваш никнейм в Twitter без знака @")

    # for user in twitter_users.data:
    #     if message.text in user.username:
    #         twitter_subscription = True
    #         break
    #     else:
    #         twitter_subscription = False


bot.polling(none_stop=True)
