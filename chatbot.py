import requests

CMC_API_KEY = "555916e7-f6f8-43fa-80c2-f646dc2cd9d5"

def get_crypto(symbol, convert="USD"):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
    params = {"symbol": symbol, "convert": convert}
    data = requests.get(url, headers=headers, params=params).json()
    return f"{symbol}/{convert}: {data['data'][symbol]['quote'][convert]['price']:.2f}"

import yfinance as yf

def get_usd_byn():
    ticker = yf.Ticker("USDBYN=X")
    price = ticker.info.get("regularMarketPrice")
    if price:
        return f"BYN/USD: {price:.2f}"
    else:
        return "USD/BYN: данные недоступны"

def get_indexes():
    sp500 = yf.Ticker("^GSPC").info["regularMarketPrice"]
    dowjones = yf.Ticker("^DJI").info["regularMarketPrice"]
    return f"S&P500/USD: {sp500:.2f}\nDow Jones/USD: {dowjones:.2f}"

def get_weather(city, lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&current_weather=true&timezone=auto"
    )
    try:
        res = requests.get(url, timeout=5).json()
        weather = res["current_weather"]
        temp = weather["temperature"]
        wind = weather["windspeed"]
        desc = weather["weathercode"]  # код погоды
        return f"{city}: {temp}°C, ветер {wind} км/ч, {decode_weather(desc)}"
    except Exception as e:
        return f"Ошибка получения погоды для {city}: {e}"

def decode_weather(code):
    mapping = {
        0: "ясно",
        1: "в основном ясно",
        2: "переменная облачность",
        3: "пасмурно",
        45: "туман",
        48: "изморозь",
        51: "слабый дождь",
        61: "дождь",
        71: "снег",
        80: "ливень",
    }
    return mapping.get(code, "неизвестная погода")

from bs4 import BeautifulSoup
import random

def get_russian_joke():
    url = "https://www.anekdot.ru/random/anekdot/"
    response = requests.get(url)
    response.encoding = "utf-8"  # чтобы корректно читать кириллицу
    soup = BeautifulSoup(response.text, "html.parser")

    # На странице анекдоты лежат в div с классом "text"
    jokes = [div.get_text(strip=True) for div in soup.find_all("div", class_="text")]

    if jokes:
        return random.choice(jokes)
    else:
        return "Не удалось получить шутку"

def get_currency():
    results = []

    # Курсы валют и крипты
    results.append("💰 КУРСЫ")
    results.append(get_crypto("BTC", "USD"))
    results.append(get_crypto("XRP", "USD"))
    results.append(get_usd_byn())
    results.append(get_indexes())

    # Погода
    results.append("\n🌤 ПОГОДА")
    results.append(get_weather("Минск", 53.9, 27.5667))
    results.append(get_weather("Мозырь", 51.9833, 29.1667))
    results.append(get_weather("Ивацевичи", 52.7, 25.34))

    # Анекдот дня
    results.append("\n🤣 АНЕКДОТ ДНЯ")
    results.append(get_russian_joke())

    return "\n".join(results) 

BOT_TOKEN = "8379323318:AAGtbyUk_BxkiREH_KIi8cWwP0DRTAaeSTo"
CHAT_ID = "-1002288244393"  # например, id канала или группы
MESSAGE = get_currency()  # твоя функция формирует текст

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    requests.post(url, data=payload)

# пример вызова
send_message(MESSAGE)

