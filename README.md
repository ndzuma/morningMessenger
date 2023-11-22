# Morning Messager

## Overview

Morning Messager is a Python script that sends a daily roundup message containing weather information, a verse from the Bible, top stock prices, and news headlines to a specified Telegram chat. The script fetches data from various APIs, including OpenWeatherMap, Alpha Vantage, Hacker News, and a custom Supabase database.

## Prerequisites

- Python 3.x
- Required Python packages: `supabase`, `requests`, `python-telegram-bot`

```bash
pip install supabase requests python-telegram-bot
```

## Usage

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/morning-messager.git
    cd morning-messager
    ```

2. **Open the script in a text editor and update the following variables with your own values:**

    - `api_token`: Your Telegram bot API token.
    - `chat_id`: The chat ID where you want to send the messages.
    - `url` and `key`: Your Supabase project URL and API key.

    ```python
    # Open the script in a text editor and update the following variables with your own values:
    
    api_token = "your_telegram_bot_api_token"
    chat_id = 'your_telegram_chat_id'
    url = "your_supabase_url"
    key = "your_supabase_api_key"
    ```

## Run the Script

```bash
python morning_messager.py
```

The script will fetch:

- Weather data
- A random Bible verse
- Top stock prices
- News headlines

It then sends a formatted message to the specified Telegram chat.

### Notes

- Ensure that your Supabase database is properly configured with a table named 'bible' containing Bible verses.
- Be mindful of API usage limits and potential charges, especially for services like Alpha Vantage.

### Disclaimer

This script is provided as-is, and the user is responsible for reviewing and complying with the terms of use of the respective APIs. Use it responsibly and respect the terms and conditions of the data providers.


