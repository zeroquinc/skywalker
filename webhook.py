from aiohttp import web
from utils.logger import logger
from src.plex.client import PlexWebhookHandler
from config import WEBHOOKS_ENABLED

class HandleWebHook:
    # Define handlers and routes inside the class
    WEBHOOKS = {
        "plex": {"handler": PlexWebhookHandler, "route": "/plex_webhook"}
    }

    def __init__(self, discord_bot, host="0.0.0.0", port=2024):
        self.discord_bot = discord_bot
        self.host = host
        self.port = port
        self.app = web.Application()

        disabled_webhooks = []  # Track disabled webhooks

        # Register only enabled webhooks
        for name, config in self.WEBHOOKS.items():
            if WEBHOOKS_ENABLED.get(name, False):  # Check if enabled in config
                self.app.router.add_post(config["route"], self.handle_webhook(config["handler"]))
            else:
                disabled_webhooks.append(name)

        # Log disabled webhooks
        if disabled_webhooks:
            logger.warning(f"Disabled webhooks: {', '.join(disabled_webhooks)}")

        self.uvicorn_params = {
            "host": self.host,
            "port": self.port,
            "access_log": False,
        }

    def handle_webhook(self, Handler):
        async def handler(request):
            try:
                payload = await request.json()
                handler = Handler(payload, self.discord_bot)
                await handler.handle_webhook()
            except Exception as e:
                logger.error(f"Error handling webhook: {e}")
                return web.Response(text='Error', status=500)
            return web.Response(text='OK')
        return handler

    async def start(self):
        try:
            runner = web.AppRunner(self.app)
            await runner.setup()
            site = web.TCPSite(runner, self.host, self.port)
            await site.start()
            logger.info(f"Webhook server started at http://{self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Error starting the server: {e}")

    async def cleanup(self):
        await self.app.cleanup()