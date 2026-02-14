import requests
import os
CMC_API_KEY = "555916e7-f6f8-43fa-80c2-f646dc2cd9d5"

def get_crypto(symbol, convert="USD"):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
    params = {"symbol": symbol, "convert": convert}
    data = requests.get(url, headers=headers, params=params).json()

    price = data['data'][symbol]['quote'][convert]['price']
    change = data['data'][symbol]['quote'][convert]['percent_change_24h']

    if symbol == "XRP":
        if change >= 0:
            arrow = "📈 +"
            return f"{symbol}/{convert}: {price:.2f}                        ({arrow}{change:.2f}%)"
        else:
            arrow = "📉 -"
            return f"{symbol}/{convert}: {price:.2f}                        ({arrow}{abs(change):.2f}%)"
    else:        
        if change >= 0:
            arrow = "📈 +"
            return f"{symbol}/{convert}: {price:.2f}              ({arrow}{change:.2f}%)"
        else:
            arrow = "📉 -"
            return f"{symbol}/{convert}: {price:.2f}              ({arrow}{abs(change):.2f}%)"

import yfinance as yf

def get_usd_byn():
    ticker = yf.Ticker("USDBYN=X")

    # текущая цена
    price = ticker.info.get("regularMarketPrice")

    # берём историю за последние 2 дня
    hist = ticker.history(period="2d")

    if price and not hist.empty:
        # цена закрытия предыдущего дня
        prev_close = hist["Close"].iloc[0]

        # считаем процентное изменение
        change = ((price - prev_close) / prev_close) * 100

        # стрелка и цвет через эмодзи
        if change >= 0:
            arrow = "📈 +"
        else:
            arrow = "📉 -"

        return f"USD/BYN: {price:.2f}                       ({arrow}{abs(change):.2f}%)"
    else:
        return "USD/BYN: данные недоступны"

def get_indexes():
    # S&P500
    sp500_ticker = yf.Ticker("^GSPC")
    sp500_price = sp500_ticker.info.get("regularMarketPrice")
    sp500_hist = sp500_ticker.history(period="2d")
    if not sp500_hist.empty:
        sp500_prev = sp500_hist["Close"].iloc[0]
        sp500_change = ((sp500_price - sp500_prev) / sp500_prev) * 100
        sp500_arrow = "📈 +" if sp500_change >= 0 else "📉 -"
        sp500_str = f"S&P500/USD: {sp500_price:.2f}         ({sp500_arrow}{abs(sp500_change):.2f}%)"
    else:
        sp500_str = "S&P500/USD: данные недоступны"

    # Dow Jones
    dow_ticker = yf.Ticker("^DJI")
    dow_price = dow_ticker.info.get("regularMarketPrice")
    dow_hist = dow_ticker.history(period="2d")
    if not dow_hist.empty:
        dow_prev = dow_hist["Close"].iloc[0]
        dow_change = ((dow_price - dow_prev) / dow_prev) * 100
        dow_arrow = "📈 +" if dow_change >= 0 else "📉 -"
        dow_str = f"Dow Jones/USD: {dow_price:.2f} ({dow_arrow}{abs(dow_change):.2f}%)"
    else:
        dow_str = "Dow Jones/USD: данные недоступны"

    return f"{sp500_str}\n{dow_str}"

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
    url = "https://adme.media/articles/20-neveroyatno-zhiznennyh-stishkov-pirozhkov-921060/"
    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    pirozhki = [p.get_text(separator='\n', strip=True) for p in soup.find_all("p") 
                if len(p.get_text(strip=True)) > 25 and len(p.get_text(strip=True)) < 120]

    if pirozhki:
        stishok = random.choice(pirozhki)
        # ✅ ПРЯМЫЯ ПЕРЕНОСЫ — СОХРАНЯЕМ ОРИГИНАЛЬНЫЕ СТРОКИ!
        lines = stishok.split('\n')
        clean_lines = [line.strip() for line in lines if line.strip()]
        return '\n'.join(clean_lines[:5])  # Максимум 3 строки
    else:
        return "Не удалось получить стишок-пирожок"

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
    results.append("\n🤣 ПИРОЖОК ДНЯ")
    results.append(get_russian_joke())

    return "\n".join(results) 
    
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

MESSAGE = get_currency()  # твоя функция формирует текст

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    requests.post(url, data=payload)

# пример вызова
send_message(MESSAGE)

