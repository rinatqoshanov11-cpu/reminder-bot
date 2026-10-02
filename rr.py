
import telebot
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import itertools


BOT_TOKEN = "TOKEN"

bot = telebot.TeleBot(BOT_TOKEN)
scheduler = BackgroundScheduler()
scheduler.start()


reminders = {}
id_counter = itertools.count(1)



def send_reminder(chat_id, reminder_id, text):
    """Belgilangan vaqt kelganda eslatmani yuboradi."""
    bot.send_message(chat_id, f"⏰ Eslatma: {text}")
    # Yuborilgandan keyin ro'yxatdan o'chiramiz
    user_reminders = reminders.get(chat_id, {})
    user_reminders.pop(reminder_id, None)



@bot.message_handler(commands=["start"])
def cmd_start(message):
    text = (
        "Salom! Men eslatma botiman. 🤖\n\n"
        "Men orqali o'zingizga eslatma qo'yishingiz mumkin.\n\n"
        "Buyruqlar ro'yxati uchun /help yozing."
    )
    bot.reply_to(message, text)


@bot.message_handler(commands=["help"])
def cmd_help(message):
    text = (
        "📋 Buyruqlar:\n\n"
        "/remind <daqiqa> <matn> — belgilangan daqiqadan keyin eslatadi\n"
        "   Masalan: /remind 10 Suv ichish vaqti keldi\n\n"
        "/myreminders — faol eslatmalaringiz ro'yxati\n\n"
        "/cancel <id> — eslatmani bekor qilish\n"
        "   Masalan: /cancel 3"
    )
    bot.reply_to(message, text)


@bot.message_handler(commands=["remind"])
def cmd_remind(message):
    chat_id = message.chat.id
    parts = message.text.split(maxsplit=2)

    if len(parts) < 3:
        bot.reply_to(
            message,
            "❗ To'g'ri format: /remind <daqiqa> <matn>\n"
            "Masalan: /remind 15 Dars boshlanadi"
        )
        return

    try:
        minutes = int(parts[1])
        if minutes <= 0:
            raise ValueError
    except ValueError:
        bot.reply_to(message, "❗ Daqiqa son bo'lishi va 0 dan katta bo'lishi kerak.")
        return

    reminder_text = parts[2]
    run_time = datetime.now() + timedelta(minutes=minutes)
    reminder_id = next(id_counter)

    reminders.setdefault(chat_id, {})[reminder_id] = {
        "text": reminder_text,
        "time": run_time,
    }

    scheduler.add_job(
        send_reminder,
        "date",
        run_date=run_time,
        args=[chat_id, reminder_id, reminder_text],
    )

    bot.reply_to(
        message,
        f"✅ Eslatma o'rnatildi (ID: {reminder_id}).\n"
        f"⏰ Vaqt: {run_time.strftime('%H:%M:%S')}\n"
        f"📝 Matn: {reminder_text}"
    )


@bot.message_handler(commands=["myreminders"])
def cmd_my_reminders(message):
    chat_id = message.chat.id
    user_reminders = reminders.get(chat_id, {})

    if not user_reminders:
        bot.reply_to(message, "Sizda hozircha faol eslatmalar yo'q.")
        return

    lines = ["📌 Sizning faol eslatmalaringiz:\n"]
    for rid, data in user_reminders.items():
        time_str = data["time"].strftime("%H:%M:%S")
        lines.append(f"ID {rid} — {time_str} — {data['text']}")

    bot.reply_to(message, "\n".join(lines))


@bot.message_handler(commands=["cancel"])
def cmd_cancel(message):
    chat_id = message.chat.id
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        bot.reply_to(message, "❗ Format: /cancel <id>\nMasalan: /cancel 2")
        return

    try:
        reminder_id = int(parts[1])
    except ValueError:
        bot.reply_to(message, "❗ ID son bo'lishi kerak.")
        return

    user_reminders = reminders.get(chat_id, {})
    if reminder_id in user_reminders:
        user_reminders.pop(reminder_id)
        bot.reply_to(message, f"🗑 Eslatma {reminder_id} bekor qilindi.")
    else:
        bot.reply_to(message, "❗ Bunday ID topilmadi.")



if __name__ == "__main__":
    print("Bot ishga tushdi...")
    bot.infinity_polling()








