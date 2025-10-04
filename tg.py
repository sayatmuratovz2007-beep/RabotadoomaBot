import telebot
from telebot import types

TOKEN = "8284021394:AAERGXoEO4SPyybbfv9GxohqyJ2bFTruMXk"
bot = telebot.TeleBot(TOKEN)

user_data = {}

# --- Команда /start ---
@bot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.username or message.from_user.first_name
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("👋 Привет! продолжить")
    markup.add(btn)
    text = f"👀 Привет, @{username}...\n\nЯ знал, что ты заглянешь.\nЗдесь не просто чат — это место, где удача улыбается смелым 🎲\n\nЖми кнопку «Привет! продолжить», и посмотрим, кто ты на самом деле 💫"
    bot.send_message(message.chat.id, text, reply_markup=markup)

# --- После приветствия ---
@bot.message_handler(func=lambda message: message.text == "👋 Привет! продолжить")
def ask_name(message):
    bot.send_message(message.chat.id, "Чтобы запомнить тебя — напиши своё имя ✍️")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_id = message.from_user.id
    user_data[user_id] = {'name': message.text}
    bot.send_message(message.chat.id, f"Отлично, {message.text}! Теперь напиши свой номер телефона 📞, чтобы зарегистрировать тебя на наши розыгрыши и мини-игры.")
    bot.register_next_step_handler(message, get_phone)

def get_phone(message):
    user_id = message.from_user.id
    user_data[user_id]['phone'] = message.text
    bot.send_message(message.chat.id, "Молодец! Теперь можешь ознакомиться с разделами 👇")
    show_menu(message)

# --- Меню ---
def show_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        "🎯 Узнать статус /status",
        "🛠 Тех.поддержка /help",
        "💬 Оставить отзыв /feedback",
        "🎮 Розыгрыши и мини-игры /raffle",
        "🏠 Главное меню /menu"
    ]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "📍 Главное меню:", reply_markup=markup)

# --- Команды ---
@bot.message_handler(commands=['menu'])
def menu(message):
    show_menu(message)

@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(message.chat.id, "Если нужна помощь — пиши сюда 👉 @abullbbul")

@bot.message_handler(commands=['feedback'])
def feedback(message):
    bot.send_message(message.chat.id, "💬 Отзыв можете оставить здесь — просто напишите сообщение.\nЯ передам его админу: @abullbbul")

@bot.message_handler(commands=['status'])
def status(message):
    bot.send_message(message.chat.id, "⏳ Следующий розыгрыш стартует в ближайшее воскресенье!")

@bot.message_handler(commands=['raffle'])
def raffle(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("🎮 Мини-игры", callback_data="mini")
    btn2 = types.InlineKeyboardButton("🎁 Розыгрыши", callback_data="raffle")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Выбери раздел 👇", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["mini", "raffle"])
def callback(call):
    if call.data == "mini":
        bot.send_message(call.message.chat.id, "🎮 Ближайшая мини-игра состоится 7 октября в 20:00!\nПриз: промокод на участие 🎫")
    elif call.data == "raffle":
        bot.send_message(call.message.chat.id, "🎁 Розыгрыш — 13 октября в 19:00!\nПриз: 10 000₸ на баланс 💰")

# --- Запуск ---
print("✅ Бот запущен и ждёт сообщений...")
bot.delete_webhook()
bot.polling(none_stop=True)
