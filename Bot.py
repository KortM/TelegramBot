import requests
import logging
from enum import Enum
import telebot
from telebot import types
from vedis_interface import set_step, get_last_step
from Main import Worker

bot = telebot.TeleBot('657281480:AAF0-_QY450Nw6jXwdrj_JdFL_aYfZSO_Bw')
worker = Worker()

@bot.message_handler(commands = ['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('\U0001F6E0 Menu'))
    bot.send_message(message.chat.id, "Hi, i'm network bot", reply_markup=keyboard)

def build_main_menu(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('\U0001F5A5 IP INFO'), types.KeyboardButton('\U00002797 HOST COUNT'))
    keyboard.add(types.KeyboardButton('\U0000260E TELEPHONY'), types.KeyboardButton('\U0001F4DF MAC INFO'))
    keyboard.add(types.KeyboardButton('\U00002B05 Back'))
    bot.send_message(message.chat.id, 'Select one', reply_markup=keyboard)

def ip_info(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('\U00002B05 Back'))

    if message.text:
        if message.text == '\U00002B05 Back':
            build_main_menu(message)
            return
        bot.send_message(message.chat.id, worker.search_ip_addr(message.text))
        bot.send_message(message.chat.id, 'Please input IP address:', reply_markup=keyboard)
        bot.register_next_step_handler(message, ip_info)

def get_count_host(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('\U00002B05 Back'))

    if message.text:
        if message.text == '\U00002B05 Back':
            build_main_menu(message)
            return
        bot.send_message(message.chat.id, worker.get_ip(message.text))
        bot.send_message(message.chat.id, 'Please input IP address and prefix:', reply_markup=keyboard)
        bot.register_next_step_handler(message, get_count_host)

def get_mac_info(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('\U00002B05 Back'))

    if message.text:
        if message.text == '\U00002B05 Back':
            build_main_menu(message)
            return
        bot.send_message(message.chat.id, worker.handle_mac(message.text))
        bot.send_message(message.chat.id, 'Please input mac address:', reply_markup=keyboard)
        bot.register_next_step_handler(message, get_mac_info)

def get_telephony_info(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('\U00002B05 Back'))

    if message.text:
        if message.text == '\U00002B05 Back':
            build_main_menu(message)
            return
        
        result = worker.handle_telephone(message.text)
        print(result)
        if result and len(result) == 2:
            bot.send_photo(message.chat.id, result[1], result[0])
            bot.send_message(message.chat.id, 'Please input telephone number:', reply_markup=keyboard)
            bot.register_next_step_handler(message, get_telephony_info)
        else:
            bot.send_message(message.chat.id, worker.handle_telephone(message.text))
            bot.send_message(message.chat.id, 'Please input telephone number:', reply_markup=keyboard)
            bot.register_next_step_handler(message, get_telephony_info)

@bot.message_handler(func=lambda call: True)
def message_handler(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    if message.text == '\U0001F6E0 Menu':
        keyboard.add(types.KeyboardButton('\U00002B05 Back'))
        build_main_menu(message)
        set_step(message.chat.id,'Main menu')

    if message.text == '\U0001F5A5 IP INFO':
        keyboard.add(types.KeyboardButton('\U00002B05 Back'))
        bot.send_message(message.chat.id, 'Please input IP address', reply_markup=keyboard)
        bot.register_next_step_handler(message, ip_info)

    if message.text == '\U00002797 HOST COUNT':
        keyboard.add(types.KeyboardButton('\U00002B05 Back'), types.KeyboardButton('192.168.1.1/30'))
        bot.send_message(message.chat.id, 'Please input IP address and prefix', reply_markup=keyboard)
        bot.register_next_step_handler(message, get_count_host)

    if message.text == '\U0001F4DF MAC INFO':
        keyboard.add(types.KeyboardButton('\U00002B05 Back'))
        bot.send_message(message.chat.id, 'Please input mac address:', reply_markup=keyboard)
        bot.register_next_step_handler(message, get_mac_info)

    if message.text == '\U0000260E TELEPHONY':
        keyboard.add(types.KeyboardButton('\U00002B05 Back'))
        bot.send_message(message.chat.id, 'Please input telephone number:', reply_markup=keyboard)
        bot.register_next_step_handler(message, get_telephony_info)

    if message.text == '\U00002B05 Back':
        if str(get_last_step(message.chat.id)) == 'Main menu':
            start(message)

if __name__ == '__main__':
    bot.polling(none_stop=True)
