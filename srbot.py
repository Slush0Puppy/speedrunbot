from utility import *
from aiohttp import ClientSession

session = ClientSession()

srbot_help = {
    "": "This is SpeedrunBot, made by Slush0Puppy.\n"
    + "To see all commands, do **+commands**, then **+help [command]** for more information.\n"
    + "To enter a parameter with spaces, place quotation marks around it.\n"
    + "For help or feedback, contact Slush Puppy#4986 on discord, or email slushpuppycontact@gmail.com\n"
    + "To add this bot to your server, type **+invite**",
    "leaderboard": "**leaderboard game [category] [subcategory]**\n"
    + "Displays the top 10 runs of a category.",
    "worldrecord": "**worldrecord game [category] [subcategory]**\n"
    + "Gives detailed information about the world record for a category.",
    "wrcount": "**wrcount user [platform]**\n"
    + "Counts the number of world records a user has.",
    "modcount": "**modcount user**\n" + "Counts the number of games a user moderates.",
    "runcount": "**runcount user [platform = all] [obsolete = true]**\n"
    + "Counts the number of runs by a user. By default, obsoleted runs are also counted.",
    "gamesplayed": "**gamesplayed user**\n"
    + "Counts the number of games a user has a run accepted in.",
    "categories": "**categories game**\n" + "Shows all categories of a game.",
    "source": "**source**\n" + "Provides a link to the bot's source code and homepage.",
    "invite": "**invite**\n" + "Shows the bot's invite link.",
    "help": "**help [command]**\n" + "Describes what a command does.",
    "ping": "**ping** \n" + "Shows the ping to discord.",
}
#   +cats
#   Creates a dictionary with information about a game's categories. key: id, value: name
async def cats(game):
    categories = {}
    async with session.get(
        "https://www.speedrun.com/api/v1/games/" + game + "/categories"
    ) as url:
        catdata = loads(await url.text())
        for each in catdata["data"]:
            if each["type"] == "per-game":
                categories[each["id"]] = each["name"]
    return categories


#   (Not actually a command but used often by other commands)
#   Creates a dictionary with information about a category's subcategories. key: name, value: id
async def subcats(game, category):
    catsdict = await cats(game)
    for each in catsdict:
        if (
            pformat(catsdict[each].lower()) == category.lower()
        ):  
            category = each
    variables = {}
    async with session.get(
        "https://www.speedrun.com/api/v1/games/" + game + "/variables"
    ) as url:
        vardata = loads(await url.text())
        for each in vardata["data"]:
            if (
                each["scope"]["type"] == "full-game"
                and each["is-subcategory"]
                and each["category"]
                and each["category"].lower() == category.lower()
            ):  # finds full-game subcategories
                for each2 in each["values"]["values"]:
                    variables[each["values"]["values"][each2]["label"]] = [
                        each["id"],
                        each2,
                    ]
    return variables


#   +leaderboard
#   Displays the top 10 runs of a category
async def leaderboard(game, category="", subcategory=""):
    if category == "":
        category = pformat(list(await cats(game))[0])
    output = "```"
    varUrl = ""  # This is put at the end of the url to filter for runs with a certain subcategory
    subcategories = await subcats(game, category)
    for each in subcategories:
        if subcategory.lower() == each.lower():
            subcategory = each

    if subcategory in subcategories:
        subcatid = subcategories[subcategory]
        varUrl = "&var-" + subcatid[0] + "=" + subcatid[1]

    async with session.get(
        "https://www.speedrun.com/api/v1/leaderboards/"
        + game
        + "/category/"
        + category
        + "?top=10"
        + varUrl
    ) as url:
        leaderboarddata = loads(
            await url.text()
        )  # gets information from speedrun.com api
        runs = leaderboarddata["data"]["runs"]  # gets all top 10 runs

        if not runs:  # if the list of runs is empty:
            return "There are no submitted runs in this category."

        for each in runs:
            output += " " * (each["place"] < 10) + ordinal(each["place"]) + ": "
            output += realtime(each["run"]["times"]["primary_t"]) + " - "
            players = []
            playercount = len(each["run"]["players"])
            for eachPlayer in each["run"]["players"]:
                if "id" in eachPlayer:
                    players.append(username(eachPlayer["id"]))
                else:
                    players.append(eachPlayer["name"])
            output += makelist(players) + "\n"
        output += "```"
        return output


