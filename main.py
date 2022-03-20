from multiprocessing import BoundedSemaphore
import telebot
import time
import strings
import user
from telebot import types

bot = telebot.TeleBot("5274220415:AAG2RQpuD2x_AOSGFP7NbxRjEFhP5US1gtk")
users = {}
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    messagetoedit = bot.send_message(chat_id = message.chat.id, text="Загрузка 0%"+ '\n' + "▒"*(10))
    time.sleep(0.25)
    for i in range(1,11):
                bot.edit_message_text(chat_id=message.chat.id, message_id=messagetoedit.message_id, text="Загрузка " + str(i*10) +"%"+ '\n' + "█"*i + "▒"*(10-i))
                time.sleep(0.1)
    bot.edit_message_text(chat_id=message.chat.id, message_id=messagetoedit.message_id, text=strings.hello_message)
    bot.send_message(chat_id = message.chat.id, text=strings.first_message)

    users[message.chat.id] = user.user_model(message.chat.id)
    users[message.chat.id].status = 1
    print(users)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
      if(message.chat.id in users):
                print(users[message.chat.id].status)
                if(users[message.chat.id].status == 5):
                                        users[message.chat.id].setifCommand(message.text)
                                        users[message.chat.id].status = 10
                
                                        messagetoedit = bot.send_message(chat_id = message.chat.id, text="Обработка 0%"+ '\n' + "▒"*(10))
                                        time.sleep(0.25)
                                        for i in range(1,11):
                                                    bot.edit_message_text(chat_id=message.chat.id, message_id=messagetoedit.message_id, text="Обработка " + str(i*10) +"%"+ '\n' + "█"*i + "▒"*(10-i))
                                                    time.sleep(0.1)
                                        bot.edit_message_text(chat_id=message.chat.id, message_id=messagetoedit.message_id, text=strings.end_of_dialog)
                                        users[message.chat.id].sendToFile()
                                        return
                if(users[message.chat.id].status == 4):
                                    if(message.text == "да(манда)"):
                                        users[message.chat.id].setStatusCommand(True)
                                        users[message.chat.id].status = 5
                                        messagetoedit = bot.send_message(chat_id = message.chat.id, reply_markup = types.ReplyKeyboardRemove (selective = False), text="Обработка 0%"+ '\n' + "▒"*(10))
                                        bot.delete_message(message.chat.id, messagetoedit.message_id)
                                        messagetoedit = bot.send_message(chat_id = message.chat.id, text="Обработка 0%"+ '\n' + "▒"*(10))

                                        time.sleep(0.25)
                                        for i in range(1,11):
                                                    bot.edit_message_text(chat_id=message.chat.id, message_id=messagetoedit.message_id, text="Обработка " + str(i*10) +"%"+ '\n' + "█"*i + "▒"*(10-i))
                                                    time.sleep(0.1)
                                        bot.edit_message_text(chat_id=message.chat.id, message_id=messagetoedit.message_id, text=strings.name_command)
                                        return
                                    if(message.text == "нет(пидора ответ)"):
                                        users[message.chat.id].setStatusCommand(False)
                                        users[message.chat.id].status = 10

                                        #TODO here we can save info about user in file
                                        messagetoedit = bot.send_message(chat_id = message.chat.id, reply_markup = types.ReplyKeyboardRemove (selective = False), text="Обработка 0%"+ '\n' + "▒"*(10))
                                        bot.delete_message(message.chat.id, messagetoedit.message_id)
                                        messagetoedit = bot.send_message(chat_id = message.chat.id, text="Обработка 0%"+ '\n' + "▒"*(10))
                                        time.sleep(0.25)
                                        for i in range(1,11):
                                                    bot.edit_message_text(chat_id=message.chat.id, message_id=messagetoedit.message_id, text="Обработка " + str(i*10) +"%"+ '\n' + "█"*i + "▒"*(10-i))
                                                    time.sleep(0.1)
                                        bot.edit_message_text(chat_id=message.chat.id, message_id=messagetoedit.message_id, text=strings.end_of_dialog)
                                        users[message.chat.id].sendToFile()

                                        return

                if(users[message.chat.id].status == 3):
                                        users[message.chat.id].setGroup(message.text)
                                        users[message.chat.id].status = 4
                                        markup = types.ReplyKeyboardMarkup().row(types.KeyboardButton('да(манда)'), types.KeyboardButton('нет(пидора ответ)'))

                                        messagetoedit = bot.send_message(chat_id = message.chat.id, text="Обработка 0%"+ '\n' + "▒"*(10))
                                        time.sleep(0.25)
                                        for i in range(1,11):
                                                    bot.edit_message_text(chat_id=message.chat.id, message_id=messagetoedit.message_id, text="Обработка " + str(i*10) +"%"+ '\n' + "█"*i + "▒"*(10-i))
                                                    time.sleep(0.1)

                                        bot.delete_message(message.chat.id, messagetoedit.message_id)
                                        bot.send_message(chat_id = message.chat.id,reply_markup = markup, text=strings.to_get_team)
                                        
                                        return
                if(users[message.chat.id].status == 2):
                                        users[message.chat.id].setGroup(message.text)
                                        users[message.chat.id].status = 3
                
                                        messagetoedit = bot.send_message(chat_id = message.chat.id, text="Обработка 0%"+ '\n' + "▒"*(10))
                                        time.sleep(0.25)
                                        for i in range(1,11):
                                                    bot.edit_message_text(chat_id=message.chat.id, message_id=messagetoedit.message_id, text="Обработка " + str(i*10) +"%"+ '\n' + "█"*i + "▒"*(10-i))
                                                    time.sleep(0.1)
                                        bot.edit_message_text(chat_id=message.chat.id, message_id=messagetoedit.message_id, text=strings.third_message)
                                        return
                if(users[message.chat.id].status == 1):
                        users[message.chat.id].setName(message.text)
                        users[message.chat.id].status = 2
  
                        messagetoedit = bot.send_message(chat_id = message.chat.id, text="Обработка 0%"+ '\n' + "▒"*(10))
                        time.sleep(0.25)
                        for i in range(1,11):
                                    bot.edit_message_text(chat_id=message.chat.id, message_id=messagetoedit.message_id, text="Обработка " + str(i*10) +"%"+ '\n' + "█"*i + "▒"*(10-i))
                                    time.sleep(0.25)
                        bot.edit_message_text(chat_id=message.chat.id, message_id=messagetoedit.message_id, text=strings.second_message)
                        return

bot.infinity_polling()