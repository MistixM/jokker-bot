from telebot import types
from googletrans import Translator

import telebot
import requests

TOKEN = 'TOKEN'
bot = telebot.TeleBot(TOKEN)
translator = Translator()
url = 'https://api.api-ninjas.com/v1/jokes?limit=1'

class UserData():
    def __init__(self) -> None:
        self.user_data = {}
        
    def set_language(self, user_id, language):
        self.user_data[user_id] = language

    def get_language(self, user_id):
        return self.user_data.get(user_id, 'eng') # Default language

user_data_manager = UserData()

def main():

    @bot.message_handler(commands=['start'])
    def send_greetings(msg):
        
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item = types.KeyboardButton('RU')
        item1 = types.KeyboardButton('ENG')

        markup.add(item)
        markup.add(item1)

        sent_message = bot.send_message(msg.chat.id, f"Hello, <b>{msg.from_user.full_name}</b>! 👀\nI'm <b>{bot.get_me().first_name}</b>, I know how to make funny jokes and lift your spirits! 😄\n\nJust use /joke or /fun to start fun 😁",
                                        reply_markup=markup,
                                        parse_mode='HTML')

    @bot.message_handler(commands=['joke', 'fun'])
    def send_joke(msg):
        request = requests.get(url, headers={'X-Api-Key': 'cgvGrG/p62+QXoif9RTzLQ==mDlqTIJH1eBP4pK9'}).json()
        
        user_language = user_data_manager.get_language(msg.chat.id)
        for item in request:
            if user_language == 'ru':
                translated_text = translator.translate(item['joke'], dest='ru')
                bot.send_message(msg.chat.id, translated_text.text)
            else:
                bot.send_message(msg.chat.id, item['joke'])

    @bot.message_handler(content_types='text')    
    def button_press(msg):
        if msg.text == 'RU':
            user_data_manager.set_language(msg.chat.id, 'ru')
            bot.send_message(msg.chat.id, f"Ваш текущий язык: {user_data_manager.get_language(msg.chat.id)}")
        else:
            user_data_manager.set_language(msg.chat.id, 'eng')
            bot.send_message(msg.chat.id, f"Your current language: {user_data_manager.get_language(msg.chat.id)}")

if __name__ == "__main__":
    main()
    bot.polling()
