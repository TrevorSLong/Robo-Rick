#Bot Rick
#-------------------------------------------------
#Discord bot for welcome messages, leave messages, and announcements
#Created by DroTron (Trevor L)
#https://github.com/DroTron/bot-rick
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
from dotenv import load_dotenv
from discord.ext import commands
from discord import Member
from discord import User
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext.commands import Bot, guild_only

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') #Grabs bot token from .env file
print("Logging in with Bot Token " + TOKEN)

BOT_UPDATE_CHANNEL = os.getenv('BOT_UPDATE_CHANNEL') #Grabs update channel .env file
print("Bot Rick sends reconnect updates to " + BOT_UPDATE_CHANNEL)

C3080_ID = os.getenv('3080_CHANNEL') #Grabs admin channel ID from .env file
print("Using 3080 channel ID " + C3080_ID)

C3070_ID = os.getenv('3070_CHANNEL') #Grabs admin channel ID from .env file
print("Using 3070 channel ID " + C3070_ID)


intents = discord.Intents.all() #Declare intents
intents.members = True
intents.typing = True
intents.presences = True
bot = commands.Bot(command_prefix="$",intents= intents) #Declares command prefix

##############Changes bot status (working)###########################################################################################
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Snake Jazz"))
    channel = bot.get_channel(int(BOT_UPDATE_CHANNEL))
    await channel.send(f'Bot Rick has successfully reconnected to Froopyland!')
    
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
    await channel.send(f'Hi everyone, thanks for inviting me to the server!\nUse $help to see all my commands and get started\nGo to the channel you want me to send updates in and do $updatechannel\nGo to the channel you want admin updates in and do $adminchannel\nWubalubadubdub!')

##############Allows for the update channel to be changed (working)##############################################################################
@bot.command(name="updatechannel",pass_context=True,help="Use /\ to change the public announcements channel to the channel that you used the command in.\n You will need to be able to ban people to use this command",brief="Use $updatechannel to change the channel where all announcements are sent. The channel will be set to the channel that you sent the message in (Needs permission ban members for this command)")
@has_permissions(ban_members=True)
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
        await ctx.send(f'Sorry **{ctx.message.author}**, you do not have permission to change the update channel.')
        
##############Allows for the admin channel to be changed (working)##############################################################################
@bot.command(name="adminchannel",pass_context=True,help="Use /\ to change the admin announcements channel to the channel that you used the command in.\n You will need to be able to ban people to use this command",brief="Use $adminchannel to change the channel where all admin announcements are sent. The channel will be set to the channel that you sent the message in (Needs permission ban members for this command)")
@has_permissions(ban_members=True)
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
        await ctx.send(f'Sorry **{ctx.message.author}**, you do not have permission to change the admin channel.')
        
##############Anouncement command (working)###########################################################################################
@bot.command(name="announce",pass_context=True,help="/\ annouces to the servers welcome channel, signs with your user name (Needs permission ban members for this command)",brief="$announce_____ annouces to the servers welcome channel, signs with your user name (Needs permission ban members for this command)")
@has_permissions(ban_members=True)
async def announce(ctx,*,message,):
    
    embed = discord.Embed(title="Announcement",description=message,color=0x9208ea)
    embed.set_footer(text=f'-{ctx.message.author} and the {ctx.message.guild} Admin team')
    
    with open("welcomechannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.message.guild.id)])
    
    await channel.send(embed=embed)
    
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.message.guild.id)])
    
    await channel.send(f'**{ctx.message.author}** sent an announcement in the updates channel')

@announce.error
async def announce_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.message.author}**, you do not have permission to announce.')
        
##############Server count command (working)###########################################################################################
@bot.command(name="servercount",pass_context=True,help="/\ lists the number of servers Robo Rick is active in",brief="$servercount lists the number of servers Robo Rick is active in")
async def servercount(ctx):
    await ctx.channel.send("I'm currently active in " + str(len(bot.guilds)) + " servers!")

##############Kick command (working)###########################################################################################
@bot.command(name="kick",pass_context=True,help="/\ kicks a member of the server (Needs permission kick members for this command)",brief="$kick _____ _____ kicks a member from the server with the following reason")
@has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason = None):
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
@bot.command(name="ban",pass_context=True,help="/\ bans a member of the server (Needs permission ban members for this command)",brief="$ban _____ _____ bans a member from the server with the following reason")
@has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason = None):
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
@bot.command(name="unban",pass_context=True,help="/\ unbans a member of the server (Needs permission ban members for this command). Syntax: '$unban User#1234'. Do not use the @name like you can with ban and kick",brief="$unban _____ _____ bans a member from the server with the following reason")
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

