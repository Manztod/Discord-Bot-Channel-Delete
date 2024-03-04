from discord.ext import commands
import discord
import logging
from colorama import Fore, Style
import random

class ColoredFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.colors = {
            'DEBUG':    Fore.CYAN,
            'INFO':     [Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN],
            'WARNING':  Fore.YELLOW,
            'ERROR':    Fore.RED,
            'CRITICAL': Fore.RED,
        }

    def format(self, record):
        if record.levelname == 'INFO':
            color = random.choice(self.colors[record.levelname])
            emoji = "💡"
        elif record.levelname == 'WARNING':
            color = self.colors[record.levelname]
            emoji = "⚠️"
        elif record.levelname == 'ERROR':
            color = self.colors[record.levelname]
            emoji = "❌"
        elif record.levelname == 'CRITICAL':
            color = self.colors[record.levelname]
            emoji = "🚨"
        else:
            color = Fore.WHITE
            emoji = "📝"

        record.msg = f"{emoji} {color}[{record.levelname}] {record.module} - {record.msg}{Style.RESET_ALL}"
        return super().format(record)

log = logging.getLogger('discord')
log.setLevel(logging.ERROR)
handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter("%(message)s"))
log.addHandler(handler)

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix = 'for example: !?', intents=intents)

@client.event
async def on_ready():
    guild = None
    while guild is None:
        guild_id = input("Masukkan ID guild Anda: ")
        guild = client.get_guild(int(guild_id))
        if guild is None:
            log.error(f"Gagal mendapatkan guild dengan ID {guild_id}")

    for channel in guild.channels:
        try:
            await channel.delete()
            log.info(f"Channel dihapus: {channel.name} di guild: {guild.name}")
        except Exception as e:
            log.error(f"Gagal menghapus channel: {channel.name} di guild: {guild.name}. Error: {e}")

    new_channel = await guild.create_text_channel('berhasil terhapus')
    embed = discord.Embed(title="Selesai, semua channel sudah dihapus", color=0x00ff00)
    await new_channel.send(embed=embed)

    await client.close()  # Close the bot

try:
    client.run("TOKEN_BOT")
except discord.errors.LoginFailure:
    log.error("Gagal login, silakan periksa token bot Anda.")
