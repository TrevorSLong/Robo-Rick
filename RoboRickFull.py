#!/usr/bin/python3.4
#Robo Rick Slash
#-------------------------------------------------
#Discord bot for welcome messages, leave messages, kicking, banning, announcements, and more
#Created by DroTron (Trevor L)
#https://github.com/TrevorSLong/Robo-Rick
#-------------------------------------------------
#This code may be used to help you build your own bot or to run on your own server
#Do not use my code for profit
#For help go to https://realpython.com/how-to-make-a-discord-bot-python/
#https://betterprogramming.pub/how-to-make-discord-bot-commands-in-python-2cae39cbfd55
#Have fun!
#-------------------------------------------------

###########################################################################################################################
#############################################      Setup       ############################################################
###########################################################################################################################


##############Import Libraries###########################################################################################
import discord
import os
import time
import smtplib
import asyncio
import logging
import random
import json
import dbl
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord import Member
from discord import User
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext.commands import Bot, guild_only

from discord_slash import SlashCommand, SlashContext #Importing slash command library
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') #Grabs bot token from .env file
print("Logging in with Bot Token " + TOKEN)
BOT_UPDATE_CHANNEL = os.getenv('BOT_UPDATE_CHANNEL') #Grabs update channel .env file
print("Robo Rick sends reconnect updates to " + BOT_UPDATE_CHANNEL)
dbl_token = os.getenv('dbl_token') #Grabs admin channel ID from .env file
print("Using DBL Token " + dbl_token)

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all()) #declare intents for bot
slash = SlashCommand(bot, sync_commands=True) #Declares command prefix

###########################################################################################################################
#############################################      TopGG       ############################################################
###########################################################################################################################

