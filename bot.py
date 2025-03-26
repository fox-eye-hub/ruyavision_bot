
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from config import TELEGRAM_TOKEN, ADMIN_ID
from google_sheet import save_to_sheet
import datetime

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("📌 Biz haqimizda"), KeyboardButton("🛠 Xizmatlarimiz")],
        [KeyboardButton("💬 Maslahat"), KeyboardButton("📝 Buyurtma berish")],
        [KeyboardButton("📄 Price List"), KeyboardButton("📱 Aloqa")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Xush kelibsiz, tanlang!", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat.id

    if text == "📌 Biz haqimizda":
        with open("about_us.jpg", "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption="Ruya Vision Media — bu yurakka yetib boradigan kontentlar yaratadigan ijodkorlar jamoasi."
            )
    elif text == "🛠 Xizmatlarimiz":
        await update.message.reply_text ("• Mobilografiya\n• Grafik dizayn\n• Target reklama\n• SMM xizmatlari\n")
    elif text == "💬 Maslahat":
        await update.message.reply_text("Maslahat uchun bizga yozing: @ruyavisionadmin")
    elif text == "📄 Price List":
        await update.message.reply_text("Narxlar bo‘yicha ma'lumot olish uchun @ruyavisionadmin bilan bog‘laning.")
    elif text == "📱 Aloqa":
        buttons = [
            [InlineKeyboardButton("Instagram", url="https://www.instagram.com/ruyavisionuz?igsh=MTF4MXp4ZDNiMHhi")],
            [InlineKeyboardButton("Telegram", url="https://t.me/ruyavisionadmin")]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await update.message.reply_text("Biz bilan bog‘lanish:", reply_markup=reply_markup)
    elif text == "📝 Buyurtma berish":
        user_data[chat_id] = {}
        await update.message.reply_text("Familiya va ismingizni kiriting:")
        return
    elif chat_id in user_data and "name" not in user_data[chat_id]:
        user_data[chat_id]["name"] = text
        await update.message.reply_text("Qanday xizmat kerak?")
    elif chat_id in user_data and "service" not in user_data[chat_id]:
        user_data[chat_id]["service"] = text
        await update.message.reply_text("Telefon raqamingizni kiriting:")
    elif chat_id in user_data and "phone" not in user_data[chat_id]:
        user_data[chat_id]["phone"] = text
        await update.message.reply_text("Qo‘shimcha izohingiz bormi?")
    elif chat_id in user_data and "note" not in user_data[chat_id]:
        user_data[chat_id]["note"] = text
        data = user_data[chat_id]
        data["date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_to_sheet(data)
        msg = f"Yangi buyurtma berishingiz mumkin!"
        Ism: {data['name']}
        Xizmat: {data['service']}
        Tel: {data['phone']}
        Izoh: {data['note']}
        await context.bot.send_message(chat_id=ADMIN_ID, text=msg)
        await update.message.reply_text("Buyurtmangiz qabul qilindi! Tez orada aloqaga chiqamiz.")
        del user_data[chat_id]

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