##############Temporary Ban command (not working)###########################################################################################               
@bot.command(name="tempban",pass_context=True,help="/\ bans a member of the server for an amount of time in days (Needs permission ban members for this command)",brief="$ban _____ _____ bans a member from the server for x days")
@has_permissions(ban_members=True)
async def tempban(ctx, user: discord.Member, duration: int, *, reason = None):
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

    await member.create_dm()
    newUDM1 = f'Hi **{member.name}**, welcome to **{member.guild}**!'
    newUDM2 = f'Please read the rules and agree to start chatting.'
    newUDM3 = f'If you need any help from me just type **$help** in any channel'
    newUDM4 = f'Im Pickle Rickkkkkkk!'
    await member.dm_channel.send(newUDM1 + '\n' + newUDM2 + '\n' + newUDM3 + '\n' + newUDM4)

    with open("welcomechannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(member.guild.id)])

 
    welcomemessages = [
        f'(WEL MSG) Boom! Big reveal! I turned myself into a pickle! Oh, also {member.name} is here.',
        f'(WEL MSG) Ill tell you how I feel about school, {member.name}: Its a waste of time. Bunch of people runnin around bumpin into each other, got a guy up front says, 2 + 2, and the people in the back say, 4. Then the bell rings and they give you a carton of milk and a piece of paper that says you can go take a dump or somethin. I mean, its not a place for smart people, {member.name}. I know thats not a popular opinion, but thats my two cents on the issue.',
        f'(WEL MSG) You gotta do it for Grandpa, {member.name}. You gotta put these seeds inside your butt.',
        f'(WEL MSG) Nobody exists on purpose. Nobody belongs anywhere. Everybodys gonna die. Come watch TV {member.name}.',
        f'(WEL MSG) SHOW ME WHAT YOU GOT {member.name}!',
        f'(WEL MSG) {member.name}, I need your help on an adventure. Eh, need is a strong word. We need door stops, but a brick would work too.',
        f'(WEL MSG) What about the reality where Hitler cured cancer, {member.name}? The answer is: Dont think about it.',
        ]
    randomwelcome = random.choice(welcomemessages)
    await channel.send(randomwelcome)
    
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(member.guild.id)])
    
    await channel.send(f'Bot Rick successfully sent welcome message and DM about **{member.name}** joining **{member.guild}**.')

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
                       
##############Responds to hello (working)###########################################################################################
@bot.event
async def on_message(message):
	if message.content == "hello":
		await message.channel.send("Wubbalubbadubdub")
	await bot.process_commands(message) # INCLUDES THE COMMANDS FOR THE BOT. WITHOUT THIS LINE, YOU CANNOT TRIGGER YOUR COMMANDS.

##############Reponds to $ping (working)########################################################################################################
@bot.command(
	help="Uses come crazy logic to determine if pong is actually the correct value or not.", 	# ADDS THIS VALUE TO THE $HELP PING MESSAGE.
	brief="Prints pong back to the channel." # ADDS THIS VALUE TO THE $HELP MESSAGE.
)
async def ping(ctx):
	await ctx.channel.send(f'🏓 Pong! {round(bot.latency * 1000)}ms') # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.

###############3080/3070 stock announcement (manually announce in multiple channels that something happened with one command)######################################################################
@bot.command(name="bbyinstock",pass_context=True,help="BBYInStock is specific to the creators server, this will not work on your server. $bbyinstock sends an announcement in 3070/3080 channels that best buy has stock of 3070/3080, to be triggered manually by Admin or Mod",brief="$bbyinstock sends an announcement in 3070/3080 channels that best buy has stock of 3070/3080, to be triggered manually by Admin or Mod")
@has_permissions(kick_members=True)
async def bbyinstock(ctx):
    if ctx.message.guild == 'Froopyland':
        channel = bot.get_channel(int(C3080_ID))
        await channel.send(f'RTX3000 Cards in stock at Best Buy!\n[3080 FE](https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440)\n[3070 FE](https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p?skuId=6429442)\n[3060TI FE](https://www.bestbuy.com/site/nvidia-geforce-rtx-3060-ti-8gb-gddr6-pci-express-4-0-graphics-card-steel-and-black/6439402.p?skuId=6439402)\nThis stock announcement was manually sent by **{ctx.message.author}**')
        channel = bot.get_channel(int(C3070_ID))
        await channel.send(f'RTX3000 Cards in stock at Best Buy!\n[3080 FE](https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440)\n[3070 FE](https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p?skuId=6429442)\n[3060TI FE](https://www.bestbuy.com/site/nvidia-geforce-rtx-3060-ti-8gb-gddr6-pci-express-4-0-graphics-card-steel-and-black/6439402.p?skuId=6439402)\nThis stock announcement was manually sent by **{ctx.message.author}**')
    else:
        await ctx.channel.send(f'Sorry **{ctx.message.author}**, this command is not ready for your server')
        
@bbyinstock.error
async def bbyinstock_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.message.author}**, you do not have permission to announce RTX3000 stock.')


##############Responds to $help (working)########################################################################################################
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
