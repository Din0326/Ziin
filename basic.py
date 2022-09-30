import discord
from discord.ext import commands
from discord import app_commands

from core.classes import Cog_Extension

class Basic(Cog_Extension):

	@commands.Cog.listener()
	async def on_message(self,msg):
		if msg.channel == self.bot.get_channel(1024723218638049280):
			#await msg.publish()
			await msg.add_reaction("✅")
	
	@app_commands.command()
	async def what(self,interaction: discord.Interaction):
		await interaction.response.send_message(f'what what?')
	
	@app_commands.command()
	async def ping(self,intercation: discord.Integration):
		Lang , guild_tz = self.ctx_check_Guild_lang_TZ(intercation)
		await intercation.response.send_message(Lang["ping"].format(round(self.bot.latency*1000)))

	@app_commands.command(name='get')
	async def get(self,intercation: discord.Integration):
		doc = self.db.collection(f'Guild').get()
		await intercation.response.send_message(doc.get())
	
	@app_commands.command()
	async def join(self, intercation: discord.Integration):
		channel = intercation.user.voice.channel
		voice = discord.utils.get(self.bot.voice_clients, guild=intercation.guild)
		
		if voice and voice.is_connected():
			await voice.move_to(channel)
		else:
			voice = await channel.connect()
			print(f"The bot has connected to {channel}\n")
	
	@app_commands.command()
	async def leave(self, intercation):
		channel = intercation.user.voice.channel
		voice = discord.utils.get(self.bot.voice_clients, guild=intercation.guild)
	
		if voice and voice.is_connected():
			await voice.disconnect()
			print(f"The bot has left {channel}")
	
async def setup(bot):
	await bot.add_cog(Basic(bot))