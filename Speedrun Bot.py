import discord
import urllib.request, json 
from discord.ext import commands

from utility import pformat, makelist       #pformat used to format user inputs
import srbot      #imports command functions


##  Bot Setup
description = "A bot connected to the speedrun.com api."
bot_prefix = "+"

client = commands.Bot(description = description, command_prefix = bot_prefix)

client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='Speedruns | +help'))
    print("Ready\n" + "\nName:\t\t " + client.user.name + "\nID:\t\t " + str(client.user.id) +
          "\nDiscord Version: " + discord.__version__ + "\n")
##  Bot Setup

@client.event
async def on_message(message):
    msg = message.content
    author = str(message.author)
    channel = message.channel

    await client.process_commands(message)

@client.command(name="leaderboard", aliases=["lb"], description="test")
async def leaderboard(ctx, game=None, cat="", subcat=""):
    if game: #checks if a game has been entered
        await ctx.send(srbot.leaderboard(pformat(game), pformat(cat), subcat))
    else:    #if not, send the result of the +help command
        await ctx.send(bot_prefix + srbot.srbot_help["leaderboard"])

@client.command(name="worldrecord", aliases=["wr"])
async def worldrecord(ctx, game=None, cat="", subcat=""):
    if game:
        await ctx.send(srbot.worldrecord(pformat(game), pformat(cat), subcat))
    else:
        await ctx.send(bot_prefix + srbot.srbot_help["worldrecord"])

@client.command(name="wrcount", aliases=["wrs"])
async def wrcount(ctx, user=None, platform=""):
    if user:
        if (user[0]+user[-1]) == "[]":
            for each in user[1:-1].split(','):
                print(each)
                await ctx.author.send(srbot.wrcount(pformat(each), platform))
        else:
            await ctx.send(srbot.wrcount(user, platform))
    else:
        await ctx.send(bot_prefix + srbot.srbot_help["wrcount"])

@client.command(name="modcount", aliases=["mods"])
async def modcount(ctx, user=None):
    if user:
        if (user[0]+user[-1]) == "[]":
            for each in user[1:-1].split(','):
                print(each)
                await ctx.author.send(srbot.modcount(pformat(each)))
        else:
            await ctx.send(srbot.modcount(user))
    else:
        await ctx.send(bot_prefix + srbot.srbot_help["modcount"])

@client.command(name="runcount", aliases=["runs"])
async def runcount(ctx, user=None, platform=""):
    if user:
        if (user[0]+user[-1]) == "[]":
            for each in user[1:-1].split(','):
                print(each)
                await ctx.author.send(srbot.runcount(pformat(each), platform))
        else:
            await ctx.send(srbot.runcount(user, platform))
    else:
        await ctx.send(bot_prefix + srbot.srbot_help["runcount"])

@client.command(name="categories", aliases=["cats"])
async def categories(ctx, game=None):
    if game:
        await ctx.send(makelist(list(srbot.cats(pformat(game)).values())))
    else:
        await ctx.send(bot_prefix + srbot.srbot_help["categories"])

@client.command(name="commands", aliases=["coms"])
async def srbot_commands(ctx):
    await ctx.send("Commands:\n"+"+leaderboard, +worldrecord, +wrcount, +modcount, +runcount, +categories, "+
                   "+source, +invite, +help\n"+
        "Do +help [command] for more info.")

@client.command(name="invite", aliases=["add"]) # !!! Change this if you are hosting the bot yourself.
async def invite(ctx):
    await ctx.send("To add speedrun.bot to your server, click here:\n"+
                   "https://discordapp.com/oauth2/authorize?client_id=644879546650198016&scope=bot")

@client.command(name="source", aliases=["credit","credits","code","sourcecode"])
async def source(ctx):
    await ctx.send("The source code is available at https://github.com/Slush0Puppy/speedrunbot")

@client.command(name="help", aliases=["?"])
async def command_help(ctx, command=""):
    if command:
        await ctx.send(bot_prefix + srbot.srbot_help[client.get_command(command).name])
    else:
        await ctx.send(srbot.srbot_help[""])

@client.event
async def on_command_error(ctx,error):
    if not isinstance(error, commands.CommandNotFound):
        await ctx.send("Something went wrong! Make sure everything is formatted and spelled correctly.")

 
print("Starting up...")

tokenfile = open('token.txt')   #Make a text file called token.txt containing token
token = tokenfile.read()
tokenfile.close()

client.run(token)
