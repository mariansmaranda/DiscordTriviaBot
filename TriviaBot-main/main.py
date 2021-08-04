import discord
from discord.ext import commands
import gspread
import json
from datetime import *
from discord_components import *
# import re
# from discord.utils import get
from discord.ext import tasks, commands
from random import *
from discord.voice_client import VoiceClient
import os
from ffmpeg import *
import youtube_dl
# import schedule
import asyncio
from discord import *
import sendgrid
from tabulate import tabulate
from PIL import Image, ImageFont, ImageDraw
from sendgrid.helpers.mail import *

from oauth2client.service_account import ServiceAccountCredentials
import tracemalloc

tracemalloc.start()

# sheets auth
scope = ['https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("secrets.json", scope)
google_client = gspread.authorize(creds)

sg_token = open("sg", "r").read()
# bot token
token_file = open("bot_secret", "r")
TOKEN = token_file.read()
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="!", intents=intents)

global now
now = datetime.now()
word = ["bad"]


@client.event
async def on_ready():
    print("Bot is online")
    msg1.start()
    del_msg1.start()
    DiscordComponents(client)

@client.command(name="clear", help="Admin command!")
@commands.has_permissions(administrator=True)
async def clear(ctx):
    await ctx.channel.purge()

@client.event
async def on_member_join(ctx):
    role = discord.utils.get(ctx.guild.roles, name = "Guest")
    await ctx.add_roles(role)


