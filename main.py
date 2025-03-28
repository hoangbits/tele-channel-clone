


from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
import asyncio
import logging

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Replace these with your own values
api_id = os.getenv("API_ID")  # Your API ID from my.telegram.org
api_hash = os.getenv("API_HASH")  # Your API Hash from my.telegram.org
phone = os.getenv("PHONE_NUMBER")  # Your phone number
source_channel = int(os.getenv("SOURCE_CHANNEL"))  # Source channel ID
target_channel = int(os.getenv("DESTINATION_CHANNEL"))  # Target channel ID

# Initialize the client
client = TelegramClient('session_name', api_id, api_hash)

# Event handler for new messages (real-time forwarding)
@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    if event.message:
        try:
            await client.send_message(target_channel, event.message)
            logger.info(f"Forwarded message {event.message.id} in real-time")
            await asyncio.sleep(1)  # 1-second delay to avoid rate limits
        except FloodWaitError as e:
            logger.warning(f"Rate limit hit, waiting {e.seconds} seconds")
            await asyncio.sleep(e.seconds)  # Wait the required time
            await client.send_message(target_channel, event.message)  # Retry
        except Exception as e:
            logger.error(f"Error forwarding message: {e}")

# Function to copy all past messages with rate limit handling
async def copy_all_messages():
    try:
        # Get the total message count first
        messages = await client.get_messages(source_channel, limit=1)  # Fetch one to get total
        total_count = messages.total
        logger.info(f"Total messages to copy: {total_count}")

        # Fetch and iterate over messages
        async for message in client.iter_messages(source_channel, limit=None, reverse=True):
            try:
                await client.send_message(target_channel, message)
                logger.info(f"Copied message {message.id}")
                await asyncio.sleep(1)  # 1-second delay between sends
            except FloodWaitError as e:
                logger.warning(f"Rate limit hit, waiting {e.seconds} seconds")
                await asyncio.sleep(e.seconds)  # Wait the required time
                await client.send_message(target_channel, message)  # Retry
            except Exception as e:
                logger.error(f"Error copying message {message.id}: {e}")
                await asyncio.sleep(1)  # Brief pause before continuing
    except Exception as e:
        logger.error(f"Error in copy_all_messages: {e}")

# Main function to run everything
async def main():
    await client.start(phone)
    logger.info("Bot started")
    
    # Copy all past messages
    logger.info("Starting to copy past messages...")
    await copy_all_messages()
    
    # Switch to real-time forwarding
    logger.info("Finished copying past messages. Now listening for new messages...")
    await client.run_until_disconnected()

# Run the bot
if __name__ == '__main__':
    try:
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")