
import schedule
import json
import re
import os
import discord
from datetime import datetime
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from config.local_settings import DISCORD_TOKEN, GUILD_ID, ROLE_ID
from config.settings import CHECK_WL_ROLE_NAME

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)

def _get_waitlist():
    if os.path.exists('wait_list.json'):
        with open('wait_list.json', 'r') as f:
            wait_list = json.load(f)
    else:
        wait_list = []
    return wait_list

async def _check_waitlist(bot=bot):
    ROLE = bot.get_guild(GUILD_ID).get_role(ROLE_ID)
    wait_list = _get_waitlist()
    all_waitlist_users = [i['username'] for i in wait_list]

    members = bot.get_guild(GUILD_ID).members
    members_names = [f"{m.name}#{m.discriminator}" for m in members]
    for member, name in zip(members, members_names):
        if name in all_waitlist_users:
            await member.add_roles(ROLE)
            wait_list = [i for i in wait_list if i['username'] != name]
            print(f'Approved {name}... Removing from waitlist')

    if not members:
        print(f'No members found on the waitlist.')
    with open('wait_list.json', 'w') as f:
        json.dump(wait_list, f, indent=4)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    scheduler = AsyncIOScheduler()
    scheduler.add_job(_check_waitlist, CronTrigger(hour="*", minute="*", second="0,30")) 
    scheduler.start()
    wait_list = _get_waitlist()
    print(f"Current wait list: \n{wait_list}")

@bot.event
async def on_command_error(ctx, error):
    print(type(error))
    if isinstance(error, commands.BadArgument):
        await ctx.send(f'Command failed. Make sure your arguments are correctly formatted.')
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send(f'Command failed. You aren\'t authorized to use it.')
    else:
        await ctx.send(f'Command failed. Please let the admin know.\n{error}')
    print(f'FAILED: {error}')

    

@bot.command(name='refer', help='Refer a new user')
async def on_message(ctx, username):
    wait_list = _get_waitlist()
    try:
        user_dict = {
            "username": username,
            "createdAt": f"{datetime.now():%Y/%m/%d %H:%M}",
            "referrer": str(ctx.author)
        }
        wait_list.append(user_dict)

        with open('wait_list.json', 'w') as f:
            json.dump(wait_list, f, indent=4)
        response = f"Successfully added {username} to the waitlist!"
    except Exception as e:
        response = f"Failed to add {username} to the waitlist... {repr(e)}"
    print(response)
    await ctx.send(response)

@bot.command(name='check_wl', help='Check the current waitlist')
@commands.has_role(CHECK_WL_ROLE_NAME)
async def print_list(ctx):
    wait_list = _get_waitlist()
    wait_list_users = [u['username'] for u in wait_list]
    wait_list_users = "\n".join(wait_list_users)
    response = f"Users currently on the waitlist: \n{wait_list_users}"

    await ctx.send(response)


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
