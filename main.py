import os
import telebot
import time
from user import Users, User
from telebot import types
from bot_logging import logger

token = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    db = Users()
    user = User()
    user.chat_id = message.chat.id
    user.status = 1
    user.username = message.from_user.username
    if db.users.get(user.chat_id):
        logger.info(f"update exists user: {user.username} {user.chat_id}")
    else:
        logger.info(f"add new user: {user.username} {user.chat_id}")
    db.users[user.chat_id] = user
    db.save()

    loading_widget(message.chat.id, "Давай познакомимся.\nСкажи мне свои фамилию и имя.")


def loading_widget(chat_id, next_message):
    message_to_edit = bot.send_message(chat_id=chat_id,
                                       text=f"Обработка 0%\n{'▒' * 10}")
    time.sleep(0.25)
    for i in [1, 5, 9]:
        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_to_edit.message_id,
                              text=f"Обработка {i * 10}%\n{'█' * i}{'▒' * (10 - i)}")
        time.sleep(0.25)
    bot.edit_message_text(chat_id=chat_id,
                          message_id=message_to_edit.message_id,
                          text=next_message)


def get_users_card(chat_id):
    db = Users()
    users_info = db.users.get(chat_id)
    if users_info:
        if users_info.team:
            start = "Отлично!\n"
            end = f"\nТы из команды {users_info.team}."
        else:
            start = "Помни, что у тебя ещё есть время найти себе кого-то в команду или присоединиться к одной из уже существующих.\n"
            end = "\nНа данный момент у тебя нет команды."
        message = f"А теперь давай сверим твои данный ещё раз:\nТебя зовут {users_info.name}.\nТы учишься в группе {users_info.group}."
        return start + message + end


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    db = Users()

    chat_id = str(message.chat.id)
    text = message.text
    if chat_id in db.users:
        if db.users[chat_id].status == 1:
            db.users[chat_id].name = text
            db.users[chat_id].status += 1
            db.save()
            logger.info(f"{chat_id}:{db.users[chat_id].username} add name: {text}")
            bot.send_message(chat_id=message.chat.id, text='А меня зовут Поти. Ты ещё узнаешь обо мне немного позже '
                                                           '😉\nМне любопытно узнать: из какой ты группы?')


        elif db.users[chat_id].status == 2:
            db.users[chat_id].set_group(text)
            db.users[chat_id].status += 1
            db.save()
            logger.info(f"{chat_id}:{db.users[chat_id].username} add group: {text}")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True).row(types.KeyboardButton('Да'),
                                                                         types.KeyboardButton('Нет'))
            bot.send_message(chat_id=message.chat.id, reply_markup=markup, text="Есть ли у тебя команда?")

        elif db.users[chat_id].status == 3:
            if text.lower() == "да":
                db.users[chat_id].status += 1
                bot.send_message(chat_id=message.chat.id,
                                 text="А как называется?",
                                 reply_markup=types.ReplyKeyboardRemove(selective=False))
                db.save()
            elif text.lower() == "нет":
                db.users[chat_id].status = 5
                db.users[chat_id].team = ''
                db.save()
                logger.info(f"{chat_id}:{db.users[chat_id].username} save empty team")
                loading_widget(chat_id, get_users_card(chat_id))

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True).row(types.KeyboardButton('Да'),
                                                                             types.KeyboardButton('Нет'))
                bot.send_message(chat_id=message.chat.id, reply_markup=markup, text='Всё верно?')
            else:
                bot.send_message(chat_id=message.chat.id, text='Я понимаю только бинарные ответы "Да" или "Нет"')
        elif db.users[chat_id].status == 4:
            db.users[chat_id].team = text
            db.users[chat_id].status += 1
            db.save()
            logger.info(f"{chat_id}:{db.users[chat_id].username} add team: {text}")
            loading_widget(chat_id, get_users_card(chat_id))
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True).row(types.KeyboardButton('Да'),
                                                                         types.KeyboardButton('Нет'))
            bot.send_message(chat_id=message.chat.id, reply_markup=markup, text='Всё верно?')

        elif db.users[chat_id].status == 5:
            if text.lower() == "да":
                db.users[chat_id].status = 10
                text = "Хорошо, тогда я отправляю твою заявку организаторам соревнований." \
                       "А ты в этом время можешь присоединиться к нашему чату <>,"
                if not db.users[chat_id].team:
                    text += "где ты можешь найти себе команду или просто поболтать с другими участниками. Удачи!"
                else:
                    text += "где ты можешь поболтать с другими участниками. Удачи!"
                logger.info(f"{chat_id}:{db.users[chat_id].username} finish registration")
                bot.send_message(chat_id=message.chat.id,
                                 text=text,
                                 reply_markup=types.ReplyKeyboardRemove(selective=False))
                db.save()
            elif text.lower() == "нет":
                db.users[chat_id].status = 1
                logger.info(f"{chat_id}:{db.users[chat_id].username} restart registration")
                bot.send_message(chat_id=message.chat.id,
                                 text="Давай попробуем ещё раз.\n\nСкажи мне свою фамилию и имя.",
                                 reply_markup=types.ReplyKeyboardRemove(selective=False))
                db.save()
            else:
                logger.warning(f"{chat_id}:{db.users[chat_id].username} unsupported answer: {text}")
                bot.send_message(chat_id=message.chat.id, text='Я понимаю только бинарные ответы "Да" или "Нет"')
        else:
            logger.warning(f"{chat_id}:{db.users[chat_id].username} receive: {text}")


if __name__ == '__main__':
    logger.info("start bot")
    bot.infinity_polling()
