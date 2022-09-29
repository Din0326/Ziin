import discord
import json
import time
import random
import datetime

import asyncio
import os
import re
import requests
from re import search
#from gtts import gTTS
#from requests import get
from time import strftime, localtime
from typing import Optional
from datetime import datetime, timedelta, date, timezone
#from googletrans import Translator
from urlextract import URLExtract
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from discord import Embed, Member, Spotify, TextChannel, VoiceChannel, Object, Role, Activity, ActivityType
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Cog, Greedy
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, cooldown, has_permissions, bot_has_permissions
from core.classed import Cog_Extension

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import lyricsgenius

cred = credentials.Certificate('serviceAccount.json')

db = firestore.client()

delete_count = 0
last_audit_log_id = 0
api_key = "5e5231bc30957e7119295f62b8e290ec"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
with open('setting.json', 'r', encoding='utf-8-sig') as jfile:
	jdata = json.load(jfile)
with open('./i18n/en.json', 'r', encoding='utf-8-sig') as lang_en:
	EN = json.load(lang_en)
with open('./i18n/zh_tw.json', 'r', encoding='utf-8-sig') as lang_tw:
	TW = json.load(lang_tw)

def ctx_Check_language(ctx):
	data = db.document(f'Guild/{ctx.guild.id}').get().to_dict()
	Language = data.get('Language')
	guild_tz = data.get('TimeZone')
	if Language == "English":
		Lang = EN
	if Language == "zh-TW":
		Lang = TW
	return Lang , guild_tz


class Basic(Cog_Extension):
	#@commands.command()
	#async def dintest(self,ctx):
	#	with open(f'./data/userdata.json','r',encoding='utf8') as jfile:
	#		jdata = json.load(jfile)
	#	num = 1
	#	for i in self.bot.guilds:
	#		userslist = []
	#		if i.id == 489008089840877568:
	#			continue
	#		await ctx.send(i.name)
	#		for user in i.members:
	#			data = db.collection("User").document(f"{user.id}").collection(f"{i.id}").document("guild").get().to_dict()
	#			if data == None:
	#				continue
	#			total = data.get("total") or 0
	#			#jdata[f"{ctx.guild.id}"] = ({'id':f'{user.id}',"total_mins":total})
	#			userslist.append(({f'{user.id}':{"total_mins":total}}))
	#		jdata[f"{i.id}"] = userslist
	#		with open('./data/userdata.json','w',encoding='utf8') as jfile:
	#			json.dump(jdata,jfile,indent=4)
	#		await ctx.send(f"{i.name} -- {i.id} -- done")
	#		num += 1
	#	await ctx.send("all done")
	#@commands.command()
	#async def tt(self, ctx):
	#	webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
	#	embed= discord.Embed(title="讀取中......", description="請稍等。")
	#	msg = await webhook.send("hi test",wait=True)
	#	print(type(msg))
	#	#msg = await webhook.send(embed=embed, username = '˚₊ ࣪« bot » ࣪ ˖', avatar_url = 'https://imgur.com/csEpNAa.png', allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False))
	#	await msg.delete()
	#def __init__(self,*args,**kwargs):
	#	super().__init__(*args,**kwargs)
#
	#	async def time_task():
	#		await self.bot.wait_until_ready()
	#		self.channel = self.bot.get_channel(489011156837597204)
	#		while not self.bot.is_closed():
	#			now_time = (datetime.now() + timedelta(hours=8)).strftime("%H%M")
	#			time = datetime.now()
	#			if now_time == '0000' and self.counter == 0:
	#				guild = self.bot.get_guild(489008089840877568)
	#				category = discord.utils.get(guild.categories, name="文字頻道")
	#				new_ch = await guild.create_text_channel("7月22日-主播生日-限定頻道",category=category,position=6)
	#				await self.channel.send(f"今天主播生日，祝福請移駕 {new_ch.mention}")
	#				await new_ch.send('everyone\n今天主播生日ㄉ辣 還不趕快祝主播生日快樂')
	#				self.counter = 1
	#				await asyncio.sleep(1)
	#			else:
	#				await asyncio.sleep(1)
	#				pass
#
	#	self.bg_task = self.bot.loop.create_task(time_task())
