# Morning Messager

## Overview

Morning Messenger is a Python script that sends a daily roundup message containing weather information, a verse from the Bible, top stock prices, and news headlines to a specified Telegram chat. The script fetches data from various APIs, including OpenWeatherMap, Alpha Vantage, Hacker News, and a custom Supabase database.

Morning Messenger was made to be used as a cron job for daily automated messages. It can be used as-is or modified to suit your needs.

## Prerequisites

- Python 3.x
- Required Python packages: `supabase`, `requests`, `python-telegram-bot`, `python-dotenv`

```bash
pip install supabase requests python-telegram-bot python-dotenv
```

## Usage

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/morning-messager.git
    cd morning-messager
    ```

2. **Edit the existing .env file:**

   Open the `.env` file in a text editor and update the following variables with your own values:

   ```env
   TELEGRAM_API_TOKEN=your_token
   TELEGRAM_CHAT_ID=your_chat_id
   SUPABASE_URL=your_url
   SUPABASE_API_KEY=your_key
   OPEN_WEATHER_API_KEY=your_key
   ALPHA_VANTAGE_API_KEY=your_key
   USERS_NAME=some_name
   TICKERS=your_tickers_separated_by_comma
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

## Customizing Output

You can edit the output of the message by going into the `generate_message` function. Feel free to explore and modify the function as needed.

## Future Developments

   ### Multiple Recipients:
   
   - Add the ability to send messages to multiple chat IDs and usernames.
   
   ### Custom Message Output:
   
   - Implement the ability to change the output message using a text file.
   
   ### Additional Data Points:
   
   - Include options to add more data points, such as additional news sources, weather locations, recommended studies, etc.
   
   ### Bible Dataset Availability:
   
   - Make the Bible dataset available for cloning.
   
   ### Database Connectivity:

   - Allow connection to other databases, not limited to Supabase.

   Feel free to contribute and explore these future developments! Contributions are welcomed.

### Notes

- Ensure that your Supabase database is properly configured with a table named 'bible' containing Bible verses.
- Be mindful of API usage limits and potential charges, especially for services like Alpha Vantage.

### Disclaimer

This script is provided as-is, and the user is responsible for reviewing and complying with the terms of use of the respective APIs. Use it responsibly and respect the terms and conditions of the data providers.


