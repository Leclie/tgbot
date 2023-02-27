import telebot
import json

bot = telebot.TeleBot('6106444108:AAEZNl3t9Qn_lKiYcBvzwL4msrUM4FDv168')


name = ''
phone_number = ''


@bot.message_handler(content_types=['text'])
def start(message):
    bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь? (/info, добавить, удалить, редактировать)")

    if message.text.lower() == '/info':
        print_all()
    elif message.text.lower() == 'добавить':
        add(message)
    elif message.text.lower() == 'удалить':
        delete(message)
    elif message.text.lower() == 'редактировать':
        update(message)


# Вывод
def print_all():
    with open('phonebook.txt') as json_file:
        data = json.load(json_file)
        for p in data['people']:
            print('Name: ' + p['name'])
            print('Phone_number: ' + p['phone_number'])
            print('')


# Добавление
def add(message):
    bot.send_message(message.from_user.id, "Введите имя")
    bot.register_next_step_handler(message, add_name)

def add_name(message): #получаем имя
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Введите номер')
    bot.register_next_step_handler(message, add_number)

def add_number(message):
    global phone_number
    phone_number = message.text
    add_to_json()

def add_to_json():
    with open('phonebook.txt') as json_file:
        data = json.load(json_file)
        data['people'].append({
            'name': name,
            'phone_number': phone_number
        })
    with open('phonebook.txt', 'w') as outfile:
        json.dump(data, outfile)


# Удаление
def delete(message):
    bot.send_message(message.from_user.id, "Введите имя")
    bot.register_next_step_handler(message, del_name_from_json)

def del_name_from_json(message): #получаем имя, которое хотим удалить
    global name
    name = message.text
    with open('phonebook.txt') as json_file:
        data = json.load(json_file)
        for i in range(len(data['people'])):
            if data['people'][i]['name'] == name:
                del data['people'][i]
                break
    with open('phonebook.txt', 'w') as outfile:
        json.dump(data, outfile)






# Редактирование
def update(message):
    bot.send_message(message.from_user.id, "Введите имя")
    bot.register_next_step_handler(message, update_name)

def update_name(message): #получаем имя
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Введите номер')
    bot.register_next_step_handler(message, update_number)

def update_number(message):
    global phone_number
    phone_number = message.text
    update_to_json()


def update_to_json():
    with open('phonebook.txt') as json_file:
        data = json.load(json_file)
        for i in range(len(data['people'])):
            if data['people'][i]['name'] == name:
                data['people'][i]['phone_number'] = phone_number
                break
    with open('phonebook.txt', 'w') as outfile:
        json.dump(data, outfile)



# Бот ожидает сообщений
bot.polling(none_stop=True, interval=0)