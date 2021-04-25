# Robo-Rick
This repository contains the code that runs the Discord bot "Robo Rick". Robo rick can be added to your server with [this link](https://discord.com/oauth2/authorize?client_id=827681932660965377&scope=bot)
This page is designed to be a help page for the bot itself and also used for learning how to program your own bot. DO NOT COPY THIS CODE AND DO NOT USE IT FOR PROFIT! Robo Rick was developed by two college students,
if you would like to help develop Robo Rick you can contribute to the code here or donate to its development [here](https://www.paypal.com/donate?hosted_button_id=RBYUJ5M6QSB52)
The functionality is listed below:

#### Welcome message
   * Welcomes new members into the server by name with a random welcome message from Rick and Morty     <br />
![WelcomeMessageImage](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/welcomemessages.PNG)
#### Welcome DM
   * Welcomes new members into the server by sending them a DM     <br />
![WelcomeDMImage](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/welcomedm.PNG)
#### Chat response
   * Responds to "hello" with "Wubbalubbadubdub"     <br />
![ChatResponseImage](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/hello.PNG)
#### Changes bot status
   * Robo Ricks status is "Listening to Snake Jazz"     <br />
![BotStatusImage](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/status.PNG)
#### Ping
   * Responds to $ping with "pong" and the bot server latency     <br />
![PingImage](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/ping.PNG)
#### UpdateChannel
   * Use $updatechannel to change the channel Robo Rick sends all public updates
   * The channel will be changed to the channel that you send the command in
   * By default this channel will be the top text channel in the server
   * To change this permission, the user must have the "Manage Channel" permission in the Discord server     <br />
![UpdateChannelImage](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/updatechannel.PNG)
   * $checkupdatechannel can be used to check which channel in your server is set to the update channel     <br />
![CheckUpdateChannelImage](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/checkupdatechannel.PNG)
#### AdminChannel
   * Use $adminchannel to change the channel Robo Rick sends all admin updates
   * The channel will be changed to the channel that you send the command in
   * By default this channel will be the top text channel in the server
   * To change this permission, the user must have the "Manage Channel" permission in the Discord server     <br />
![AdminChannelImage](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/adminchannel.PNG)
   * $checkadminchannel can be used to check which channel in your server is set to the admin update channel     <br />
![CheckAdminChannelImage](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/checkadminchannel.PNG)
#### Join server message
   * Robo Rick sends a message in the default channel when he joins the server for the first time introducing himself     <br />
![JoinServerImage](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/joinmessage.PNG)
#### Announcements
   * $announce "_____" will send an announcement in the updates channel in your server. To change the channel it is sent in use $updatechannel     <br />
   * You will need the permission 'Manage Channel' to use this command
![AnnouncementsImage](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/announce.PNG)
   * Announcements can be sent to a specific channel by adding the channel ID as an optional arguement
   * Example: $announce 123456789 This announcement was sent to a specific channel instead of the update channel     <br />
![SpecificChannelAnnouncementsImage](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/announcespecific.jpg)
#### Kick
   * $kick "__" "__" kicks a member for a either a specified or unspecified reason
   * Sends an update in Admin channel and sends the reason in a DM to the member who was kicked
   * Example: `$kick @DroTron#1863 for this really valid reason` 
   * If a reason is specified:
      * In chat where command was issued     <br />
![KickImage1](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/kick1.PNG)
      * In Admin channel     <br />
![KickImage2](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/kick2.PNG)
      * In users DM with Robo Rick     <br />
![KickImage3](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/kick3.png)
   * If no reason is specified:
      * In chat where command was issued     <br />
![aKickImage4](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/kickNR1.PNG)
      * In Admin channel     <br />
![KickImage5](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/kickNR2.PNG)
      * In users DM with Robo Rick     <br />
![KickImage6](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/kickNR3.png) 
#### Ban
   * $ban "__" "__" bans a member for a either a specified or unspecified reason
   * Sends an update in Admin channel and sends the reason in a DM to the member who was banned
   * Example: `$ban @DroTron#1863 for this really valid reason` 
   * If a reason is specified:
      * In chat where command was issued     <br />
![BanImage1](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/ban1.PNG)
      * In Admin channel     <br />
![BanImage2](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/ban2.PNG)
      * In users DM with Robo Rick     <br />
![BanImage3](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/ban3.png)
   * If no reason is specified:  
      * In text chat where the command was issued     <br />
![BanImage4](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/banNR1.PNG)
      * In Admin channel     <br />
![BanImage5](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/banNR2.PNG)
      * In users DM with Robo Rick     <br />
![BanImage6](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/banNR3.png)
#### Unban
   * $unban unbans a user that was previously banned
   * Example: `$unban DroTron#1863` 
   * **Important**: in ban and kick use @DroTron after the command but here use DroTron#1863 with no @
      * In the admin channel     <br />
![UnbanImage1](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/unban1.PNG)
      * In the users DM with Robo Rick     <br />
![UnbanImage2](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/unban2.png)
#### Tempban
   * `$tempban user days reason` bans a user for a certain number of days for a reason and then unbans them
   * Example: `$tempban @Knightmare 2 because he sucks` 
   * **Important**: This command is not perfect, if Robo Rick is restarted or updated while a temporary ban is in place he will forget the ban and will not execute the unban. This is a known issue and is in the pipeline to be fixed.
   * Robo Rick sends an announcement in the admin channel and sends the user a DM
      * In the admin channel     <br />
![TempbanImage1](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/tempban1.PNG)
      * In the users DM with Robo Rick     <br />
![TempbanImage2](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/tempban2.png)
      * In the users DM with Robo Rick after the time has passed     <br />
![TempbanImage3](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/tempban3.png)
      * In the admin channel after the time has passed     <br />
![TempbanImage4](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/tempban4.PNG)
#### Error handling
   * Sends an error if a member tries to use a command they do not have access to       <br />
![ErrorHandlingImage](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/errorhandling.png)   
#### 3070/3080 Stock announcement
   * IMPORTANT: If you use the bot I host you will not be able to use this command
   * This command essentially lets you broadcast a preset message to two channels with a simple command
#### Help
   * $help is here! Type this to get a less detailed summary of what is above.       <br /> 
![HelpImage](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/help.PNG)

# Git Command
`git clone https://github.com/DroTron/Robo-Rick`
*  Clones entire repository
*  add `~/FOLDER/SUBFOLDER` after PROGRAM.m to clone to specific folder
   * Ex: `git clone https://github.com/DroTron/Robo-Rick ~/Robo-Rick`
   * to clone repository to a folder in home named Robo-Rick
