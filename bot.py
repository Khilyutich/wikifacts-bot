import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from wikipedia_facts_parser import WikipediaFactsParser  # Импортируем парсер

#Настройки бота
API_KEY = '7641088706:AAGoLn7cm98oiCCn-q4WZuKuWIQwyzwn1aI'
bot = telebot.TeleBot(API_KEY)

#Инициализация парсера
parser = WikipediaFactsParser()
def initialize_parser():
    """Инициализация парсера с обработкой ошибок"""
    try:
        parser.fetch_latest_month()
        parser.fetch_facts()
        return True
    except Exception as e:
        print(f"Ошибка инициализации парсера: {e}")
        return False

if not initialize_parser():
    print("Предупреждение: не удалось инициализировать парсер при старте")

#Клавиатура
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button_fact = KeyboardButton('Факт')
button_update = KeyboardButton('Обновить')
keyboard.add(button_fact, button_update)

# Приветственное сообщение с описанием функций
WELCOME_MESSAGE = """
🌟 *Добро пожаловать в бот "Интересные факты с Википедии"!* 🌟

Я могу:
🔹 Показывать интересные факты из Википедии (кнопка "Факт")
🔹 Обновлять базу фактов (кнопка "Обновить")

Просто нажми на одну из кнопок ниже, чтобы начать!

Если хочешь обновить список фактов - нажми "Обновить". Это может занять некоторое время.

Если у тебя есть вопросы или предложения, напиши /help.
"""

# Сообщение помощи
HELP_MESSAGE = """
ℹ️ *Помощь по боту*

Я понимаю следующие команды:
/start - начать работу с ботом
/help - показать это сообщение
"Факт" - показать случайный факт
"Обновить" - обновить базу фактов

Если что-то не работает, попробуй:
1. Нажать "Обновить"
2. Подождать минуту и попробовать снова
3. Написать разработчику
"""

# Сообщение для неизвестных команд
UNKNOWN_COMMAND_MESSAGE = """
🤔 Я не понял вашего сообщения. 

Пожалуйста, используйте кнопки ниже или команды:
- "Факт" - получить интересный факт
- "Обновить" - обновить базу фактов
- /help - помощь по боту
"""

#Обработчики команд бота
@bot.message_handler(commands=['start', 'начать'])
def welcome(message):
    """Обработчик команды start"""
    bot.send_message(message.chat.id, WELCOME_MESSAGE, parse_mode='Markdown', reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def help_command(message):
    """Обработчик команды help"""
    bot.send_message(message.chat.id, HELP_MESSAGE, parse_mode='Markdown')


@bot.message_handler(func=lambda message: message.text == 'Факт')
def send_fact(message):
    """Обработчик кнопки Факт"""
    if not parser.facts:
        bot.send_message(message.chat.id, "Факты не загружены. Пожалуйста, нажмите 'Обновить'.")
        return

    fact = parser.get_next_fact()
    if fact == "Больше фактов нет.":
        bot.send_message(message.chat.id, "Вы просмотрели все факты. Нажмите 'Обновить' для загрузки новых.")
    else:
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

@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    """Обработчик неизвестных сообщений"""
    bot.send_message(message.chat.id, UNKNOWN_COMMAND_MESSAGE, reply_markup=keyboard)

#Запуск бота
bot.polling()
