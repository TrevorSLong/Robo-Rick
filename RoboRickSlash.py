#!/usr/bin/env python3
# Robo Rick - Modern Discord.py 2.x Version
# -------------------------------------------------
# Discord bot for welcome messages, leave messages, kicking, banning, announcements, and more
# Created by DroTron (Trevor L)
# https://github.com/TrevorSLong/Robo-Rick
# -------------------------------------------------
# Updated to discord.py 2.x with native slash commands
# -------------------------------------------------

import discord
from discord import app_commands
from discord.ext import commands, tasks
import os
import asyncio
import logging
import random
import json
from dotenv import load_dotenv

# Optional Top.gg integration
try:
    import topgg
    TOPGG_AVAILABLE = True
except ImportError:
    TOPGG_AVAILABLE = False

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BOT_UPDATE_CHANNEL = os.getenv('BOT_UPDATE_CHANNEL')
dbl_token = os.getenv('dbl_token')

print(f"Logging in with Bot Token {TOKEN[:20]}..." if TOKEN else "ERROR: No DISCORD_TOKEN found!")
print(f"Robo Rick sends reconnect updates to {BOT_UPDATE_CHANNEL}")
if dbl_token:
    print(f"Using DBL Token {dbl_token[:10]}...")

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('bot')

# Bot setup with intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)


# ============================================================================
# Top.gg Integration (optional)
# ============================================================================
class TopGG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if TOPGG_AVAILABLE and dbl_token:
            self.topgg_client = topgg.DBLClient(self.bot, dbl_token)
            self.update_stats.start()
        else:
            self.topgg_client = None
            logger.info("Top.gg integration disabled (no token or package not installed)")

    def cog_unload(self):
        if hasattr(self, 'update_stats'):
            self.update_stats.cancel()

    @tasks.loop(minutes=30)
    async def update_stats(self):
        await self.bot.wait_until_ready()
        if self.topgg_client:
            try:
                await self.topgg_client.post_guild_count()
                logger.info(f'Posted server count ({len(self.bot.guilds)})')
            except Exception as e:
                logger.warning(f'Failed to post server count: {type(e).__name__}: {e}')


# ============================================================================
# Helper Functions
# ============================================================================
def load_json(filename):
    """Load JSON file, return empty dict if file doesn't exist or is invalid."""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_json(filename, data):
    """Save data to JSON file."""
    with open(filename, "w") as f:
        json.dump(data, f)


# ============================================================================
# Events
# ============================================================================
@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')

    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        logger.info(f'Synced {len(synced)} command(s)')
    except Exception as e:
        logger.error(f'Failed to sync commands: {e}')

    # Set status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Interdimensional Cable"
        )
    )

    # Send restart notification
    if BOT_UPDATE_CHANNEL:
        try:
            channel = bot.get_channel(int(BOT_UPDATE_CHANNEL))
            if channel:
                await channel.send('Robo Rick has restarted and has successfully reconnected to Discord!')
        except Exception as e:
            logger.warning(f'Could not send restart notification: {e}')

    # Add TopGG cog
    await bot.add_cog(TopGG(bot))