#   +worldrecord
#   Displays information about the world record of a category
async def worldrecord(game, category="", subcategory=""):
    if category == "":
        category = pformat(list(await cats(game))[0])
    wr = {
        "game": "",
        "category": "",
        "subcategory": "",
        "time": "",
        "runner": "",
        "video": "",
        "date": "",
        "desc": "",
    }

    varUrl = ""  # This is put at the end of the url to filter for runs with a certain subcategory
    subcategories = await subcats(game, category)
    for each in subcategories:
        if subcategory.lower() == each.lower():
            subcategory = each
            wr["subcategory"] = " - " + each
    if subcategory in subcategories:
        subcatid = subcategories[subcategory]
        varUrl = "&var-" + subcatid[0] + "=" + subcatid[1]

    async with session.get(
        "https://www.speedrun.com/api/v1/leaderboards/"
        + game
        + "/category/"
        + category
        + "?top=1"
        + varUrl
    ) as url:
        rundata = loads(await url.text())

        if not rundata["data"]["runs"]:  # if there is no data for runs:
            return "There are no submitted runs in this category."

        run = rundata["data"]["runs"][0]

        async with session.get(
            "https://www.speedrun.com/api/v1/games/" + game
        ) as gameurl:
            wr["game"] = loads(await gameurl.text())["data"]["names"]["international"]

        categories = await cats(game)
        wr["category"] = categories[rundata["data"]["category"]]
        wr["time"] = realtime(run["run"]["times"]["primary_t"])
        try:
            wr["video"] = run["run"]["videos"]["links"][0]["uri"]
        except:
            wr["video"] = "None"
        if wr["desc"]:
            wr["desc"] = '"' + run["run"]["comment"] + '"'
        date = run["run"]["date"].split("T")[0].split("-")
        wr["date"] = (
            ordinal(int(date[2])) + " " + month[int(date[1]) - 1] + " " + str(date[0])
        )

        players = []
        playercount = len(run["run"]["players"])
        for eachPlayer in run["run"]["players"]:
            if "id" in eachPlayer:
                players.append(username(eachPlayer["id"]))
            else:
                players.append(eachPlayer["name"])
        wr["runner"] = makelist(players)

    return (
        wr["game"]
        + ": "
        + wr["category"]
        + wr["subcategory"]
        + " in "
        + wr["time"]
        + " by "
        + wr["runner"]
        + "\n"
        + "Video: "
        + wr["video"]
        + "\n"
        + "Played on "
        + wr["date"]
        + "\n"
        + wr["desc"]
    )


#   +wrcount
#   Counts the number of world records a user has (on a given platform if specified)
async def wrcount(user, platform=""):
    for each in platforms:  # fixes case
        if each.lower() == platform.lower():
            platform = each
    fullgamewrs = 0
    levelwrs = 0
    async with session.get(
        "https://www.speedrun.com/api/v1/users/" + user + "/personal-bests"
    ) as url:
        pbdata = loads(await url.text())

        if platform:
            if platform in platforms:
                for each in pbdata["data"]:
                    if (
                        each["place"] == 1
                        and each["run"]["system"]["platform"] == platforms[platform]
                    ):
                        # iterates through 1st place runs
                        if each["run"]["level"]:  # checks if level or full game
                            levelwrs += 1
                        else:
                            fullgamewrs += 1
            elif (
                platform.lower() == "mobile"
            ):  # group of platforms including all mobile platforms
                for each in pbdata["data"]:
                    if each["place"] == 1 and each["run"]["system"]["platform"] in [
                        platforms["iOS"],
                        platforms["Android"],
                        platforms["Windows Phone"],
                    ]:
                        if each["run"]["level"]:
                            levelwrs += 1
                        else:
                            fullgamewrs += 1
        else:
            for each in pbdata["data"]:
                if each["place"] == 1:
                    if each["run"]["level"]:  # checks if level or full game
                        levelwrs += 1
                    else:
                        fullgamewrs += 1

    if fullgamewrs == 1:
        fullgamemsg = " full game record and "
    else:
        fullgamemsg = " full game records and "
    if levelwrs == 1:
        levelmsg = " IL record."
    else:
        levelmsg = " IL records."  # Grammar pls

    return (
        username(userid(user))
        + " has "
        + str(levelwrs + fullgamewrs)
        + " world records"
        + bool(platform) * (" on " + platform)
        + ":\n"
        + str(fullgamewrs)  # username userid
        + fullgamemsg
        + str(levelwrs)
        + levelmsg
        + "\n"
    )  #   fixes capitalisation


