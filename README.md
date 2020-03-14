# SpeedrunBot
SpeedrunBot is a discord.py bot which accesses run information from the speedrun.com REST API. Its purpose is to provide a fast way to look up speedrun information.
The official hosted version is\
https://discordapp.com/oauth2/authorize?client_id=644879546650198016&scope=bot.

## Usage (users)
By default, the bot's prefix is +. To get a list of commands, type **+commands**. To see what a command does, type **+help [command]**.
The output will be the format for using the command, such as **+leaderboard game [category] [subcategory]**, alongside a brief description of what the command does.
To enter a parameter with spaces, place quotation marks around it.

### Advanced Usage
For the +wrcount and +runcount commands, *Mobile* can be used as a **platform** parameter which includes iOS, Android, and Windows Phone.

Also, in place of the parameter **user**, users can place an array containing a list of names (separated by commas) for which the commands will be executed. For example, instead of typing **+wrs user1 iOS** then **+wrs user2 iOS** then **+wrs user3 iOS**, users can type **+wrs [user1,user2,user3] iOS** to get the same output in one command. Note that this sends the result to the person executing the command as a direct message to reduce spam.

## Usage (hosts/developers)
The main file for the bot is "Speedrun Bot.py", the other .py files containing functions that the main file imports.

Before running the bot, create a text file in the same directory called "token.txt". Its content must be the ID token for the bot, and nothing else. It is also recommended to change the text contained in the +invite command.

## Usage Permissions
Features from this bot may be added to other bots as long as this page (https://github.com/Slush0Puppy/speedrunbot) is credited somewhere such as in documentation or in a command.