@client.command(name="trivia", help="Starts a game of trivia!")
async def trivia(ctx):
    if ctx.channel.id == 852995220320288768:
        emb_msj = discord.Embed(title=f"Choose a difficulty from below!", )
        def check(res):
            return res

        msj = await ctx.channel.send(embed=emb_msj, components=[[Button(style=1, label="Easy")],
                                                                [Button(style=1, label="Normal")],
                                                                [Button(style=1, label="Hard")]])
        try:
            res = await client.wait_for("button_click", check=check)
            choice = res.component.label
            if choice == "Easy":
                for i in range(10):
                    def not_bot_reaction(reaction, user):
                        return user != client.user
                    if ctx.channel.id == 852995220320288768:
                        questions_sheet = google_client.open("TriviaSheet").worksheet("questions_easy")
                        number_of_questions = questions_sheet.row_count
                        selected_question = randint(1, number_of_questions)
                        question_list = questions_sheet.row_values(selected_question)
                        q_id = question_list[0]
                        question = question_list[1]
                        render_question = f"Question ID: {q_id}\n{question}"
                        msg = await ctx.send(render_question)
                        await msg.add_reaction("✅")
                        await msg.add_reaction("❌")
                        try:

                            reaction, user = await client.wait_for('reaction_add', timeout=10,
                                                                   check=not_bot_reaction)
                            map_answers = {
                                "True": "✅",
                                "False": "❌"
                            }
                            print(reaction.message.content)
                            question_id = int(reaction.message.content.lstrip("Question ID: ").split("\n")[0])
                            question_answers = questions_sheet.row_values(question_id)
                            if reaction.emoji == map_answers[question_answers[2]]:
                                await reaction.message.channel.send(f"Correct {user.mention}")
                                userid = user.id
                                with open("users.json") as punctaj:
                                    data = json.load(punctaj)
                                    for i in data:
                                        if i["id"] == userid:
                                            i["scor"] = i["scor"] + 1
                                            if i["scor"] == 100:
                                                sg = sendgrid.SendGridAPIClient(api_key=sg_token)
                                                from_email = Email("robert.carciumarescu97@gmail.com")
                                                to_email = i["email"]
                                                nume = i["name"]
                                                level1 = "1"
                                                mail = Mail(from_email, to_email)
                                                template_id = "d-603475a23d6b4687afe1bc5000261fad"
                                                mail.dynamic_template_data = {
                                                    "nume": nume,
                                                    "level": level1
                                                }
                                                mail.template_id = template_id
                                                response = sg.client.mail.send.post(request_body=mail.get())
                                                print(response.status_code)
                                            elif i["scor"] == 200:
                                                sg = sendgrid.SendGridAPIClient(api_key=sg_token)
                                                from_email = Email("robert.carciumarescu97@gmail.com")
                                                to_email = i["email"]
                                                nume = i["name"]
                                                level2 = "2"
                                                mail = Mail(from_email, to_email)
                                                template_id = "d-f9b2cbbabf1c42f2b6e30cbcaf2d2930"
                                                mail.dynamic_template_data = {
                                                    "nume": nume,
                                                    "level": level2
                                                }
                                                mail.template_id = template_id
                                                response = sg.client.mail.send.post(request_body=mail.get())
                                                print(response.status_code)
                                            elif i["scor"] == 300:
                                                sg = sendgrid.SendGridAPIClient(api_key=sg_token)
                                                from_email = Email("robert.carciumarescu97@gmail.com")
                                                to_email = i["email"]
                                                nume = i["name"]
                                                mail = Mail(from_email, to_email)
                                                template_id = "d-0afefe86d8f14fce86d7a732ad263e4d"
                                                mail.dynamic_template_data = {
                                                    "nume": nume,

                                                }
                                                mail.template_id = template_id
                                                response = sg.client.mail.send.post(request_body=mail.get())
                                                print(response.status_code)
                                            else:
                                                pass
                                with open('users.json', 'w') as f:
                                    json.dump(data, f, indent=4)
                                await reaction.message.delete()
                            else:
                                bad_msg = await reaction.message.channel.send(f"Incorrect! Try better next time!")
                                await bad_msg.add_reaction("💩")
                                await reaction.message.delete()
                        except asyncio.TimeoutError:
                            bad_msg = await ctx.send(f"Too SLOW!!! Be faster!")
                            await bad_msg.add_reaction("🐌")
                            await msg.delete()
                        await ctx.channel.purge()
            elif choice == "Medium":
                for i in range(10):
                    def not_bot_reaction(reaction, user):
                        return user != client.user

                    if ctx.channel.id == 852995220320288768:
                        questions_sheet = google_client.open("TriviaSheet").worksheet("questions_medium")
                        number_of_questions = questions_sheet.row_count
                        selected_question = randint(1, number_of_questions)
                        question_list = questions_sheet.row_values(selected_question)
                        q_id = question_list[0]
                        question = question_list[1]
                        render_question = f"Question ID: {q_id}\n{question}"
                        msg = await ctx.send(render_question)
                        await msg.add_reaction("✅")
                        await msg.add_reaction("❌")
                        try:

                            reaction, user = await client.wait_for('reaction_add', timeout=10,
                                                                   check=not_bot_reaction)
                            map_answers = {
                                "True": "✅",
                                "False": "❌"
                            }
                            print(reaction.message.content)
                            question_id = int(reaction.message.content.lstrip("Question ID: ").split("\n")[0])
                            question_answers = questions_sheet.row_values(question_id)
                            if reaction.emoji == map_answers[question_answers[2]]:
                                await reaction.message.channel.send(f"Correct {user.mention}")
                                userid = user.id
                                with open("users.json") as punctaj:
                                    data = json.load(punctaj)
                                    for i in data:
                                        if i["id"] == userid:
                                            i["scor"] = i["scor"] + 2
                                            if i["scor"] == 100:
                                                sg = sendgrid.SendGridAPIClient(api_key=sg_token)
                                                from_email = Email("robert.carciumarescu97@gmail.com")
                                                to_email = i["email"]
                                                nume = i["name"]
                                                level1 = "1"
                                                mail = Mail(from_email, to_email)
                                                template_id = "d-603475a23d6b4687afe1bc5000261fad"
                                                mail.dynamic_template_data = {
                                                    "nume": nume,
                                                    "level": level1
                                                }
                                                mail.template_id = template_id
                                                response = sg.client.mail.send.post(request_body=mail.get())
                                                print(response.status_code)
                                            elif i["scor"] == 200:
                                                sg = sendgrid.SendGridAPIClient(api_key=sg_token)
                                                from_email = Email("robert.carciumarescu97@gmail.com")
                                                to_email = i["email"]
                                                nume = i["name"]
                                                level2 = "2"
                                                mail = Mail(from_email, to_email)
                                                template_id = "d-f9b2cbbabf1c42f2b6e30cbcaf2d2930"
                                                mail.dynamic_template_data = {
                                                    "nume": nume,
                                                    "level": level2
                                                }
                                                mail.template_id = template_id
                                                response = sg.client.mail.send.post(request_body=mail.get())
                                                print(response.status_code)
                                            elif i["scor"] == 300:
                                                sg = sendgrid.SendGridAPIClient(api_key=sg_token)
                                                from_email = Email("robert.carciumarescu97@gmail.com")
                                                to_email = i["email"]
                                                nume = i["name"]
                                                mail = Mail(from_email, to_email)
                                                template_id = "d-0afefe86d8f14fce86d7a732ad263e4d"
                                                mail.dynamic_template_data = {
                                                    "nume": nume,

                                                }
                                                mail.template_id = template_id
                                                response = sg.client.mail.send.post(request_body=mail.get())
                                                print(response.status_code)
                                            else:
                                                pass
                                with open('users.json', 'w') as f:
                                    json.dump(data, f, indent=4)
                                await reaction.message.delete()
                            else:
                                bad_msg = await reaction.message.channel.send(f"Incorrect! Try better next time!")
                                await bad_msg.add_reaction("💩")
                                await reaction.message.delete()
                        except asyncio.TimeoutError:
                            bad_msg = await ctx.send(f"Too SLOW!!! Be faster!")
                            await bad_msg.add_reaction("🐌")
                            await msg.delete()
                        await ctx.channel.purge()
            elif choice == "Hard":
                for i in range(10):
                    def not_bot_reaction(reaction, user):
                        return user != client.user

                    if ctx.channel.id == 852995220320288768:
                        questions_sheet = google_client.open("TriviaSheet").worksheet("questions_hard")
                        number_of_questions = questions_sheet.row_count
                        selected_question = randint(1, number_of_questions)
                        question_list = questions_sheet.row_values(selected_question)
                        q_id = question_list[0]
                        question = question_list[1]
                        render_question = f"Question ID: {q_id}\n{question}"
                        msg = await ctx.send(render_question)
                        await msg.add_reaction("✅")
                        await msg.add_reaction("❌")
                        try:

                            reaction, user = await client.wait_for('reaction_add', timeout=10,
                                                                   check=not_bot_reaction)
                            map_answers = {
                                "True": "✅",
                                "False": "❌"
                            }
                            print(reaction.message.content)
                            question_id = int(reaction.message.content.lstrip("Question ID: ").split("\n")[0])
                            question_answers = questions_sheet.row_values(question_id)
                            if reaction.emoji == map_answers[question_answers[2]]:
                                await reaction.message.channel.send(f"Correct {user.mention}")
                                userid = user.id
                                with open("users.json") as punctaj:
                                    data = json.load(punctaj)
                                    for i in data:
                                        if i["id"] == userid:
                                            i["scor"] = i["scor"] + 3
                                            if i["scor"] == 100:
                                                sg = sendgrid.SendGridAPIClient(api_key=sg_token)
                                                from_email = Email("robert.carciumarescu97@gmail.com")
                                                to_email = i["email"]
                                                nume = i["name"]
                                                level1 = "1"
                                                mail = Mail(from_email, to_email)
                                                template_id = "d-603475a23d6b4687afe1bc5000261fad"
                                                mail.dynamic_template_data = {
                                                    "nume": nume,
                                                    "level": level1
                                                }
                                                mail.template_id = template_id
                                                response = sg.client.mail.send.post(request_body=mail.get())
                                                print(response.status_code)
                                            elif i["scor"] == 200:
                                                sg = sendgrid.SendGridAPIClient(api_key=sg_token)
                                                from_email = Email("robert.carciumarescu97@gmail.com")
                                                to_email = i["email"]
                                                nume = i["name"]
                                                level2 = "2"
                                                mail = Mail(from_email, to_email)
                                                template_id = "d-f9b2cbbabf1c42f2b6e30cbcaf2d2930"
                                                mail.dynamic_template_data = {
                                                    "nume": nume,
                                                    "level": level2
                                                }
                                                mail.template_id = template_id
                                                response = sg.client.mail.send.post(request_body=mail.get())
                                                print(response.status_code)
                                            elif i["scor"] == 300:
                                                sg = sendgrid.SendGridAPIClient(api_key=sg_token)
                                                from_email = Email("robert.carciumarescu97@gmail.com")
                                                to_email = i["email"]
                                                nume = i["name"]
                                                mail = Mail(from_email, to_email)
                                                template_id = "d-0afefe86d8f14fce86d7a732ad263e4d"
                                                mail.dynamic_template_data = {
                                                    "nume": nume,

                                                }
                                                mail.template_id = template_id
                                                response = sg.client.mail.send.post(request_body=mail.get())
                                                print(response.status_code)
                                            else:
                                                pass
                                with open('users.json', 'w') as f:
                                    json.dump(data, f, indent=4)
                                await reaction.message.delete()
                            else:
                                bad_msg = await reaction.message.channel.send(f"Incorrect! Try better next time!")
                                await bad_msg.add_reaction("💩")
                                await reaction.message.delete()
                        except asyncio.TimeoutError:
                            bad_msg = await ctx.send(f"Too SLOW!!! Be faster!")
                            await bad_msg.add_reaction("🐌")
                            await msg.delete()
                        await ctx.channel.purge()
            await msj.edit(components=[])
        except:
            pass

            await msj.edit(components=[])
    else:
        await ctx.send("Please use this command in trivia channel!")
        await ctx.message.delete()