#
#
	#@commands.command()
	#@has_permissions(administrator=True)
	#async def waiting(self,ctx):
	#	#await ctx.send((datetime.now() + timedelta(hours=8)).strftime("%H%M"))
	#	#await time_task()
	#	self.counter = 0
	#	await ctx.send("waiting...")
	#	#channel = self.bot.get_channel(489011156837597204)
	#	#guild = self.bot.get_guild(489008089840877568)
	#	#category = discord.utils.get(ctx.guild.categories, name="文字頻道")
	#	#new_ch = await ctx.guild.create_text_channel("7月22日-主播生日-限定頻道",category=category,position=6)
	#	#await ctx.send(f"今天主播生日，祝福請移駕 {new_ch.mention}")
	#	#await new_ch.send('@everyone\n今天主播生日ㄉ辣 還不趕快祝主播生日快樂')
	@commands.Cog.listener()
	async def on_message(self,msg):
		if msg.channel == self.bot.get_channel(680011513331056640):
			await msg.publish()
			await msg.add_reaction("✅")

	@commands.command()
	async def test(self,ctx):
		await ctx.send("in")
		await asyncio.sleep(15)
		await ctx.send("15s done")
	#	for i in ctx.guild.members:
	#		await ctx.send(i.status)

	@commands.command()
	async def lyrics(self, ctx, *,user: discord.Member = None):
		spot = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)
		if spot is None:
			await ctx.send("none")
			return
		await ctx.trigger_typing()
		genius = lyricsgenius.Genius("TQLOoaxHfBxoh7oQtm0IPoMLT2Mx2DYhK2IoFxVlSlM68zYi9lkQVghQ1BB_miXl")
		result = genius.search_song(spot.title, spot.artist)
		if result == None:
			await ctx.send("Sorry! I didn't find this song lyrics.")
			return
		#if len(result.lyrics) > 1020:
		#	await ctx.send("Sorry!")
			#return
		embed = discord.Embed(title=f"**{spot.title}**",
							  #timestamp=datetime.utcnow(),
							  description=result.lyrics.replace("EmbedShare URLCopyEmbedCopy",""),
							  url=f"https://open.spotify.com/track/{spot.track_id}")
		#embed.add_field(name=f"**[Lyrics]**",value=result.lyrics.replace("EmbedShare URLCopyEmbedCopy",""),inline=False)
		embed.set_thumbnail(url=spot.album_cover_url)
		embed.set_footer(text=f"Requested by {ctx.author.name}")
		if result == None:
			await ctx.send("None")
			return
		await ctx.send(embed=embed)

	@commands.command()
	async def weather(self,ctx, *, city: str):
		city_name = city
		complete_url = base_url + "appid=" + api_key + "&q=" + city_name
		response = requests.get(complete_url)
		x = response.json()
		if x["cod"] != "404":
			y = x["main"]
			#await ctx.send(x["name"])
			current_temperature = y["temp"]
			current_temperature_celsiuis = str(round(current_temperature - 273.15))
			current_pressure = y["pressure"]
			current_humidity = y["humidity"]
			z = x["weather"]
			weather_description = z[0]["description"]
			embed = discord.Embed(
				title=f"Weather forecast - {city_name}",
				timestamp=datetime.utcnow(),
			)
			embed.add_field(
				name="Description",
				value=f"**{weather_description}**",
				inline=False)
			embed.add_field(
				name="Temperature(C)",
				value=f"**{current_temperature_celsiuis}°C**",
				inline=False)
			embed.add_field(
				name="Humidity(%)", value=f"**{current_humidity}%**", inline=False)
			embed.add_field(
				name="Atmospheric Pressure(hPa)",
				value=f"**{current_pressure}hPa**",
				inline=False)
			embed.set_footer(text=f"Requested by {ctx.author.name}")
			await ctx.send(embed=embed)

		else:
			await ctx.send(f"There was no results about this place!")
	@commands.command(aliases=['slots', 'bet'])
	@commands.cooldown(1,30,commands.BucketType.user)
	async def slot(self, ctx):
		""" Roll the slot machine """
		emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
		a = random.choice(emojis)
		b = random.choice(emojis)
		c = random.choice(emojis)

		slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

		if a == b == c:
			await ctx.send(f"{slotmachine} All matching, you won! 🎉")
		elif (a == b) or (a == c) or (b == c):
			await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
		else:
			await ctx.send(f"{slotmachine} No match, you lost 😢")
			
	@commands.command(aliases=['rm','getrolemember'])
	async def rolemember(self, ctx, target: Optional[Role]):
		target = target or ctx.author.top_role
		in_role_member = []

		for i in range(len(target.members)):
			in_role_member.append(target.members[i].mention)
		ans = ','.join(in_role_member)

		embed = Embed(title="Role Members",
					  colour=target.colour,
					  timestamp=datetime.utcnow())
	
		fields = [("Name", target, True),
				  ("Total", len(target.members),True),
				  ("Member",ans,False)]

		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)

		await ctx.send(embed=embed)
		
	@commands.command()
	async def ping(self, ctx):
		Lang , guild_tz = ctx_Check_language(ctx)
		await ctx.send(Lang["ping"].format(round(self.bot.latency*1000)))

	#@commands.command(aliases=['hello','嗨','c9'])
	#async def hi(self, ctx):
	#	def image_cut(input_img):
    #		img = cv2.imread(input_img, cv2.IMREAD_UNCHANGED)
    #		height, width, channel = img.shape
    #		img_new = np.zeros((height, width, 4), np.uint8)
    #		img_new[:, :, 0:3] = img[:, :, 0:3]
    #		img_circle = np.zeros((height, width, 1), np.uint8)
    #		img_circle[:, :, :] = 0
    #		img_circle = cv2.circle(img_circle, (width // 2, height // 2), int(min(height, width)/2), 255, -1)
    #		img_new[:, :, 3] = img_circle[:, :, 0]
    #		return img_new
