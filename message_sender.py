from supabase import create_client, Client
from dotenv import load_dotenv
import requests_cache
import requests
import telegram
import asyncio
import random
import time
import os

""""
TODO:
FIND A WAY TO GET WEATHER FROM DIF CITIES
ADD A CONDITION, IF NOT MORE THAN A USER IGNORE USE
    IF THERE ARE MULTIPLE USERS AND ONE CONDITION, USE IT FOR ALL
    IF THERE IS MULTIPLE NO CONDITION, DEFAULT TO TRUE
"""


def parse_env(env_name, is_bool: bool = False) -> list:
    env = os.getenv(env_name)
    parsed = []
    env = env.split(",")
    print(env)
    if is_bool:
        for i in env:
            if i.lower() == "true":
                i = True
            else:
                i = False
            parsed.append(i)
        return parsed
    else:
        return env


# Load environment variables
load_dotenv()

telegram_apiKey = os.getenv("TELEGRAM_API_TOKEN")
telegram_chatId = parse_env("TELEGRAM_CHAT_ID")
supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_API_KEY")
openWeatherMap_apiKey = os.getenv("OPEN_WEATHER_API_KEY")
alphaVantage_apiKey = os.getenv("ALPHA_VANTAGE_API_KEY")
users_name = parse_env("USERS_NAME")
stockTickers = parse_env("TICKERS")
use_weather = parse_env("USE_WEATHER", is_bool=True)
use_stocks = parse_env("USE_STOCKS", is_bool=True)
use_news = parse_env("USE_NEWS", is_bool=True)
use_verse = parse_env("USE_VERSE", is_bool=True)

# Enable caching with a SQLite backend (this creates a file named 'main_cache.sqlite'). Cache expires after 1 hour
requests_cache.install_cache('main_cache', expire_after=600)


class Data:
    @staticmethod
    def weather():
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

    @staticmethod
    def news():
        # Using Hacker News API
        url = 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'
        data = {}

        response = requests.get(url)
        if response.status_code == 200:
            print("Fetching news data")
            response = response.json()

            count = 1
            for story_id in response[:5]:
                print(story_id)
                story_url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty'
                story_response = requests.get(story_url)
                if story_response.status_code == 200:
                    story_data = story_response.json()
                    try:
                        data[count] = {"title": story_data["title"], "url": story_data["url"]}
                    except KeyError:
                        pass
                    count += 1
                else:
                    print(f"Error fetching story details. Status code: {story_response.status_code}")
            return data, False
        else:
            for count in range(1, 6):
                data[count] = {"title": "Error", "url": "Error"}
            return data, True

    @staticmethod
    def stocks(tickers: list):
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

    @staticmethod
    def verse(verse: int):
        supabase: Client = create_client(supabase_url, supabase_key)
        response = supabase.table('bible').select("*").eq("id", verse).execute()
        book = response.data[0]["book"].capitalize().rstrip()
        chapter = response.data[0]["chapter"]
        verse = response.data[0]["verse"]
        text = response.data[0]["text"]
        return book, chapter, verse, text


class Message:
    @staticmethod
    def verse():
        verse_text = "<b>Verse of the day</b>\n"
        verse = random.randint(1, 31099)
        book, chapter, verse, text = Data.verse(verse=verse)
        verse_text += f"""{book} {chapter}:{verse} - "{text}"\n"""
        return verse_text

    @staticmethod
    def weather():
        summary, current_temp, day_temp, weather, weather_error = Data.weather()
        weather_text = "<b>Today's weather</b>\n"
        if not weather_error:
            weather_text += f"""The vibe today is {summary}.
                Current temp: {current_temp}°C
                Today's temp: {day_temp}°C
                Weather: {weather}\n"""
            weather_text = weather_text.replace('        ', '')
        else:
            weather_text = f"""Error fetching weather data\n"""
        return weather_text

    @staticmethod
    def stocks():
        stocks = Data.stocks(tickers=stockTickers)
        stocks_text = "<b>Top stock prices</b>\n"
        for stock in stocks:
            stock_index = list(stocks).index(stock) + 1
            if not stocks[stock]["error"]:
                stocks_text += f"""{stock_index}. {stock}: {stocks[stock]["price"]}, {stocks[stock]["comment"]} {stocks[stock]["percent_change"]} from yesterday.\n"""
            else:
                stocks_text += f"""{stock_index}. Error fetching {stock} data\n"""
        return stocks_text

    @staticmethod
    def news():
        news, news_error = Data.news()
        news_text = "<b>Top stock prices</b>\n"
        if not news_error:
            for i in range(len(news)):
                news_text += f"""{i + 1}. {news[i + 1]["title"]} {news[i + 1]["url"]}\n"""
        else:
            news_text += f"""Error fetching news data\n"""
        return news_text


def generate_message(name: str, weather: bool, verse: bool, stocks: bool, news: bool):
    main_message = f"""Hi {name}. Here is your daily round up:\n"""

    if weather:
        main_message += f"""{Message.weather()}"""
    if verse:
        main_message += f"""{Message.verse()}"""
    if stocks:
        main_message += f"""{Message.stocks()}"""
    if news:
        main_message += f"""{Message.news()}"""

    main_message += "<b>Have a nice day!!!</b>"
    main_message = main_message.replace('    ', '')

    return main_message


# Main function
async def main():
    number_of_ids = len(telegram_chatId)
    for index in range(number_of_ids):
        # Checks if there are enough usernames for the provided chat ids
        if number_of_ids > len(users_name):
            print("Error: Number of chat_ids > number of users, therefore only the first user will be used for all chat ids")
            username = users_name[0]
        else:
            username = users_name[index]

        main_message = generate_message(name=username, weather=use_weather[index], verse=use_verse[index], stocks=use_stocks[index], news=use_news[index])
        bot = telegram.Bot(telegram_apiKey)
        print(f"Sending message to username: {username}, chat id: {telegram_chatId[index]}")
        async with bot:
            await bot.send_message(text=main_message, chat_id=telegram_chatId[index], parse_mode="html")

        # The sleep is to ensure telegram doesn't block the bot
        # You can increase this time or outright remove it if you want
        # The rate limit is 30 messages per second
        time.sleep(1)


# Start of the program
if __name__ == '__main__':
    print("Starting Morning Messenger")
    asyncio.run(main())
    print("Finished")
