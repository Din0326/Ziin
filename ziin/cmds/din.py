import discord
import json
from typing import Optional
from datetime import datetime, timedelta, date

from discord import Member, TextChannel, VoiceChannel
from discord.ext import commands
from discord.ext.commands import Cog, Greedy
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, cooldown, has_permissions, bot_has_permissions

from core.classed import Cog_Extension
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate('serviceAccount.json')
db = firestore.client()

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

class Din(Cog_Extension):
	async def dinID(ctx):
		if ctx.author.id == 193637455725985792:
			return True
		else:
			await ctx.send("想偷用阿垃圾 這 **Din** 專屬的好嗎",delete_after=10)

	#@commands.command(hidden=True)
	#@commands.check(dinID)
	#async def ss(self,ctx):
	#	with open('keyword.json', 'r', encoding='utf-8-sig') as tfile:
	#		tdata = json.load(tfile)
	#		val = '4'
	#	keys = [k for k, v in tdata.items() if v == 'hi']
	#	await ctx.send(tdata.items())
	#	await ctx.send(keys)
	@commands.command()
	@commands.check(dinID)
	async def renick(self,ctx):
		for i in ctx.guild.members:
			await ctx.send(i)
			member = self.bot.get_guild.get_member(i.id)
			await member.edit(nick=None)


	@commands.command()
	@commands.check(dinID)
	async def din_steal(self,ctx, emoji: discord.PartialEmoji, *roles: discord.Role):
		"""This clones a specified emoji that only specified roles
		are allowed to use.
		"""
	
		# fetch the emoji asset and read it as byte
		emoji_bytes = await emoji.url.read()
	
		# the key parameter here is `roles`, which controls
		# what roles are able to use the emoji.
		await ctx.guild.create_custom_emoji(
			name=emoji.name,
			image=emoji_bytes,
			reason=None
		)
		await ctx.send("done")
		await ctx.send(emoji)

	@commands.command(hidden=True)
	@commands.check(dinID)
	async def din_add(self,ctx,*,msg):
		keyword = str(msg.split(' ')[0])
		reply = str(msg.split(' ')[1])
		if reply == None:
			return
		with open('keyword.json', 'r', encoding='utf8') as tfile:
			tdata = json.load(tfile)
		with open('keyword.json', 'w', encoding='utf8') as tfile:
			if keyword in tdata.keys(): #判斷 觸發詞 有沒有在 msgre 裡面
				oldmsg = tdata[keyword]  # 抓取對應的 setting.json 名稱
				oldmsg.append(f"{reply}")
				json.dump(tdata,tfile,indent=4,ensure_ascii=False)  #剛剛是判斷他有再msgre 裡面 所以直接在原本有的 "xx" 去新增1
				await ctx.send("已新增新觸發詞")
			else:
				tdata[keyword] = [reply]
				json.dump(tdata,tfile,indent=4,ensure_ascii=False)
				await ctx.send("已新增新觸發詞及回復")

	@commands.command(hidden=True)
	@commands.check(dinID)
	async def din_forall(self,ctx,*,msg):
		for x in range(len(self.bot.guilds)):
			owner = self.bot.guilds[x-1].owner
			await owner.send(msg)
		await ctx.send("done!")

	@commands.command(hidden=True)
	@commands.check(dinID)
	async def din_ua(self, ctx, target: int):
		target = await self.bot.fetch_user(target)
		target_icon = target.avatar or target_default_avatar
		await ctx.send(target_icon.url)
		#embed = Embed(title=f"{target} Avatar",
		#			  timestamp=datetime.utcnow())
