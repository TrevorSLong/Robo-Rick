# Robo-Rick
This repository contains the code that runs the Discord bot "Robo Rick". Robo rick can be added to your server with `https://discord.com/oauth2/authorize?client_id=827681932660965377&scope=bot`
This page is designed to be a help page for the bot itself and also used for learning how to program your own bot. DO NOT COPY THIS CODE AND DO NOT USE IT FOR PROFIT!
The functionality is listed below:

#### Welcome message
   * Welcomes new members into the server by name with a random welcome message from Rick and Morty
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/welcomemessages.PNG)
#### Welcome DM
   * Welcomes new members into the server by sending them a DM
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/welcomedm.PNG)
#### Chat response
   * Responds to "hello" with "Wubbalubbadubdub"
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/hello.PNG)
#### Changes bot status
   * Robo Ricks status is "Listening to Snake Jazz"
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/status.PNG)
#### Ping
   * Responds to $ping with "pong" and the bot server latency
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/ping.PNG)
#### UpdateChannel
   * Use $updatechannel to change the channel Robo Rick sends all public updates
   * The channel will be changed to the channel that you send the command in
   * By default this channel will be the top text channel in the server
   * To change this permission, the user must have the "Ban members" permission in the Discord server
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/updatechannel.PNG)
#### AdminChannel
   * Use $adminchannel to change the channel Robo Rick sends all admin updates
   * The channel will be changed to the channel that you send the command in
   * By default this channel will be the top text channel in the server
   * To change this permission, the user must have the "Ban members" permission in the Discord server
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/adminchannel.PNG)
#### Join server message
   * Robo Rick sends a message in the default channel when he joins the server for the first time introducing himself
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/joinmessage.PNG)
#### Announcements
   * $announce "_____" will send an announcement in the updates channel in your server. To change the channel it is sent in use $updatechannel
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/announce.PNG)
=======
#### Kick
   * $kick "__" "__" kicks a member for a either a specified or unspecified reason
   * Sends an update in Admin channel and sends the reason in a DM to the member who was kicked
   * Example: `$kick @DroTron#1863 for this really valid reason` 
   * If a reason is specified:
      * In chat where command was issued
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/kick1.PNG)
      * In Admin channel
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/kick2.PNG)
      * In users DM with Robo Rick
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/kick3.png)
   * If no reason is specified:
      * In chat where command was issued
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/kickNR1.PNG)
      * In Admin channel
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/kickNR2.PNG)
      * In users DM with Robo Rick
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/kickNR3.png) 
#### Ban
   * $ban "__" "__" bans a member for a either a specified or unspecified reason
   * Sends an update in Admin channel and sends the reason in a DM to the member who was banned
   * Example: `$ban @DroTron#1863 for this really valid reason` 
   * If a reason is specified:
      * In chat where command was issued
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/ban1.PNG)
      * In Admin channel
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/ban2.PNG)
      * In users DM with Robo Rick
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/ban3.png)
   * If no reason is specified:  
      * In chat where command was issued
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/banNR1.PNG)
      * In Admin channel
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/banNR2.PNG)
      * In users DM with Robo Rick
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/banNR3.png)
#### Error handling
   * Sends an error if a member tries to use a command they do not have access to  
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/errorhandling.png)   
#### 3070/3080 Stock announcement
   * IMPORTANT: If you use the bot I host you will not be able to use this command
   * This command essentially lets you broadcast a preset message to two channels with a simple command
#### Help
   * $help is here! Type this to get a less detailed summary of what is above.   
![alt text](https://raw.githubusercontent.com/DroTron/Robo-Rick/main/Screenshots/help.PNG)

# Git Command
`git clone https://github.com/DroTron/Robo-Rick`
*  Clones entire repository
*  add `~/FOLDER/SUBFOLDER` after PROGRAM.m to clone to specific folder
   * Ex: `git clone https://github.com/DroTron/Robo-Rick ~/Robo-Rick`
   * to clone repository to a folder in home named Robo-Rick
