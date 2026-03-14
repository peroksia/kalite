import discord
from discord.ext import commands
from discord import app_commands
import os

intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} aktif!")

@bot.tree.command(name="join", description="Botu ses kanalına çeker")
async def join(interaction: discord.Interaction):
    if interaction.user.voice is None:
        await interaction.response.send_message("Önce bir ses kanalına gir!", ephemeral=True)
        return
    channel = interaction.user.voice.channel
    await channel.connect()
    await interaction.response.send_message(f"✅ **{channel.name}** kanalına katıldım!")

@bot.tree.command(name="leave", description="Botu ses kanalından çıkarır")
async def leave(interaction: discord.Interaction):
    if interaction.guild.voice_client is None:
        await interaction.response.send_message("Zaten bir kanalda değilim!", ephemeral=True)
        return
    await interaction.guild.voice_client.disconnect()
    await interaction.response.send_message("👋 Kanaldan ayrıldım!")

bot.run(os.environ["DISCORD_TOKEN"])