#
		#embed.set_image(url=target.avatar.url)
		#await ctx.send(embed=embed)

	@commands.command(hidden=True)
	@commands.check(dinID)
	async def din_sl(self,ctx,*,lang: str):
		info = db.document(f'Guild/{ctx.guild.id}')
		language = db.document(f'Guild/{ctx.guild.id}').get().to_dict().get('Language')
		if lang.lower() == "tw": 
			doc = {'Language': "zh-TW"}
			info.update(doc)
			await ctx.send("語言設置已更改為 **繁體中文**")
		elif lang.lower() == "en": 
			doc = {'Language': "English"}
			info.update(doc)
			await ctx.send("Language change to **English**")

	@commands.command()
	@commands.check(dinID)
	async def din_p(self,ctx,*,new_prefix: str):
		Lang , guild_tz = ctx_Check_language(ctx)
		if len(new_prefix) <= 3: 
			info = db.document(f'Guild/{ctx.guild.id}').get().to_dict()
			old = info.get('Prefix')
			doc_ref = db.document(f'Guild/{ctx.guild.id}')
			doc = {'Prefix': new_prefix}
			doc_ref.update(doc)
			await ctx.send(Lang["prefix_new"].format(new_prefix))
		else:
			await ctx.send(Lang["prefix_max"])

	@commands.command(hidden=True)
	@commands.check(dinID)
	async def din_tz(self,ctx,*,utc_time: int):
		info = db.document(f'Guild/{ctx.guild.id}')
		if 12 >= utc_time >= -12:
			doc = {'TimeZone': utc_time}
			info.update(doc)
			if utc_time >= 0:
				await ctx.send(f"時區已設置為 **UTC+{utc_time}**")
			else:
				await ctx.send(f"時區已設置為 **UTC{utc_time}**")
		else:
			await ctx.send("請輸入正確UTC時間 **12** ~ **-12**")

	@commands.command(hidden=True)
	@commands.check(dinID)
	async def din_send(self,ctx,*,msg):
		ChannelID = int(msg.split( )[0])
		text = msg.split( )[1]
		textchannel = self.bot.get_channel(ChannelID)
		await textchannel.send(text)


	@commands.command(hidden=True)
	@commands.check(dinID)
	async def din_dm(self,ctx,*,msg):
		dmID = int(msg.split( )[0])
		dmmsg = msg.split( )[1]
		dmmember = self.bot.get_user(dmID)
		await dmmember.send(dmmsg)