@client.event
@commands.has_permissions(administrator=True, manage_roles=True)
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        pass

    else:
        with open('react_role.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name:
                    role = discord.utils.get(client.get_guild(
                        payload.guild_id).roles, id=x['role_id'])
                    await client.get_guild(payload.guild_id).get_member(payload.user_id).add_roles(role)

        with open('rules.json') as rules_file:
            data = json.load(rules_file)
            for x in data:
                if x['emoji'] == payload.emoji.name:
                    role = discord.utils.get(client.get_guild(
                        payload.guild_id).roles, id=x['role_id'])
                    await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)

                    def check1(m):
                        return m.content

                    target = await client.fetch_user(payload.user_id)
                    await target.send("Petnru login, introdu adresa de email!")
                    msg = await client.wait_for('message', check=check1)
                    if check1 != payload.member.bot:
                        user_id = payload.user_id
                        global variabila
                        variabila = check1(msg)
                        print(variabila)
                        with open("users.json") as users:
                            data = json.load(users)
                            new_user = {
                                "name": payload.member.name,
                                "id": user_id,
                                "email": variabila,
                                "scor": 0
                            }
                            data.append(new_user)
                        with open('users.json', 'w') as f:
                            json.dump(data, f, indent=4)
                        sg = sendgrid.SendGridAPIClient(api_key=sg_token)
                        from_email = Email("robert.carciumarescu97@gmail.com")
                        to_email = To(variabila)
                        nume = payload.member.name
                        mail = Mail(from_email, to_email)
                        template_id = "d-805b2d9991f3431eb526370756f53d7e"
                        mail.dynamic_template_data = {
                            "nume": nume
                        }

                        mail.template_id = template_id
                        response = sg.client.mail.send.post(request_body=mail.get())
                        print(response.status_code)

