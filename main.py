import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8987929464:AAF6GyVmTlhf6RxasRXZpZ5LwA3T4cb_0Go"
GEMINI_KEY = "AQ.Ab8RN6IhhROx663Ese26T_I0Or_a61lQ1vpt6o0mXSfc-UVP1A"

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("هلا! ارسلي صورة الشارت وانا احللها لك 📈")

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لحظة بحلل... ⏳")
    try:
        file = await update.message.photo[-1].get_file()
        img = await file.download_as_bytearray()
        res = model.generate_content([
            "انت خبير ذهب محترف. حلل الشارت: الترند، دعم، مقاومة، نقطة دخول، ستوب، هدف. جاوب عربي مختصر واضح مع ايموجي.",
            {"mime_type": "image/jpeg", "data": bytes(img)}
        ])
        await update.message.reply_text(res.text)
    except Exception as e:
        await update.message.reply_text(f"خطأ: {e}")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, analyze))
app.run_polling()
