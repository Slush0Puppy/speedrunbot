import discord
import random
import time
import math
import urllib.request, json 
from discord.ext import commands

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
    "help": "+help [command]\n"+"Explains how a command works.",
    "default": "This is SpeedrunBot, made by conor and SlushPuppy.\n\n"+
        "To see all of the commands, do +commands, then do +help <command> for more information. <> denotes a "+
    "required parameter, and [] denotes an optional parameter. Parameters are always separated by commas (,).\n"+
    "If a command has parameter <user>, it can be replaced by a list of usernames by putting an asterisk (*) in"+
    "place of the name, then ending the command with a list of names prefixed with slashes like so:\n"+
    "```+runs *, Web /SlushPuppy/conormcmahon/SaturnRunsGames```\n"+
    "To ask for help or report an issue, message Slush Puppy#4986."
    }

month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4]) #converts 1 to 1st etc



platforms = {}
with urllib.request.urlopen("https://www.speedrun.com/api/v1/platforms?max=10000") as platurl:
    platdata = json.loads(platurl.read().decode())
    for each in platdata['data']:
        platforms[each['name']]=each['id']
#print(platforms)
    

def pformat(s):
    s=s.replace(' ','_')
    for eachchar in "%()":
            s = s.replace(eachchar,'')
    return s
    

def realtime(time): # turns XXX.xxx into h m s ms
    ms = int(time*1000)
    s,ms = divmod(ms,1000)
    m,s = divmod(s,60)
    h,m = divmod(m,60)  # separates time into h m s ms
    ms = "{:03d}".format(ms)
    s = "{:02d}".format(s)  #pads ms and s with 0s
    if h>0:
        m = "{:02d}".format(m)  #if in hours, pad m with 0s
    return ((h>0) * (str(h)+'h ')) + str(m)+'m ' + str(s)+'s ' + ((str(ms)+'ms') * (ms!='000')) #src formatting

def makelist(arr): # turns array into syndetic list
    output = ''
    for i in range(len(arr)):
        output += arr[i]
        if i < len(arr)-1 and len(arr)>2:
            output += ', '
        if i == len(arr)-2:
            if len(arr)<=2:
                output += ' '
            output += 'and '
    return output

def username(userid):       #gets username from userid
    with urllib.request.urlopen("https://www.speedrun.com/api/v1/users/" + userid) as url:
        userdata = json.loads(url.read().decode())          #gets information from speedrun.com api
        return userdata['data']['names']['international']   #reads the international name from api

def userid(username):
    with urllib.request.urlopen("https://www.speedrun.com/api/v1/users/" + username) as url:
        userdata = json.loads(url.read().decode())
        return userdata['data']['id']

def subcats(game,category):  # gets dictionary of subcategory ids. subcats[var] = id
    catsdict=cats(game)
    for each in catsdict:
        if pformat(catsdict[each].lower())==category.lower():###################################
            category = each
    variables={}
    categories={}
    with urllib.request.urlopen("https://www.speedrun.com/api/v1/games/" + game + "/variables") as url:
        vardata = json.loads(url.read().decode())
        for each in vardata['data']:
            if (each['scope']['type']=="full-game" and each['is-subcategory'] and
                each['category'].lower()==category.lower()):   #finds full-game subcategories
                for each2 in each['values']['values']:
                    variables[each['values']['values'][each2]['label']] = [each['id'],each2]
                    
        return variables
    

def cats(game): # gets dictionary of category ids. cats[id] = var
    categories={}
    with urllib.request.urlopen("https://www.speedrun.com/api/v1/games/" + game +
                                "/categories?type=\"per-game\"") as url:
        catdata = json.loads(url.read().decode())
        for each in catdata['data']:
            categories[each['id']] = each['name']
    return categories

#c=cats('cm')
#for each in c:
#    if c[each]=='Any%':
#        aaa=each
#print(subcats('cm',aaa))
###


