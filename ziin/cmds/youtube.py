import os
import re
import requests
import json
import discord
from datetime import datetime , timedelta
from discord.ext import commands,tasks
from discord.ext.tasks import loop
from discord.ext.commands import has_permissions

from core.classed import Cog_Extension

api_key = "AIzaSyC-CD86GLwW1F-lr1RhaPVlkvWp9GdhGGM"

def yt_video_check(ytber,guild):
	with open('channeldata.json', 'r', encoding='utf8') as c_file:
		c_data = json.load(c_file)
	search_url = "https://www.youtube.com/channel/"+ ytber + "/videos"
	info = None
	r = requests.get(search_url,timeout=15)
	r.raise_for_status()
	info = r.text
	if info == None:
		print('Error')
	else:
		video_id = re.search('(?<={"videoId":").*?(?=",)', info).group()
		title = re.search('(?<={"text":").*?(?="})', info).group()
		Channel_Name = re.search('(?<="channelMetadataRenderer":{"title":").*?(?=",)', info).group()
		c_data[str(guild.id)]["yt_youtuber"][ytber]["name"] = Channel_Name
		if video_id != c_data[str(guild.id)]["yt_youtuber"][ytber]["yt_id_before"]:
			c_data[str(guild.id)]["yt_youtuber"][ytber]["yt_id_before"] = video_id
			with open('channeldata.json','w',encoding='utf8') as c_file:
				json.dump(c_data,c_file,indent=4)
			return video_id , Channel_Name
		else:
			with open('channeldata.json','w',encoding='utf8') as c_file:
				json.dump(c_data,c_file,indent=4)
			return False , False

class Youtube(Cog_Extension):
	@commands.Cog.listener()
	async def on_ready(self):
		self.check_video_youtube.start()

	@tasks.loop(seconds=300)
	async def check_video_youtube(self):
		with open('channeldata.json', 'r', encoding='utf8') as c_file:
			c_data = json.load(c_file)
		for guild in self.bot.guilds:
			try:
				for ytber in c_data[f"{guild.id}"]["yt_youtuber"].keys():
					video_id , Channel_Name = yt_video_check(ytber,guild)
					if video_id and Channel_Name:
						yt_link = "https://youtu.be/" + video_id
						youtube_notification_text = c_data[f"{guild.id}"]["youtube_notification_text"].replace("{ytber}",Channel_Name).replace("{url}",yt_link)
						channel = self.bot.get_channel(c_data[f"{guild.id}"]["notification_channel"])
						await channel.send(youtube_notification_text)
			except:
				pass
	
	@has_permissions(manage_guild=True)
	@commands.command()
	async def youtubers(self,ctx,arg,youtuber = None):
		with open('channeldata.json', 'r', encoding='utf8') as c_file:
			c_data = json.load(c_file)
		if arg == "all":
			ytber_list = []
			for ytber in c_data[f"{ctx.guild.id}"]["yt_youtuber"].keys():
				ytber_list.append(c_data[f"{ctx.guild.id}"]["yt_youtuber"][ytber]["name"])
			await ctx.send(ytber_list)
		if arg in ['add','del']:
			if youtuber != None:
				if c_data[f"{ctx.guild.id}"]["notification_channel"] == None:
					await ctx.send("pls setup the notification channel\nexample: !notify #channel")
					return
				load_msg = await ctx.send("<a:load:854870818982723604> searching... <a:load:854870818982723604>")
				if arg == "add":
					search_url = "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId="+youtuber+"&maxResults=1&order=date&key="+api_key
					info = None
					r = requests.get(search_url,timeout=15)
					r.raise_for_status()
					info = r.json()
					if info != None:
						ytb_name = info['items'][0]['snippet']['channelTitle']
						ytb_last_id = info['items'][0]['id']['videoId']
						c_data[f"{ctx.guild.id}"]["yt_youtuber"][youtuber] = {"id":youtuber,"name":ytb_name,"yt_id_before":ytb_last_id}
						await ctx.send(f"已開啟 **{ytb_name}** Youtube通知.")
					await load_msg.delete()
				if arg == "del":
					ytb_name = c_data[f"{ctx.guild.id}"]["yt_youtuber"][youtuber]["name"]
					del c_data[f"{ctx.guild.id}"]["yt_youtuber"][youtuber]
					await ctx.send(f"已關閉 **{ytb_name}** Youtube通知.")
					await load_msg.delete()
				with open('channeldata.json','w',encoding='utf8') as c_file:
					json.dump(c_data,c_file,indent=4)
			else:
				await ctx.send("pls input streamer id.\nexample: **!youtubers add din4ni**")

	@has_permissions(manage_guild=True)
	@commands.command()
	async def youtube_text(self,ctx,*,text):
		#text = "**{streamer}** is live now!!\n**{url}**"
		with open('channeldata.json', 'r', encoding='utf8') as c_file:
			c_data = json.load(c_file)
		c_data[f"{ctx.guild.id}"]["youtube_notification_text"] = f"{text}"
		with open('channeldata.json','w',encoding='utf8') as c_file:
			json.dump(c_data,c_file,indent=4)
		await ctx.send(f"youtube notification text\n```{text}```")


def setup(bot):
		bot.add_cog(Youtube(bot))