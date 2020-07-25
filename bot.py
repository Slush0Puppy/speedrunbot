import discord

from discord.ext import commands

initial_extensions = (
    "cogs.src",
    "cogs.admin"
)


class SpeedrunBot(commands.Bot):
    # The __init__ method is a standard method seen at the beginning of most classes
    # it declares the variables that will be used throughout the class
    def __init__(self):
        self.description = "A bot connected to the speedrun.com api."
        self.bot_prefix = "+"
        super().__init__(description = self.description, 
            command_prefix = self.bot_prefix, 
            allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=False))

        self.remove_command("help")

        # Load all extensions (see the cogs folder)
        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as extension:
                print(extension.args)

    async def on_message(self, message):
        msg = message.content
        author = str(message.author)
        channel = message.channel

        if message.author.bot:
            return

        await self.process_commands(message)

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name='Speedruns | +help'))
        print("Ready\n" + "\nName:\t\t " + self.user.name + "\nID:\t\t " + str(self.user.id) +
              "\nDiscord Version: " + discord.__version__ + "\n")


# the following if statement ensures that bot.py is the actual file being executed
# the alternative is that this file might be imported into another file (in which case, we don't run the following)
if __name__ == "__main__":
    print("Starting up...")
    try:
        with open('token.txt') as f:
            token = f.read()
        bot = SpeedrunBot()
        bot.run(token)
    except Exception as e:
        print(e.args)