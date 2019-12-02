import discord
import urllib.request, json 
from discord.ext import commands

from utility import *       #utility functions used by commands
from commands import *      #imports command functions


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

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='Speedrunning'))
    print("Suited and Booted\n" + "\nName:\t\t " + client.user.name + "\nID:\t\t " + str(client.user.id) +
          "\nDiscord Version: " + discord.__version__ + "\n")
##  Bot Setup


@client.event
async def on_message(message):
    msg = message.content
    author = str(message.author)
    channel = message.channel

    if len(msg)>0 and msg[0]=="+" and author!="SpeedrunBot#8305":
        response = ""
        command = msg.split(' ')[0]
        extraparams=msg.split('\n')[1:]  #extra params are used for doing multiple commands for a list of users
        extraparams = [each.strip(' ') for each in extraparams]      #Put a * in place of the <user> parameter
        if extraparams:
            while not extraparams[-1]:
                extraparams=extraparams[:-1]
        msg=msg.split('\n')[0]

        param = msg[len(command):].split(',')
        param = [each.strip(' ') for each in param]
        param = [pformat(each) for each in param[:2]]+param[2:]

        param += (3-len(param))*['']    #pads array with empty values to prevent errors
        
        if param == ['','',''] and command in alias and alias[command] not in ["help","commands"]:
            param[0] = command
            command = "+help"

        if command in alias:
            command = alias[command]
            #try:
            if command=="leaderboard":
                response = leaderboard(param[0],param[1],param[2])
            elif command=="worldrecord":
                response = worldrecord(param[0],param[1],param[2])
            elif command=="wrcount":
                if param[0]=='*':
                    for each in extraparams:
                        await channel.send(wrcount(each,param[1]))
                    response = "Done!"
                else:
                    response = wrcount(param[0],param[1])
            elif command=="modcount":
                if param[0]=='*':
                    for each in extraparams:
                        await channel.send(modcount(each))
                        response = "Done!"
                else:
                    response = [modcount(param[0])]
            elif command=="runcount":
                if param[0]=='*':
                    for each in extraparams:
                        await channel.send(runcount(each,param[1]))
                        response = "Done!"
                else:
                    response = runcount(param[0],param[1])
            elif command=="cats":
                categories = cats(param[0])
                response = makelist(list(categories.values()))
            elif command=="commands":
                response = helpguide["commands"]
            elif command=="help":
                if param[0] in alias:
                    param[0] = [alias[param[0]]]
                    response = helpguide[param[0]]
                elif '+'+param[0] in alias:
                    response = helpguide[alias['+'+param[0]]]
                elif param[0] == "":
                    response = helpguide["default"]
            except:
                response = "Something went wrong! Make sure spelling and syntax are correct."
        if response:
            await channel.send(response)


                    
                        
 
print("Starting up...")
client.run("")#insert token here
