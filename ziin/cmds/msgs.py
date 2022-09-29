import discord
from discord import Embed, Member
from discord.ext import commands
from discord.utils import get
import re
import json
import time
import random
import asyncio
from datetime import datetime, timedelta, date

from core.classed import Cog_Extension

with open('setting.json', 'r', encoding='utf-8-sig') as jfile:
	jdata = json.load(jfile)


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate('serviceAccount.json')
db = firestore.client()

class Msgs(Cog_Extension):

	async def imgc(self,msg):
		din = self.bot.get_user(193637455725985792)
		timestr = time.strftime("%m%d_%H:%M:%S")
		imchannel = self.bot.get_channel(753407077778456726)
		msginfo = (f'Time: {timestr} From {msg.guild}-{msg.channel.mention} By {msg.author.mention}\nJump to >>> {msg.jump_url} <<<')
		msginfoD = (f'Time: {timestr} From {msg.guild}-{msg.channel.mention} By ||{msg.author.name}||\nJump to >>> {msg.jump_url} <<<')
		if msg.author != din:
			await imchannel.send(msginfo)
			await imchannel.send(msg.content)
		else:
			await imchannel.send(msginfoD)
			await imchannel.send(msg.content)

	@commands.Cog.listener()
	async def on_raw_reaction_add(self,payload):
		if payload.member.bot:
			return
		if payload.guild_id == 489008089840877568:
			guild = self.bot.get_guild(payload.guild_id)
			ch = self.bot.get_channel(payload.channel_id)
			msg = await ch.fetch_message(payload.message_id)
			if payload.emoji.id == 706505677450903652:
				for i in msg.reactions:
					if i.emoji.id == 706505677450903652:
						user_list = []
						async for y in i.users():
							user_list.append(y.id)
						if self.bot.user.id in user_list:
							if i.count >= 6:
								for channel in guild.text_channels:
									public = [489011156837597204,489013738058547210,712683884717801575]
									if channel.id in public:
										def _check(message):
											return message.author == payload.member
										try:
											await channel.purge(limit=30,check=_check)
										except:
											pass
#
	@commands.Cog.listener()
	async def on_message(self,msg):	
		if str(msg.channel.type) != "private":




			#儲存最後一次訊息紀錄

			user_guild_data = db.collection("User").document(f"{msg.author.id}").collection(f"{msg.guild.id}").document("guild")
			data = db.document(f'Guild/{msg.guild.id}').get().to_dict()
			guild_tz = data.get('TimeZone')
			msg_time = (msg.created_at + timedelta(hours=int(guild_tz))).strftime("%d/%m/%Y %H:%M:%S")
			info = {"last_message": f"{msg_time}"}
			if user_guild_data.get().to_dict() == None:
				user_guild_data.set(info)
			else:
				user_guild_data.update(info)
####	 	文字觸發
			#馬鈴薯 匿名
			if msg.channel.id == 903081545311617034 and msg.author != self.bot.user:
				if msg.author.id == 458165526363897856:
					return
				con = msg.content
				await msg.delete()
				await msg.channel.send(con)
				#await msg.delete()
			#susu群組
			if msg.channel.id == 625729755991506986 and msg.author != self.bot.user:
				if msg.content == '幹':
					random_fuck = random.choice(jdata['fuck'])
					await msg.channel.send(random_fuck)
				if msg.content.lower() == 'matt':
					ava = self.bot.get_user(166901140162740224).avatar.url
					mat = [f'{ava}','垃圾一個','死廢物']
					random_mat = random.choice(mat)
					await msg.channel.send(random_mat)
				keys_List = ['笑死','校死','校鼠','效死','笑鼠']
				if msg.content in keys_List and msg.author != self.bot.user:
					await msg.channel.send("笑死")
				#if msg.content in tdata.keys() and msg.author != self.bot.user:
			#flash群組
			if msg.guild.id == 489008089840877568 and msg.author != self.bot.user:
				risky = ['nitro','discord','gift','@everyone','free','免費','game','test']
				#if 'http://steancomunnity.ru/'in msg.content.lower() or 'discord nitro for free' in msg.content.lower():
				#	await msg.author.ban(reason="釣魚鏈接")
				#	await msg.channel.send(f'{msg.author.mention}　死去 原因: 發送釣魚網址\n||ID : {msg.author.id}|| \nR.I.P. \n{msg.author.joined_at.strftime("%Y-%m-%d")} ~ {date.today()}')
				#elif '.ru/' in msg.content.lower():
				#	admin = msg.guild.get_role(489009209044631553)
				#	if 'new/?partner=' in msg.content.lower() and 'token=' in msg.content.lower():
				#		await msg.author.ban(reason="釣魚鏈接")
				#		await msg.channel.send(f'{msg.author.mention}　死去 原因: 發送釣魚網址\n||ID : {msg.author.id}|| \nR.I.P. \n{msg.author.joined_at.strftime("%Y-%m-%d")} ~ {date.today()}')
				#	else:
				#		await msg.channel.send(f"{admin.mention} check message.")
				count = 0
				url = True
				for keyword in risky:
					urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',msg.content.lower())
					if urls and url:
						count += 1
						url = False
					if keyword in msg.content.lower():
						count += 1
				if count >= 3:
					await msg.add_reaction(":thinking1:706505677450903652")
			#剪刀石頭布
			if msg.content == '布' and msg.author != self.bot.user:
				random_quanbu = random.choice(jdata['quanbu'])
				await msg.channel.send(random_quanbu)
			if msg.content == '剪刀' and msg.author != self.bot.user:
				random_quanjia = random.choice(jdata['quanjia'])
				await msg.channel.send(random_quanjia)
			if msg.content == '石頭' and msg.author != self.bot.user:
				random_quanshi = random.choice(jdata['quanshi'])
				await msg.channel.send(random_quanshi)
			#bot reaction
			noot_keyword = ['noot','嘟嘟','嘟','NOOT']
			if msg.content in noot_keyword and msg.author != self.bot.user:
				await msg.channel.send('<a:noot1:744756406783180840><a:noot2:744756406514745354><a:noot3:744756405982068767>')
