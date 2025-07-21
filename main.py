import asyncio

from webhook import HandleWebHook
from bot import DiscordBot

from config import DISCORD_TOKEN
from utils.logger import logger

async def main():
    discord_bot = DiscordBot(DISCORD_TOKEN)
    webhook = HandleWebHook(discord_bot)

    await asyncio.gather(
        webhook.start(),
        discord_bot.start()
    )

    await webhook.cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by keyboard interrupt.")