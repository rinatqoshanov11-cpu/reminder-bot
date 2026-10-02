from telegram import (Update,
                      ReplyKeyboardMarkup,
                      KeyboardButton,
                      InlineKeyboardMarkup,
                      InlineKeyboardButton
                      )
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
    ApplicationBuilder,
    CallbackContext
)

TOKEN = "8703074491:AAGBRzpX0xq6Bam39z3hoX4FOjtxkLWl-4A"


async def start_rinat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tashqi_knopka = ReplyKeyboardMarkup([
        [KeyboardButton(text="📝 Ro'yxatdan o'tish"), KeyboardButton(text="🌐 Malumot")],
        [KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True)]

    ], resize_keyboard=True)

    await update.message.reply_text("Mana knopkalar: ", reply_markup=tashqi_knopka)


async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    phone_number = contact.phone_number
    first_name = contact.first_name

    await update.message.reply_text(
        f"Rahmat, {first_name}! Sizning telefon raqamingiz qabul qilindi: {phone_number}"
    )



async def start_again(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inline_knopka = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚽ Ronaldo akkaunti", url="https://www.instagram.com/cristiano?utm_source=ig_web_button_share_sheet&igsi=ZDNlZDc0MzIxNw==",callback_data="register")],
            [InlineKeyboardButton("🔗 Bot silkasi", url="t.me/rinat04_bot==", callback_data="bot")],

        ])

    await update.message.reply_text("Mana Inline knopkalar ⬇️:", reply_markup=inline_knopka)



async def command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    sms = update.message.text

    if sms == "📝 Ro'yxatdan o'tish":
        await update.message.reply_text("Siz 📝 Ro'yxatdan o'tish knopkasini bosdingiz")
    if sms == "🌐 Malumot":
        await update.message.reply_text("Siz 🌐 Malumot knopkasini bosdingiz")


async def inline_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Knopka bosilgandagi yuklanish (loading) effektini to'xtatadi

    if query.data == "register":
        await query.message.reply_text("Siz 📝 Ro'yxatdan o'tish knopkasini bosdingiz")

    if query.data == "bot":
       await query.message.reply_text("Siz bosdingiz ")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_rinat))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, command))
    app.add_handler(CallbackQueryHandler(command))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    print("Bot ishga tushdi...🤖")
    app.run_polling()


