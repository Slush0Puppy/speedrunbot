from discord.ext import commands

from utility import pformat, makelist       #pformat used to format user inputs
import srbot      #imports command functions

class Src(commands.Cog):
    """Communicate with speedrun.com"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx,error):
        if not isinstance(error, commands.CommandNotFound):
            await ctx.send("Something went wrong! Make sure everything is formatted and spelled correctly.")

    @commands.command(name="leaderboard", aliases=["lb"], description="test")
    async def leaderboard(self, ctx, game=None, cat="", subcat=""):
        if game: #checks if a game has been entered
            await ctx.send(srbot.leaderboard(pformat(game), pformat(cat), subcat))
        else:    #if not, send the result of the +help command
            await ctx.send(ctx.prefix + srbot.srbot_help["leaderboard"])

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency*1000)}ms')

    @commands.command(name="worldrecord", aliases=["wr"])
    async def worldrecord(self, ctx, game=None, cat="", subcat=""):
        if game:
            await ctx.send(srbot.worldrecord(pformat(game), pformat(cat), subcat))
        else:
            await ctx.send(ctx.prefix + srbot.srbot_help["worldrecord"])

    @commands.command(name="wrcount", aliases=["wrs"])
    async def wrcount(self, ctx, user=None, platform=""):
        if user:
            if (user[0]+user[-1]) == "[]":
                for each in user[1:-1].split(','):
                    print(each)
                    await ctx.author.send(srbot.wrcount(pformat(each), platform))
            else:
                await ctx.send(srbot.wrcount(user, platform))
        else:
            await ctx.send(ctx.prefix + srbot.srbot_help["wrcount"])

    @commands.command(name="modcount", aliases=["mods"])
    async def modcount(self, ctx, user=None):
        if user:
            if (user[0]+user[-1]) == "[]":
                for each in user[1:-1].split(','):
                    print(each)
                    await ctx.author.send(srbot.modcount(pformat(each)))
            else:
                await ctx.send(srbot.modcount(user))
        else:
            await ctx.send(ctx.prefix + srbot.srbot_help["modcount"])

    @commands.command(name="runcount", aliases=["runs"])
    async def runcount(self, ctx, user=None, platform=""):
        if user:
            if (user[0]+user[-1]) == "[]":
                for each in user[1:-1].split(','):
                    print(each)
                    await ctx.author.send(srbot.runcount(pformat(each), platform))
            else:
                await ctx.send(srbot.runcount(user, platform))
        else:
            await ctx.send(ctx.prefix + srbot.srbot_help["runcount"])

    @commands.command(name="categories", aliases=["cats"])
    async def categories(self, ctx, game=None):
        if game:
            await ctx.send(makelist(list(srbot.cats(pformat(game)).values())))
        else:
            await ctx.send(ctx.prefix + srbot.srbot_help["categories"])

    @commands.command(name="commands", aliases=["coms"])
    async def srbot_commands(self, ctx):
        await ctx.send("Commands:\n"+"+leaderboard, +worldrecord, +wrcount, +modcount, +runcount, +categories, "+
                       "+source, +invite, +ping, +help\n"+
            "Do +help [command] for more info.")

    @commands.command(name="invite", aliases=["add"])
    async def invite(self, ctx):
        await ctx.send("To add speedrun.bot to your server, click here:\n<"+
                      discord.utils.oauth_url(self.bot.user.id, permissions=None, guild=None, redirect_uri=None)+">")

    @commands.command(name="source", aliases=["credit","credits","code","sourcecode"])
    async def source(self, ctx):
        await ctx.send("The source code is available at https://github.com/Slush0Puppy/speedrunbot")

    @commands.command(name="help", aliases=["?"])
    async def command_help(self, ctx, command=""):
        if command:
            await ctx.send(ctx.prefix + srbot.srbot_help[self.bot.get_command(command).name])
        else:
            await ctx.send(srbot.srbot_help[""])

def setup(bot):
    bot.add_cog(Src(bot))
