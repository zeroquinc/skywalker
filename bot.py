import discord
from discord.ext import commands

from utils.logger import logger

class DiscordBot:
    def __init__(self, token):
        intents = discord.Intents.default()
        intents.message_content = True

        self.token = token
        self.bot = commands.Bot(
            command_prefix="!",
            intents=intents,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="127.0.0.1"
            )
        )

        # Register event listeners properly
        self.bot.add_listener(self.on_ready, 'on_ready')

    ## Start the bot
    def run(self):
        try:
            self.bot.run(self.token)
        except Exception as e:
            logger.error(f"Error running the bot: {e}")

    ## Event listener for when the bot is ready
    async def on_ready(self):
        await self.bot.wait_until_ready()
        logger.info(
            f'Logged in as {self.bot.user.name} ({self.bot.user.id}) and is ready!'
        )

    ## Post a single embed to a channel
    async def dispatch_embed(self, channel_id, embed):
        try:
            # fetch_channel is more reliable than get_channel
            channel = await self.bot.fetch_channel(channel_id)
            await channel.send(embed=embed)
            logger.info(f"Embed dispatched with title: {getattr(embed, 'title', 'No Title')}")
        except discord.NotFound:
            logger.error(f"Channel {channel_id} not found")
        except Exception as e:
            logger.error(f"Error dispatching embed: {e}")


class EmbedBuilder:
    def __init__(self, title='', description='', color=discord.Color.default(), url=''):
        self.embed = discord.Embed(title=title, description=description, color=color, url=url)

    def set_author(self, name, icon_url=None, url=None):
        self.embed.set_author(name=name, icon_url=icon_url, url=url)
        return self

    def add_field(self, name, value, inline=True):
        self.embed.add_field(name=name, value=value, inline=inline)
        return self

    def set_footer(self, text, icon_url=None):
        self.embed.set_footer(text=text, icon_url=icon_url)
        return self
    
    def set_thumbnail(self, url):
        self.embed.set_thumbnail(url=url)
        return self
    
    def set_image(self, url):
        self.embed.set_image(url=url)
        return self

    def build(self):
        return self.embed
    
    async def send_embed(self, channel):
        # Send the embed to the specified channel
        await channel.send(embed=self.build())