@bot.event
async def on_guild_join(guild):
    """Set up default channels when bot joins a server."""
    # Set default update channel
    welcome_channels = load_json("welcomechannels.json")
    welcome_channels[str(guild.id)] = guild.text_channels[0].id
    save_json("welcomechannels.json", welcome_channels)

    # Set default admin channel
    admin_channels = load_json("adminchannels.json")
    admin_channels[str(guild.id)] = guild.text_channels[0].id
    save_json("adminchannels.json", admin_channels)

    # Send join message
    channel = guild.text_channels[0]
    embed = discord.Embed(
        colour=discord.Colour(0x788dee),
        description=f"I turned myself into a Discord bot, **{guild}**! Boom! Big reveal: I'm a Discord bot. What do you think about that? I turned myself into a Discord bot! W-what are you just staring at me for, bro. I turned myself into a Discord bot, **{guild}**!"
    )
    embed.set_thumbnail(url="https://raw.githubusercontent.com/TrevorSLong/Robo-Rick/main/Screenshots/rick.jpg")
    embed.set_author(
        name="Robo Rick",
        url="https://top.gg/bot/827681932660965377",
        icon_url="https://raw.githubusercontent.com/TrevorSLong/Robo-Rick/main/Screenshots/rick.jpg"
    )
    embed.add_field(
        name="Well since I have to be here....",
        value="I guess I'll give you the run down on my basic functions",
        inline=False
    )
    embed.add_field(
        name="Basic commands:",
        value="• Use ``/updatechannel`` to set where updates go\n• Use ``/adminchannel`` to set where admin updates go\n• Use ``/help`` or ``$help`` for all commands",
        inline=False
    )
    embed.add_field(
        name="Help support my growth",
        value="I was made by two full time students, if you enjoy having me around please consider **supporting my development** by contributing code to me [here](https://github.com/TrevorSLong/Robo-Rick) or **donating** to help fund development and hosting costs [here](https://www.paypal.com/donate?hosted_button_id=RBYUJ5M6QSB52)",
        inline=False
    )
    await channel.send(embed=embed)


@bot.event
async def on_member_join(member):
    """Send welcome message when member joins."""
    # Send DM to new member
    try:
        embed = discord.Embed(
            colour=discord.Colour(0x788dee),
            description=f"I turned myself into a Discord bot, **{member.name}**! Boom! Big reveal: I'm a Discord bot. What do you think about that? I turned myself into a Discord bot! W-what are you just staring at me for, bro. I turned myself into a Discord bot, **{member.name}**!"
        )
        embed.set_thumbnail(url="https://raw.githubusercontent.com/TrevorSLong/Robo-Rick/main/Screenshots/rick.jpg")
        embed.set_author(
            name="Robo Rick",
            url="https://top.gg/bot/827681932660965377",
            icon_url="https://raw.githubusercontent.com/TrevorSLong/Robo-Rick/main/Screenshots/rick.jpg"
        )
        embed.add_field(
            name=f"Every Morty needs a Rick, and every **{member.guild}** needs a Robo Rick:",
            value=f"Welcome to **{member.guild}**, I'm Robo Rick, one of the moderation bots here. Please read through the servers specific rules and agree to them to start chatting.",
            inline=False
        )
        embed.add_field(
            name="A few notes:",
            value="• Use ``/help`` to get a full list of my features\n• This message is not editable by the server you're joining, please be sure to read their rules and welcome page.",
            inline=False
        )
        await member.send(embed=embed)
    except discord.Forbidden:
        logger.info(f"Could not DM {member.name} - DMs disabled")

    # Send welcome message in update channel
    welcome_channels = load_json("welcomechannels.json")
    channel_id = welcome_channels.get(str(member.guild.id))
    if channel_id:
        channel = bot.get_channel(int(channel_id))
        if channel:
            welcomemessages = [
                f'➡️ Boom! Big reveal! I turned myself into a pickle, **{member.name}**! I\'m Pickle Rick!',
                f'➡️ Ill tell you how I feel about school, **{member.name}**: Its a waste of time.',
                f'➡️ You gotta do it for Grandpa, **{member.name}**. You gotta put these seeds inside your butt.',
                f'➡️ Nobody exists on purpose. Nobody belongs anywhere. Everybodys gonna die. Come watch TV **{member.name}**.',
                f'➡️ SHOW ME WHAT YOU GOT **{member.name}**!',
                f'➡️ **{member.name}**, I need your help on an adventure. Eh, need is a strong word. We need door stops, but a brick would work too.',
                f'➡️ What about the reality where Hitler cured cancer, **{member.name}**? The answer is: Dont think about it.',
                f'➡️ Hey, **{member.name}**, does your planet have wiper fluid yet or you gonna freak out and start worshipping us?',
                f'➡️ Listen, **{member.name}**, I hate to break it to you, but what people call "love" is just a chemical reaction that compels animals to breed.',
                f'➡️ You\'re missing the point, **{member.name}**. Why would he drive a smaller toaster with wheels?',
                f'➡️ Don\'t get drawn into the culture, **{member.name}**. Stealing stuff is about the stuff, not the stealing.',
                f'➡️ Yeah, sure, I mean, if you spend all day shuffling words around, you can make anything sound bad, **{member.name}**.',
                f'➡️ Get Out Of Here, **{member.name}**! You Ruined The Season 4 Premiere!',
                f"➡️ Now if you'll excuse me, I've got a quick solo adventure to go on and this one will not be directed by **{member.name}**.",
            ]
            await channel.send(random.choice(welcomemessages))

    # Send admin notification
    admin_channels = load_json("adminchannels.json")
    admin_channel_id = admin_channels.get(str(member.guild.id))
    if admin_channel_id:
        admin_channel = bot.get_channel(int(admin_channel_id))
        if admin_channel:
            await admin_channel.send(f'Robo Rick successfully sent welcome message about **{member.name}** joining **{member.guild}**.')


