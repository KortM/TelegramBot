import logging
import telebot
from telebot import types
from vedis_config import register_next_step, get_last_step
from Main import Worker

bot = telebot.TeleBot('1405995555:AAF-3x1I3aVTbpPjWK92TFaV8JdTE9rZNFQ')
worker = Worker()

@bot.message_handler(commands = ['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    main_menu = types.KeyboardButton('Main menu')
    keyboard.add(main_menu)
    bot.send_message(message.chat.id, "HI, i'm network bot", reply_markup=keyboard)
    register_next_step(message.chat.id, 'start')

def build_menu(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    ip_whois = types.KeyboardButton('\U0001F310 IP whois')
    mac_info = types.KeyboardButton('\U00002699 MAC info')
    phone = types.KeyboardButton('\U0001F4DE Telephony')
    ip_calc = types.KeyboardButton('\U00002795 Calculate IP')
    back_btn = types.KeyboardButton('\U000021A9 Back')
    next_btn = types.KeyboardButton('\U000021AA Next')
    keyboard.add(ip_whois, ip_calc)
    keyboard.add(phone, mac_info)
    keyboard.add(back_btn, next_btn)
    bot.send_message(message.chat.id, 'Main menu', reply_markup=keyboard)
    message = bot.send_message(message.chat.id, "Select the appropriate one")

@bot.message_handler(func = lambda call: True)
def menu_handler(message):
    if message:
        if message.text == '\U0001F310 IP whois':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.KeyboardButton('\U000021A9 Back'))
            bot.send_message(message.chat.id, "Enter the ip address:", reply_markup=keyboard)
            bot.register_next_step_handler(message, get_ip_info)
            register_next_step(message.chat.id, '\U0001F310 IP whois')
        if message.text == '\U00002795 Calculate IP':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.KeyboardButton('\U000021A9 Back'), types.KeyboardButton('192.168.1.1/24'))
            bot.send_message(message.chat.id, 'Enter the Ip address and prefix:', reply_markup=keyboard)
            bot.register_next_step_handler(message, get_count_host)

        if message.text == 'Main menu':
            register_next_step(message.chat.id, 'Main menu')
            build_menu(message)         
        if message.text == '\U000021A9 Back':
            if get_last_step(message.chat.id) == 'Main menu':
                start(message)
            if get_last_step(message.chat.id) == '\U0001F310 IP whois':
                bot.register_next_step_handler(message, build_menu)
                register_next_step(message.chat.id,'Main menu')
        
def get_ip_info(request):
    if request.text == '\U000021A9 Back':
        build_menu(request)
        register_next_step(request.chat.id, 'Main menu')
        return
    if request.text:
        res = worker.search_ip_addr(request.text)
        bot.send_message(request.chat.id, res)
        message = bot.send_message(request.chat.id, "Enter the ip address:")
        bot.register_next_step_handler(message, get_ip_info)

def get_count_host(request):
    if request.text == '\U000021A9 Back':
        build_menu(request)
        register_next_step(request.chat.id, 'Main menu')
        return
    if request.text:
        request = bot.send_message(request.chat.id, worker.claculate_ip(request.text))
        bot.register_next_step_handler(request, get_count_host)
        bot.send_message(request.chat.id, 'Enter the Ip address and prefix:')

bot.polling(none_stop=True)
