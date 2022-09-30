import discord
from discord.ext import commands
from discord import app_commands

from core.classes import Cog_Extension

class Firebase(Cog_Extension):

	@commands.Cog.listener()
	async def on_ready(self) -> None:
		print('start.')
		guildFirebase = [int(guild.id) for guild in self.db.collection(f'Guild').stream()]
		LogsettingFirebase = [int(guild.id) for guild in self.db.collection(f'Logsetting').stream()]
		for i in self.bot.guilds:
			count = 0
			if i.id in guildFirebase:
				count += 1
			if i.id in LogsettingFirebase:
				count += 5
			
			if count != 6:
				if count == 0:
					print(f"{i.id,i.name} not in both.")
				elif count == 1:
					print(f"{i.id,i.name} not in logset.")
				elif count == 5:
					print(f"{i.id,i.name} not in guild.")
		print('done.')

	@commands.Cog.listener()
	async def on_guild_join(self,guild):
		join = self.bot.get_channel(766318401441628210)
		##### guild 資料
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
		info_ref = self.db.collection("Guild").document(f"{guild.id}")
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
		set_ref = self.db.collection("Logsetting").document(f"{guild.id}")
		set_ref.set(logsetting)

		await join.send(f'Name: {guild.name}\nID: {guild.id}\nDatabase Done!')

		async for entry in guild.audit_logs(limit=1,action=discord.AuditLogAction.bot_add):
			await entry.user.send(self.jdata['welcome_text'])
#
	@commands.Cog.listener()
	async def on_guild_leave(self,guild):
		join = self.bot.get_channel(766318401441628210)
		await join.send(f'Name: {guild.name}\nID: {guild.id}\nLeave Guild!')
	
	@app_commands.command()
	async def test(self,intercation: discord.Integration):
		await intercation.response.send_message(self.jdata['welcome_text'])
	
async def setup(bot):
	await bot.add_cog(Firebase(bot))