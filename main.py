import telebot
import json
from telebot import types
from telebot.types import ReplyKeyboardRemove



boss = [1376233184]
trusted_chats = []
queue = []

with open("contacts", "r") as file:
    lines = file.read()

contacts = eval(lines)

with open("trust", "r") as file:
    lines = file.read()

trusted_chats = eval(lines)
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
        #print(message.contact)
        #print(message.contact.first_name, message.contact.last_name, message.contact.user_id)
        try:
            print(contacts[message.contact.phone_number])
        except:
            print({'first_name': message.contact.first_name, 'last_name': message.contact.last_name, 'user_id': message.contact.user_id, "date": message.json["date"]    })
            contacts[message.contact.phone_number] = {'first_name': message.contact.first_name, 'last_name': message.contact.last_name, 'user_id': message.contact.user_id, "date": message.json["date"]    }

        queue.append(message.chat.id)


        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Да', callback_data=str(message.chat.id))
        button2 = types.InlineKeyboardButton('Нет', callback_data=str(message.chat.id)+'a')
        markup.add(button1)
        markup.add(button2)
        if message.from_user.last_name != None:
            bot.send_message(boss[0], text=f"Регестрация нового пользователя c: \nИменем: `{message.from_user.first_name} {message.from_user.last_name}`\nНиком: `{message.from_user.username}` \nТелефоном: `{message.contact.phone_number}` ", parse_mode='MarkdownV2', reply_markup=markup)
        else:
            bot.send_message(boss[0], text=f"Регестрация нового пользователя c: \nИменем: `{message.from_user.first_name}`\nНиком: `{message.from_user.username}` \nТелефоном: `{message.contact.phone_number}` ", parse_mode='MarkdownV2', reply_markup=markup)


        with open("contacts", "w") as file:
            file.write(str(contacts))

        bot.send_message(message.chat.id, "Thanks you for your phone number \n /start", reply_markup=ReplyKeyboardRemove())

@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, str(contacts))


@bot.message_handler(commands=['menu'])
def menu(message):
    if message.chat.id in trusted_chats:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Активный пароль")
        btn2 = types.KeyboardButton("Выйти из профиля")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text="Меню появилось", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="Пожалуйста зарегестрируйтесь\n/register")

@bot.message_handler(commands=['asd'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Да', callback_data='yes')
    button2 = types.InlineKeyboardButton('Нет', callback_data='no')
    markup.add(button1)
    markup.add(button2)
    bot.send_message(message.chat.id, 'Привет! Нажми кнопку:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        bot.send_message(int(call.data), 'Ваша заявка на регестрацию одобрена')
        bot.send_message(boss[0], 'Заявка на регестрацию одобрена')
        trusted_chats.append(int(call.data))
    except:
        try:
            trusted_chats.pop(trusted_chats.index(int(call.data[:-1])))
        except:
            pass
        bot.send_message(int(call.data[:-1]), 'Ваша заявка на регестрацию отклонена')
        bot.send_message(boss[0], 'Заявка на регестрацию отклонена')

    print(trusted_chats)

    with open("trust", "w") as file:
            file.write(str(trusted_chats))



@bot.message_handler(content_types=['text'])
def func(message):
    if message.chat.id in trusted_chats:
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
    else:
        bot.send_message(message.chat.id, text="Пожалуйста зарегестрируйтесь\n/register")




bot.infinity_polling()