@bot.event
async def on_member_remove(member):
    """Send leave message when member leaves."""
    welcome_channels = load_json("welcomechannels.json")
    channel_id = welcome_channels.get(str(member.guild.id))
    if channel_id:
        channel = bot.get_channel(int(channel_id))
        if channel:
            await channel.send(f'Looks like **{member.name}** decided to leave, good riddance.')

    admin_channels = load_json("adminchannels.json")
    admin_channel_id = admin_channels.get(str(member.guild.id))
    if admin_channel_id:
        admin_channel = bot.get_channel(int(admin_channel_id))
        if admin_channel:
            await admin_channel.send(f'Robo Rick sent leave message about **{member.name}** leaving **{member.guild}**.')


@bot.event
async def on_message(message):
    """Respond to 'rick' messages."""
    if message.author == bot.user:
        return
    if message.content.lower() == "rick":
        await message.channel.send("Wubbalubbadubdub")
    await bot.process_commands(message)


# ============================================================================
# Slash Commands
# ============================================================================
@bot.tree.command(name="ping", description="Responds with Pong and the bot's server latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'🏓 Pong! {round(bot.latency * 1000)}ms')


@bot.tree.command(name="donate", description="Information on how to donate towards Robo Rick's development")
async def donate(interaction: discord.Interaction):
    embed = discord.Embed(
        colour=discord.Colour(0x788dee),
        description=f"Hello **{interaction.user}**, I'm glad someone finally appreciates my genius! Thank you for your interest in donating!"
    )
    embed.set_thumbnail(url="https://raw.githubusercontent.com/TrevorSLong/Robo-Rick/main/Screenshots/DonateQRCode.png")
    embed.set_author(
        name="Robo Rick",
        url="https://top.gg/bot/827681932660965377",
        icon_url="https://raw.githubusercontent.com/TrevorSLong/Robo-Rick/main/Screenshots/rick.jpg"
    )
    embed.add_field(
        name="Help support my growth",
        value="I was made by two full time students. Consider **supporting my development** [here](https://github.com/TrevorSLong/Robo-Rick) or **donating** [here](https://www.paypal.com/donate?hosted_button_id=RBYUJ5M6QSB52)"
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="servercount", description="Lists the number of servers Robo Rick is active in")
async def servercount(interaction: discord.Interaction):
    await interaction.response.send_message(f"I'm currently active in {len(bot.guilds)} servers!")


@bot.tree.command(name="announce", description="Sends an announcement to a channel")
@app_commands.describe(
    message="The message you want to send",
    channel="The channel to send the announcement to"
)
@app_commands.checks.has_permissions(manage_guild=True)
async def announce(interaction: discord.Interaction, message: str, channel: discord.TextChannel):
    embed = discord.Embed(title="Announcement", description=message, color=0x9208ea)
    embed.set_footer(text=f'-{interaction.user} and the {interaction.guild} Admin team')
    await channel.send(embed=embed)
    await interaction.response.send_message(f"Announcement sent to {channel.mention}!", ephemeral=True)


@bot.tree.command(name="kick", description="Kicks a member from the server")
@app_commands.describe(
    member="The member to kick",
    reason="The reason for kicking"
)
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str):
    admin_channels = load_json("adminchannels.json")
    admin_channel_id = admin_channels.get(str(interaction.guild_id))

    try:
        await member.send(f'Hello **{member}**, you have been kicked from **{interaction.guild}** for **{reason}**. Please contact the server Admins for questions.')
    except discord.Forbidden:
        pass

    await member.kick(reason=reason)
    await interaction.response.send_message(f"Success! {member} has been kicked from {interaction.guild}!")

    if admin_channel_id:
        admin_channel = bot.get_channel(int(admin_channel_id))
        if admin_channel:
            await admin_channel.send(f"**{member}** has been kicked for **{reason}** by **{interaction.user}**.")


