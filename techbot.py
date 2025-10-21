import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# === CARREGA VARIÁVEIS DE AMBIENTE ===
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")

# === COMANDOS ===

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra as 3 principais notícias de tecnologia"""
    url = f"https://newsapi.org/v2/top-headlines?category=technology&language=en&apiKey={NEWS_API_KEY}"
    data = requests.get(url).json()

    articles = data.get("articles", [])[:3]
    if not articles:
        await update.message.reply_text("Não encontrei notícias no momento 😕")
        return

    msg = "📰 *Top notícias de tecnologia:*\n\n"
    for a in articles:
        msg += f"• [{a['title']}]({a['url']})\n"
    await update.message.reply_markdown(msg)


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra o clima atual de uma cidade"""
    if not context.args:
        await update.message.reply_text("Digite o nome da cidade, ex: /weather São Paulo")
        return

    city = " ".join(context.args)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=pt_br&appid={OPENWEATHER_KEY}"
    data = requests.get(url).json()

    if data.get("cod") != 200:
        await update.message.reply_text("Cidade não encontrada 😕")
        return

    desc = data["weather"][0]["description"].capitalize()
    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    msg = f"🌦️ *Clima em {city.title()}*\n{desc}\n🌡️ {temp}°C (sensação {feels}°C)"
    await update.message.reply_markdown(msg)


async def crypto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra o preço atual de uma criptomoeda"""
    coin = context.args[0].lower() if context.args else "bitcoin"
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd,brl"
    data = requests.get(url).json()

    if coin not in data:
        await update.message.reply_text("Criptomoeda não encontrada 😕 (ex: /crypto ethereum)")
        return

    price_usd = data[coin]["usd"]
    price_brl = data[coin]["brl"]
    msg = f"💰 *{coin.title()}*\n💵 USD: ${price_usd}\n💸 BRL: R${price_brl}"
    await update.message.reply_markdown(msg)


# === EXECUÇÃO ===
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("news", news))
app.add_handler(CommandHandler("weather", weather))
app.add_handler(CommandHandler("crypto", crypto))

print("🚀 Bot iniciado! Use Ctrl+C para parar.")
app.run_polling()
