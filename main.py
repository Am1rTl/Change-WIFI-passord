import telebot
import json
from telebot import types
from telebot.types import ReplyKeyboardRemove



boss = [1376233184]

with open("contacts", "r") as file:
    lines = file.read()

contacts = eval(lines)

with open("token", "r") as file:
    token = file.read()[:-1]

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    print(message)
    if message.from_user.id in boss:
            bot.send_message(message.chat.id, 'Привет')
    else:
        bot.send_message(message.chat.id, "Пожалуйста зарегестрируйтесь командой \n /register")
        print("asd")

@bot.message_handler(commands=['register'])
def phone(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить телефон", request_contact=True)
    keyboard.add(button_phone) #Добавляем эту кнопку
    bot.send_message(message.chat.id, 'Номер телефона', reply_markup=keyboard)

@bot.message_handler(content_types=['contact'])
def contact(message):

    if message.contact is not None:
        print(message.contact)
        print(message.contact.first_name, message.contact.last_name, message.contact.user_id)
        try:
            print(contacts[message.contact.phone_number])
        except:
            contacts[message.contact.phone_number] = {'first_name': message.contact.first_name, 'last_name': message.contact.last_name, 'user_id': message.contact.user_id, "date": message.json["date"]    }
        bot.send_message(message.chat.id, "Thanks you for your phone number \n /start", reply_markup=ReplyKeyboardRemove())

        with open("contacts", "w") as file:
            file.write(str(contacts))


bot.infinity_polling()