@client.event
@commands.has_permissions(administrator=True, manage_roles=True)
async def on_raw_reaction_remove(payload):
    with open('react_role.json') as react_file:
        data = json.load(react_file)
        for x in data:
            if x['emoji'] == payload.emoji.name:
                role = discord.utils.get(client.get_guild(
                    payload.guild_id).roles, id=x['role_id'])
                await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)

@client.command(name="role",help="admin command!")
@commands.has_permissions(administrator=True, manage_roles=True)
async def role(ctx, emoji, role: discord.Role, *, message):

    emb = discord.Embed(description=message)
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('rules.json') as json_file:
        data = json.load(json_file)

        new_react_role = {'role_name': role.name,
        'role_id': role.id,
        'emoji': emoji,
        'message_id': msg.id}

        data.append(new_react_role)

    with open('rules.json', 'w') as f:
        json.dump(data, f, indent=4)

@client.command(name="profile",help="Displays user profile on server!")
async def profile(ctx):
    if ctx.channel.id == 850381537982939176:
        userid = ctx.author.id
        with open("users.json") as punctaj:
            data = json.load(punctaj)
            for i in data:
                if userid == i["id"]:
                    embed = Embed(
                        title ="Trivia Score",
                        color=0x8400DB
                    )
                    embed.add_field(
                        name=f"Player {ctx.author.name}",
                        value=f"Trivia score {i['scor']}",
                        inline=False
                    )
                    if i["scor"] < 100:
                        embed.add_field(
                            name="New trivia player\nLevel UP",
                            value=f"{100 - i['scor']} points left to next level\nJunior trivia player!",
                            inline=False
                        )
                        embed.set_thumbnail(
                            url="https://cdn.discordapp.com/attachments/860479627881218058/860479793186603008/shutterstock_686118184.jpg")
                        embed.set_footer(text=f"Scris la {now.strftime('%Y-%m-%d %H:%M:%S')}")
                        await ctx.channel.send(embed=embed)

                    elif i["scor"] < 200:
                        embed.add_field(
                            name=f"Junior trivia player\nLevel UP",
                            value=f"{200 - i['scor']} points left to next level\n Experienced trivia player!",
                            inline=False
                        )
                        embed.set_thumbnail(
                            url="https://cdn.discordapp.com/attachments/860479627881218058/860479793186603008/shutterstock_686118184.jpg")
                        embed.set_footer(text=f"Scris la {now.strftime('%Y-%m-%d %H:%M:%S')}")
                        await ctx.channel.send(embed=embed)
                    elif i['scor'] < 300:
                        embed.add_field(
                            name=f"Experienced trivia player!\nLevel UP",
                            value=f"{300 - i['scor']} points left to next level\n GOD trivia player!",
                            inline=False
                        )
                        embed.set_thumbnail(
                            url="https://cdn.discordapp.com/attachments/860479627881218058/860479793186603008/shutterstock_686118184.jpg")
                        embed.set_footer(text=f"Scris la {now.strftime('%Y-%m-%d %H:%M:%S')}")
                        await ctx.channel.send(embed=embed)
                    elif i['scor'] > 300:
                        embed.add_field(
                            name=f"Maximum LEVEL reached!\nGOD trivia player!",
                            value="Now compete to be on top\n of leaderboards",
                            inline=False
                        )
                        embed.set_thumbnail(
                            url="https://cdn.discordapp.com/attachments/860479627881218058/860479793186603008/shutterstock_686118184.jpg")
                        embed.set_footer(text=f"Scris la {now.strftime('%Y-%m-%d %H:%M:%S')}")
                        await ctx.channel.send(embed=embed)
    else:
        await ctx.send("Please use this command in chat channel!")
        await ctx.message.delete()
