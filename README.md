# Morning Messenger

## Overview

Morning Messenger is a Python script that sends a daily roundup message containing weather information, a verse from the Bible, top stock prices, and news headlines to a specified Telegram chat. The script fetches data from various APIs, including OpenWeatherMap, Alpha Vantage, Hacker News, and a custom Supabase database.

Morning Messenger was made to be used as a cron job for daily automated messages. It can be used as-is or modified to suit your needs.

## Prerequisites

- Python 3.x
- Required Python packages: `supabase`, `requests`, `requests_cache`, `python-telegram-bot`, `python-dotenv`

   ```bash
   pip install supabase requests requests_cache python-telegram-bot python-dotenv
   ```

## Usage

1. **Clone the repository:**

    ```bash
    git clone https://github.com/ndzuma/morningMessenger.git
    cd morningMessenger
    ```

2. **Edit the existing .env file:**

   Open the `.env` file in a text editor and update the following variables with your own values:

   ```env
   TELEGRAM_API_TOKEN=your_token
   TELEGRAM_CHAT_ID=your_chat_id1,your_chat_id2,your_chat_id3,...
   SUPABASE_URL=your_url
   SUPABASE_API_KEY=your_key
   OPEN_WEATHER_API_KEY=your_key
   ALPHA_VANTAGE_API_KEY=your_key
   USERS_NAME=some_name1,some_name2,some_name3,...
   TICKERS=your_tickers1,your_tickers2,your_tickers3,...
   ```
   ### Multiple TICKERS Values:

   You can add multiple TICKERS values in the `.env` file separated by a comma(without spaces), e.g., `TICKERS=voo,tsla,aapl,brk.b`.

   ### Chat ID and Username Priority

   When specifying both chat IDs and usernames, priority is given to chat IDs. Here's how it works:

   - **Scenario 1: More Chat IDs than Users**
      If you provide 5 chat IDs and 10 usernames, only the first 5 chat IDs will be utilized.

   - **Scenario 2: Equal Chat IDs and Users**
   When inputting 5 different chat IDs and 5 usernames, they will be matched accordingly.

   - **Scenario 3: Fewer Users than Chat IDs**
    In cases where you have fewer users than chat IDs, the first specified username will be used for all 5 chat IDs.

   This ensures a systematic and predictable approach to handling both chat IDs and usernames.


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

