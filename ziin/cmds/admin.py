import discord
import json
import requests
from io import BytesIO
import os
import aiohttp
from discord import Embed, Member, TextChannel, VoiceChannel, PartialEmoji, Role
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions, has_guild_permissions
from discord.ext.commands import Cog, Greedy

from typing import Optional
from datetime import datetime, date, timedelta


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
	if Language == "English":
		Lang = EN
	if Language == "zh-TW":
		Lang = TW
	return Lang

class Admin(Cog_Extension):
	" 管理員 "
	@commands.command()
	@has_permissions(administrator=True)
	async def prefix(self,ctx,*,new_prefix: str):
		Lang = ctx_Check_language(ctx)
		if len(new_prefix) <= 3: 
			info = db.document(f'Guild/{ctx.guild.id}').get().to_dict()
			old = info.get('Prefix')
			doc_ref = db.document(f'Guild/{ctx.guild.id}')
			doc = {'Prefix': new_prefix}
			doc_ref.update(doc)
			await ctx.send(Lang["prefix_new"].format(new_prefix))
		else:
			await ctx.send(Lang["prefix_max"])

	@commands.command(aliases=["lang"])
	@has_permissions(administrator=True)
	async def language(self,ctx,*,lang: str):
		info = db.document(f'Guild/{ctx.guild.id}')
		language = db.document(f'Guild/{ctx.guild.id}').get().to_dict().get('Language')
		if lang.lower() == "chinese" or lang == "中文": 
			doc = {'Language': "zh-TW"}
			info.update(doc)
			await ctx.send("語言設置已更改為 **繁體中文**")
		elif lang.lower() == "english" or lang.lower() == "en" or lang == "英文": 
			doc = {'Language': "English"}
			info.update(doc)
			await ctx.send("Language change to **English**")

	@commands.command()
	@has_permissions(administrator=True)
	async def timezone(self,ctx,*,utc_time: int):
		info = db.document(f'Guild/{ctx.guild.id}')
		Lang = ctx_Check_language(ctx)
		if 12 >= utc_time >= -12:
			doc = {'TimeZone': utc_time}
			info.update(doc)
			if utc_time >= 0:
				await ctx.send(Lang['tz_set_more0'].format(utc_time))
			else:
				await ctx.send(Lang['tz_set_less0'].format(utc_time))
		else:
			await ctx.send(Lang['tz_error'])
	
	@commands.command()
	@has_permissions(manage_emojis=True)
	async def addemote(self,ctx,*,msg):
		name = msg.split(" ")[0]
		link = msg.split(" ")[1].read()
		response = requests.get(link)
		img = (Image.open(BytesIO(response.content))).read()
		await ctx.guild.create_custom_emoji(name=name,image=img)

	@commands.command()
	@has_permissions(manage_nicknames=True)
	async def nick(self, ctx, member: discord.Member, *,nick):
		Lang = ctx_Check_language(ctx)
		await member.edit(nick=nick)
		await ctx.send(Lang["nick_change"].format(member.mention,nick))

	@commands.command()
	@has_guild_permissions(mute_members = True)
	async def mute(self, ctx, member: discord.Member, *, reason=None):
		Lang = ctx_Check_language(ctx)
		await member.edit(mute=True,reason=reason)
		await ctx.send(Lang["member_mute"].format(member.mention))

	@commands.command()
	@has_guild_permissions(mute_members = True)
	async def unmute(self, ctx, member: discord.Member, *, reason=None):
		Lang = ctx_Check_language(ctx)
		await member.edit(reason=reason,mute= False)
		await ctx.send(Lang["member_unmute"].format(member.mention))

	@commands.command()
	@has_permissions(ban_members = True)
	async def ban(self, ctx, member: discord.Member, *, reason=None):
		Lang = ctx_Check_language(ctx)
		await member.ban(reason=reason)
		await ctx.send(Lang["member_ban"].format(member.mention))

	@commands.command()
	@has_permissions(ban_members = True)
	async def unban(self, ctx, target: int, *, reason=None):
		Lang = ctx_Check_language(ctx)
		user = self.bot.get_user(target)
		await ctx.guild.unban(user, reason=reason)
		await ctx.send(Lang["member_unban"].format(user.name,user.discriminator))
		

	@commands.command()
	@has_permissions(kick_members = True)
	async def kick(self, ctx, target: discord.Member, *, reason=None):
		Lang = ctx_Check_language(ctx)
		await target.kick(reason=reason)
		await ctx.send(Lang["member_kick"].format(target.mention))

	@commands.command()
	@has_permissions(manage_messages=True)
	@bot_has_permissions(manage_messages=True)
	async def clear(self, ctx, limit: Optional[int], targets: Greedy[Member]):
		def _check(message):
			return not len(targets) or message.author in targets
		Lang = ctx_Check_language(ctx)
		limit = limit or 1
		if 0 < limit <= 500:
			with ctx.channel.typing():
				await ctx.message.delete()
				deleted = await ctx.channel.purge(limit=limit, after=datetime.utcnow()-timedelta(days=14),
												  check=_check)

				await ctx.send(Lang["message_clear"].format(len(deleted)), delete_after=5)

		else:
			await ctx.send(Lang["message_clear_limit"])

	@commands.command()
	@has_permissions(manage_emojis=True)
	@bot_has_permissions(manage_emojis=True)
	async def steal(self,ctx, emoji: discord.PartialEmoji, *roles: discord.Role):
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


def setup(bot):
		bot.add_cog(Admin(bot))