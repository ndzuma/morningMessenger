from supabase import create_client, Client
from dotenv import load_dotenv
import requests
import telegram
import asyncio
import random
import time
import os


# Load stock ticker symbols
def load_ticker() -> list:
    tickers = os.getenv("TICKERS")
    tickers = tickers.split(",")
    return tickers


# Load usernames of recipients
def load_usernames() -> list:
    usernames = os.getenv("USERS_NAME")
    usernames = usernames.split(",")
    return usernames


# Load chat IDs of recipients
def load_chat_ids() -> list:
    chat_ids = os.getenv("TELEGRAM_CHAT_ID")
    chat_ids = chat_ids.split(",")
    return chat_ids


# Load environment variables
load_dotenv("private.env")
telegram_apiKey = os.getenv("TELEGRAM_API_TOKEN")
telegram_chatId = load_chat_ids()
supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_API_KEY")
openWeatherMap_apiKey = os.getenv("OPEN_WEATHER_API_KEY")
alphaVantage_apiKey = os.getenv("ALPHA_VANTAGE_API_KEY")
users_name = load_usernames()
stockTickers = load_ticker()


def get_weather_data():
    lat = 51
    lon = 0
    units = "metric"

    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units={units}&appid={openWeatherMap_apiKey}"
    response = requests.get(url)
    if response.status_code == 200:
        print("Fetching weather data")
        response = response.json()

        summary = response["current"]["weather"][0]["description"]
        current_temp = response["current"]["temp"]
        day_temp = response["daily"][0]["temp"]["day"]
        weather = response["current"]["weather"][0]["main"]

        return summary, current_temp, day_temp, weather, False
    else:
        print(f"Error fetching weather data. Status code: {response.status_code}")
        return "Error", "Error", "Error", "Error", True


def get_news_data():
    # Using Hacker News API
    url = 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'
    data = {}

    response = requests.get(url)
    if response.status_code == 200:
        print("Fetching news data")
        response = response.json()

        count = 1
        for story_id in response[:5]:
            story_url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty'
            story_response = requests.get(story_url)
            if story_response.status_code == 200:
                story_data = story_response.json()
                data[count] = {"title": story_data["title"], "url": story_data["url"]}
                count += 1
            else:
                print(f"Error fetching story details. Status code: {story_response.status_code}")
        return data, False
    else:
        for count in range(1, 6):
            data[count] = {"title": "Error", "url": "Error"}
        return data, True


def get_stock_data(tickers: list):
    # Using Alpha Vantage API
    data = {}

    for symbol in tickers:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={alphaVantage_apiKey}"
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Fetching data for {symbol}")
            response = response.json()

            count = 0
            new = 0
            old = 0
            for i in response["Time Series (Daily)"]:
                if count == 0:
                    new += float(response["Time Series (Daily)"][i]["4. close"])
                else:
                    old += float(response["Time Series (Daily)"][i]["4. close"])
                count += 1
                if count == 2:
                    break
            change = round((new - old), 2)
            percent_change = str(round(((change / old) * 100), 2)) + "%"
            if change < 0:
                comment = "down"
            elif change > 0:
                comment = "up"
            else:
                comment = "unchanged"
            data[symbol] = {"price": ("$" + str(new)), "change": change, "percent_change": percent_change, "comment": comment, "error": False}
        else:
            print(f"Error fetching stock data. Status code: {response.status_code}")
            data[symbol] = {"price": "Error", "change": "Error", "percent_change": "Error", "comment": "Error", "error": True}
    return data


def get_random_verse(verse: int):
    supabase: Client = create_client(supabase_url, supabase_key)
    response = supabase.table('bible').select("*").eq("id", verse).execute()
    book = response.data[0]["book"].capitalize().rstrip()
    chapter = response.data[0]["chapter"]
    verse = response.data[0]["verse"]
    text = response.data[0]["text"]
    return book, chapter, verse, text


def generate_message(name: str):
    verse = random.randint(1, 31099)
    book, chapter, verse, text = get_random_verse(verse=verse)
    summary, current_temp, day_temp, weather, weather_error = get_weather_data()
    stocks = get_stock_data(tickers=stockTickers)
    news, news_error = get_news_data()

    # Verse
    verse_text = f"""{book} {chapter}:{verse} - "{text}"\n"""

    # Weather
    if not weather_error:
        weather_text = f"""The vibe today is {summary}.
        Current temp: {current_temp}°C
        Today's temp: {day_temp}°C
        Weather: {weather}\n"""
        weather_text = weather_text.replace('        ', '')
    else:
        weather_text = f"""Error fetching weather data\n"""

    # Stocks
    stocks_text = ""
    for stock in stocks:
        stock_index = list(stocks).index(stock) + 1
        if not stocks[stock]["error"]:
            stocks_text += f"""{stock_index}. {stock}: {stocks[stock]["price"]}, {stocks[stock]["comment"]} {stocks[stock]["percent_change"]} from yesterday.\n"""
        else:
            stocks_text += f"""{stock_index}. Error fetching {stock} data\n"""

    # News
    news_text = "Hi, here is your daily round up:\n\n"
    if not news_error:
        for i in range(len(news)):
            news_text += f"""{i+1}. {news[i+1]["title"]} {news[i+1]["url"]}\n"""
    else:
        news_text += f"""Error fetching news data\n"""

    main_message = f"""Hi {name}. Here is your daily round up:\n
    <b>Today's weather</b>
    {weather_text}
    <b>Verse of the day</b>
    {verse_text}
    <b>Top stock prices</b>
    {stocks_text}
    <b>Have a nice day!!!</b>"""
    main_message = main_message.replace('    ', '')

    news_message = f"""{news_text}"""
    return main_message, news_message


# Main function
async def main():
    number_of_ids = len(telegram_chatId)
    for index in range(number_of_ids):
        if number_of_ids > len(users_name):
            print("Error: Number of chat_ids > number of users, therefore only the first user will be used for all chat ids")
            username = users_name[0]
        else:
            username = users_name[index]
        main_message, news_message = generate_message(name=username)
        bot = telegram.Bot(telegram_apiKey)
        print(f"Sending message to username: {username}, chat id: {telegram_chatId[index]}")
        async with bot:
            await bot.send_message(text=main_message, chat_id=telegram_chatId[index], parse_mode="html")
            await bot.send_message(text=news_message, chat_id=telegram_chatId[index], parse_mode="html")

        # The sleep is to ensure telegram doesn't block the bot
        # You can increase this time or outright remove it if you want
        # The rate limit is 30 messages per second
        time.sleep(1)


# Start of the program
if __name__ == '__main__':
    print("Starting Morning Messenger")
    asyncio.run(main())
    print("Finished")
