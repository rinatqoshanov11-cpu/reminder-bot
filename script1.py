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


GAMES = {
    "free fire": {"name": "GARENA FREE FIRE", "price": "15,000 so'm", "desc": "Mobile oyin"},
    "cs2": {"name": "CS2 ", "price": "45,000 so'm", "desc": "Steam rasmiy oyini"},
    "gta5": {"name": "GTA V Premium Edition", "price": "150,000 so'm", "desc": "PC uchun"}
}

async def start_rinat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tashqi_knopka = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True),
            KeyboardButton(text="🎮 O'yin sotib olish")]
    ], resize_keyboard=True)

    await update.message.reply_text("Mana knopkalar: ⬇️", reply_markup=tashqi_knopka)


async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.contact:
        contact = update.message.contact
        phone_number = contact.phone_number
        first_name = contact.first_name

        await update.message.reply_text(
            f"Rahmat, {first_name}! Sizning telefon raqamingiz qabul qilindi: {phone_number}"
        )

    elif update.message.text == "🎮 O'yin sotib olish":
        await show_store(update, context)


async def show_store(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(text="GARENA FREE FIRE", callback_data="game_free fire")],
        [InlineKeyboardButton(text="CS2", callback_data="game_cs2")],
        [InlineKeyboardButton(text="GTA V", callback_data="game_gta5")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text="🎮 Mavjud o'yinlar: ⬇️\n\nTanlang:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def store_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data


    if data.startswith("game_"):
        game_key = data.split("_")[1]
        game = GAMES.get(game_key)

        if game:
            text = f"🎮 **{game['name']}**\n\n📝 Tavsif: {game['desc']}\n💰 Narxi: **{game['price']}**"
            buy_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(text="💳 Xarid qilish", callback_data=f"buy_{game_key}")],
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_store")],
            ])
            await query.edit_message_text(text=text, reply_markup=buy_keyboard, parse_mode="Markdown")


    elif data.startswith("buy_"):
        game_key = data.split("_")[1]
        game = GAMES.get(game_key)


        text = (
            f"🛒 **Buyurtma:** {game['name']}\n"
            f"💵 **To'lov summasi:** {game['price']}\n\n"
            f"💳 **To'lov karta raqami:** `(karta raqam hozircha yoq)` (Click / Payme)\n\n"
            f"⚠️ To'lovni amalga oshirgach, chekni yuboring!"
        )
        await query.edit_message_text(text=text, parse_mode="Markdown")


    elif data == "back_to_store":
        keyboard = [
            [InlineKeyboardButton(text="GARENA FREE FIRE", callback_data="game_free fire")],
            [InlineKeyboardButton(text=" CS2 ", callback_data="game_cs2")],
            [InlineKeyboardButton(text=" GTA V", callback_data="game_gta5")]
        ]
        await query.edit_message_text("🎮 **Mavjud o'yinlar va xizmatlar:**\n\nTanlang:",
                                      reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    elif data == "menu":
        keyboard = [

        ]

if __name__ == "__main__":
    app = ApplicationBuilder().token("8703074491:AAGBRzpX0xq6Bam39z3hoX4FOjtxkLWl-4A").build()
    #app.add_handler(CommandHandler("start", show_store))
    app.add_handler(CommandHandler("start", start_rinat))
    app.add_handler(MessageHandler(filters.TEXT | filters.CONTACT, contact_handler))
    app.add_handler(CallbackQueryHandler(store_callback))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    print("Bot ishga tushdi...🤖")
    app.run_polling()
