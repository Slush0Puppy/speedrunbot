import math
import urllib.request, json 

#   An array of every month. Used to convert numbers to month names.
month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']


#   Converts 1 to "1st", 2 to "2nd", etc.
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])


#   platforms is a dictionary where the keys are the names of each platform, and the values are the respective ids.
platforms = {}
with urllib.request.urlopen("https://www.speedrun.com/api/v1/platforms?max=10000") as platurl:
    platdata = json.loads(platurl.read().decode())
    for each in platdata['data']:
        platforms[each['name']]=each['id']


#   Formats a string by removing special chars and replacing spaces with underscores.
def pformat(s):
    s=s.replace(' ','_')
    for eachchar in "%()":
            s = s.replace(eachchar,'')
    return s


#   Converts times in the format XXX.xxx into h m s ms
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


#   Converts ["x", "y", "z"] into "x, y, and z"
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


#   username() gets userid from a username; userid() does the inverse
def username(userid):
    with urllib.request.urlopen("https://www.speedrun.com/api/v1/users/" + userid) as url:
        userdata = json.loads(url.read().decode())          #gets information from speedrun.com api
        return userdata['data']['names']['international']   #reads the international name from api

def userid(username):
    with urllib.request.urlopen("https://www.speedrun.com/api/v1/users/" + username) as url:
        userdata = json.loads(url.read().decode())
        return userdata['data']['id']



