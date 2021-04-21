# Robo-Rick
This repository contains the code that runs the Discord bot "Robo Rick". Robo rick can be added to your server with [this link](https://discord.com/oauth2/authorize?client_id=827681932660965377&scope=bot)
This page is designed to be a help page for the bot itself and also used for learning how to program your own bot. DO NOT COPY THIS CODE AND DO NOT USE IT FOR PROFIT! Robo Rick was developed by two college students,
if you would like to help develop Robo Rick you can contribute to the code here or donate to its development [here](https://www.paypal.com/donate?hosted_button_id=RBYUJ5M6QSB52)
The functionality is listed below:

#### Welcome message
   * Welcomes new members into the server by name with a random welcome message from Rick and Morty     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/welcomemessages.PNG)
#### Welcome DM
   * Welcomes new members into the server by sending them a DM     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/welcomedm.PNG)
#### Chat response
   * Responds to "hello" with "Wubbalubbadubdub"     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/hello.PNG)
#### Changes bot status
   * Robo Ricks status is "Listening to Snake Jazz"     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/status.PNG)
#### Ping
   * Responds to $ping with "pong" and the bot server latency     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/ping.PNG)
#### UpdateChannel
   * Use $updatechannel to change the channel Robo Rick sends all public updates
   * The channel will be changed to the channel that you send the command in
   * By default this channel will be the top text channel in the server
   * To change this permission, the user must have the "Manage Channel" permission in the Discord server     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/updatechannel.PNG)
#### AdminChannel
   * Use $adminchannel to change the channel Robo Rick sends all admin updates
   * The channel will be changed to the channel that you send the command in
   * By default this channel will be the top text channel in the server
   * To change this permission, the user must have the "Manage Channel" permission in the Discord server     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/adminchannel.PNG)
#### Join server message
   * Robo Rick sends a message in the default channel when he joins the server for the first time introducing himself     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/joinmessage.PNG)
#### Announcements
   * $announce "_____" will send an announcement in the updates channel in your server. To change the channel it is sent in use $updatechannel     return
   * You will need the permission 'Manage Channel' to use this command
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/announce.PNG)
   * Announcements can be sent to a specific channel by adding the channel ID as an optional arguement
   * Example: $announce 123456789 This announcement was sent to a specific channel instead of the update channel
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/announcespecific.PNG)
#### Kick
   * $kick "__" "__" kicks a member for a either a specified or unspecified reason
   * Sends an update in Admin channel and sends the reason in a DM to the member who was kicked
   * Example: `$kick @DroTron#1863 for this really valid reason` 
   * If a reason is specified:
      * In chat where command was issued     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/kick1.PNG)
      * In Admin channel     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/kick2.PNG)
      * In users DM with Robo Rick     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/kick3.png)
   * If no reason is specified:
      * In chat where command was issued     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/kickNR1.PNG)
      * In Admin channel     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/kickNR2.PNG)
      * In users DM with Robo Rick     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/kickNR3.png) 
#### Ban
   * $ban "__" "__" bans a member for a either a specified or unspecified reason
   * Sends an update in Admin channel and sends the reason in a DM to the member who was banned
   * Example: `$ban @DroTron#1863 for this really valid reason` 
   * If a reason is specified:
      * In chat where command was issued     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/ban1.PNG)
      * In Admin channel     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/ban2.PNG)
      * In users DM with Robo Rick     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/ban3.png)
   * If no reason is specified:  
      * In text chat where the command was issued     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/banNR1.PNG)
      * In Admin channel     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/banNR2.PNG)
      * In users DM with Robo Rick     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/banNR3.png)
#### Unban
   * $unban unbans a user that was previously banned
   * Example: `$unban DroTron#1863` 
   * **Important**: in ban and kick use @DroTron after the command but here use DroTron#1863 with no @
      * In the admin channel     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/unban1.PNG)
      * In the users DM with Robo Rick     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/unban2.png)
#### Tempban
   * `$tempban user days reason` bans a user for a certain number of days for a reason and then unbans them
   * Example: `$tempban @Knightmare 2 because he sucks` 
   * Robo Rick sends an announcement in the admin channel and sends the user a DM
      * In the admin channel     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/tempban1.PNG)
      * In the users DM with Robo Rick     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/tempban2.png)
      * In the users DM with Robo Rick after the time has passed     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/tempban3.png)
      * In the admin channel after the time has passed     return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/tempban4.PNG)
#### Error handling
   * Sends an error if a member tries to use a command they do not have access to       return
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/errorhandling.png)   
#### 3070/3080 Stock announcement
   * IMPORTANT: If you use the bot I host you will not be able to use this command
   * This command essentially lets you broadcast a preset message to two channels with a simple command
#### Help
   * $help is here! Type this to get a less detailed summary of what is above.       return 
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/help.PNG)

# Git Command
`git clone https://github.com/DroTron/Robo-Rick`
*  Clones entire repository
*  add `~/FOLDER/SUBFOLDER` after PROGRAM.m to clone to specific folder
   * Ex: `git clone https://github.com/DroTron/Robo-Rick ~/Robo-Rick`
   * to clone repository to a folder in home named Robo-Rick
