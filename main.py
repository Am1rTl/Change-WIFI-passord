import telebot
import json
from telebot import types
from telebot.types import ReplyKeyboardRemove



boss = [1376233184]

with open("contacts", "r") as file:
    lines = file.read()

contacts = eval(lines)
#contacts = {}

with open("token", "r") as file:
    token = file.read()[:-1]
print(contacts)
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    #print(message)
    has_person_in_contacts = False
    for i in list(contacts.keys()):
        if contacts[i]['user_id'] == message.chat.id:
            has_person_in_contacts = True

    if message.from_user.id in boss:
        bot.send_message(message.chat.id, 'Привет босс, чтобы открыть меню админитратора отправь \n /admin_menu \n А чтобы открыть обычное меню открой \n /menu')
    elif has_person_in_contacts == True:
        bot.send_message(message.chat.id, 'Привет, чтобы открыть меню нажми команду \n /menu')
    else:
        bot.send_message(message.chat.id, "Пожалуйста зарегестрируйтесь командой \n /register")
        #print("asd")

@bot.message_handler(commands=['register'])
def phone(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить телефон", request_contact=True)
    keyboard.add(button_phone) #Добавляем эту кнопку
    bot.send_message(message.chat.id, 'Для регистрации нажмите на кнопку в меню ', reply_markup=keyboard)

@bot.message_handler(content_types=['contact'])
def contact(message):

    if message.contact is not None:
        print(message.contact)
        print(message.contact.first_name, message.contact.last_name, message.contact.user_id)
        try:
            print(contacts[message.contact.phone_number])
        except:
            print({'first_name': message.contact.first_name, 'last_name': message.contact.last_name, 'user_id': message.contact.user_id, "date": message.json["date"]    })
            contacts[message.contact.phone_number] = {'first_name': message.contact.first_name, 'last_name': message.contact.last_name, 'user_id': message.contact.user_id, "date": message.json["date"]    }
        bot.send_message(message.chat.id, "Thanks you for your phone number \n /start", reply_markup=ReplyKeyboardRemove())

        with open("contacts", "w") as file:
            file.write(str(contacts))

@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, str(contacts))


@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Активный пароль")
    btn2 = types.KeyboardButton("Выйти из профиля")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Меню появилось", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Активный пароль"):
        #
        ##
        ###
        ####
        #####
        ######
        #######
        ########            ВЫСЫЛАЕМ АКТИВНЫЙ ПАРОЛЬ
        password = 'active_password'
        bot.send_message(message.chat.id, text=f"`active_password`", parse_mode='MarkdownV2')
    elif message.text == "Выйти из профиля":
        contacts_number = False
        for i in list(contacts.keys()):
            if contacts[i]['user_id'] == message.chat.id:
                contacts_number = i
        try:
            contacts.pop(contacts_number)
        except:
            print("Something went wrong")
        bot.send_message(message.chat.id, "Вы успешно вышли", reply_markup=ReplyKeyboardRemove())
        bot.send_message(message.chat.id, "Для дальнейших действий оправьте /start")
        with open("contacts", "w") as file:
            file.write(str(contacts))




bot.infinity_polling()
