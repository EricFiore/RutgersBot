#clientID = 530896765445210113
#token = NTMwODk2NzY1NDQ1MjEwMTEz.DxGFiA.sJBQZgGTOpxmTDqMxEwFAeNKJKg
#permissions = 223296

# https://discordapp.com/oauth2/authorize?client_id=530896765445210113&scope=bot&permissions=223296

import discord
import parseData as pd
import MessageInfo as mi
from BusData import RouteData

client = discord.Client()
bus_info = RouteData()
command_dict = {'rte': mi.rtrv_rte, 'stp': mi.rtrv_stps, 'arvl': mi.rtrv_arvl, 'rucs': mi.rtrv_rucs }

@client.event
async def on_ready():
        #the moment the bot is initialized we set its status to online and set the "game" it is playing
        await client.change_presence(status=discord.Status.online,activity=discord.Game(name="office hours"))
        print('we have logged in as {0!r}'.format(client.user.name))




@client.event
async def on_message(message):
    if isinstance(message.channel, discord.abc.GuildChannel):
        print("{0:s} {1:s} {2:d} {3:s}: {4:s}".format(message.guild.name, message.channel.name, message.author.id, message.author.name, message.content))
    elif isinstance(message.channel, discord.abc.PrivateChannel):
        print("Direct Message {0:d} {1:s}: {2:s} ".format(message.author.id, message.author.name, message.content))

    if '=rbot' in message.content.lower():
        command = pd.msg_parse(message.content, bus_info)
        if isinstance(command[len(command)-1], list):
            msg = pd.error_parse(command[len(command)-1], bus_info)
            await message.channel.send(msg)
        else:
            embed = command_dict[command[0]](bus_info, command)

            await message.channel.send(embed = embed)
"""
import discord
import urllib.request
from xml.dom import minidom

client = discord.Client()

@client.event
async def on_ready():
	print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
	print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
	
	if "=rbot get route list" in message.content.lower():
		url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=rutgers'
		dom = minidom.parse(urllib.request.urlopen(url))
		route = dom.getElementsByTagName('route')
		totalroute = ''
		for iterator in range(len(route)):
			totalroute += str(route[iterator].attributes['title'].value) + '\n'
		await message.channel.send(totalroute)

	elif "=rbot get stops for" in message.content.lower():
		msg = message.content.split()
		try:
			lwr_msg = msg[4].lower()
		except:
			await message.channel.send('did not provide correct route information')	
		routeConfigURL = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=rutgers&r=' + lwr_msg
		dom = minidom.parse(urllib.request.urlopen(routeConfigURL))
		routeConfig = dom.getElementsByTagName('stop')
		routeConfigLength = routeConfig.length
		routeStops = ''
		for counter in range(routeConfigLength):
			node = routeConfig[counter].attributes
			for iterator in range(len(node)):
				if str(node.item(iterator).nodeName) == 'title':
					routeStops += str(routeConfig[counter].attributes['tag'].value) + '\n'
		await message.channel.send(routeStops)
	
	elif "=rbot get arrival time for" in message.content.lower():
		msg = message.content.split()
		try:
			route = msg[5].lower()
			stop = msg[6].lower()
		except:
			await message.channel.send('did not provide correct route information')
		stop_config_url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=rutgers&r=' + route + '&s=' + stop
		dom = minidom.parse(urllib.request.urlopen(stop_config_url))
		predictions = dom.getElementsByTagName('predictions')
		attributes = predictions[0].attributes
		notRunning = False
		for counter in range(len(attributes)):
			if str(attributes.item(counter).nodeName) == 'dirTitleBecauseNoPredictions':
				notRunning = True
		if notRunning:
			await message.channel.send('This bus is not currently running')
		else:
			arrivalInfo = dom.getElementsByTagName('prediction')
			arrivalTime = str(arrivalInfo[0].attributes['minutes'].value)
			await message.channel.send('This bus will arrive in ' + arrivalTime + ' minutes')
"""


client.run("NTI4MzI0NjYzNzU2MDYyNzM5.Dwhc1w.ses0qDrs8mYOfuqY66jcRMHChzU")