@tasks.loop(minutes=4)
async def msg1():
    message_channel = client.get_channel(860663292921380864)
    with open("users.json") as tabel:
        data = json.load(tabel)
        for i in data:
            embed = Embed(
                title=f"Player: {i['name']} --------------- {i['scor']} points",
                color=0x8400DB
            )
            await message_channel.send(embed=embed)
@tasks.loop(minutes=3)
async def del_msg1():
    message_channel = client.get_channel(860663292921380864)
    await message_channel.purge()



youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

@client.command(name='play',help="Plays a song from a specific url!")
async def play(ctx, url):
    if ctx.channel.id == 864043898506969138:
        if not ctx.message.author.voice:
            await ctx.send("You are not connected to a voice channel")
            return

        else:
            channel = ctx.message.author.voice.channel

        await channel.connect()

        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=client.loop)
            voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('**Now playing:** {}'.format(player.title))
    else:

        await ctx.send("You are not in the music channel!")
        await ctx.message.delete()
@client.command(name='stop', help="Stops the song!")
async def stop(ctx):
    if ctx.channel.id == 864043898506969138:
        voice_client = ctx.message.guild.voice_client
        await voice_client.disconnect()
    else:
        await ctx.send("You are not in the music channel!")
        await ctx.message.delete()
@client.command(name="pause", help="Pauses the current song!")
async def pause(ctx):
    if ctx.channel.id == 864043898506969138:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Currently no audio is playing.")
    else:
        await ctx.send("You are not in the music channel!")
        await ctx.message.delete()
@client.command(name="resume", help="Reumes the current song!")
async def resume(ctx):
    if ctx.channel.id == 864043898506969138:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("The audio is not paused.")
    else:
        await ctx.send("You are not in the music channel!")
        await ctx.message.delete()


@commands.command(name="help", help="Displays all the available commands!")
@commands.has_permissions(administrator=True)
async def help(self, ctx):
    await ctx.send(self.help_message)

@client.command(name="premium_help",help="Premium Help!")
@commands.has_permissions(administrator=True)
async def premium_help(ctx):
    embed = Embed(
        title="Premium Feautres",
        color=0x8400DB,

    )
    embed.add_field(
        name="Music",
        value="Premium user can use music function on music channel!"
              "\nAll commands from above for music player are:"
              "\n!play -use this command with a link next to it to play a song that you want"
              "\n!stop -use this command to stop the current song and change with another one using !play again"
              "\n!pause -use this command to pause the current song"
              "\n!resume -use this command to resume the current song",
        inline=True
    )
    await ctx.channel.send(embed=embed)

@client.command(name="getpremium",help="Purchase premium status!")
async def getpremium(ctx):
    if ctx.channel.id == 850381537982939176:
        def check1(m):
            return m.content

        target = await client.fetch_user(ctx.author.id)
        await target.send("Introdu codul paysafe de 16 cifre")
        msg = await client.wait_for('message', check=check1)
        plata = open("paysafe_codes.txt", "a")
        plata.write(f"{check1(msg)}\n")
        plata.close()
        if check1 != ctx.author.bot:
            if len(check1(msg)) == 16:
                role = discord.utils.get(ctx.guild.roles, name="Premium")
                await ctx.author.add_roles(role)
                await ctx.send(f"{ctx.author.mention} has now Premium!")
            else:
                await target.send("Cod incorect!\nIncearca iar comanda!")
    else:
        await ctx.send("Please use this command in chat channel!")
        await ctx.message.delete()

client.run(TOKEN)