#	
			if self.bot.user in msg.mentions and msg.author != self.bot.user:
				random_pingu = random.choice(jdata['pingu'])
				a = re.sub('<@!\d*>|\s','',msg.content)
				if not a:
					await msg.channel.send(random_pingu)
	

####	 自動存檔
			if 'https://' in msg.content.lower() and 'jpg' in msg.content.lower() and msg.author != self.bot.user:
				await self.imgc(msg)
			if 'https://' in msg.content.lower() and 'png' in msg.content.lower() and msg.author != self.bot.user:
				await self.imgc(msg)
			if 'https://' in msg.content.lower() and 'gif' in msg.content.lower() and msg.author != self.bot.user:
				await self.imgc(msg)
			if 'https://' in msg.content.lower() and 'mp4' in msg.content.lower() and msg.author != self.bot.user:
				await self.imgc(msg)
			if 'https://' in msg.content.lower() and 'mkv' in msg.content.lower() and msg.author != self.bot.user:
				await self.imgc(msg)
			if 'https://' in msg.content.lower() and 'mov' in msg.content.lower() and msg.author != self.bot.user:
				await self.imgc(msg)
	
			if msg.attachments and len(msg.attachments) >= 1:
				timestr = time.strftime("%m%d_%H:%M:%S")
				din = self.bot.get_user(193637455725985792)
				imchannel = self.bot.get_channel(753407077778456726)
				msginfo = (f'Time: {timestr} From {msg.guild}-{msg.channel.mention} By {msg.author.mention}\nJump to >>> {msg.jump_url} <<<')
				msginfoD = (f'Time: {timestr} From {msg.guild}-{msg.channel.mention} By ||{msg.author.name}||\nJump to >>> {msg.jump_url} <<<')
				if msg.author != din:
					await imchannel.send(msginfo)
					for x in range(len(msg.attachments)):
						await imchannel.send(msg.attachments[x-1].url)
					#await msg.attachments[x-1].save(fp=f"C:\\789\\imgur\\{timestr}_{msg.attachments[x-1].id}.png")
					#print (f'Save {timestr}_{msg.attachments[x-1].id}.png')
				else:
					await imchannel.send(msginfoD)
					for x in range(len(msg.attachments)):
						await imchannel.send(msg.attachments[x-1].url)
		else:
			if msg.content == "z!link":
				user = self.bot.get_user(193637455725985792)
				user_img = user.avatar or user.default_avatar
				embed = discord.Embed(title=f"{self.bot.user.name} 邀請鏈結 點我!", url="https://discord.com/api/oauth2/authorize?client_id=616799674396967003&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.com%2Fapi%2Foauth2%2Fauthorize%3Fclient_id%3D616799674396967003%26permissions%3D8%26redirect_uri%3Dhttps%253A%252F%252Fdiscord.com%252Fapi%252Foauth2%252Fauthorize%253Fclient_id%253D616799&scope=applications.commands%20bot",timestamp=datetime.utcnow())
				embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar.url)
				embed.set_thumbnail(url=self.bot.user.avatar.url)
				embed.set_footer(icon_url=(user_img.url),text=f'{user}')
				fields = [("Owner　　　　　預設前綴", "**Din#0203　　　　　z!**\n\n邀請Bot需要有管理員權限，才能使用Log功能  \n邀請後請先查閱 z!help 說明書\n有遇到任何問題或是建議，請進入 [Support Server](https://discord.gg/EtQX9RB9Xr)", True)]
		
				for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)
				await msg.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Msgs(bot))