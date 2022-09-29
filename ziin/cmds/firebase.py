import discord
from discord.ext import commands
from discord.ext.commands import command, has_permissions
import json
import time
from discord import Embed
from datetime import datetime, timedelta, date, timezone

from core.classed import Cog_Extension

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate('serviceAccount.json')
db = firestore.client()

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
def data_Check_language(data):
	Language = data.get('Language')
	if Language == "English":
		Lang = EN
	if Language == "zh-TW":
		Lang = TW
	return Lang
class Firebase(Cog_Extension):	
#
	@commands.Cog.listener()
	async def on_guild_join(self,guild):
		join = self.bot.get_channel(766318401441628210)
		#### guild 資料
		info = {
			"Name": guild.name,
			"ID": guild.id,
			"Language": "English",
			"TimeZone": "0",
			"Prefix": "z!",
			"admin_msg_id": None,
			"basic_msg_id": None,
			"logger_msg_id": None,
			"setting_msg_id": None,
			"setting_user_id": None,
			"use_msg_id": None,
			"use_user_id": None,
			"guild_log_id": None,
			"member_log_id": None,
			"message_log_id": None,
			"voice_log_id": None,
			"ignore_channel": []
		}
		info_ref = db.collection("Guild").document(f"{guild.id}")
		info_ref.set(info)
		### guild logsetting
		logsetting = {
			"-Name": guild.name,
			"-ID": guild.id,
			"guildUpdate": "off", #群組更新
			"messageUpdate": "on", #文字編輯
			"messageDelete": "on", #文字刪除
			"RoleCreate": "off", #新增身分組
			"RoleDelete": "off", #刪除身分組
			"RoleUpdate": "off", #身分組更新
			"MemberUpdate": "on", #成員更新
			"MemberAdd": "off",	#成員加入
			"MemberKick": "off", #成員剔除
			"MemberUnban": "off", #成員解封
			"MemberRemove": "off", #成員離開
			"MemberNickUpdate": "on", #暱稱變更
			"channelCreate": "off", #創建頻道
			"channelDelete": "off", #刪除頻道
			"voiceChannelJoin": "off", #語音頻道進入
			"voiceChannelLeave": "off", #語音頻道離開
			"voiceStateUpdate": "off", #語音狀態更新
			"voiceChannelSwitch": "off", #成員切換語音頻道
			"messageDeleteBulk": "off" #暫不開放
		}
		set_ref = db.collection("Logsetting").document(f"{guild.id}")
		set_ref.set(logsetting)

		await join.send(f'Name: {guild.name}\nID: {guild.id}\nDatabase Done!')

		async for entry in guild.audit_logs(limit=1,action=discord.AuditLogAction.bot_add):
			await entry.user.send('''謝謝您邀請 Ziin 至群組
Thank you invite "Ziin" to guild

需要您先在群組完成前置設定 (語言/時區)
You need to complete the pre-settings in the group first (language/time zone)

預設前綴為: **z!**
prefix: **z!**

```z!language X
X = english / chinese
語言預設為英文
Default：English```
```z!timezone X
X = 12  ~  -12
時區為UTC 預設為 UTC+0  (台灣請輸入 8)
Time zone is UTC, default is UTC+0
```
				''')
#
	@commands.Cog.listener()
	async def on_guild_leave(self,guild):
		join = self.bot.get_channel(766318401441628210)
		await join.send(f'Name: {guild.name}\nID: {guild.id}\nLeave Guild!')

	@commands.command()
	async def project(self, ctx,*,msg):
		project_name = msg.split(" ")[0]
		#project_value = msg.split(" ")[1]
		await ctx.send("new project start!")
		for x in range(len(self.bot.guilds)):
			logsetting = {
				f"{project_name}": "on", 
			}
			#doc_ref = db.collection("Guild").document("737830509798883378")
			doc_ref = db.collection("Logsetting").document(f"{self.bot.guilds[x-1].id}")
			doc_ref.update(logsetting)
		await ctx.send("Done!")
