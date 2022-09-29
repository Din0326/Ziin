import discord
from discord.ext import commands
import json
import random
import os
import asyncio
import datetime
import schedule
import requests
import datetime
import logging
from time import strftime
from datetime import datetime


from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import (CommandNotFound)

# Firebase 資料庫
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def get_prefix(bot, message):
    if str(message.channel.type) != "private":
        doc = db.document(f'Guild/{message.guild.id}').get().to_dict()
        return doc.get('Prefix')
    else:
        return "cantuse"

# 讀取setting.json
with open('setting.json', 'r', encoding='utf-8-sig') as jfile:
    jdata = json.load(jfile)

with open('./i18n/en.json', 'r', encoding='utf-8-sig') as lang_en:
    EN = json.load(lang_en)

with open('./i18n/zh_tw.json', 'r', encoding='utf-8-sig') as lang_tw:
    TW = json.load(lang_tw)

bot = commands.Bot(command_prefix=get_prefix,intents = discord.Intents.all(),help_command=None)
#slash = SlashCommand(bot, sync_commands = True)
bot.VERSION = "2.0"

        

@bot.event
async def on_ready():
    print(" Bot ONLINE ! ")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="• z!link • z!help"))
    #bot.reload_extension(F'cmds.meta')

@bot.command(hidden=True)
async def load(ctx, extension):
    user = bot.get_user(193637455725985792)
    if ctx.author == user:
        bot.load_extension(F'cmds.{extension}')
        print(F'Loaded {extension} done.')
        await ctx.send(F'Loaded {extension} done.')

@bot.command(hidden=True)
async def unload(ctx, extension):
    user = bot.get_user(193637455725985792)
    if ctx.author == user:
        bot.unload_extension(F'cmds.{extension}')
        print(F'Unloaded {extension} done.')
        await ctx.send(F'Unloaded {extension} done.')

@bot.command(hidden=True)
async def reload(ctx, extension):
    user = bot.get_user(193637455725985792)
    if ctx.author == user:
        bot.reload_extension(F'cmds.{extension}')
        print(F'Reloaded {extension} done.')
        await ctx.send(F'Reloaded {extension} done.')

@bot.command(name="shutdown" , aliases=["關閉"],hidden=True)
async def shutdown(ctx):
    user = bot.get_user(193637455725985792)
    if ctx.author == user:
        await ctx.send("Shutting down...")
        await bot.logout()
    else:
        await ctx.send("你沒權限啦 機掰")

#
for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(F'cmds.{filename[:-3]}')
        print(f"{filename[:-3]} done.")

if __name__ =="__main__":
    bot.run(jdata['TOKEN'])