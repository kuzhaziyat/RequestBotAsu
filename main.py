import telebot
from telebot import types
import numpy as np
from datetime import datetime
import config
import DBmanager
import handler
bot = telebot.TeleBot(config.Token)
adminChat = config.chatId
korpus = [
    ['Главный корпус','Терапевтический корпус']
]
otdelGK = [
    ['ПП №1',
    'РДО'],
    ['ОФД',
    'ФТО'],
    ['ОРИТ №1',
    'Эндоскопия'],
    ['КЛД',
    'Урология'],
    ['ХО №1',
    'ХО №2'],
    ['ДХО',
    'ЧЛХ'],
    ['НХО',
    'НО №1'],
    ['КО №1',
    'Травматалогия'],
    ['КХО',
    'Ожоговое'],
    ['РХМДЛ',
    ''],
]
otdelTK = [
    ['Реабилитация',
    'НО №2'],
    ['ОРИТ №2',
    'КО №2'],
    ['ОКИ',
    'Токсикология'],
    ['Пульмонология',
    'Гастроэнторология'],
]

status = ['На формировании',
          'В ожидании',
          'Принят в обработку',
          'Выполнен']



@bot.message_handler(content_types=['text','photo','video','document'])
def get_text_messages(message):
    dt = message.date
    date = datetime.fromtimestamp(dt)
    if message.chat.id != config.chatId:
        if message.text == '/start':
            if DBmanager.select_users_id(message.from_user.id) == 0:
                msg = handler.start(message)
                bot.register_next_step_handler(msg, contact)
            else:
                msg = handler.choose_korpus(message,korpus)
                bot.register_next_step_handler(msg, check_korpus)
        else:
            bot.send_message(message.chat.id,'Начните заполнять заявку с команды /start')
    else:
        handler.admin_(message, date, adminChat, status)
        handler.admin(message,date)
def send_button_start(message):
    handler.send_button_start(message)

def contact(message):
    print('Регистрация')
    handler.processing_contact(message)
    send_button_start(message)

def check_korpus(message):
    isKorpus = False
    for i in korpus:
        for k in i:
            if message.text == k:
                choose_otdel(message,message.text)
                DBmanager.insert_record_requests(message.from_user.id, message.text,status[0])
                isKorpus = True
        if(isKorpus):
            break
    else:
        handler.undo(message,status)

def choose_otdel(message,korpus):
    if korpus == 'Главный корпус':
        msg = handler.choose_otdel(message, otdelGK)
        bot.register_next_step_handler(msg, check_otdel)
    else:
        msg = handler.choose_otdel(message, otdelTK)
        bot.register_next_step_handler(msg, check_otdel)

def check_otdel(message):
    isOtdel = False
    otdel = np.concatenate ((otdelTK, otdelGK), axis= 0 )

    for i in otdel:
        for k in i:
            if message.text == k:
                get_file(message)
                DBmanager.update_otdel(message.text, message.from_user.id,status)
                isOtdel = True
        if isOtdel:
            break
    else:
        handler.undo(message,status)

def get_file(message):
    msg = handler.get_file(message)
    bot.register_next_step_handler(msg, check_file)

def check_file(message):
    if message.content_type == 'photo':
        photo_id = message.photo[-1].file_id
        DBmanager.update_photo(photo_id, message.from_user.id, status)
        get_requests(message)
    elif message.content_type == 'video':
        video_id = message.video.file_id
        DBmanager.update_video(video_id, message.from_user.id, status)
        get_requests(message)
    elif message.content_type == 'document':
        document_id = message.document.file_id
        DBmanager.update_document(document_id, message.from_user.id, status)
        get_requests(message)
    elif message.text == 'Пропустить':
        get_requests(message)
    else:
        handler.undo(message,status)

def get_requests(message):
    msg = bot.send_message(message.chat.id,'Напишите вашу проблему текстом',reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, create_request)

def create_request(message):
    handler.create_request(message,status)

bot.infinity_polling(timeout=10, long_polling_timeout = 5)
bot.polling(none_stop=True, interval=1)
