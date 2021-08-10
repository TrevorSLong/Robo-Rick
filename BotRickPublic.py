#!/usr/bin/python3.4
#Robo Rick
#-------------------------------------------------
#Discord bot for welcome messages, leave messages, kicking, banning, announcements, and more
#Created by DroTron (Trevor L)
#https://github.com/DroTron/Robo-Rick
#-------------------------------------------------
#This code may be used to help you build your own bot or to run on your own server
#Do not use my code for profit
#For help go to https://realpython.com/how-to-make-a-discord-bot-python/
#https://betterprogramming.pub/how-to-make-discord-bot-commands-in-python-2cae39cbfd55
#Have fun!
#-------------------------------------------------

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
print("Bot Rick sends reconnect updates to " + BOT_UPDATE_CHANNEL)

C3080_ID = os.getenv('3080_CHANNEL') #Grabs admin channel ID from .env file
print("Using 3080 channel ID " + C3080_ID)

C3070_ID = os.getenv('3070_CHANNEL') #Grabs admin channel ID from .env file
print("Using 3070 channel ID " + C3070_ID)

dbl_token = os.getenv('dbl_token') #Grabs admin channel ID from .env file
print("Using DBL Token " + dbl_token)

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all()) #declare intents for bot
slash = SlashCommand(bot, sync_commands=True) #Declares command prefix

##############Changes bot status (working)###########################################################################################
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Snake Jazz"))
    channel = bot.get_channel(int(BOT_UPDATE_CHANNEL))
    await channel.send(f'Robo Rick has restarted and has successfully reconnected to Discord!')
    
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

    embed.set_thumbnail(url="https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/rick.jpg")
    embed.set_author(name="Robo Rick", url="https://top.gg/bot/827681932660965377", icon_url="https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/rick.jpg")

    embed.add_field(name="Well since I have to be here....", value="I guess I'll give you the run down on my basic functions",inline=False)
    embed.add_field(name="Basic commands:", value="• Go to the channel you want updates and messages in and type the command ``$updatechannel``\n• Go to the channel you want admin updates in and type the command ``$adminchannel``\n• ``$help`` will give you the rundown of all of the inventions I have to offer",inline=False)
    embed.add_field(name="Help support my growth", value="I was made by two full time students, if you enjoy having me around please consider **supporting my development** by contributing code to me [here](https://github.com/DroTron/Robo-Rick) or **donating** to help fund development and hosting costs [here](https://www.paypal.com/donate?hosted_button_id=RBYUJ5M6QSB52)",inline=False)

    await channel.send(embed=embed)

##############Allows for the update channel to be changed (working)##############################################################################
@slash.slash(name="updatechannel",
            description="Changes the public announcements channel to the channel that you used the command in.",
            )
async def updatechannel(ctx:SlashContext):
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
@slash.slash(name="checkupdatechannel",
            description="Checks the public announcements channel.",
            )
async def checkupdatechannel(ctx:SlashContext):
    with open("welcomechannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.message.guild.id)])
    await ctx.send(f'The update channel is set to {channel.name}')

@checkupdatechannel.error
async def checkupdatechannel_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.message.author}**, you need the permission `Manage Server` to check the update channel.')
        
##############Allows for the admin channel to be changed (working)##############################################################################
@slash.slash(name="adminchannel",
            description="Changes the admin announcements channel to the channel that you used the command in.",
            )
async def adminchannel(ctx:SlashContext):
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
@slash.slash(name="checkadminchannel",
            description="Checks the admin update channel.",
            )
async def checkadminchannel(ctx:SlashContext):
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.message.guild.id)])
    await ctx.send(f'The admin channel is set to {channel.name}')

@checkadminchannel.error
async def checkadminchannel_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.message.author}**, you need the permission `Manage Server` to check the admin channel.')
            
##############Anouncement command (working)###########################################################################################
@slash.slash(name="announce",
            description="Sends an announcement to either the updates channel or to any channel ID.",
            options=[
                create_option(
                    name="channelid",
                    description="Optional addition of the channel the announcement will be sent to.",
                    option_type=7,
                    required=False
                ),
                create_option(
                    name="message",
                    description="Type the message you want to send in the announcement",
                    option_type=3,
                    required=False
                )
            ])