class TopGG(commands.Cog):
    """
    This example uses tasks provided by discord.ext to create a task that posts guild count to top.gg every 30 minutes.
    """

    def __init__(self, bot):
        self.bot = bot
        self.token = dbl_token  # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token)
        self.update_stats.start()

    def cog_unload(self):
        self.update_stats.cancel()

    @tasks.loop(minutes=30)
    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count."""
        await self.bot.wait_until_ready()
        try:
            server_count = len(self.bot.guilds)
            await self.dblpy.post_guild_count(server_count)
            logger.warning('Posted server count ({})'.format(server_count))
        except Exception as e:
            logger.warning('Failed to post server count\n{}: {}'.format(type(e).__name__, e))


def setup(bot):
    bot.add_cog(TopGG(bot))


global logger
logger = logging.getLogger('bot')

setup(bot)
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

###########################################################################################################################
#############################################      Events      ############################################################
###########################################################################################################################

#############Adds server to json database on bot server join (working)##############################################################################
@bot.event
async def on_guild_join(guild):

#------------------ Set default update channel (working)------------------
    with open("welcomechannels.json", "r") as f:   #loads json file to dictionary
        guildInfo = json.load(f)

    guildInfo[guild.id] = guild.text_channels[0].id #sets key to guilds id and value to top textchannel
    
    #writes dictionary to json file
    with open("welcomechannels.json", "w") as f:
        json.dump(guildInfo, f)

#------------------ Set default admin channels (working)------------------
        
    #loads json file to dictionary
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)

    guildInfo[guild.id] = guild.text_channels[0].id #sets key to guilds id and value to top textchannel
    
    #writes dictionary to json file
    with open("adminchannels.json", "w") as f:
        json.dump(guildInfo, f)

#------------------ Sends join message (working) ------------------

    with open("welcomechannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guild.text_channels[0].id)
    embed = discord.Embed(colour=discord.Colour(0x788dee), url="https://discordapp.com", description=f" I turned myself into a Discord bot, **{guild}**! Boom! Big reveal: I'm a Discord bot. What do you think about that? I turned myself into a Discord bot! W-what are you just staring at me for, bro. I turned myself into a Discord bot, **{guild}**!")

    embed.set_thumbnail(url="https://raw.githubusercontent.com/TrevorSLong/Robo-Rick/main/Screenshots/rick.jpg")
    embed.set_author(name="Robo Rick", url="https://top.gg/bot/827681932660965377", icon_url="https://raw.githubusercontent.com/TrevorSLong/Robo-Rick/main/Screenshots/rick.jpg")

    embed.add_field(name="Well since I have to be here....", value="I guess I'll give you the run down on my basic functions",inline=False)
    embed.add_field(name="Basic commands:", value="• Type the command ``/updatechannel`` and follow the onscreen help to set the update/welcome channel. \n• Or go to the channel you want updates and messages in and type the command ``$updatechannel``\n• Type the command ``/adminchannel`` and follow the onscreen help to set the admin update channel. \n• Or go to the channel you want admin updates in and type the command ``$adminchannel``\n• Typing / will show you all of the command other bots and I offer. \n• ``$help`` will give you the rundown of all of the inventions I have to offer (legacy non-slash commands)",inline=False)
    embed.add_field(name="Help support my growth", value="I was made by two full time students, if you enjoy having me around please consider **supporting my development** by contributing code to me [here](https://github.com/TrevorSLong/Robo-Rick) or **donating** to help fund development and hosting costs [here](https://www.paypal.com/donate?hosted_button_id=RBYUJ5M6QSB52)",inline=False)

    await channel.send(embed=embed)

##############Changes bot status (working)###########################################################################################
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Interdimensional Cable"))
    channel = bot.get_channel(int(BOT_UPDATE_CHANNEL))
    await channel.send(f'Robo Rick has restarted and has successfully reconnected to Discord!')

##############Public Welcome (working)########################################################################################################
@bot.event
async def on_member_join(member):

###########Sends DM to member who joined############
    await member.create_dm()
    embed = discord.Embed(colour=discord.Colour(0x788dee), url="https://discordapp.com", description=f" I turned myself into a Discord bot, **{member.name}**! Boom! Big reveal: I'm a Discord bot. What do you think about that? I turned myself into a Discord bot! W-what are you just staring at me for, bro. I turned myself into a Discord bot, **{member.name}**!")

    embed.set_thumbnail(url="https://raw.githubusercontent.com/TrevorSLong/Robo-Rick/main/Screenshots/rick.jpg")
    embed.set_author(name="Robo Rick", url="https://top.gg/bot/827681932660965377", icon_url="https://raw.githubusercontent.com/TrevorSLong/Robo-Rick/main/Screenshots/rick.jpg")

    embed.add_field(name=f"Every Morty needs a Rick, and every **{member.guild}** needs a Robo Rick: ", value=f"Welcome to **{member.guild}**, I'm Robo Rick, one of the moderation bots here. Please read through the servers specific rules and agree to them to start chatting.",inline=False)
    embed.add_field(name="A few notes:", value="• Type / or use ``$help`` to get a full list of my featues\n• This message is not editable by the server your joining, please be sure to read their rules and welcome page to make sure you aren't missing anything. ",inline=False)
    embed.add_field(name="Help support my growth", value="I was made by two full time students, if you enjoy having me around please consider **supporting my development** by contributing code to me [here](https://github.com/DroTron/Robo-Rick) or **donating** to help fund development and hosting costs [here](https://www.paypal.com/donate?hosted_button_id=RBYUJ5M6QSB52)",inline=False)

    await member.dm_channel.send(embed=embed)

###########Sends welcome message in update channel###########
    with open("welcomechannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(member.guild.id)])

 
    welcomemessages = [
        f'➡️ Boom! Big reveal! I turned myself into a pickle, **{member.name}**! I’m Pickle Rick!',
        f'➡️ Ill tell you how I feel about school, **{member.name}**: Its a waste of time. Bunch of people runnin around bumpin into each other, got a guy up front says, 2 + 2, and the people in the back say, 4. Then the bell rings and they give you a carton of milk and a piece of paper that says you can go take a dump or somethin. I mean, its not a place for smart people, **{member.name}**. I know thats not a popular opinion, but thats my two cents on the issue.',
        f'➡️ You gotta do it for Grandpa, **{member.name}**. You gotta put these seeds inside your butt.',
        f'➡️ Nobody exists on purpose. Nobody belongs anywhere. Everybodys gonna die. Come watch TV **{member.name}**.',
        f'➡️ SHOW ME WHAT YOU GOT **{member.name}**!',
        f'➡️ **{member.name}**, I need your help on an adventure. Eh, need is a strong word. We need door stops, but a brick would work too.',
        f'➡️ What about the reality where Hitler cured cancer, **{member.name}**? The answer is: Dont think about it.',
        f'➡️ Hey, **{member.name}**, does your planet have wiper fluid yet or you gonna freak out and start worshipping us?',
        f'➡️ Listen, **{member.name}**, I hate to break it to you, but what people call “love” is just a chemical reaction that compels animals to breed. It hits hard, **{member.name}**, then it slowly fades, leaving you stranded in a failing marriage. I did it. Your parents are gonna do it. Break the cycle, **{member.name}**. Rise above. Focus on science.',
        f'➡️ You’re missing the point, **{member.name}**. Why would he drive a smaller toaster with wheels? I mean, does your car look like a smaller version of your house? No.',
        f'➡️ Don’t get drawn into the culture, **{member.name}**. Stealing stuff is about the stuff, not the stealing.',
        f'➡️ Yeah, sure, I mean, if you spend all day shuffling words around, you can make anything sound bad, **{member.name}**.',
        f'➡️ Get Out Of Here, **{member.name}**! You Ruined The Season 4 Premiere!',
        f"➡️ Now if you'll excuse me, I've got a quick solo adventure to go on and this one will not be directed by **{member.name}**.",
        ]
    randomwelcome = random.choice(welcomemessages)
    await channel.send(randomwelcome)
    
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(member.guild.id)])
    
    await channel.send(f'Robo Rick successfully sent welcome message and DM about **{member.name}** joining **{member.guild}**.')

##############Public Leave message (working)###########################################################################################
@bot.event
async def on_member_remove(member):
    
    with open("welcomechannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(member.guild.id)])
    
    await channel.send(f'Looks like **{member.name}** decided to leave, good riddance.')
    
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(member.guild.id)])
    
    await channel.send(f'Bot Rick successfully sent leave message about **{member.name}** leaving **{member.guild}**.')

##############Responds to rick (working)###########################################################################################
@bot.event
async def on_message(message):
	if message.content == "rick":
		await message.channel.send("Wubbalubbadubdub")
	await bot.process_commands(message) # INCLUDES THE COMMANDS FOR THE BOT. WITHOUT THIS LINE, YOU CANNOT TRIGGER YOUR COMMANDS.

###########################################################################################################################
#############################################Slash Commands (/)############################################################
###########################################################################################################################

##############Reponds to /ping (working)########################################################################################################
@slash.slash(
	description="Responds with Pong and the bots server latency", 	# ADDS THIS VALUE TO THE $HELP PING MESSAGE.
)
async def ping(ctx:SlashContext):
	await ctx.send(f'🏓 Pong! {round(bot.latency * 1000)}ms') # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.

##############Reponds to /donate (working)########################################################################################################
@slash.slash(
	description="Brings up information on how to donate towards Robo Ricks development", 	 
)
async def donate(ctx:SlashContext):
    embed = discord.Embed(colour=discord.Colour(0x788dee), url="https://discordapp.com", description=f" Hello **{ctx.author}**, I'm glad someone finally appreciates my genius! Thank you for your interest in donating! Your donation will help with the cost of hosting and developing me for servers like **{ctx.guild}**!")

    embed.set_thumbnail(url="https://raw.githubusercontent.com/TrevorSLong/Robo-Rick/main/Screenshots/DonateQRCode.png")
    embed.set_author(name="Robo Rick", url="https://top.gg/bot/827681932660965377", icon_url="https://raw.githubusercontent.com/TrevorSLong/Robo-Rick/main/Screenshots/rick.jpg")

    embed.add_field(name="Help support my growth", value="I was made by two full time students, if you enjoy having me around please consider **supporting my development** by contributing code to me [here](https://github.com/TrevorSLong/Robo-Rick) or **donating** to help fund development and hosting costs [here](https://www.paypal.com/donate?hosted_button_id=RBYUJ5M6QSB52)")

    await ctx.send(embed=embed)

##############Server count command (working)###########################################################################################
@slash.slash(
    description="Lists the number of servers Robo Rick is active in",
)
async def servercount(ctx:SlashContext):
    await ctx.send("I'm currently active in " + str(len(bot.guilds)) + " servers!")

##############Anouncement command (working)###########################################################################################
@slash.slash(
    description="Sends an announcement to either the updates channel or to any channel ID.",
    options=[
        create_option(
            name="message",
            description="Type the message you want to send in the announcement",
            option_type=3,
            required=True
        ),
        create_option(
            name="channelid",
            description="Optional addition of the channel the announcement will be sent to.",
            option_type=7,
            required=True,
        )
    ])
@has_permissions(manage_guild=True)
async def announce(ctx:SlashContext, message, channelid):

    embed = discord.Embed(title="Announcement",description=message,color=0x9208ea)
    embed.set_footer(text=f'-{ctx.author} and the {ctx.guild} Admin team')
    channel = channelid
    await channel.send(embed=embed)
    await ctx.send(f"Announcement sent to {channelid}!")

    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.guild_id)])
    await channel.send(f"**{ctx.author}** sent an announcement to **{channelid}**!")

@announce.error
async def announce_error(ctx, error):
    if isinstance(error, MissingPermissions):
         await ctx.send(f'Sorry **{ctx.author}**, you need the permission `Manage Server` to make announcements.')

##############Kick command (working)###########################################################################################
@slash.slash(
            description="Kicks a member of the server.",
            options=[
        create_option(
            name="member",
            description="Select the member you would like to kick",
            option_type=6,
            required=True
        ),
        create_option(
            name="reason",
            description="Please type a reason for kicking the member",
            option_type=3,
            required=True,
        )
    ])
@has_permissions(kick_members=True)
async def kick(ctx:SlashContext, member, reason):

    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.guild_id)])

    await member.send(f'Hello **{member}**, you have been kicked from **{ctx.guild}** for **{reason}**. This message has been automatically sent by Robo Rick. Please contact the server Admins of **{ctx.guild}** for questions or concerns')
    await ctx.send(f"Success! **{member}** has been kicked from **{ctx.guild}**!")
    await channel.send(f"**{member}** has been kicked for **{reason}** by **{ctx.author}**.")
    await member.kick(reason=reason)

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.author}**, you do not have permission to kick members.')

##############Ban command (working)###########################################################################################
@slash.slash(
            description="Bans a member of the server.",
            options=[
        create_option(
            name="member",
            description="Select the member you would like to ban",
            option_type=6,
            required=True
        ),
        create_option(
            name="reason",
            description="Please type a reason for banning the member",
            option_type=3,
            required=True,
        )
    ]
            )
@has_permissions(ban_members=True)
async def ban(ctx:SlashContext, member, reason):   
    
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.guild_id)])

    await member.send(f'Hello **{member}**, you have been banned from **{ctx.guild}** for **{reason}**. This message has been automatically sent by Robo Rick. Please contact the server Admins of **{ctx.guild}** for questions or concerns')
    
    await channel.send(f"**{member}** has been banned for **{reason}** by **{ctx.author}**.")
    await ctx.send(f"Success! Banned **{member}** for **{reason}**!")
    await member.ban(reason=reason)

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.author}**, you do not have permission to ban members.')

##############Unban command (working)###########################################################################################
@slash.slash(
    description="Unbans a member of the server.",
            options=[
        create_option(
            name="member1234",
            description="Select the member you would like to unban in the format member#1234.",
            option_type=3,
            required=True
        )
        ]
)
@has_permissions(ban_members=True)
@guild_only()
async def unban(ctx:SlashContext, member1234):
  user = member1234
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = user.split('#')
  for ban_entry in banned_users:
    user = ban_entry.user
  
  if (user.name, user.discriminator) == (member_name, member_discriminator):
    await ctx.guild.unban(user)

    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.guild_id)])
    
    await channel.send(f"**{user}** has been unbanned by **{ctx.author}**.")
    await ctx.send(f"**{user}** successfully unbanned!")
    await user.send(f'Hello **{user}**, you have been unbanned from **{ctx.guild}**. This message has been automatically sent by Robo Rick. Please contact the server Admins of **{ctx.guild}** for questions or concerns')

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.author}**, you do not have permission to unban members.')

##############Temporary Ban command (working)###########################################################################################               
@slash.slash(
            description="Bans a member of the server for a number of days.",
            options=[
        create_option(
            name="member",
            description="Select the member you would like to temporary ban",
            option_type=6,
            required=True
        ),
        create_option(
            name="reason",
            description="Please type a reason for temporary banning the member",
            option_type=3,
            required=True,
        ),
        create_option(
            name="duration",
            description="The number of days the user will be banned for",
            option_type=4,
            required=True
        )
    ]
            )
@has_permissions(ban_members=True)
async def tempban(ctx:SlashContext, member, reason, duration):   
    user = member
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.guild_id)])

    await user.send(f'Hello **{user}**, you have been banned from **{ctx.guild}** for **{reason}** for **{duration}** days. This message has been automatically sent by Robo Rick. Please contact the server Admins of **{ctx.guild}** for questions or concerns')
    
    await channel.send(f"**{user}** has been banned for **{reason}** by **{ctx.author}** for **{duration}** days.")
    await user.ban(reason=reason)
    await ctx.send(f"Success! You have banned **{member}** for **{duration}** days!")
    #Unban process below
    await asyncio.sleep(duration*60*60*24)
    await ctx.guild.unban(user)

    await channel.send(f"**{user}** has been unbanned after **{duration}** days.")
    await user.send(f'Hello **{user}**, you have been unbanned from **{ctx.guild}** after **{duration}** days for **{reason}**. This message has been automatically sent by Robo Rick. Please contact the server Admins of **{ctx.guild}** for questions or concerns')
        
@tempban.error
async def tempban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.author}**, you do not have permission to ban members.')

##############Allows for the update channel to be changed (working)##############################################################################
@slash.slash(
            description="Changes the public announcements channel to the channel that you used the command in.",
            options=[
        create_option(
            name="channel",
            description="Select the channel updates will be sent in",
            option_type=7,
            required=True
        )
            ])
@has_permissions(manage_guild=True)
async def updatechannel(ctx:SlashContext, channel):

    with open("welcomechannels.json", "r") as f:
        guildInfo = json.load(f)

    guildInfo[ctx.guild_id] = channel.id #sets channel to send message to as the channel the command was sent to

    with open("welcomechannels.json", "w") as f:
        json.dump(guildInfo, f)
    await ctx.send(f'You have successfully changed the update channel to **{channel}**!')
    
@updatechannel.error
async def updatechannel_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.author}**, you need the permission `Manage Server` to change the update channel.')

##############Allows for the update channel to be checked (working)##############################################################################
@slash.slash(
            description="Checks the public announcements channel.",
            )
@has_permissions(manage_guild=True)
async def checkupdatechannel(ctx:SlashContext):
    with open("welcomechannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.guild_id)])
    await ctx.send(f'The update channel is set to **{channel.name}**')

@checkupdatechannel.error
async def checkupdatechannel_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.author}**, you need the permission `Manage Server` to check the update channel.')
        
##############Allows for the admin channel to be changed (working)##############################################################################
@slash.slash(
            description="Changes the admin announcements channel to the channel that you used the command in.",
            options=[
        create_option(
            name="channel",
            description="Select the channel admin updates will be sent in",
            option_type=7,
            required=True
        )
            ]
            )
@has_permissions(manage_guild=True)
async def adminchannel(ctx:SlashContext, channel):
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)

    guildInfo[ctx.guild_id] = channel.id #sets channel to send message to as the channel the command was sent to

    with open("adminchannels.json", "w") as f:
        json.dump(guildInfo, f)
    await ctx.send(f'You have successfully changed the admin channel to **{channel}**!')

@adminchannel.error
async def adminchannel_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.author}**, you need the permission `Manage Server` to change the admin channel.')

##############Allows for the admin channel to be checked (working)##############################################################################
@slash.slash(
            description="Checks the admin update channel.",
            )
@has_permissions(manage_guild=True)
async def checkadminchannel(ctx:SlashContext):
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.guild_id)])
    await ctx.send(f'The admin channel is set to **{channel.name}**')

@checkadminchannel.error
async def checkadminchannel_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.author}**, you need the permission `Manage Server` to check the admin channel.')
            
###########################################################################################################################
#############################################Legacy Commands ($)############################################################
##############)#############################################################################################################

##############Allows for the update channel to be changed (working)##############################################################################
@bot.command(name="updatechannel",pass_context=True,help="•Changes the public announcements channel to the channel that you used the command in.\n•You will need to be able to `Manage Server` people to use this command\n•Welcome messages, announcements, and leave messages are sent here\n•By default this channel is set to the top text channel in your server",brief="•Changes the channel updates are sent to")
@has_permissions(manage_guild=True)
async def updatechannel(ctx):
    with open("welcomechannels.json", "r") as f:
        guildInfo = json.load(f)

    guildInfo[ctx.message.guild.id] = ctx.message.channel.id #sets channel to send message to as the channel the command was sent to

    with open("welcomechannels.json", "w") as f:
        json.dump(guildInfo, f)
    await ctx.send(f'You have successfully changed the update channel to this channel')
    
@updatechannel.error
async def updatechannel_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.message.author}**, you need the permission `Manage Server` to change the update channel.')

##############Allows for the update channel to be checked (working)##############################################################################
@bot.command(name="checkupdatechannel",pass_context=True,help="•Checks the public announcements channel.\n•You will need to be able to `Manage Server` people to use this command\n•Welcome messages, announcements, and leave messages are sent here\n•By default this channel is set to the top text channel in your server",brief="•Checks the channel updates are sent to")
@has_permissions(manage_guild=True)
async def checkupdatechannel(ctx):
    with open("welcomechannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.message.guild.id)])
    await ctx.send(f'The update channel is set to {channel.name}')

@checkupdatechannel.error
async def checkupdatechannel_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.message.author}**, you need the permission `Manage Server` to check the update channel.')
        
##############Allows for the admin channel to be changed (working)##############################################################################
@bot.command(name="adminchannel",pass_context=True,help="•Changes the admin announcements channel to the channel that you used the command in.\n•You will need to be able to `Manage Server` to use this command\n•By default this channel is set to the top text channel in your server",brief="•Changes the channel admin updates are sent to")
@has_permissions(manage_guild=True)
async def adminchannel(ctx):
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)

    guildInfo[ctx.message.guild.id] = ctx.message.channel.id #sets channel to send message to as the channel the command was sent to

    with open("adminchannels.json", "w") as f:
        json.dump(guildInfo, f)
    await ctx.send(f'You have successfully changed the admin channel to this channel')

@adminchannel.error
async def adminchannel_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.message.author}**, you need the permission `Manage Server` to change the admin channel.')

##############Allows for the admin channel to be checked (working)##############################################################################
@bot.command(name="checkadminchannel",pass_context=True,help="•Checks the admin update channel.\n•You will need to be able to `Manage Server` people to use this command\n•By default this channel is set to the top text channel in your server",brief="•Checks the channel admin updates are sent to")
@has_permissions(manage_guild=True)
async def checkadminchannel(ctx):
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.message.guild.id)])
    await ctx.send(f'The admin channel is set to {channel.name}')

@checkadminchannel.error
async def checkadminchannel_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.message.author}**, you need the permission `Manage Server` to check the admin channel.')
            
##############Anouncement command (working)###########################################################################################
@bot.command(name="announce",pass_context=True,help="•Sends announcements (see below)\n•Need permission `Manage Server` to use this commmand\n•$announce hello - sends an announcement in the update channel\n•$announce 123456789 hello - sends an announcement in the channel ID specified\n•Channel ID is an optional arguement\n•Use developer mode and right click a channel to get the ID",brief="•Sends announcements to the channel of your choice")
@has_permissions(manage_guild=True)
async def announce(ctx, *, message):
    if message.split()[0].isdigit():
        isChannelIDincluded = bot.get_channel(int(message.split()[0])) is not None
    else:
        isChannelIDincluded = False
    if isChannelIDincluded:
        embed = discord.Embed(title="Announcement",description=message[message.index(' ') + 1:],color=0x9208ea)
    else:
        embed = discord.Embed(title="Announcement",description=message,color=0x9208ea)
    embed.set_footer(text=f'-{ctx.message.author} and the {ctx.message.guild} Admin team')
    if not isChannelIDincluded:
        with open("welcomechannels.json", "r") as f:
            guildInfo = json.load(f)
        channel = bot.get_channel(guildInfo[str(ctx.message.guild.id)])
    else:
        channel = bot.get_channel(int(message.split()[0]))
    await channel.send(embed=embed)
    channelname = channel.name
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.message.guild.id)])
    await channel.send(f'**{ctx.message.author}** sent an announcement in the {channelname} channel')

@announce.error
async def announce_error(ctx, error):
    if isinstance(error, MissingPermissions):
         await ctx.send(f'Sorry **{ctx.message.author}**, you need the permission `Manage Server` to make announcements.')

##############Server count command (working)###########################################################################################
@bot.command(name="servercount",pass_context=True,help="•Lists the number of servers Robo Rick is active in",brief="•Lists the number of servers Robo Rick is active in")
async def servercount(ctx):
    await ctx.channel.send("I'm currently active in " + str(len(bot.guilds)) + " servers!")

##############$Kick command (working)###########################################################################################
@bot.command(name="kick",pass_context=True,help="•Kicks a member of the server (Needs permission kick members for this command)\n•Sends an update in the admin channel saying what happened\n•$kick Morty - kicks Morty for no reason\n•$kick Summer because shes annoying - kicks Summer because shes being annoying.\n•Summer and Morty would be sent messages saying that they were kicked for either no reason or the reason you specified\n•The admin channel will also see who kicked who for what reason if one was specified",brief="•Kicks a member from the server with or without a reason")
@has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason = None):
  if not reason:
    
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.message.guild.id)])
    
    await channel.send(f"**{user}** has been kicked for **no reason** by **{ctx.message.author}**.")

    await user.send(f'Hello **{user}**, you have been kicked from **{ctx.message.guild}** for **reason not specified**. This message has been automatically sent by Robo Rick. Please contact the server Admins of **{ctx.message.guild}** for questions or concerns')
    await user.kick()

  else:
    
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.message.guild.id)])

    await user.send(f'Hello **{user}**, you have been kicked from **{ctx.message.guild}** for **{reason}**. This message has been automatically sent by Robo Rick. Please contact the server Admins of **{ctx.message.guild}** for questions or concerns')
    
    await channel.send(f"**{user}** has been kicked for **{reason}** by **{ctx.message.author}**.")
    await user.kick(reason=reason)

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.message.author}**, you do not have permission to kick members.')

        
##############Ban command (working)###########################################################################################
@bot.command(name="ban",pass_context=True,help="•Bans a member of the server (Needs permission ban members for this command)\n•Sends an update in the admin channel saying what happened\n•$ban Morty - bans Morty for no reason\n•$ban Summer because shes annoying - bans Summer because shes being annoying.\n•Summer and Morty would be sent messages saying that they were banned for either no reason or the reason you specified\n•The admin channel will also see who banned who for what reason if one was specified",brief="•Bans a member from the server with or without a reason")
@has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason = None):
  if not reason:
    
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.message.guild.id)])
    
    await channel.send(f"**{user}** has been banned for **no reason** by **{ctx.message.author}**.")

    await user.send(f'Hello **{user}**, you have been banned from **{ctx.message.guild}** for **reason not specified**. This message has been automatically sent by Robo Rick. Please contact the server Admins of **{ctx.message.guild}** for questions or concerns')
    await user.ban()

  else:
    
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.message.guild.id)])

    await user.send(f'Hello **{user}**, you have been banned from **{ctx.message.guild}** for **{reason}**. This message has been automatically sent by Robo Rick. Please contact the server Admins of **{ctx.message.guild}** for questions or concerns')
    
    await channel.send(f"**{user}** has been banned for **{reason}** by **{ctx.message.author}**.")
    await user.ban(reason=reason)

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.message.author}**, you do not have permission to ban members.')

##############Unban command (working)###########################################################################################
@bot.command(name="unban",pass_context=True,help="•Unbans a member of the server (Needs permission ban members for this command). Syntax: '$unban User#1234'. Do not use the @name like you can with ban and kick",brief="•Unbans someone from the server")
@has_permissions(ban_members=True)
@guild_only()
async def unban(ctx, *, member,):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')
  for ban_entry in banned_users:
    user = ban_entry.user
  
  if (user.name, user.discriminator) == (member_name, member_discriminator):
    await ctx.guild.unban(user)

    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.message.guild.id)])
    
    await channel.send(f"**{user}** has been unbanned by **{ctx.message.author}**.")

    await user.send(f'Hello **{user}**, you have been unbanned from **{ctx.message.guild}**. This message has been automatically sent by Robo Rick. Please contact the server Admins of **{ctx.message.guild}** for questions or concerns')
    return

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.message.author}**, you do not have permission to unban members.')

##############Temporary Ban command (working)###########################################################################################               
@bot.command(name="tempban",pass_context=True,help="•Bans a member of the server for a number of days (Needs permission ban members for this command)\n•Sends an update in the admin channel saying what happened\n•$tempban Morty 2 - bans Morty for no reason for 2 days\n•$tempban Summer 3 because shes annoying - bans Summer because shes being annoying for 3 days.\n•Summer and Morty would be sent messages saying that they were banned for either no reason or the reason you specified and it will tell them for how many days\n•The admin channel will also see who banned who for what reason if one was specified and for how long\n•Both the user and admin channel will be notified when someone has been unbanned because the time period expired",brief="•Temporarily bans a member from the server with or without a reason for a certain amount of days")
@has_permissions(ban_members=True)
async def tempban(ctx, user: discord.Member, duration: int, *, reason = None):
    if not reason:
    
        with open("adminchannels.json", "r") as f:
            guildInfo = json.load(f)
        channel = bot.get_channel(guildInfo[str(ctx.message.guild.id)])
    
        await channel.send(f"**{user}** has been banned for **no reason** by **{ctx.message.author}** for **{duration}** days.")

        await user.send(f'Hello **{user}**, you have been banned from **{ctx.message.guild}** for **reason not specified** for **{duration}** days. This message has been automatically sent by Robo Rick. Please contact the server Admins of **{ctx.message.guild}** for questions or concerns')
        await user.ban()

        #Unban process below
        await asyncio.sleep(duration*60*60*24)
        await ctx.guild.unban(user)

        with open("adminchannels.json", "r") as f:
            guildInfo = json.load(f)
        channel = bot.get_channel(guildInfo[str(ctx.message.guild.id)])
    
        await channel.send(f"**{user}** has been unbanned after **{duration}** days.")
        
    else:
    
        with open("adminchannels.json", "r") as f:
            guildInfo = json.load(f)
        channel = bot.get_channel(guildInfo[str(ctx.message.guild.id)])

        await user.send(f'Hello **{user}**, you have been banned from **{ctx.message.guild}** for **{reason}** for **{duration}** days. This message has been automatically sent by Robo Rick. Please contact the server Admins of **{ctx.message.guild}** for questions or concerns')
    
        await channel.send(f"**{user}** has been banned for **{reason}** by **{ctx.message.author}** for **{duration}** days.")
        await user.ban(reason=reason)

        #Unban process below
        await asyncio.sleep(duration*60*60*24)
        await ctx.guild.unban(user)

        await channel.send(f"**{user}** has been unbanned after **{duration}** days.")
        await user.send(f'Hello **{user}**, you have been unbanned from **{ctx.message.guild}** after **{duration}** days for **{reason}**. This message has been automatically sent by Robo Rick. Please contact the server Admins of **{ctx.message.guild}** for questions or concerns')
        
@tempban.error
async def tempban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.message.author}**, you do not have permission to ban members.')

##############Reponds to $ping (working)########################################################################################################
@bot.command(
	help="•Responds with Pong and the bots server latency", 	# ADDS THIS VALUE TO THE $HELP PING MESSAGE.
	brief="•Responds with Pong and the bots server latency" # ADDS THIS VALUE TO THE $HELP MESSAGE.
)
async def ping(ctx):
	await ctx.channel.send(f'🏓 Pong! {round(bot.latency * 1000)}ms') # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.

##############Reponds to $donate (working)########################################################################################################
@bot.command(
	help="•Brings up information on how to donate towards Robo Ricks development", 	
	brief="•Brings up information on how to donate towards Robo Ricks development" 
)
async def donate(ctx):
    embed = discord.Embed(colour=discord.Colour(0x788dee), url="https://discordapp.com", description=f" Hello **{ctx.message.author}**, I'm glad someone finally appreciates my genius! Thank you for your interest in donating! Your donation will help with the cost of hosting and developing me for servers like **{ctx.message.guild}**!")

    embed.set_thumbnail(url="https://raw.githubusercontent.com/TrevorSLong/Robo-Rick/main/Screenshots/DonateQRCode.png")
    embed.set_author(name="Robo Rick", url="https://top.gg/bot/827681932660965377", icon_url="https://raw.githubusercontent.com/TrevorSLong/Robo-Rick/main/Screenshots/rick.jpg")

    embed.add_field(name="Help support my growth", value="I was made by two full time students, if you enjoy having me around please consider **supporting my development** by contributing code to me [here](https://github.com/DroTron/Robo-Rick) or **donating** to help fund development and hosting costs [here](https://www.paypal.com/donate?hosted_button_id=RBYUJ5M6QSB52)")

    await ctx.channel.send(embed=embed)

##############Responds to $help (working)########################################################################################################
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)
@bot.command(
	help="Looks like you need some help.", # ADDS THIS VALUE TO THE $HELP PRINT MESSAGE.
	brief="Prints the list of values back to the channel." # ADDS THIS VALUE TO THE $HELP MESSAGE.
)
async def print(ctx, *args):
	response = ""
	for arg in args:
		response = response + " " + arg
	await ctx.channel.send(response)


bot.run(TOKEN)