@bot.tree.command(name="ban", description="Bans a member from the server")
@app_commands.describe(
    member="The member to ban",
    reason="The reason for banning"
)
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str):
    admin_channels = load_json("adminchannels.json")
    admin_channel_id = admin_channels.get(str(interaction.guild_id))

    try:
        await member.send(f'Hello **{member}**, you have been banned from **{interaction.guild}** for **{reason}**. Please contact the server Admins for questions.')
    except discord.Forbidden:
        pass

    await member.ban(reason=reason)
    await interaction.response.send_message(f"Success! Banned {member} for {reason}!")

    if admin_channel_id:
        admin_channel = bot.get_channel(int(admin_channel_id))
        if admin_channel:
            await admin_channel.send(f"**{member}** has been banned for **{reason}** by **{interaction.user}**.")


@bot.tree.command(name="unban", description="Unbans a user from the server")
@app_commands.describe(member="The user to unban (format: username#1234 or just username)")
@app_commands.checks.has_permissions(ban_members=True)
async def unban(interaction: discord.Interaction, member: str):
    admin_channels = load_json("adminchannels.json")
    admin_channel_id = admin_channels.get(str(interaction.guild_id))

    # Handle both username#discriminator and just username (new Discord format)
    if '#' in member:
        member_name, member_discriminator = member.split('#')
    else:
        member_name = member
        member_discriminator = '0'  # New Discord usernames have no discriminator

    async for ban_entry in interaction.guild.bans():
        user = ban_entry.user
        if user.name == member_name and (member_discriminator == '0' or user.discriminator == member_discriminator):
            await interaction.guild.unban(user)
            await interaction.response.send_message(f"{user} successfully unbanned!")

            if admin_channel_id:
                admin_channel = bot.get_channel(int(admin_channel_id))
                if admin_channel:
                    await admin_channel.send(f"**{user}** has been unbanned by **{interaction.user}**.")

            try:
                await user.send(f'Hello **{user}**, you have been unbanned from **{interaction.guild}**.')
            except discord.Forbidden:
                pass
            return

    await interaction.response.send_message(f"Could not find banned user: {member}", ephemeral=True)


