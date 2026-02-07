# Robo-Rick

A Rick and Morty themed Discord bot for welcome messages, moderation, and server management.

[![Discord Bots](https://top.gg/api/widget/827681932660965377.svg)](https://top.gg/bot/827681932660965377)

## Add to Your Server

[Click here to add Robo Rick to your server](https://discord.com/api/oauth2/authorize?client_id=827681932660965377&permissions=1099511696470&scope=bot%20applications.commands)

## Features

### Bot Events
- **Welcome Messages** - Welcomes new members with random Rick and Morty quotes
- **Welcome DMs** - Sends new members a direct message introduction
- **Leave Messages** - Announces when members leave the server
- **Chat Response** - Responds to "rick" with "Wubbalubbadubdub"
- **Status** - Displays Rick and Morty themed status messages

### Slash Commands

| Command | Description | Permission |
|---------|-------------|------------|
| `/ping` | Check bot latency | Everyone |
| `/donate` | Support development | Everyone |
| `/servercount` | Show how many servers use Robo Rick | Everyone |
| `/announce <message> <channel>` | Send an announcement | Manage Server |
| `/kick <member> <reason>` | Kick a member with reason | Kick Members |
| `/ban <member> <reason>` | Ban a member with reason | Ban Members |
| `/unban <username>` | Unban a user | Ban Members |
| `/tempban <member> <reason> <days>` | Temporarily ban a member | Ban Members |
| `/updatechannel <channel>` | Set the welcome/updates channel | Manage Server |
| `/adminchannel <channel>` | Set the admin notifications channel | Manage Server |
| `/checkupdatechannel` | Show current update channel | Manage Server |
| `/checkadminchannel` | Show current admin channel | Manage Server |

---

## Self-Hosting

Want to run your own instance? Follow these instructions.

### Prerequisites

1. **Create a Discord Application**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications/)
   - Click "New Application" and name it
   - Go to **Bot** section and click "Add Bot"
   - Copy the **Token** (you'll need this later)

2. **Enable Privileged Intents**
   - In the Bot section, scroll to "Privileged Gateway Intents"
   - Enable ALL THREE:
     - Presence Intent
     - Server Members Intent
     - Message Content Intent
   - Save changes

3. **Generate Invite URL**
   - Go to **OAuth2 > URL Generator**
   - Select scopes: `bot`, `applications.commands`
   - Select permissions: `Send Messages`, `Embed Links`, `Read Message History`, `Kick Members`, `Ban Members`, `Manage Guild`
   - Use the generated URL to add the bot to your server

### Docker Deployment (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/TrevorSLong/Robo-Rick.git
   cd Robo-Rick
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your values:
   ```
   DISCORD_TOKEN=your_bot_token_here
   BOT_UPDATE_CHANNEL=channel_id_for_restart_notifications
   dbl_token=optional_topgg_token
   ```

3. **Create data files**
   ```bash
   echo '{}' > adminchannels.json
   echo '{}' > welcomechannels.json
   ```

4. **Start the bot**
   ```bash
   docker compose up -d --build
   ```

5. **Check logs**
   ```bash
   docker logs -f robo-rick
   ```

### Manual Deployment

1. **Requirements**
   - Python 3.10+
   - pip

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your bot token
   ```

4. **Create data files**
   ```bash
   echo '{}' > adminchannels.json
   echo '{}' > welcomechannels.json
   ```

5. **Run the bot**
   ```bash
   python RoboRickSlash.py
   ```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DISCORD_TOKEN` | Yes | Your Discord bot token |
| `BOT_UPDATE_CHANNEL` | No | Channel ID for restart notifications |
| `dbl_token` | No | Top.gg token for server count stats |

---

## Development

This bot was originally created by two college students as a learning project.

### Tech Stack
- Python 3.10+
- discord.py 2.x (with native slash commands)
- Docker for deployment

### Contributing
Contributions are welcome! Please feel free to submit pull requests.

### Support Development
If you enjoy Robo Rick, consider [donating](https://www.paypal.com/donate?hosted_button_id=RBYUJ5M6QSB52) to help fund development and hosting costs.

---

## License

See [LICENSE](LICENSE) for details.

**DO NOT COPY THIS CODE FOR PROFIT.** This project is for learning and personal use.
