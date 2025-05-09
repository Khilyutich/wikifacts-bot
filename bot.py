import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from wikipedia_facts_parser import WikipediaFactsParser  # Импортируем парсер

#Настройки бота
API_KEY = '7641088706:AAGoLn7cm98oiCCn-q4WZuKuWIQwyzwn1aI'
bot = telebot.TeleBot(API_KEY)

#Инициализация парсера
parser = WikipediaFactsParser()
parser.fetch_latest_month()
parser.fetch_facts()

#Клавиатура
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button_fact = KeyboardButton('Факт')
button_update = KeyboardButton('Обновить')
keyboard.add(button_fact, button_update)

#Обработчики команд бота
@bot.message_handler(commands=['start', 'начать'])
def welcome(message):
    bot.send_message(message.chat.id, "Привет! Выбери действие:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == 'Факт')
def send_fact(message):
    fact = parser.get_next_fact()
    bot.send_message(message.chat.id, fact)

@bot.message_handler(func=lambda message: message.text == 'Обновить')
def update_facts(message):
    bot.send_message(message.chat.id, "Пожалуйста, подожди, я обновляю данные... 🔄")
    try:
        parser.fetch_latest_month()
        parser.fetch_facts()
        bot.send_message(message.chat.id, "Факты успешно обновлены! Теперь можешь снова нажимать 'Факт'. ✅")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при обновлении: {e}")

#Запуск бота
bot.polling()