async def announce(ctx:SlashContext, channelid:str, message:str):
    if channelid:
        embed = discord.Embed(title="Announcement",description=message,color=0x9208ea)
        embed.set_footer(text=f'footer')
        channel = channelid
        await channel.send(embed=embed)
    if not channelid:
        with open("welcomechannels.json", "r") as f:
            guildInfo = json.load(f)
        channel = bot.get_channel(guildInfo[str(ctx.message.guild.id)])
        await channel.send(embed=embed)

#@announce.error
#async def announce_error(ctx, error):
#    if isinstance(error, MissingPermissions):
#         await ctx.send(f'Sorry **{ctx.message.author}**, you need the permission `Manage Server` to make announcements.')

##############Server count command (working)###########################################################################################
@slash.slash(name="servercount",
            description="Lists the number of servers Robo Rick is active in",
            )
async def servercount(ctx:SlashContext):
    await ctx.channel.send("I'm currently active in " + str(len(bot.guilds)) + " servers!")

##############Kick command (working)###########################################################################################
@slash.slash(name="kick",
            description="Kicks a member of the server.",
            )
async def kick(ctx:SlashContext, user: discord.Member, *, reason = None):
  if not reason:
    await user.kick()
    
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.message.guild.id)])
    
    await channel.send(f"**{user}** has been kicked for **no reason** by **{ctx.message.author}**.")

    await user.send(f'Hello **{user}**, you have been kicked from **{ctx.message.guild}** for **reason not specified**. This message has been automatically sent by Robo Rick. Please contact the server Admins of **{ctx.message.guild}** for questions or concerns')
    
  else:
    await user.kick(reason=reason)
    
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.message.guild.id)])

    await user.send(f'Hello **{user}**, you have been kicked from **{ctx.message.guild}** for **{reason}**. This message has been automatically sent by Robo Rick. Please contact the server Admins of **{ctx.message.guild}** for questions or concerns')
    
    await channel.send(f"**{user}** has been kicked for **{reason}** by **{ctx.message.author}**.")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.message.author}**, you do not have permission to kick members.')

        
##############Ban command (working)###########################################################################################
@slash.slash(name="ban",
            description="Bans a member of the server.",
            )
async def ban(ctx:SlashContext, user: discord.Member, *, reason = None):
  if not reason:
    await user.ban()
    
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.message.guild.id)])
    
    await channel.send(f"**{user}** has been banned for **no reason** by **{ctx.message.author}**.")

    await user.send(f'Hello **{user}**, you have been banned from **{ctx.message.guild}** for **reason not specified**. This message has been automatically sent by Robo Rick. Please contact the server Admins of **{ctx.message.guild}** for questions or concerns')
    
  else:
    await user.ban(reason=reason)
    
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.message.guild.id)])

    await user.send(f'Hello **{user}**, you have been banned from **{ctx.message.guild}** for **{reason}**. This message has been automatically sent by Robo Rick. Please contact the server Admins of **{ctx.message.guild}** for questions or concerns')
    
    await channel.send(f"**{user}** has been banned for **{reason}** by **{ctx.message.author}**.")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.message.author}**, you do not have permission to ban members.')

##############Unban command (working)###########################################################################################
@slash.slash(name="unban",
            description="Unbans a member of the server.",
            )
@guild_only()
async def unban(ctx:SlashContext, *, member,):
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
@slash.slash(name="tempban",
            description="Bans a member of the server for a number of days.",
            )
