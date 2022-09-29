import os
import requests
import json
import discord
from datetime import datetime
from discord.ext import commands,tasks
from discord.ext.tasks import loop
from discord.ext.commands import has_permissions

from core.classed import Cog_Extension

Twitch_ID = "pqoi7kzdcv4b6nbyvmyn8rejhd73ci"
Twitch_S  = "y0qzlscmiq983f8taqiq1i50u2f2wb"
authURL = 'https://id.twitch.tv/oauth2/token'

online_title = [{}]

def stream_check(usr,guild):
	with open('channeldata.json', 'r', encoding='utf8') as c_file:
		c_data = json.load(c_file)
	AutParams = {'client_id': Twitch_ID,
			 'client_secret': Twitch_S,
			 'grant_type': 'client_credentials'
			 }
	AutCall = requests.post(url=authURL, params=AutParams) 
	access_token = AutCall.json()['access_token']
	head = {
	'Client-ID' : Twitch_ID,
	'Authorization' :  "Bearer " + access_token
	}
	URL = 'https://api.twitch.tv/helix/streams?user_login=' + usr
	r = requests.get(URL, headers = head).json()['data']
	diff = True
	if r:
		r = r[0]
		if r['type'] == 'live' and usr not in c_data[f"{guild.id}"]["online_streamers"]:
			if r['user_login'] in online_title[0].keys():
				if r['title'] == online_title[0][r['user_login']]["title"]:
					diff = False
			online_title[0][r['user_login']] = {"title":r['title']}
			if usr in c_data[f"{guild.id}"]["offline_streamers"]:
				c_data[f"{guild.id}"]["offline_streamers"].remove(usr)
			c_data[f"{guild.id}"]["online_streamers"].append(usr)
			usr_icon = requests.get(f"https://api.twitch.tv/helix/users?login={usr}", headers = head).json()['data'][0]['profile_image_url']
			with open('channeldata.json','w',encoding='utf8') as c_file:
				json.dump(c_data,c_file,indent=4)
			if diff:
				return r,usr_icon
			else:
				r = diff
				return r,usr_icon
		else:
			pass
	else:
		if usr in c_data[f"{guild.id}"]["online_streamers"]:
			c_data[f"{guild.id}"]["online_streamers"].remove(usr)
		if usr not in c_data[f"{guild.id}"]["offline_streamers"]:
			c_data[f"{guild.id}"]["offline_streamers"].append(usr)
		with open('channeldata.json','w',encoding='utf8') as c_file:
			json.dump(c_data,c_file,indent=4)
		return

def user_check(streamer):
	AutParams = {'client_id': Twitch_ID,
			 'client_secret': Twitch_S,
			 'grant_type': 'client_credentials'
			 }
	AutCall = requests.post(url=authURL, params=AutParams) 
	access_token = AutCall.json()['access_token']
	head = {
	'Client-ID' : Twitch_ID,
	'Authorization' :  "Bearer " + access_token
	}
	URL = 'https://api.twitch.tv/helix/users?login=' + streamer
	r = requests.get(URL, headers = head).json()['data']
	if r:
		r = r[0]
		return r
	else:
		return False

