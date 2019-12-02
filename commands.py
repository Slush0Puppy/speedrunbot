from utility import *


#   +leaderboard
#   Displays the top 10 runs of a category
def leaderboard(game, category="", subcategory=""):
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

        if not runs:    #if the list of runs is empty:
            return "There are no submitted runs in this category."

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


#   +worldrecord
#   Displays information about the world record of a category
def worldrecord(game,category="",subcategory=""):
    if category == "":
        category = pformat(list(cats(game))[0])
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
        
        if not rundata['data']['runs']: #if there is no data for runs:
            return "There are no submitted runs in this category."
        
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


#   +wrcount
#   Counts the number of world records a user has (on a given platform if specified)
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
            elif platform.lower()=="mobile":    #group of platforms including all mobile platforms
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
    return (username(userid(user)) + ' has ' + str(levelwrs+fullgamewrs) +
            " world records"+bool(platform)*(" on "+platform)+":\n"+#username userid
            str(fullgamewrs) + ' full game records and ' + str(levelwrs) + ' IL records.\n')#   fixes capitalisation


#   +modcount
#   Counts the number of games and series a user moderates. 
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


#   +runcount
#   Counts the number of runs a user has submitted.
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