#
	#	image = cv2.imread(,1)
	#	#cv2.imshow('image',image)
	#	dst = image_cut('dog.png')
	#	cv2.imwrite("done.png", dst)
	@commands.command(aliases=["tc"])
	async def converter(self,ctx,*,args):
		#if args.split(f"\n")[0] != :
		#	return
		gmttime = eval(args.split(f"\n")[0])
		if gmttime >= 0:
			des = f"+{gmttime}"
		else:
			des = gmttime
		embed = Embed(title="Time Converter",
					description=f"Convert from UTC{des}",
					colour=ctx.author.colour,
					timestamp=datetime.utcnow())
		for i in range(len(args.split(f"\n")) - 1):
			if args.split(f"\n")[0] > "0":
				tran_time = datetime.strptime(args.split(f"\n")[1+i], "%Y-%m-%d %H:%M:%S") + timedelta(hours=int(gmttime))
			elif args.split(f"\n")[0] < "0":
				tran_time = datetime.strptime(args.split(f"\n")[1+i], "%Y-%m-%d %H:%M:%S") - timedelta(hours=int(args.split(f"\n")[0][1:]))
			elif args.split(f"\n")[0] == "0":
				tran_time = datetime.strptime(args.split("\n",1)[1+i], "%Y-%m-%d %H:%M:%S")
			unix_time = time.mktime(tran_time.timetuple())
			embed.add_field(name=str(args.split(f"\n")[1+i]),value=f"unix > `{str(int(unix_time))}`",inline=True)
		await ctx.send(embed=embed)



	@commands.command(hidden=True)
	async def tran(self, ctx, *,args):
		#translator = Translator()
		#await ctx.send(translator)
		#entts = (translator.translate(msg, dest='en').text)
		#await ctx.send("1")
		#await ctx.send(ctx.guild.default_role.mention)
		gmt = args.split(" ")[0][1:] if int(args.split(" ")[0]) <= 0 else args.split(" ")[0]
		tt = args.split(" ",1)[1]
		if gmt != "0":
			tran_time = datetime.strptime(args.split(" ",1)[1], "%Y-%m-%d %H:%M:%S") - timedelta(hours=int(gmt))
		else:
			tran_time = datetime.strptime(args.split(" ",1)[1], "%Y-%m-%d %H:%M:%S")
		unix_time = time.mktime(tran_time.timetuple())
		#await ctx.send(type(unix_time))
		await ctx.send(f"<t:{int(unix_time)}:F>")
			

	@commands.command()
	async def echo(self, ctx, *, msg):
		await ctx.message.delete()
		await ctx.channel.send(msg)

	@commands.command()
	async def pick(self, ctx, *, args):
		answer = random.choice((args.split(' ')))
		await ctx.send(answer)

	@commands.command()
	async def din(self, ctx):
		now = date.today()
		birthday = date(now.year, 2, 3)
		if birthday < now:
			birthday = birthday.replace(year=now.year + 1)
		btddate = birthday - now
		await ctx.send(f"距離丁丁生日還有 {btddate.days} 天，請問有人要先送禮物嗎？<:xoo:691455469415301201>")


	@commands.command()
	async def bd(self, ctx, *, msg):
		now = date.today()
		now_year = datetime.now().strftime('%Y-')
		BD = {"Null":"01-25",
			  "Kono":"01-18",
			  "Din":"02-03",
			  "畜生":"01-23",
			  "Mingzi":"10-29",
			  "忍耐汁":"05-03",
			  "一米":"08-15",
			  "彈珠":"05-23"}
		if msg.capitalize() in BD:
			Name = msg.capitalize()
			conversion = now_year+BD[Name]
			Day =  (date.fromisoformat(str(conversion)))
		if Day < now:
			Day = Day.replace(year=now.year + 1)
		if (Day - now).days == 0:
			if Name != "Din":
				await ctx.send(f"今天{Name}生日，他說要請客，要吃的打+1")
			else:
				await ctx.send(f"今天 {Name} 生日，不趕緊送禮物是在幹嘛?")
		else:
			await ctx.send(f"距離 {Name} 生日還有 {(Day - now).days} 天，請問有人要先送禮物嗎？<:xoo:691455469415301201>")

			
	@commands.command()
	async def pingu(self, ctx):
		random_emoji = random.choice(jdata['emoji'])
		await ctx.send(random_emoji)

	@commands.command()
	async def join(self, ctx):
		channel = ctx.message.author.voice.channel
		voice = get(self.bot.voice_clients, guild=ctx.guild)
		
		if voice and voice.is_connected():
			await voice.move_to(channel)
		else:
			voice = await channel.connect()
		
		if voice and voice.is_connected():
			await voice.move_to(channel)
		else:
			voice = await channel.connect()
			print(f"The bot has connected to {channel}\n")
	
	@commands.command()
	async def leave(self, ctx):
		channel = ctx.message.author.voice.channel
		voice = get(self.bot.voice_clients, guild=ctx.guild)
	
		if voice and voice.is_connected():
			await voice.disconnect()
			print(f"The bot has left {channel}")

def setup(bot):
	bot.add_cog(Basic(bot))