class Twitch(Cog_Extension):
	@commands.Cog.listener()
	async def on_ready(self):
		self.check_online_twitch.start()

	@commands.Cog.listener()
	async def on_guild_join(self,guild):
		text = "**{streamer}** is live now!!\n**{url}**"
		with open('channeldata.json', 'r', encoding='utf8') as c_file:
			c_data = json.load(c_file)
		title = {"id":guild.id,"notification_channel":None,"all_streamers":[],"online_streamers":[],"offline_streamers":[],"twitch_notification_text":text,"yt_youtuber":{},"youtube_notification_text":"**{ytber}** upload a video!!\n**{url}**"}
		c_data.update({f"{guild.id}":title})
		with open('channeldata.json','w',encoding='utf8') as c_file:
			json.dump(c_data,c_file,indent=4)
	@tasks.loop(seconds=30)
	async def check_online_twitch(self):
		with open('channeldata.json', 'r', encoding='utf8') as c_file:
			c_data = json.load(c_file)
		for guild in self.bot.guilds:
			for usr in c_data[f"{guild.id}"]["all_streamers"]:
				try:
					r , usr_icon = stream_check(usr,guild)
					print(f"{guild}/{usr} return back true.")
				except:
					continue
				if r:
					title = r['title']
					twitch_link = 'https://www.twitch.tv/' + r['user_login']
					author_name = r['user_name'] + " 正在實況中~!!"
					thumbnail = r['thumbnail_url'].replace('{width}x{height}','1920x1080')
					#description = 'Playing ' + r['game_name'] + ' for ' + str(r['viewer_count']) + ' viewers.'
					channel = self.bot.get_channel(int(c_data[f'{guild.id}']["notification_channel"]))
					if not channel:
						continue
					text = c_data[f"{guild.id}"]["twitch_notification_text"].replace('{streamer}',r['user_name']).replace('{url}',twitch_link)
					embed = discord.Embed(title=title,
										  url=twitch_link,
										  #description=description,
										  timestamp=datetime.utcnow())
					embed.set_author(name=author_name,icon_url=usr_icon)
					embed.add_field(name='Game',value=(r['game_name'] if r['game_name'] else "---"),inline=True)
					embed.add_field(name='Viewers',value=str(r['viewer_count']),inline=True)
					embed.set_thumbnail(url=usr_icon)
					embed.set_image(url=thumbnail)
					embed.set_footer(text='Made by Din#0203')
					await channel.send(content=text,embed=embed)
	
	@has_permissions(manage_guild=True)
	@commands.command()
	async def streamers(self,ctx,arg,streamer = None):
		with open('channeldata.json', 'r', encoding='utf8') as c_file:
			c_data = json.load(c_file)
		if arg == "online":
			await ctx.send(c_data[f"{ctx.guild.id}"]["online_streamers"])
		if arg == "offline":	
			await ctx.send(c_data[f"{ctx.guild.id}"]["offline_streamers"])
		if arg == "all":
			await ctx.send(c_data[f"{ctx.guild.id}"]["all_streamers"])
		if arg in ['add','del']:
			if streamer != None:
				if c_data[f"{ctx.guild.id}"]["notification_channel"] == None:
					await ctx.send("pls setup the notification channel\nexample: !notify #channel")
					return
				load_msg = await ctx.send("<a:load:854870818982723604> searching... <a:load:854870818982723604>")
				if arg == "add":
					valid_user = user_check(streamer)
					if valid_user:
						c_data[f"{ctx.guild.id}"]["all_streamers"].append(streamer)
						add_text = f">>> added! Twitch > **{valid_user['login']}({valid_user['display_name']})**\nhttps://www.twitch.tv/{valid_user['login']}"
						await ctx.send(add_text)
					else:
						await ctx.send(f"cant find this streamer **{streamer}**")
					await load_msg.delete()
				if arg == "del":
					if streamer in c_data[f"{ctx.guild.id}"]["all_streamers"]:
						c_data[f"{ctx.guild.id}"]["all_streamers"].remove(streamer)
						if streamer in c_data[f"{ctx.guild.id}"]["online_streamers"]:
							c_data[f"{ctx.guild.id}"]["online_streamers"].remove(streamer)
						if streamer in c_data[f"{ctx.guild.id}"]["offline_streamers"]:
							c_data[f"{ctx.guild.id}"]["offline_streamers"].remove(streamer)
						await ctx.send(f"deleted {streamer} in streamers list.")
						await load_msg.delete()
				with open('channeldata.json','w',encoding='utf8') as c_file:
					json.dump(c_data,c_file,indent=4)
			else:
				await ctx.send("pls input streamer id.\nexample: **!streamers add din4ni**")

	@has_permissions(manage_guild=True)
	@commands.command()
	async def twitch_text(self,ctx,*,text):
		#text = "**{streamer}** is live now!!\n**{url}**"
		with open('channeldata.json', 'r', encoding='utf8') as c_file:
			c_data = json.load(c_file)
		c_data[f"{ctx.guild.id}"]["twitch_notification_text"] = f"{text}"
		with open('channeldata.json','w',encoding='utf8') as c_file:
			json.dump(c_data,c_file,indent=4)
		await ctx.send(f"twtich notification text\n```{text}```")

	@has_permissions(manage_guild=True)
	@commands.command()
	async def notify(self,ctx,channel: discord.TextChannel):
		if channel != None:
			with open('channeldata.json', 'r', encoding='utf8') as c_file:
				c_data = json.load(c_file)
			c_data[f"{ctx.guild.id}"]["notification_channel"] = channel.id
			with open('channeldata.json','w',encoding='utf8') as c_file:
				json.dump(c_data,c_file,indent=4)
			await ctx.send(f"twitch/youtube notification channel setup to {channel.mention}")
		else:
			await ctx.send("pls mention a channel or give a channel id")


	#@commands.command()
	#async def twtichstart(self,ctx):
	#	if ctx.author.id != 193637455725985792:
	#		return
	#	with open('channeldata.json', 'r', encoding='utf8') as c_file:
	#		c_data = json.load(c_file)
	#	for guild in self.bot.guilds:
	#		try:
	#			c_data[f"{guild.id}"]["online_streamers"].clear()
	#			c_data[f"{guild.id}"]["offline_streamers"].clear()
	#		except:
	#			pass
	#	with open('channeldata.json','w',encoding='utf8') as c_file:
	#		json.dump(c_data,c_file,indent=4)
	#	self.check_online.start()

	#@commands.command()
	#async def createtwtichdata(self,ctx):
	#	with open('channeldata.json', 'r', encoding='utf8') as c_file:
	#		c_data = json.load(c_file)
	#	for guild in self.bot.guilds:
	#		title = {"id":guild.id,"notification_channel":None,"all_streamers":[],"online_streamers":[],"offline_streamers":[]}
	#		c_data.update({f"{guild.id}":title})
	#		with open('channeldata.json','w',encoding='utf8') as c_file:
	#			json.dump(c_data,c_file,indent=4)
	#	await ctx.send("Done")




def setup(bot):
		bot.add_cog(Twitch(bot))