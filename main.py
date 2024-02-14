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


def send_scheduled_message():
    data = load_data()
    save_data(data)
    data = load_data()
    message = "Доброе утро!"
    for user_id in data:
        bot.send_message(user_id, message)


schedule.every().day.at("01:30").do(send_scheduled_message)


def send_scheduled_message2():
    data = load_data()
    save_data(data)
    data = load_data()
    message = "Спокойной ночи, сладких снов и апельсинов! 🍊🍊🍊"
    for user_id in data:
        bot.send_message(user_id, message)
        bot.send_sticker(user_id, 'CAACAgIAAxkBAAEDfAxlzKFOIybEIMUtkRlBdn-WQwIfaQACODEAAkpvYUhVZUvs2_rBqTQE')


schedule.every().day.at("17:00").do(send_scheduled_message2)


@bot.message_handler(commands=['start'])
def start(message):
    data = load_data()
    user_id = message.chat.id
    bot.send_message(user_id, 'Ок')
    if str(user_id) not in data:
        data[str(user_id)] = ''
    save_data(data)
    # Запускаем планировщик в отдельном потоке
    while True:
        schedule.run_pending()
        time.sleep(1)


bot.infinity_polling()
