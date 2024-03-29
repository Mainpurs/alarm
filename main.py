import telebot
import json
import time
import schedule


TOKEN = "6740118233:AAGvSXXAqGBP_wtolH9K92B1AHdA5YSPO4Q"
bot = telebot.TeleBot(TOKEN)
filename = "user_data.json"


def load_data():
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    return data


def save_data(data):
    with open(filename, "w") as f:
        json.dump(data, f)


def send_message(message):
    data = load_data()
    if message == "morning":
        msg = "Доброе утро!"
    elif message == "evening":
        msg = "Спокойной ночи, сладких снов и апельсинов! 🍊🍊🍊"
    for user_id in data:
        bot.send_message(user_id, msg)
        if message == "evening":
            bot.send_sticker(user_id, 'CAACAgIAAxkBAAEDfAxlzKFOIybEIMUtkRlBdn-WQwIfaQACODEAAkpvYUhVZUvs2_rBqTQE')


schedule.every().day.at("01:30").do(send_message, "morning")
schedule.every().day.at("17:00").do(send_message, "evening")


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    bot.send_message(user_id, 'Ок')
    data = load_data()
    if str(user_id) not in data:
        data[str(user_id)] = ''
    save_data(data)


# Запускаем планировщик в отдельном потоке
while True:
    schedule.run_pending()
    time.sleep(1)
