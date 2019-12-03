import discord
import urllib.request, json 
from discord.ext import commands

from utility import *       #utility functions used by commands
import srbot      #imports command functions


#   All command aliases
alias = {
    "+leaderboard": "leaderboard",
    "+lb": "leaderboard",
    "+worldrecord": "worldrecord",
    "+wr": "worldrecord",
    "+wrcount": "wrcount",
    "+wrs": "wrcount",
    "+modcount": "modcount",
    "+mods": "modcount",
    "+runcount":"runcount",
    "+runs":"runcount",
    "+categories":"cats",
    "+cats":"cats",
    "+help": "help",
    "+commands": "commands",
    "+coms": "commands",
    "+?": "help"
    }


#   List of outputs from the +help command
helpguide = {
    "commands": "Commands:\n"+"+leaderboard, +worldrecord, +wrcount, +modcount, +runcount, +categories, +help\n"+
        "Do +help [command] for more info.",
    "leaderboard": "+lb <game>, [category] [subcategory]\n"+"Displays the top 10 speedruns.",
    "worldrecord": "+wr <game>, [category] [subcategory]\n"+
        "Gives detailed information about the world record.",
    "wrcount": "+wrcount <user>, [platform]\n"+"Counts the number of world records a user has.",
    "modcount": "+mods <user>\n"+"Counts the number of games a user moderates.",
    "runcount": "+runs <user>, [platform], [obsolete]\n"+"Counts the number of runs by a user. "+
        "by default, obsoleted runs are also counted.",
    "cats": "+cats <game>\n"+"Shows all categories of a game.",
    "help": "+help [command]\n"+"Describes what a command does.",
    "default": "This is SpeedrunBot, made by conor and SlushPuppy.\n\n"+
        "To see all of the commands, do +commands, then do +help <command> for more information.\n<> means a "+
    "required parameter, and [] means an optional parameter. Parameters are always separated by commas (,).\n"+
    "If a command has parameter <user>, it can be replaced by a list of usernames by putting an asterisk (*) in"+
    "place of the name, then ending the command with a list of names prefixed with slashes like so:\n"+
    "```+runs *, Web /SlushPuppy/conormcmahon/SaturnRunsGames```\n"+
    "To ask for help or report an issue, message Slush Puppy#4986 on Discord."
    }


def pformat(s):
    s=s.replace(' ','_')
    for eachchar in "%()":
            s = s.replace(eachchar,'')
    return s


##  Bot Setup
description = "A bot connected to the speedrun.com api."
bot_prefix = "+"

client = commands.Bot(description = description, command_prefix = bot_prefix)

client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='Speedrunning'))
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
    await ctx.send(srbot.cats(pformat(game)))

@client.command(name="commands", aliases=["coms"])
async def srbot_commands(ctx):
    await ctx.send("Commands:\n"+"+leaderboard, +worldrecord, +wrcount, +modcount, +runcount, +categories, +help\n"+
        "Do +help [command] for more info.")

@client.command(name="help", aliases=["?"])
async def help(ctx, command=""):
    await ctx.send(srbot.srbot_help[command])


 
print("Starting up...")
client.run("")#insert token here
