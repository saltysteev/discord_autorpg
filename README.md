# autorpg

A discord bot game that players can idle and earn experience/fight monsters/gain items/level up/other fun stuff!

See a live leaderboard, overworld, and more at https://autorpg.deadnet.org

# self-hosted installation

- Go to the Discord Developer Portal (https://discord.com/developers/applications)
  - Create a bot application and generate a token / app ID
- Use pip to install dependencies (use requirements.txt or install one by one manually)
- Edit config.example.py and change to your liking.
- Rename config.example.py to config.py
- Run bot.py

# self-hosted setup
- Once bot is running, invite into your Discord server
- The bot should automatically register everyone in the server and start playing
  - If not, use the command /initialize to fix the usercount. This command does NOT reset progress.
- The bot should also create the item rarity server roles to provide a bit of flair to items.
  - If not, use the command /createroles
- See admincomms.py for a list of commands the server admin can use