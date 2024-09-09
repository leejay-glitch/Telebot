import asyncio
import logging
import httpx

# Set up logging
logging.basicConfig(level=logging.INFO)

# Function to get bot information
async def get_me(token):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.telegram.org/bot{token}/getMe")
        return response.json()

# Function to get updates using long polling
async def get_updates(token, offset):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.telegram.org/bot{token}/getUpdates?offset={offset}&timeout=30")  # Set timeout for long polling
        return response.json()

# Function to send a simple message
async def send_message(token, chat_id, text):
    async with httpx.AsyncClient() as client:
        await client.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": text})

# Function to send a message with inline keyboard markup
async def send_markup(token, chat_id, text, reply_markup):
    async with httpx.AsyncClient() as client:
        await client.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": text, "reply_markup": reply_markup})

# Function to set a webhook (if needed for production)
async def set_webhook(token, webhook_url):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.telegram.org/bot{token}/setWebhook?url={webhook_url}")
        return response.json()

# Main function
async def main():
    token = "7018715312:AAHD1pRhzTiPjhiQIABHZvi49sWR516nFzs"  # Replace with your actual token
    webhook_url = "YOUR_WEBHOOK_URL"  # Replace with your public server URL (if using webhooks)
    
    # Uncomment the line below to use webhook instead of long polling
    # webhook = await set_webhook(token, webhook_url)
    
    me = await get_me(token)
    if not me.get("ok"):
        logging.error("Could not retrieve bot info. Exiting...")
        return

    logging.info(me)

    offset = 0  # Start with offset 0
    links = [
        {"text": "Tomarket🍅", "url": "https://t.me/Tomarket_ai_bot/app?startapp=0000Js6g"},
        {"text": "Cats🐈‍", "url": "https://t.me/catsgang_bot/join?startapp=2gu-FdJwLKo70MSt7X7rI"},
        {"text": "Hamster kombat🐹", "url": "https://t.me/hamster_komBat_bot/start?startapp=kentId1129557053"},
        {"text": "bluefarming", "url": "https://t.me/bluefarming_bot/play?startapp=71355532"},
        {"text": "pigs🐷📈", "url": "https://t.me/PigshouseBot?start=1129557053"},
        {"text": "BLUM", "url": "https://t.me/blum/app?startapp=ref_hJa6wU04a1"},
        {"text": "MONEKY🙉", "url": "https://t.me/monkeycost_bot/app?startapp=r_1129557053"},
        {"text": "MAJOR⭐️", "url": "https://t.me/major/start?startapp=1129557053"},
        {"text": "AGENT 301", "url": "https://t.me/Agent301Bot/app?startapp=onetime1129557053"},
        {"text": "ROCKY RABBIT🐰", "url": "https://t.me/rocky_rabbit_bot/play?startapp=frId1129557053"},
        {"text": "X EMPIRE🤘❤️‍🔥", "url": "https://t.me/empirebot/game?startapp=hero1129557053"},
        {"text": "BYIN🖼 ", "url": "https://t.me/BYIN_official_bot/BYIN?startapp=dB1MDL9A"}
    ]

    bot_active = False  # Flag to track bot state

    while True:
        updates = await get_updates(token, offset)
        logging.info(f"Current offset: {offset}")
        
        if updates.get("ok"):
            for update in updates.get("result", []):
                # Only process new updates
                if update["update_id"] > offset:
                    offset = update["update_id"] + 1  # Update offset to the last processed update
                    if "message" in update:
                        chat_id = update["message"]["chat"]["id"]
                        text = update.get("message", {}).get("text")

                        logging.info(f"Received command: {text}")

                        if text == "/start":
                            bot_active = True  # Activate the bot
                            markup = {
                                "inline_keyboard": [[{"text": link["text"], "url": link["url"]}] for link in links]
                            }
                            await send_markup(token, chat_id, "Click on all the links below:", markup)
                        elif text == "/end" and bot_active:
                            await send_message(token, chat_id, "Bot is shutting down. Goodbye!")
                            logging.info("Bot is shutting down.")
                            return  # Exit the main loop
                        elif text == "/exit" and bot_active:
                            await send_message(token, chat_id, "Are you sure you want to exit? Type /end to confirm.")
                        else:
                            if not bot_active:
                                await send_message(token, chat_id, "Please start the bot with /start before sending other commands.")
                            else:
                                logging.info("Unrecognized command. Bot will continue running.")
        else:
            logging.warning("Received error response from getUpdates, retrying in 5 seconds...")

        await asyncio.sleep(5)  # Adjust the polling delay to 5 seconds

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except Exception as e:
        logging.error("Error occurred: %s", e)
