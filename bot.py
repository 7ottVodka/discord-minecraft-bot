import discord
import os
from discord import app_commands

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# Emojis
EMOJIS = {
    "map": "🗺️ Map",
    "resource": "🔗 Resource Pack", 
    "mod": "📦 Mod",
    "skin": "🦎 Skin",
    "mashup": "🌈 Mash-Up"
}

@bot.event
async def on_ready():
    print(f'✅ Bot is online!')
    try:
        await tree.sync()
        print("✅ Commands ready!")
    except:
        pass
    
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Mod Requests"
        )
    )

# 🎯 COMMAND 1: REQUEST
@tree.command(name="request", description="Request Minecraft content")
@app_commands.describe(
    type="Choose type",
    name="What you want",
    link="Link (optional)"
)
@app_commands.choices(type=[
    app_commands.Choice(name="🗺️ Map", value="map"),
    app_commands.Choice(name="🔗 Resource Pack", value="resource"),
    app_commands.Choice(name="📦 Mod", value="mod"),
    app_commands.Choice(name="🦎 Skin", value="skin"),
    app_commands.Choice(name="🌈 Mash-Up", value="mashup")
])
async def request_cmd(interaction: discord.Interaction, 
                     type: app_commands.Choice[str], 
                     name: str,
                     link: str = ""):
    
    # Send message with user mention
    await interaction.response.send_message(
        f"✅ REQUEST SUBMITTED!\n\n"
        f"Content: {name}\n"
        f"Type: {type.name}\n"
        f"Link: {link if link else 'No link'}\n\n"
        f"Requested by: {interaction.user.mention}\n"
        f"⏳ You will be mentioned (@) when ready!"
    )

# 🎯 COMMAND 2: FULFILL (ADMIN)
@tree.command(name="fulfill", description="Complete a request - MENTIONS USER")
@app_commands.describe(
    user="Mention the user (@username)",
    content="Name of mod/map",
    link="Download link",
    image="Image URL (optional)"
)
async def fulfill_cmd(interaction: discord.Interaction,
                     user: discord.User,
                     content: str,
                     link: str,
                     image: str = ""):
    
    # Check if admin
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("❌ Only admins can use this!", ephemeral=True)
        return
    
    # 🎯 THIS MENTIONS THE USER!
    await interaction.response.send_message(
        f"📢 {user.mention} YOUR REQUEST IS READY!\n\n"
        f"{content}\n"
        f"Download: {link}\n\n"
        f"✅ Added by: {interaction.user.mention}"
    )
    
    # Try to DM user too
    try:
        await user.send(
            f"🎉 YOUR REQUEST IS READY!\n\n"
            f"{content}\n"
            f"Download: {link}\n\n"
            f"Request fulfilled by: {interaction.user.mention}"
        )
    except:
        pass

# Start bot
TOKEN = os.getenv("TOKEN")
if TOKEN:
    print("🚀 Starting bot...")
    bot.run(TOKEN)
else:
    print("❌ ERROR: Add TOKEN in Railway Variables!")
