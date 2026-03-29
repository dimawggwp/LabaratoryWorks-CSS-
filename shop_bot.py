from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)
 
# ==================== БАПТАУЛАР ====================
TOKEN = "8701758387:AAGUnrJebztltY3j_IUXT347LoUnB1tNrxo\"          
ADMIN_CHAT_ID = "2018648930"
# ===================================================
 
КАТАЛОГ = {
    "Tamak": {"Pizza": 2500, "Burger": 1800, "Shaurma": 1500},
    "Kiim": {"Futbolka": 3500, "Hudi": 7000, "Jynsy": 9000},
    "Elektronika": {"Kulakkap": 12000, "Zaryadtaghysh": 3000, "Qap": 1500},
}
 
KATALOG_KAZ = {
    "Tamak": "Tамак",
    "Kiim": "Киім",
    "Elektronika": "Электроника",
    "Pizza": "Пицца",
    "Burger": "Бургер",
    "Shaurma": "Шаурма",
    "Futbolka": "Футболка",
    "Hudi": "Худи",
    "Jynsy": "Джинсы",
    "Kulakkap": "Құлаққап",
    "Zaryadtaghysh": "Зарядтағыш",
    "Qap": "Қап",
}
 
SANAT_KORSETU = {
    "Tamak": "Тамақ",
    "Kiim": "Киім",
    "Elektronika": "Электроника",
}
 
# Сұхбат күйлері
SANAT_TANDAU, TAUАР_TANDAU, TAPSYRYS_RASTAU, ATY, TELEFON, MEKENJAY = range(6)
 
 
async def bastau(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(SANAT_KORSETU[sanat], callback_data=f"sanat_{sanat}")]
        for sanat in КАТАЛОГ
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Дүкенге қош келдіңіз!\nСанатты таңдаңыз:",
        reply_markup=reply_markup,
    )
    return SANAT_TANDAU
 
 
async def sanat_tandau(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    sanat_key = query.data.replace("sanat_", "")
    context.user_data["sanat"] = sanat_key
    tauarlar = КАТАЛОГ[sanat_key]
    keyboard = [
        [InlineKeyboardButton(f"{KATALOG_KAZ.get(tauар, tauар)} — {baga} тг", callback_data=f"tauar_{tauар}")]
        for tauар, baga in tauarlar.items()
    ]
    keyboard.append([InlineKeyboardButton("Артқа", callback_data="artqa_sanattarga")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        f"Санат: {SANAT_KORSETU[sanat_key]}\nТауарды таңдаңыз:",
        reply_markup=reply_markup,
    )
    return TAUАР_TANDAU
 
 
async def tauар_tandau(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
 
    if query.data == "artqa_sanattarga":
        keyboard = [
            [InlineKeyboardButton(SANAT_KORSETU[sanat], callback_data=f"sanat_{sanat}")]
            for sanat in КАТАЛОГ
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Санатты таңдаңыз:", reply_markup=reply_markup)
        return SANAT_TANDAU
 
    tauар_aty = query.data.replace("tauar_", "")
    sanat_key = context.user_data.get("sanat")
    baga = КАТАЛОГ[sanat_key][tauар_aty]
    context.user_data["tauар"] = tauар_aty
    context.user_data["baga"] = baga
 
    korsetu_aty = KATALOG_KAZ.get(tauар_aty, tauар_aty)
 
    keyboard = [
        [InlineKeyboardButton("Тапсырыс беру", callback_data="tapsyrys_rastau")],
        [InlineKeyboardButton("Артқа", callback_data=f"sanat_{sanat_key}")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        f"Тауар: {korsetu_aty}\nБағасы: {baga} тг\n\nТапсырыс беруді қалайсыз ба?",
        reply_markup=reply_markup,
    )
    return TAPSYRYS_RASTAU
 
 
async def tapsyrys_rastau(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Атыңызды жазыңыз:")
    return ATY
 
 
async def aty_alu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["aty"] = update.message.text
    await update.message.reply_text("Телефон нөміріңізді жазыңыз:")
    return TELEFON
 
 
async def telefon_alu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["telefon"] =
update.message.text
    await update.message.reply_text("Жеткізу мекенжайыңызды жазыңыз:")
    return MEKENJAY
 
 
async def mekenjay_alu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mekenjay"] = update.message.text
    paydalanushy_id = update.effective_user.id
 
    aty = context.user_data.get("aty")
    telefon = context.user_data.get("telefon")
    mekenjay = context.user_data.get("mekenjay")
    tauар_key = context.user_data.get("tauар")
    baga = context.user_data.get("baga")
    sanat_key = context.user_data.get("sanat")
 
    tauар_korsetu = KATALOG_KAZ.get(tauар_key, tauар_key)
    sanat_korsetu = SANAT_KORSETU.get(sanat_key, sanat_key)
 
    tapsyrys_matin = (
        f"Жаңа тапсырыс!\n"
        f"Санат: {sanat_korsetu}\n"
        f"Тауар: {tauар_korsetu}\n"
        f"Бағасы: {baga} тг\n"
        f"Аты: {aty}\n"
        f"Телефон: {telefon}\n"
        f"Мекенжай: {mekenjay}\n"
        f"Пайдаланушы ID: {paydalanushy_id}"
    )
 
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=tapsyrys_matin)
    await update.message.reply_text(
        f"Рахмет, {aty}!\n"
        f"Тапсырысыңыз қабылданды.\n"
        f"Тауар: {tauар_korsetu} — {baga} тг\n"
        f"Сізге {telefon} нөміріне хабарласамыз.\n\n"
        f"Жаңа тапсырыс үшін /start жазыңыз."
    )
    return ConversationHandler.END
 
 
async def boldyrмau(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Тапсырыс болдырылмады.\nҚайта бастау үшін /start жазыңыз."
    )
    return ConversationHandler.END
 
 
def negizgi():
    qoldanba = ApplicationBuilder().token(TOKEN).build()
 
    suhbat_ondеushi = ConversationHandler(
        entry_points=[CommandHandler("start", bastau)],
        states={
            SANAT_TANDAU: [CallbackQueryHandler(sanat_tandau, pattern="^sanat_")],
            TAUАР_TANDAU: [CallbackQueryHandler(tauар_tandau)],
            TAPSYRYS_RASTAU: [
                CallbackQueryHandler(tapsyrys_rastau, pattern="^tapsyrys_rastau$"),
                CallbackQueryHandler(sanat_tandau, pattern="^sanat_"),
            ],
            ATY: [MessageHandler(filters.TEXT & ~filters.COMMAND, aty_alu)],
            TELEFON: [MessageHandler(filters.TEXT & ~filters.COMMAND, telefon_alu)],
            MEKENJAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, mekenjay_alu)],
        },
        fallbacks=[CommandHandler("boldyrma", boldyrмau)],
    )
 
    qoldanba.add_handler(suhbat_ondеushi)
    print("Бот іске қосылды...")
    qoldanba.run_polling()
 
 
if __name__ == "__main__":
    negizgi()