@bot.tree.command(name="tempban", description="Temporarily bans a member for a specified number of days")
@app_commands.describe(
    member="The member to temporarily ban",
    reason="The reason for the ban",
    duration="Number of days to ban"
)
@app_commands.checks.has_permissions(ban_members=True)
async def tempban(interaction: discord.Interaction, member: discord.Member, reason: str, duration: int):
    admin_channels = load_json("adminchannels.json")
    admin_channel_id = admin_channels.get(str(interaction.guild_id))

    try:
        await member.send(f'Hello **{member}**, you have been banned from **{interaction.guild}** for **{reason}** for **{duration}** days.')
    except discord.Forbidden:
        pass

    await member.ban(reason=reason)
    await interaction.response.send_message(f"Success! You have banned {member} for {duration} days!")

    if admin_channel_id:
        admin_channel = bot.get_channel(int(admin_channel_id))
        if admin_channel:
            await admin_channel.send(f"**{member}** has been banned for **{reason}** by **{interaction.user}** for **{duration}** days.")

    # Schedule unban
    await asyncio.sleep(duration * 60 * 60 * 24)

    try:
        await interaction.guild.unban(member)
        if admin_channel_id:
            admin_channel = bot.get_channel(int(admin_channel_id))
            if admin_channel:
                await admin_channel.send(f"**{member}** has been unbanned after **{duration}** days.")
        try:
            await member.send(f'Hello **{member}**, you have been unbanned from **{interaction.guild}** after **{duration}** days.')
        except discord.Forbidden:
            pass
    except Exception as e:
        logger.error(f"Failed to unban {member}: {e}")


@bot.tree.command(name="updatechannel", description="Sets the channel for public announcements and welcome messages")
@app_commands.describe(channel="The channel for updates")
@app_commands.checks.has_permissions(manage_guild=True)
async def updatechannel(interaction: discord.Interaction, channel: discord.TextChannel):
    welcome_channels = load_json("welcomechannels.json")
    welcome_channels[str(interaction.guild_id)] = channel.id
    save_json("welcomechannels.json", welcome_channels)
    await interaction.response.send_message(f'You have successfully changed the update channel to **{channel.mention}**!')


@bot.tree.command(name="checkupdatechannel", description="Shows the current update channel")
@app_commands.checks.has_permissions(manage_guild=True)
async def checkupdatechannel(interaction: discord.Interaction):
    welcome_channels = load_json("welcomechannels.json")
    channel_id = welcome_channels.get(str(interaction.guild_id))
    if channel_id:
        channel = bot.get_channel(int(channel_id))
        if channel:
            await interaction.response.send_message(f'The update channel is set to **{channel.mention}**')
            return
    await interaction.response.send_message('No update channel set. Use `/updatechannel` to set one.', ephemeral=True)


@bot.tree.command(name="adminchannel", description="Sets the channel for admin notifications")
@app_commands.describe(channel="The channel for admin updates")
@app_commands.checks.has_permissions(manage_guild=True)
async def adminchannel(interaction: discord.Interaction, channel: discord.TextChannel):
    admin_channels = load_json("adminchannels.json")
    admin_channels[str(interaction.guild_id)] = channel.id
    save_json("adminchannels.json", admin_channels)
    await interaction.response.send_message(f'You have successfully changed the admin channel to **{channel.mention}**!')


@bot.tree.command(name="checkadminchannel", description="Shows the current admin channel")
@app_commands.checks.has_permissions(manage_guild=True)
async def checkadminchannel(interaction: discord.Interaction):
    admin_channels = load_json("adminchannels.json")
    channel_id = admin_channels.get(str(interaction.guild_id))
    if channel_id:
        channel = bot.get_channel(int(channel_id))
        if channel:
            await interaction.response.send_message(f'The admin channel is set to **{channel.mention}**')
            return
    await interaction.response.send_message('No admin channel set. Use `/adminchannel` to set one.', ephemeral=True)


# ============================================================================
# Error Handlers
# ============================================================================
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(
            f'Sorry **{interaction.user}**, you do not have permission to use this command.',
            ephemeral=True
        )
    else:
        logger.error(f'Command error: {error}')
        await interaction.response.send_message(
            'An error occurred while processing this command.',
            ephemeral=True
        )


# ============================================================================
# Run Bot
# ============================================================================
if __name__ == "__main__":
    if not TOKEN:
        print("ERROR: DISCORD_TOKEN not found in environment variables!")
        exit(1)
    bot.run(TOKEN)
