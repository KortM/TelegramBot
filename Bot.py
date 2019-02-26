import requests
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import logging
import Config
from Main import UpdateBD

class Bot():
    #инициализация бота
    def __init__(self):
        self.updater = Updater(token='657281480:AAF0-_QY450Nw6jXwdrj_JdFL_aYfZSO_Bw')
        self.dispatcher = self.updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.u  = UpdateBD()
    def start(self, bot, update):
        text = "Привет! Начнем? Высылай мак-адрес "
        rain = '\U0001F609'
        m = "Внимание! Бета-тест!"
        bot.send_message(chat_id=update.message.chat_id, text=text+rain+'\n'+m)
    def getMessage(self, bot, update):
        result =self.u.splitStr(update.message.text)
        if type(result)==tuple:
            bot.send_message(chat_id=update.message.chat_id, text='<b style="color:blue;">'+result[1]+'\n'+result[0]+"</b>", parse_mode='HTML')
        else:
            bot.send_message(chat_id=update.message.chat_id, text='<b style="color:blue;">' + result + "</b>", parse_mode='HTML')


    #метод запуска бота
    def main(self):
        echo_handler = MessageHandler(Filters.text, self.getMessage)
        start_handler = MessageHandler(Filters.command, self.start)
        self.dispatcher.add_handler(echo_handler)
        self.dispatcher.add_handler(start_handler)
        self.updater.start_polling()
if __name__ == '__main__':
    b = Bot()
    b.main()