def leaderboard(game, category="", subcategory=""):    #prints top 10 runs of a category
    if category == "":
        category = pformat(list(cats(game))[0])
    output = "```"
    varUrl = "" #This is put at the end of the url to filter for runs with a certain subcategory
    subcategories = subcats(game,category)
    for each in subcategories:
        if subcategory.lower() == each.lower():
            subcategory = each
    
    if subcategory in subcategories:
        subcatid = subcategories[subcategory]
        varUrl = "&var-"+subcatid[0]+"="+subcatid[1]
        
    with urllib.request.urlopen("https://www.speedrun.com/api/v1/leaderboards/"+game+"/category/"+category+
                                "?top=10"+varUrl) as url:
        leaderboarddata = json.loads(url.read().decode())   #gets information from speedrun.com api
        runs = leaderboarddata['data']['runs']              #gets all top 10 runs

        for each in runs:
            output += (" " * (each['place']<10) + ordinal(each['place']) + ": ")
            output += (realtime(each['run']['times']['primary_t'])+" - ")
            players=[]
            playercount = len(each['run']['players'])
            for eachPlayer in each['run']['players']:
                if 'id' in eachPlayer:
                    players.append(username(eachPlayer['id']))
                else:
                    players.append(eachPlayer['name'])
            output += (makelist(players) + "\n")
        output += '```'
        return output


def worldrecord(game,category="",subcategory=""):
    if category == "":
        category = pformat(list(cats(game))[0])
    print(category) #doesn't work for nmd :(
    wr = {'game':'','category':'','subcategory':'','time':'','runner':'','video':'','date':'','desc':''}
    
    varUrl = "" #This is put at the end of the url to filter for runs with a certain subcategory
    subcategories = subcats(game,category)
    for each in subcategories:
        if subcategory.lower() == each.lower():
            subcategory = each
            wr['subcategory'] = " - "+each
    if subcategory in subcategories:
        subcatid = subcategories[subcategory]
        varUrl = "&var-"+subcatid[0]+"="+subcatid[1]

    with urllib.request.urlopen("https://www.speedrun.com/api/v1/leaderboards/"+game+"/category/"+category+
                                "?top=1"+varUrl) as url:
        rundata = json.loads(url.read().decode())
        run = rundata['data']['runs'][0]
        
        with urllib.request.urlopen("https://www.speedrun.com/api/v1/games/"+game) as gameurl:
            wr['game'] = json.loads(gameurl.read().decode())['data']['names']['international']

        wr['category'] = cats(game)[rundata['data']['category']]
        wr['time'] = realtime(run['run']['times']['primary_t'])
        try:
            wr['video'] = run['run']['videos']['links'][0]['uri']
        except:
            wr['video'] = "None"
        if wr['desc']:
            wr['desc'] = '"'+run['run']['comment']+'"'
        date = run['run']['date'].split('T')[0].split('-')
        wr['date'] = ordinal(int(date[2])) + ' ' + month[int(date[1])-1] + ' ' + str(date[0])

        players=[]
        playercount = len(run['run']['players'])
        for eachPlayer in run['run']['players']:
            if 'id' in eachPlayer:
                players.append(username(eachPlayer['id']))
            else:
                players.append(eachPlayer['name'])
        wr['runner'] = makelist(players)

    return(wr['game']+": "+wr['category']+wr['subcategory']+" in "+wr['time']+" by "+wr['runner']+"\n"+
           "Video: "+wr['video']+"\n"+
           "Played on "+wr['date']+"\n"+
           wr['desc'])


