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
async def leaderboard(ctx, game, cat="", subcat=""):
    await ctx.send(srbot.leaderboard(pformat(game), pformat(cat), subcat))

@client.command(name="worldrecord", aliases=["wr"])
async def worldrecord(ctx, game, cat="", subcat=""):
    await ctx.send(srbot.worldrecord(pformat(game), pformat(cat), subcat))

@client.command(name="wrcount", aliases=["wrs"])
async def wrcount(ctx, user, platform=""):
    if (user[0]+user[-1]) == "[]":
        for each in user[1:-1].split(','):
            print(each)
            await ctx.author.send(srbot.wrcount, platform)()
    else:
        await ctx.send(srbot.wrcount(user, platform))

@client.command(name="modcount", aliases=["mods"])
async def modcount(ctx, user):
    if (user[0]+user[-1]) == "[]":
        for each in user[1:-1].split(','):
            print(each)
            await ctx.author.send(srbot.modcount(pformat(each)))
    else:
        await ctx.send(srbot.modcount(user))

@client.command(name="runcount", aliases=["runs"])
async def runcount(ctx, user, platform=""):
    if (user[0]+user[-1]) == "[]":
        for each in user[1:-1].split(','):
            print(each)
            await ctx.author.send(srbot.runcount(pformat(each), platform))
    else:
        await ctx.send(srbot.runcount(user, platform))

@client.command(name="categories", aliases=["cats"])
async def categories(ctx, game):
    await ctx.send(makelist(list(srbot.cats(pformat(game)).values())))

@client.command(name="commands", aliases=["coms"])
async def srbot_commands(ctx):
    await ctx.send("Commands:\n"+"+leaderboard, +worldrecord, +wrcount, +modcount, +runcount, +categories, +help\n"+
        "Do +help [command] for more info.")

@client.command(name="help", aliases=["?"])
async def help(ctx, command=""):
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