#### 最高權限指令
	@commands.command(hidden=True)
	@commands.check(dinID)
	async def din_n(self, ctx, member: discord.Member, *,nick):
		await member.edit(nick=nick)
		await ctx.send(f'{member.mention} 暱稱已更改為 __{nick}__')

	@commands.command(hidden=True)
	@commands.check(dinID)
	async def din_m(self, ctx, member: discord.Member, *, reason=None):
		await member.edit(reason=reason,mute= True)
		await ctx.send(f'{member.mention} 耖你媽閉嘴.')

	@commands.command(hidden=True)
	@commands.check(dinID)
	async def din_um(self, ctx, member: discord.Member, *, reason=None):
		await member.edit(reason=reason,mute= False)
		await ctx.send(f'{member.mention} 原諒你一次.')

	@commands.command(hidden=True)
	@commands.check(dinID)
	async def din_b(self, ctx, user : discord.Member, *, reason=None):
		await user.ban(reason=reason)
		await ctx.send(f'{user.mention}　死去\n||ID : {user.id}|| \nR.I.P. \n{user.joined_at.strftime("%Y-%m-%d")} ~ {date.today()}')

	@commands.command(hidden=True)
	@commands.check(dinID)
	async def din_ub(self, ctx, target: int, *, reason=None):
		user = self.bot.get_user(target)
		await ctx.guild.unban(user, reason=reason)
		await ctx.send(f'{user.name}#{user.discriminator} unbanned')
		

	@commands.command(hidden=True)
	@commands.check(dinID)
	async def din_k(self, ctx, target: discord.Member, *, reason=None):
		await target.kick(reason=reason)
		await ctx.send(f'{target.mention} 遠走高飛了')

	@commands.command(hidden=True)
	@commands.check(dinID)
	async def din_c(self, ctx, targets: Greedy[Member], limit: Optional[int] = 1):
		def _check(message):
			return not len(targets) or message.author in targets
		if 0 < limit <= 500:
			with ctx.channel.typing():
				await ctx.message.delete()
				deleted = await ctx.channel.purge(limit=limit, after=datetime.utcnow()-timedelta(days=14),
												  check=_check)

				await ctx.send(f"Deleted {len(deleted):,} messages.", delete_after=5)
		else:
			await ctx.send("一次最多500啦 智障")

	@commands.command(hidden=True)
	@commands.check(dinID)
	async def din_inv(self, ctx, *, serverid:int):
		channelid = self.bot.get_guild(serverid).channels[10].id
		channel = self.bot.get_channel(channelid)
		link = await channel.create_invite()
		await ctx.send(link)

	@commands.command(hidden=True)
	@commands.check(dinID)
	async def din_get(self, ctx):
		users = len(self.bot.users)
		guilds = len(self.bot.guilds)
		await ctx.send(f"user : {users}\nguild : {guilds}")

	@commands.command(hidden=True)
	@commands.check(dinID)
	async def din_lg(self, ctx, *, serverid:int):
		guild = self.bot.get_guild(serverid)
		await self.bot.get_guild(serverid).leave()
		await ctx.send(f"leave {guild}")

	#@commands.command(hidden=True)
	#@commands.check(dinID)
	#async def checknick(self, ctx):
	#	for i in ctx.guild.member:
	#		if i.nick.startswith()

	@commands.command(hidden=True)
	@has_permissions(ban_members = True)
	async def din_rc(self, ctx):
		if ctx.guild.id == 804604858090127360:
			#guild = ctx.guild
			boost = ctx.guild.get_role(805074449668898878)
			vip = ctx.guild.get_role(855376997429673985)
			await ctx.send("start")
			for i in ctx.guild.members:
				if boost not in i.roles:
					if vip not in i.roles:
						count = 0
						for x in i.roles:
							if 38 <= x.position and x.name not in ["BOT","Manager","Trial Mod","Bot Manager","Moderator","Quarantine","Statbot","Dev","First God-Like","God-Like","Lexa","Streamer"] and count == 0:
								await ctx.send(f"!!! {i.mention}  //  {x}")
								count = 1
							#else:
							#	if 38 <= x.position and x.name not in ["BOT","Manager","Trial Mod","Bot Supreme Leader","Moderator"]:
							#		await ctx.send(f"!!! {i.mention}  //  {x}")
					else:
						count == 0
						for x in i.roles:
							if 38 <= x.position and x.name not in ["BOT","Manager","Trial Mod","Bot Manager","Moderator","Quarantine","Statbot","Dev","First God-Like","God-Like","Lexa","Streamer"] and count == 0:
								await ctx.send(f"!!! {i.mention}  //  {x} // {vip}")
								count = 1
							else:
								if x.id == 855376997429673985:
									await ctx.send(f"!!! {i.mention} // {vip}")
									count = 1
	@commands.command(hidden=True)
	@has_permissions(ban_members = True)
	async def din_nickc(self, ctx):
		if ctx.guild.id == 804604858090127360:
			#guild = ctx.guild
			boost = ctx.guild.get_role(805074449668898878)
			vip = ctx.guild.get_role(855376997429673985)
			await ctx.send("start")
			for i in ctx.guild.members:
				if i.nick != None:
					if boost not in i.roles:
						await ctx.send(i.mention)
			await ctx.send("done")
	@commands.command(hidden=True)
	@has_permissions(ban_members = True)
	async def din_vvc(self, ctx):
		if ctx.guild.id == 804604858090127360:
			#guild = ctx.guild
			boost = ctx.guild.get_role(805074449668898878)
			vip = ctx.guild.get_role(855376997429673985)
			await ctx.send("start")
			for i in ctx.guild.members:
				if boost not in i.roles and vip in i.roles:
						await ctx.send(f"!!! {i.mention} // {vip}")

			await ctx.send("done")
#
		




def setup(bot):
		bot.add_cog(Din(bot))