#   +modcount
#   Counts the number of games and series a user moderates.
async def modcount(user):
    async with session.get(
        "https://www.speedrun.com/api/v1/games?max=200&moderator=" + userid(user)
    ) as url:
        moddata = loads(await url.text())
        games = len(moddata["data"])
        if games == 0:
            games = "no"
    async with session.get(
        "https://www.speedrun.com/api/v1/series?moderator=" + userid(user)
    ) as url:
        moddata = loads(await url.text())
        series = len(moddata["data"])
        if series == 0:
            series = "no"
    return (
        username(userid(user))
        + " moderates "
        + str(games)
        + " game"
        + ((games != 1) * "s")
        + " and "
        + str(series)
        + " series.\n"
    )


#   +runcount
#   Counts the number of runs a user has submitted.
async def runcount(user, platform="", obsolete="yes"):
    for each in platforms:  # fixes case
        if each.lower() == platform.lower():
            platform = each
    if platform.lower() == "all":
        platform = ""
    rundata = []
    runs = 0
    fullruns = 0
    if obsolete.lower() == "no" or obsolete.lower() == "-":
        async with session.get(
            "https://www.speedrun.com/api/v1/users/" + user + "/personal-bests"
        ) as url:
            data = loads(await url.text())
            for each in data["data"]:
                rundata.append(each["run"])
    else:
        offset = 0
        repeat = True
        while repeat:
            async with session.get(
                "https://www.speedrun.com/api/v1/runs?user="
                + userid(user)
                + "&max=200&offset="
                + str(offset)
            ) as url:
                data = loads(await url.text())
                rundata += data["data"]
                offset += 200
                try:
                    if (
                        data["pagination"]["links"][-1]["rel"] == "prev"
                    ):  # if last link is prev page, this is last page
                        repeat = False
                except:
                    repeat = False
    if platform:
        for each in rundata:
            if platform in platforms:
                if each["system"]["platform"] == platforms[platform]:
                    if each["level"] == None:
                        fullruns += 1
                    runs += 1
            elif platform.lower() == "mobile":
                if each["system"]["platform"] in [
                    platforms["iOS"],
                    platforms["Android"],
                    platforms["Windows Phone"],
                ]:
                    if each["level"] == None:
                        fullruns += 1
                    runs += 1
    else:
        for each in rundata:
            if each["level"] == None:
                fullruns += 1
            runs += 1

    return (
        username(userid(user))
        + " has "
        + str(runs)
        + " runs"
        + bool(platform) * (" on " + platform)
        + ":\n"
        + str(fullruns)
        + " full game runs and "
        + str(runs - fullruns)
        + " IL runs.\n"
    )


async def gamecount(user):
    async with session.get(
        "https://www.speedrun.com/api/v1/users/" + user + "/personal-bests"
    ) as url:
        data = loads(await url.text())
        games = []
        gamesplayed = 0
        for pb in data["data"]:
            if not pb["run"]["game"] in games:
                gamesplayed += 1
                games.append(pb["run"]["game"])

    return username(userid(user)) + " has played " + str(gamesplayed) + " games"
