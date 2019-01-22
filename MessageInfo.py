import urllib.request
import discord
from xml.dom import minidom


def rtrv_rte(bus_obj, *arg):
    embed = discord.Embed(title="Please use the abbreviated name in the commands", description="", color=0xb00800)
    arvl = bus_obj.rte
    keys = ""
    vals = ""
    for key, val in arvl.items():
        keys = keys + key + "\n"
        vals = vals + val + "\n"
    embed = embed.add_field(name = "Bus Line", value = keys, inline= True)
    embed = embed.add_field(name = "\u200b",value = "\u200b", inline= True)
    embed = embed.add_field(name = "Abbreviated Name", value = vals, inline=True)
    return embed


def rtrv_stps(bus_obj, command):
    stp_lst = ''
    stops = bus_obj.stp[command[1]]
    for val in stops:
        stp_lst += val + '\n'
    return stp_lst

def rtrv_arvl(bus_obj, command):
    arvl_msg = 'This bus will arrive in '
    arvl_tms = []
    arv_url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=rutgers&r=' \
              + command[1] + '&s=' + command[2]
    dom = minidom.parse(urllib.request.urlopen(arv_url))
    predictions = dom.getElementsByTagName('predictions')
    attributes = predictions[0].attributes
    for counter in range(len(attributes)):
        if str(attributes.item(counter).nodeName) == 'dirTitleBecauseNoPredictions':
            return 'This bus is not currently running'
    arvl_info = dom.getElementsByTagName('prediction')
    for counter in range(arvl_info.length):
        arvl_tms.append(str(arvl_info[counter].attributes['minutes'].value))
    for counter, time in enumerate(arvl_tms):
        if counter == (len(arvl_tms) - 1):
            arvl_msg += 'and ' + time + ' minutes'
        else:
            arvl_msg += time + ', '
    embed = discord.Embed(title="Arrival Times", description=arvl_msg, color=0xb00800)

    return embed

def rtrv_rucs(*args):
    embed = discord.Embed(title="Follow these instructions in order to find out how to access the rutgers minecraft server!", description="1) Download twitch client at https://app.twitch.tv/download and install\n\
2) Once installed go into mods and then Minecraft and search for FTB presents Direwolf20 mod pack \n\
3) DO NOT INSTALL YET \n\
4) Go into versions and select 2.4.0 (should be first in list) \n\
5) While mod is installing go to top right of twitch app \n\
   go to setting -> minecraft and change max allocated memory to at least 4 gigs \n\
6) After mod has finished installing start mod and then connect to RUCS server at IP address 149.56.242:25595", color=0xb00800)

    return embed
