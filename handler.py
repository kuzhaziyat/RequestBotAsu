import telebot
from telebot import types
import config
import DBmanager
import json
from datetime import datetime

bot = telebot.TeleBot(config.Token)

def start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить свой контакт", request_contact=True)
    keyboard.add(button_phone)
    return bot.send_message(message.chat.id,
                    "Вы не зарегистрированны,\n"
                    "отправтье нам свой контакт",
                    reply_markup=keyboard)

def send_button_start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button_start = types.KeyboardButton(text="/start")
    keyboard.add(button_start)
    bot.send_message(message.chat.id,
                            "Чтобы начать заявку нажмите на /start",
                            reply_markup=keyboard)

def choose_korpus(message,korpus):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    for i in range(len(korpus)):
        keyboard.row(korpus[i][0], korpus[i][1])
    return bot.send_message(message.chat.id, "Пожалуйста, выберите корпус",
                            reply_markup=keyboard)
def choose_otdel(message,otdel):

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    for i in range(len(otdel)):
        keyboard.row(otdel[i][0], otdel[i][1])
    return bot.send_message(message.chat.id, "Пожалуйста, выберите отдел",
                     reply_markup=keyboard)

def get_file(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('Пропустить')
    return bot.send_message(message.chat.id, "Отправьте видео или фото (пока принимаем или 1 фото ,или 1 видео)",
                            reply_markup=keyboard)
def create_request(message,status):
    dt = message.date
    date = datetime.fromtimestamp(dt)
    DBmanager.update_request(message.text,message.from_user.id, status[0])
    bot.send_message(message.chat.id, "Мы получили вашу заявку №" + DBmanager.select_id_requests(message.from_user.id,status[0]) + "\n\n" + str(date))
    DBmanager.update_status(status[1], DBmanager.select_id_requests(message.from_user.id,status[0]))
    bot.send_message(config.chatId, DBmanager.select_text_requests(message.from_user.id,status[1]) + '\n\n' + str(date),parse_mode='Markdown')
    if DBmanager.select_document_request(DBmanager.select_id_requests(message.from_user.id,status[1]))!=0:
        bot.send_message(config.chatId,(f'http://api.telegram.org/file/bot{config.Token}/{bot.get_file(DBmanager.select_document_request(DBmanager.select_id_requests(message.from_user.id,status[1]))).file_path}'))
    else:
        pass
def undo(message,status):
    bot.send_message(message.chat.id,
                     "Вы ввели неверные данные, ваша заявка отменена, Для создания нового обращения, пожалуйста, введите команду /start")
    DBmanager.undo_request(message.chat.id, status[0])
    print('неправильно ввели')

def admin_(message,date,admin_chat_id,status):
    try:
        items = json.dumps(message.json)
        messageid = str(json.loads(items)['reply_to_message']['message_id'])
        reply = str(json.loads(items)['text'])
        admin = str(json.loads(items)['from']['first_name'])
        text = str(json.loads(items)['reply_to_message']['text'])
        id = text[text.find('№') + 1:]
        id = id[:id.find('\n')]
        if 'Приня' in message.text or 'приня' in message.text:
            bot.send_message(DBmanager.select_id_request_userid(id),
                             "Статус вашей заявки №" + id + " "+ status[2] +"\n\n" + str(date))
            DBmanager.update_status(status[2], id)
            bot.edit_message_text(text + '\n\n' + 'Принят ' + str(date) + '\n' + admin, admin_chat_id, messageid)
        elif 'Выполн' in message.text or 'выполн' in message.text:
            bot.send_message(DBmanager.select_id_request_userid(id),
                             "Статус вашей заявки №" + id + " "+ status[3] +"\n\n" + str(date))
            DBmanager.update_status(status[3], id)
            bot.edit_message_text(text + '\n\n' + 'Выполнен ' + str(date) + '\n' + admin, admin_chat_id, messageid)
        else:
            bot.send_message(DBmanager.select_id_request_userid(id),
                             'Ответ по заявке №' + id + '\n\n' + reply + '\n\n' + str(date))
    except:
        pass

def processing_contact(message):
    if message.contact is not None: #Если присланный объект <strong>contact</strong> не равен нулю
        if DBmanager.select_users_id(message.contact.user_id) == 0:
            DBmanager.insert_record_users(
                str(message.contact.user_id),
                str(message.contact.first_name),
                str(message.contact.last_name),
                str(message.contact.phone_number)
            )
            bot.send_message(message.chat.id, "Вы успешно зарегистрировались")

def admin(message,date):
    try:
        if '/helpadmin' in message.text:
            bot.send_message(config.chatId,'Найди (написать id человека) - даст ссылку на пользователя\n'
                                           'Зарегестрировано - выводит число зарегестрированных пользователей\n'
                                           'Время - выводит настоящее время\n'
                                           'Заявок - выводит количество заявок\n'
                                           'Пользователи - выводит список всех зарегестрированных')
        if 'айди ' in message.text:
            user = '[Пользователь](tg://user?id=' + str(''.join(ele for ele in message.text if ele.isdigit())) + ')'
            bot.send_message(config.chatId, user, parse_mode='MarkdownV2')
        if 'арегистрировано' in message.text:
            bot.send_message(config.chatId,str(DBmanager.select_users()) + ' пользователя')
        if 'има' in message.text:
            bot.send_message(config.chatId,'Заебал')
        if 'зият' in message.text:
            bot.send_message(config.chatId,'Молодец!')
        if 'ремя' in message.text:
            bot.send_message(config.chatId, str(date))
        if 'аявок' in message.text:
            bot.send_message(config.chatId, str(DBmanager.select_requests()) + ' заявок')
        if 'ользователи' in message.text:
            bot.send_message(config.chatId,'не доделанно')
    except:
        pass