async def tempban(ctx:SlashContext, user: discord.Member, duration: int, *, reason = None):
    if not reason:
        await user.ban()
    
        with open("adminchannels.json", "r") as f:
            guildInfo = json.load(f)
        channel = bot.get_channel(guildInfo[str(ctx.message.guild.id)])
    
        await channel.send(f"**{user}** has been banned for **no reason** by **{ctx.message.author}** for **{duration}** days.")

        await user.send(f'Hello **{user}**, you have been banned from **{ctx.message.guild}** for **reason not specified** for **{duration}** days. This message has been automatically sent by Robo Rick. Please contact the server Admins of **{ctx.message.guild}** for questions or concerns')

        #Unban process below
        await asyncio.sleep(duration*60*60*24)
        await ctx.guild.unban(user)

        with open("adminchannels.json", "r") as f:
            guildInfo = json.load(f)
        channel = bot.get_channel(guildInfo[str(ctx.message.guild.id)])
    
        await channel.send(f"**{user}** has been unbanned after **{duration}** days.")
        
    else:
        await user.ban(reason=reason)
    
        with open("adminchannels.json", "r") as f:
            guildInfo = json.load(f)
        channel = bot.get_channel(guildInfo[str(ctx.message.guild.id)])

        await user.send(f'Hello **{user}**, you have been banned from **{ctx.message.guild}** for **{reason}** for **{duration}** days. This message has been automatically sent by Robo Rick. Please contact the server Admins of **{ctx.message.guild}** for questions or concerns')
    
        await channel.send(f"**{user}** has been banned for **{reason}** by **{ctx.message.author}** for **{duration}** days.")

        #Unban process below
        await asyncio.sleep(duration*60*60*24)
        await ctx.guild.unban(user)

        await channel.send(f"**{user}** has been unbanned after **{duration}** days.")
        await user.send(f'Hello **{user}**, you have been unbanned from **{ctx.message.guild}** after **{duration}** days for **{reason}**. This message has been automatically sent by Robo Rick. Please contact the server Admins of **{ctx.message.guild}** for questions or concerns')
        
@tempban.error
async def tempban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.message.author}**, you do not have permission to ban members.')

##############Public Welcome (working)########################################################################################################
@bot.event
async def on_member_join(member):

###########Sends DM to member who joined############
    await member.create_dm()
    embed = discord.Embed(colour=discord.Colour(0x788dee), url="https://discordapp.com", description=f" I turned myself into a Discord bot, **{member.name}**! Boom! Big reveal: I'm a Discord bot. What do you think about that? I turned myself into a Discord bot! W-what are you just staring at me for, bro. I turned myself into a Discord bot, **{member.name}**!")

    embed.set_thumbnail(url="https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/rick.jpg")
    embed.set_author(name="Robo Rick", url="https://top.gg/bot/827681932660965377", icon_url="https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/rick.jpg")

    embed.add_field(name=f"Every Morty needs a Rick, and every **{member.guild}** needs a Robo Rick: ", value=f"Welcome to **{member.guild}**, I'm Robo Rick, one of the moderation bots here. Please read through the servers specific rules and agree to them to start chatting.",inline=False)
    embed.add_field(name="A few notes:", value="• Use ``$help`` to get a full list of my featues\n• This message is not editable by the server your joining, please be sure to read their rules and welcome page to make sure you aren't missing anything. ",inline=False)
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

##############Reponds to $ping (working)########################################################################################################
@slash.slash(
	description="Responds with Pong and the bots server latency", 	# ADDS THIS VALUE TO THE $HELP PING MESSAGE.
)
async def ping(ctx:SlashContext):
	await ctx.send(f'🏓 Pong! {round(bot.latency * 1000)}ms') # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.

##############Reponds to $donate (working)########################################################################################################
@slash.slash(
	description="Brings up information on how to donate towards Robo Ricks development", 	 
)
async def donate(ctx:SlashContext):
    embed = discord.Embed(colour=discord.Colour(0x788dee), url="https://discordapp.com", description=f" Hello **{ctx.message.author}**, I'm glad someone finally appreciates my genius! Thank you for your interest in donating! Your donation will help with the cost of hosting and developing me for servers like **{ctx.message.guild}**!")

    embed.set_thumbnail(url="https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/DonateQRCode.png")
    embed.set_author(name="Robo Rick", url="https://top.gg/bot/827681932660965377", icon_url="https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/rick.jpg")

    embed.add_field(name="Help support my growth", value="I was made by two full time students, if you enjoy having me around please consider **supporting my development** by contributing code to me [here](https://github.com/DroTron/Robo-Rick) or **donating** to help fund development and hosting costs [here](https://www.paypal.com/donate?hosted_button_id=RBYUJ5M6QSB52)")

    await ctx.send(embed=embed)

##############Responds to $help (working)########################################################################################################
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)
@slash.slash(
	description="Looks like you need some help.", # ADDS THIS VALUE TO THE $HELP PRINT MESSAGE. 
)
async def print(ctx, *args):
	response = ""
	for arg in args:
		response = response + " " + arg
	await ctx.channel.send(response)

bot.run(TOKEN)
