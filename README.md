# Twitter Scheduler Bot

This is a Python-based Twitter Scheduler Bot that allows users to schedule tweets at specific times, with optional recurring intervals (e.g., daily, weekly, or monthly). The bot includes a graphical user interface (GUI) built with Tkinter, making it easy to set up tweet schedules with image attachments and timezone adjustments.

## Features
- **Tweet Scheduling**: Schedule tweets for specific dates and times.
- **Recurring Tweets**: Set recurring tweets on daily, weekly, or monthly intervals.
- **Media Attachments**: Attach images to your scheduled tweets.
- **Timezone Support**: Automatically set the timezone based on ZIP code.
- **User-Friendly GUI**: Easy-to-use graphical interface to configure tweet settings.
![image](https://github.com/user-attachments/assets/cea2d478-2407-4815-9f3b-77a8b65c8bd9)

## Prerequisites
- **Python 3.6+**
- **Twitter Developer Account**: You'll need Twitter API credentials to use this bot.

 **Set up your environment variables**:
   Create a `.env` file in the project directory with the following content:
   ```
   CONSUMER_KEY=your_consumer_key
   CONSUMER_SECRET=your_consumer_secret
   ACCESS_TOKEN=your_access_token
   ACCESS_TOKEN_SECRET=your_access_token_secret
   ```
   Replace `your_consumer_key`, `your_consumer_secret`, `your_access_token`, and `your_access_token_secret` with your Twitter API credentials.

## Usage

1. **Run the application**:
   ```bash
   python main.py
   ```

2. **Using the GUI**:
   - Enter a **ZIP code** (optional) to automatically set the timezone.
   - Select the **date** and **time** for your tweet.
   - Choose a **time zone** if not using the ZIP code option.
   - **Type your message** in the text area.
   - **Select an image** (optional) to attach to the tweet.
   - **Set an interval** if you want the tweet to recur (e.g., daily, weekly).
   - Click **"Schedule Tweet"** to set the tweet.

## Environment Variables

Make sure to set the following environment variables in a `.env` file:

| Variable Name           | Description                            |
|-------------------------|----------------------------------------|
| `CONSUMER_KEY`          | Twitter API consumer key              |
| `CONSUMER_SECRET`       | Twitter API consumer secret           |
| `ACCESS_TOKEN`          | Twitter API access token              |
| `ACCESS_TOKEN_SECRET`   | Twitter API access token secret       |

## File Structure

- `main.py`: The main script containing the GUI and tweet scheduling functionality.
- `.env`: (Not included in the repository) The file storing environment variables for API credentials.

## Requirements

Add the following packages to your `requirements.txt`:
```
tweepy
requests
pytz
timezonefinder
schedule
python-dotenv
tkinter
tkcalendar
Pillow
matplotlib
```

## Contributing
Feel free to submit issues and pull requests to improve the functionality, interface, or documentation of this bot.
