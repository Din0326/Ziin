import discord
from discord.ext import commands

from apscheduler.triggers.cron import CronTrigger

class Cog_Extension(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
		self.bot.remove_command("help")