#
	@commands.command()
	@has_permissions(administrator=True)
	async def setting(self,ctx):
		Lang , guild_tz = ctx_Check_language(ctx)
		log = db.document(f'Logsetting/{ctx.guild.id}').get().to_dict()
		g1 = log.get('guildUpdate') #群組更新
		m1 = log.get('messageUpdate')#文字編輯
		m2 = log.get('messageDelete')#文字刪除
		g2 = log.get('RoleCreate') #新增身分組
		g3 = log.get('RoleDelete') #刪除身分組
		g6 = log.get('RoleUpdate')
		m3 = log.get('MemberUpdate')#成員更新
		m4 = log.get('MemberAdd')	#成員加入
		m5 = log.get('MemberKick') #成員剔除
		m6 = log.get('MemberRemove') #成員離開
		m7 = log.get('MemberNickUpdate')#暱稱變更
		g4 = log.get('channelCreate') #創建頻道
		g5 = log.get('channelDelete') #刪除頻道
		g7 = log.get('channelUpdate') #更新頻道
		v1 = log.get('voiceChannelJoin') #語音頻道進入
		v2 = log.get('voiceChannelLeave') #語音頻道離開
		v3 = log.get('voiceStateUpdate') #語音狀態更新
		v4 = log.get('voiceChannelSwitch') #成員切換語音頻道
		mT = log.get('messageDeleteBulk')#暫不開放 #暫不開放: {mT} await S_ID.add_reaction("🥰")
		u1 = log.get('MemberUnban') #成員解封
		embed = Embed(title=Lang['set_title'],
					description=Lang['set_docs'],
					colour=ctx.author.colour,
					timestamp=datetime.utcnow())
		embed.add_field(name="Message", value=Lang['set_msg'].format(m1,m2), inline=True)
		embed.add_field(name="Guild", value=Lang['set_guild'].format(g4,g2,g5,g3,g7,g6,g1), inline=True)
		embed.add_field(name="\u200b",value="\u200b",inline=True)
		embed.add_field(name="Member", value=Lang['set_member'].format(m4,m6,m5,m3,u1), inline=True)
		embed.add_field(name="Voice", value=Lang['set_voice'].format(v1,v2,v3), inline=True)
		embed.add_field(name="\u200b",value="\u200b",inline=True)
		S_ID = await ctx.send(embed=embed)
		doc_ref = db.document(f'Guild/{ctx.guild.id}')
		doc = {'setting_msg_id': S_ID.id}
		doc_ref.update(doc)
		docu = {'setting_user_id': ctx.author.id}
		doc_ref.update(docu)
		await S_ID.add_reaction("<:1_:768785369704562688>")
		await S_ID.add_reaction("<:2_:768785371231289364>")
		await S_ID.add_reaction("<:3_:768785371709440020>")
		await S_ID.add_reaction("<:4_:768785477393580032>")
		await S_ID.add_reaction("<:5_:768785697079033866>")
		await S_ID.add_reaction("<:6_:768785476995383316>")
		await S_ID.add_reaction("<:7_:768785698207170590>")
		await S_ID.add_reaction("<:8_:768785697749729300>")
		await S_ID.add_reaction("<:9_:768785696902479872>")
		await S_ID.add_reaction("<:10:768785697066188840>")
		await S_ID.add_reaction("<:11:768785696903135232>")
		await S_ID.add_reaction("<:12:768785699032924161>")
		await S_ID.add_reaction("<:13:768785697116782592>")
		await S_ID.add_reaction("<:14:768785697708179496>")
		await S_ID.add_reaction("<:15:768785697683144704>")
		await S_ID.add_reaction("<:16:768785698093662218>")
		await S_ID.add_reaction("<:17:768785696433242133>")

	@commands.command()
	@has_permissions(administrator=True)
	async def ignore(self,ctx, channel: discord.TextChannel = None):
		Lang , guild_tz = ctx_Check_language(ctx)
		doc_ref = db.document(f'Guild/{ctx.guild.id}')
		id_list = doc_ref.get().to_dict().get("ignore_channel")
		if str(channel.id) not in id_list:
			doc = {'ignore_channel': firestore.ArrayUnion([f'{channel.id}'])}
			doc_ref.update(doc)
			await ctx.send(Lang['ignore_add'].format(channel.mention))
		else:
			doc = {'ignore_channel': firestore.ArrayRemove([f'{channel.id}'])}
			doc_ref.update(doc)
			await ctx.send(Lang['ignore_del'].format(channel.mention))

	@commands.command()
	async def show(self,ctx):
		Lang , guild_tz = ctx_Check_language(ctx)
		doc_ref = db.document(f'Guild/{ctx.guild.id}').get().to_dict()
		id_list = doc_ref.get("ignore_channel")
		embed = discord.Embed(title=Lang['ignore_all'].format(ctx.guild.name),
				color=ctx.author.colour,
				timestamp=datetime.utcnow())
		embed.set_footer(text=f'{ctx.author}')
		if id_list != []:
			for i in id_list:
				igg_ch = self.bot.get_channel(int(i))
				embed.add_field(name=igg_ch, value=igg_ch.mention)
		else:
			embed.add_field(name=Lang['ignore_none'], value="------")
		await ctx.send(embed=embed)

	@commands.command()
	@has_permissions(administrator=True)
	async def setlog(self,ctx,info,channel: discord.TextChannel = None):
		channel = channel or ctx.channel
		Lang , guild_tz = ctx_Check_language(ctx)
		doc_ref = db.document(f'Guild/{ctx.guild.id}')
		doce = db.document(f'Guild/{ctx.guild.id}').get().to_dict()
		if info == "member":
			doc = {'member_log_id': channel.id}
			doc_ref.update(doc)
			await ctx.send(Lang["setlog_member"].format(channel.mention))
		if info == "msg":
			doc = {'message_log_id': channel.id}
			doc_ref.update(doc)
			await ctx.send(Lang["setlog_msg"].format(channel.mention))
		if info == "voice":
			doc = {'voice_log_id': channel.id}
			doc_ref.update(doc)
			await ctx.send(Lang["setlog_voice"].format(channel.mention))
		if info == "guild":
			doc = {'guild_log_id': channel.id}
			doc_ref.update(doc)
			await ctx.send(Lang["setlog_guild"].format(channel.mention))

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		data = db.document(f'Guild/{payload.guild_id}').get().to_dict()
		Lang = data_Check_language(data)
		S_ID = data.get('setting_msg_id')
		S_UID = data.get('setting_user_id')
		U_ID = data.get('use_msg_id')
		U_UID = data.get('use_user_id')
		if payload.message_id == S_ID:
			colours = {
				"1_": "messageUpdate",
				"2_": "messageDelete",
				"3_": "channelCreate",
				"4_": "channelDelete",
				"5_": "channelUpdate",
				"6_": "RoleCreate",
				"7_": "RoleDelete",
				"8_": "RoleUpdate",
				"9_": "guildUpdate",
				"10": "MemberAdd",
				"11": "MemberRemove",
				"12": "MemberKick",
				"13": "MemberUpdate",
				"14": "MemberUnban",
				"15": "voiceChannelJoin",
				"16": "voiceChannelLeave",
				"17": "voiceStateUpdate"
			}
			if payload.user_id == S_UID:
				Remsg = await self.bot.get_channel(payload.channel_id).fetch_message(S_ID)
				new = colours[payload.emoji.name]
				doc_ref = db.document(f'Logsetting/{payload.guild_id}')
				doc = {new: "on"}
				doc_ref.update(doc)
				###
				log = db.document(f'Logsetting/{payload.guild_id}').get().to_dict()
				g1 = log.get('guildUpdate') #群組更新
				m1 = log.get('messageUpdate')#文字編輯
				m2 = log.get('messageDelete')#文字刪除
				g2 = log.get('RoleCreate') #新增身分組
				g3 = log.get('RoleDelete') #刪除身分組
				g6 = log.get('RoleUpdate')
				m3 = log.get('MemberUpdate')#成員更新
				m4 = log.get('MemberAdd')	#成員加入
				m5 = log.get('MemberKick') #成員剔除
				m6 = log.get('MemberRemove') #成員離開
				m7 = log.get('MemberNickUpdate')#暱稱變更
				g4 = log.get('channelCreate') #創建頻道
				g5 = log.get('channelDelete') #刪除頻道
				g7 = log.get('channelUpdate') #更新頻道
				v1 = log.get('voiceChannelJoin') #語音頻道進入
				v2 = log.get('voiceChannelLeave') #語音頻道離開
				v3 = log.get('voiceStateUpdate') #語音狀態更新
				v4 = log.get('voiceChannelSwitch') #成員切換語音頻道
				mT = log.get('messageDeleteBulk')#暫不開放 #暫不開放: {mT} await S_ID.add_reaction("🥰")
				u1 = log.get('MemberUnban') #成員解封
				embed = Embed(title=Lang['set_title'],
					description=Lang['set_docs'],
					colour=self.bot.user.colour,
					timestamp=datetime.utcnow())
				embed.add_field(name="Message", value=Lang['set_msg'].format(m1,m2), inline=True)
				embed.add_field(name="Guild", value=Lang['set_guild'].format(g4,g2,g5,g3,g7,g6,g1), inline=True)
				embed.add_field(name="\u200b",value="\u200b",inline=True)
				embed.add_field(name="Member", value=Lang['set_member'].format(m4,m6,m5,m3,u1), inline=True)
				embed.add_field(name="Voice", value=Lang['set_voice'].format(v1,v2,v3), inline=True)
				embed.add_field(name="\u200b",value="\u200b",inline=True)
				user_img = self.bot.get_user(S_UID).avatar or self.bot.get_user(S_UID).default_avatar
				embed.set_footer(icon_url=user_img.url,text=Lang['set_footer'].format(self.bot.get_user(S_UID)))
				await Remsg.edit(embed=embed)

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
		data = db.document(f'Guild/{payload.guild_id}').get().to_dict()
		Lang = data_Check_language(data)
		S_ID = data.get('setting_msg_id')
		S_UID = data.get('setting_user_id')
		U_ID = data.get('use_msg_id')
		U_UID = data.get('use_user_id')
		if payload.message_id == S_ID:
			colours = {
				"1_": "messageUpdate",
				"2_": "messageDelete",
				"3_": "channelCreate",
				"4_": "channelDelete",
				"5_": "channelUpdate",
				"6_": "RoleCreate",
				"7_": "RoleDelete",
				"8_": "RoleUpdate",
				"9_": "guildUpdate",
				"10": "MemberAdd",
				"11": "MemberRemove",
				"12": "MemberKick",
				"13": "MemberUpdate",
				"14": "MemberUnban",
				"15": "voiceChannelJoin",
				"16": "voiceChannelLeave",
				"17": "voiceStateUpdate"
			}
			if payload.user_id == S_UID:
				Remsg = await self.bot.get_channel(payload.channel_id).fetch_message(S_ID)
				new = colours[payload.emoji.name]
				doc_ref = db.document(f'Logsetting/{payload.guild_id}')
				doc = {new: "off"}
				doc_ref.update(doc)
				###
				log = db.document(f'Logsetting/{payload.guild_id}').get().to_dict()
				g1 = log.get('guildUpdate') #群組更新
				m1 = log.get('messageUpdate')#文字編輯
				m2 = log.get('messageDelete')#文字刪除
				g2 = log.get('RoleCreate') #新增身分組
				g3 = log.get('RoleDelete') #刪除身分組
				g6 = log.get('RoleUpdate')
				m3 = log.get('MemberUpdate')#成員更新
				m4 = log.get('MemberAdd')	#成員加入
				m5 = log.get('MemberKick') #成員剔除
				m6 = log.get('MemberRemove') #成員離開
				m7 = log.get('MemberNickUpdate')#暱稱變更
				g4 = log.get('channelCreate') #創建頻道
				g5 = log.get('channelDelete') #刪除頻道
				g7 = log.get('channelUpdate') #更新頻道
				v1 = log.get('voiceChannelJoin') #語音頻道進入
				v2 = log.get('voiceChannelLeave') #語音頻道離開
				v3 = log.get('voiceStateUpdate') #語音狀態更新
				v4 = log.get('voiceChannelSwitch') #成員切換語音頻道
				mT = log.get('messageDeleteBulk')#暫不開放 #暫不開放: {mT} await S_ID.add_reaction("🥰")
				u1 = log.get('MemberUnban') #成員解封
				embed = Embed(title=Lang['set_title'],
					description=Lang['set_docs'],
					colour=self.bot.user.colour,
					timestamp=datetime.utcnow())
				embed.add_field(name="Message", value=Lang['set_msg'].format(m1,m2), inline=True)
				embed.add_field(name="Guild", value=Lang['set_guild'].format(g4,g2,g5,g3,g7,g6,g1), inline=True)
				embed.add_field(name="\u200b",value="\u200b",inline=True)
				embed.add_field(name="Member", value=Lang['set_member'].format(m4,m6,m5,m3,u1), inline=True)
				embed.add_field(name="Voice", value=Lang['set_voice'].format(v1,v2,v3), inline=True)
				embed.add_field(name="\u200b",value="\u200b",inline=True)
				user_img = self.bot.get_user(S_UID).avatar or self.bot.get_user(S_UID).default_avatar
				embed.set_footer(icon_url=user_img,text=Lang['set_footer'].format(self.bot.get_user(S_UID)))
				await Remsg.edit(embed=embed)

def setup(bot):
	bot.add_cog(Firebase(bot))