def wrcount(user,platform=""):
    for each in platforms:      #fixes case
        if each.lower()==platform.lower():
            platform = each
    fullgamewrs = 0
    levelwrs = 0
    with urllib.request.urlopen("https://www.speedrun.com/api/v1/users/" + user + "/personal-bests") as url:
        pbdata = json.loads(url.read().decode())

        if platform:
            if platform in platforms:
                for each in pbdata['data']:
                    if each['place']==1 and each['run']['system']['platform']==platforms[platform]:
                        # iterates through 1st place runs
                        if each['run']['level']:    # checks if level or full game
                            levelwrs+=1
                        else:
                            fullgamewrs+=1
            elif platform.lower()=="mobile":
                for each in pbdata['data']:
                    if each['place']==1 and each['run']['system']['platform'] in [platforms["iOS"],
                                                                                  platforms["Android"],
                                                                           platforms["Windows Phone"]]:
                        if each['run']['level']:
                            levelwrs+=1
                        else:
                            fullgamewrs+=1
        else:
            for each in pbdata['data']:
                if each['place']==1:
                    if each['run']['level']:    # checks if level or full game
                        levelwrs+=1
                    else:
                        fullgamewrs+=1
    return (username(userid(user)) + ' has ' + str(levelwrs+fullgamewrs) + " world records"+bool(platform)*(" on "+platform)+":\n"+#username userid
            str(fullgamewrs) + ' full game records and ' + str(levelwrs) + ' IL records.\n')#    fixes capitalisation

                
def modcount(user):
    with urllib.request.urlopen("https://www.speedrun.com/api/v1/games?moderator=" + userid(user)) as url:
        moddata = json.loads(url.read().decode())
        games = len(moddata['data'])
        if games == 0:
            games = 'no'
    with urllib.request.urlopen("https://www.speedrun.com/api/v1/series?moderator=" + userid(user)) as url:
        moddata = json.loads(url.read().decode())
        series = len(moddata['data'])
        if series == 0:
            series = 'no'
    return (username(userid(user)) + ' moderates ' + str(games) + " game" + ((games!=1)*'s') + " and " +
            str(series) + " series.\n")


def runcount(user,platform="",obsolete="yes"):
    for each in platforms:      #fixes case
        if each.lower()==platform.lower():
            platform = each
    if platform.lower()=="all":
        platform=""
    rundata = []
    runs = 0
    fullruns = 0
    if obsolete.lower()=="no" or obsolete.lower()=="-":
        with urllib.request.urlopen("https://www.speedrun.com/api/v1/users/" + user + "/personal-bests") as url:
            data = json.loads(url.read().decode())
            for each in data['data']:
                rundata.append(each['run'])
    else:
        offset=0
        repeat=True
        while repeat:
            with urllib.request.urlopen("https://www.speedrun.com/api/v1/runs?user=" + userid(user) +
                                        "&max=200&offset="+str(offset)) as url:
                data = json.loads(url.read().decode())
                rundata += data['data']
                offset+=200
                try:
                    if data['pagination']['links'][-1]['rel']=="prev":  #if last link is prev page, this is last page
                        repeat=False
                except:
                    repeat=False
            
    if platform:
        for each in rundata:
            if platform in platforms:
                if each['system']['platform'] == platforms[platform]:
                    if each['level']==None:
                        fullruns += 1
                    runs+=1
            elif platform.lower() == "mobile":
                if each['system']['platform'] in [platforms["iOS"],platforms["Android"],platforms["Windows Phone"]]:
                    if each['level']==None:
                        fullruns += 1
                    runs+=1
    else:
        for each in rundata:
            if each['level']==None:
                fullruns += 1
            runs+=1

    return (username(userid(user))+" has "+str(runs)+" runs"+bool(platform)*(" on "+platform)+":\n"+
            str(fullruns)+" full game runs and "+str(runs-fullruns)+" IL runs.\n")

######################
        

description = "A bot connected to the speedrun.com api."
bot_prefix = "-"

client = commands.Bot(description = description, command_prefix = bot_prefix)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='Speedrunning'))
    print("Suited and Booted\n" + "\nName:\t\t " + client.user.name + "\nID:\t\t " + str(client.user.id) +
          "\nDiscord Version: " + discord.__version__ + "\n")

@client.event
async def on_message(message):
    msg = message.content
    author = str(message.author)
    channel = message.channel

    if len(msg)>0 and msg[0]=="+" and author!="SpeedrunBot#8305":
        response = ""
        command = msg.split(' ')[0]
##########vvvvvvvvvvvvvvvvvvvvvvvvvvvvv
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
            #except:
            #    response = "Something went wrong! Make sure spelling and syntax are correct."
        if response:
            await channel.send(response)


                    
                        
 
print("Starting up...")
client.run("")#insert bot token into quotation marks
