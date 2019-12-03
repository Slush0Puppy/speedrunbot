# SpeedrunBot

SpeedrunBot is a discord.py bot which accesses run information from the speedrun.com REST API. Its purpose is to provide a fast way to look up speedrun information.

## Usage

By default, the bot's prefix is +. To get a list of commands, type **+commands**. To see what a command does, type **+help [command]**.
The output will be the format for using the command, such as **+leaderboard game [category] [subcategory]**, alongside a brief description of what the command does.

### Advanced Usage

For the +wrcount and +runcount commands, *Mobile* can be used as a **platform** parameter which includes iOS, Android, and Windows Phone.

Also, in place of the parameter **user**, users can place an array containing a list of names (separated by commas) for which the commands will be executed. For example, instead of typing **+wrs user1 iOS** then **+wrs user2 iOS** then **+wrs user3 iOS**, users can type **+wrs [user1,user2,user3] iOS** to get the same output in one command. Note that this sends the result to the person executing the command as a direct message to reduce spam.

## Usage Permissions

Features from this bot may be added to other bots as long as this page (https://github.com/Slush0Puppy/speedrunbot) is credited somewhere such as in documentation or in a command.
