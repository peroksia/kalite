import discord
from discord.ext import commands
from discord import app_commands
import os

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Sync hatası: {e}")
    print(f"{bot.user} aktif!")

@bot.command()
async def sync(ctx):
    synced = await bot.tree.sync()
    await ctx.send(f"{len(synced)} komut sync edildi!")

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

@bot.tree.command(name="sahte", description="Birinin adına sahte mesaj gönderir")
@app_commands.describe(kisi="Mesajı kimin adına gönderelim?", mesaj="Ne yazsın?")
async def sahte(interaction: discord.Interaction, kisi: discord.Member, mesaj: str):
    webhooks = await interaction.channel.webhooks()
    webhook = None
    for wh in webhooks:
        if wh.name == "SahteBot":
            webhook = wh
            break
    if webhook is None:
        webhook = await interaction.channel.create_webhook(name="SahteBot")
    await interaction.response.send_message("✅ Gönderildi!", ephemeral=True)
    await webhook.send(
        content=mesaj,
        username=kisi.display_name,
        avatar_url=kisi.display_avatar.url
    )

token = os.environ.get("DISCORD_TOKEN")
if not token:
    raise ValueError("DISCORD_TOKEN bulunamadı!")
bot.run(token)
