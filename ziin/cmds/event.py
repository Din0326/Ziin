import time
import discord
import json
from discord import Embed
from discord.ext import commands
from discord.ext.commands import CheckFailure

from datetime import datetime

from core.classed import Cog_Extension

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('serviceAccount.json')

db = firestore.client()
delete_count = 0
last_audit_log_id = 0

with open('./i18n/en.json', 'r', encoding='utf-8-sig') as lang_en:
	EN = json.load(lang_en)
with open('./i18n/zh_tw.json', 'r', encoding='utf-8-sig') as lang_tw:
	TW = json.load(lang_tw)

def ctx_Check_language(ctx):
	if str(ctx.channel.type) != "private":
		data = db.document(f'Guild/{ctx.guild.id}').get().to_dict()
		Language = data.get('Language')
		if Language == "English":
			Lang = EN
		if Language == "zh-TW":
			Lang = TW
		return Lang

class Event(Cog_Extension):
	@commands.Cog.listener() #指令錯誤回報
	async def on_command_error(self, ctx, error):
		timestr = time.strftime("%m/%d-%H:%M")
		Lang = ctx_Check_language(ctx)
		user_img = ctx.author.avatar or ctx.author.default_avatar
		if isinstance(error, commands.errors.MissingRequiredArgument):
			missarg = str(error).split()[0]
			channel = self.bot.get_channel(737830510952185878)
			embed = Embed(title=Lang["error_missarg"].format(ctx.author),
					  colour=0xFF0000,
					  timestamp=datetime.utcnow())

			embed.set_thumbnail(url=user_img.url)
			fields = [(Lang["error_arg"],missarg,True)]
		
			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
			await ctx.send(embed=embed)

		elif isinstance(error, commands.errors.CommandNotFound):
			notfound = str(error).split()[1]
			channel = self.bot.get_channel(737830510952185878)
			embed = Embed(title="指令輸入錯誤",
						  colour=0xFF0000,
					      timestamp=datetime.utcnow())

			embed.set_thumbnail(url=user_img.url)
			fields = [("群组", ctx.guild.name, True),
					  ("頻道", ctx.channel.mention, True),
					  ("使用者", ctx.author, True),
					  ("指令",notfound,True)]
		
			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
			await channel.send(embed=embed)
		elif isinstance(error, commands.CommandOnCooldown):
			await ctx.channel.send(Lang["error_delay"].format(f"{error.retry_after:.1f}"),delete_after=int(error.retry_after))



def setup(bot):
		bot.add_cog(Event(bot))