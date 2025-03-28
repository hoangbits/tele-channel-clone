

## Prerequisites

- Python 3.7+
- A Telegram account and API credentials (API ID, API Hash).
- Source and Destination Channel IDs.

## Setup

1. Clone this repository.
   ```bash
   git clone https://github.com/yourusername/telegram-forward-bot.git
   cd telegram-forward-bot
   ```

2. Install dependencies.
   ```bash
   pip install -r requirements.txt
   ```

3. Edit the `.env` file with your API credentials and channel information.
   ```plaintext
   API_ID=YOUR_API_ID
   API_HASH=YOUR_API_HASH
   PHONE_NUMBER=YOUR_PHONE_NUMBER
   SOURCE_CHANNEL=SOURCE_CHANNEL_ID
   DESTINATION_CHANNEL=DESTINATION_CHANNEL_ID
   ```

## Running the Bot

Run the bot with:
```bash
python main.py
```

The bot will automatically fetch messages from the source channel and forward them to the destination channel with progress tracking. If interrupted, it will resume from the last forwarded message.
