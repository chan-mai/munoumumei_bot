# coding: utf-8
from asyncio.windows_events import NULL
from itertools import count
from config import config
import asyncio
import discord
from discord.ext import commands
from dislash import slash_commands, Option, OptionType
from datetime import datetime, timedelta
import os
import re

client = commands.Bot(command_prefix='/')
slash = slash_commands.SlashClient(client)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="新鮮な社会不適合者", type=1))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

#VC参加
@slash.command(
    name = 'join',
    description = '現在参加中のVCに接続',
)
async def join(inter):
    now = datetime.utcnow() + timedelta(hours=9)
    await inter.reply('wait...')

    if inter.author.voice is None:
        error_embed = discord.Embed(title=f"Error {now:%m/%d-%H:%M}",description="現在ボイスチャンネルに接続されていません",color=discord.Colour.red())
        await client.get_channel(inter.channel.id).send(embed=error_embed)
    
    await inter.author.voice.channel.connect()

#VC退出
@slash.command(
    name = 'exit',
    description = '現在参加中のVCから切断',
)
async def exit(inter):
    now = datetime.utcnow() + timedelta(hours=9)
    await inter.reply('wait...')

    if inter.guild.voice_client is None:
        error_embed = discord.Embed(title=f"Error {now:%m/%d-%H:%M}",description="現在ボイスチャンネルに接続されていません",color=discord.Colour.red())
        await client.get_channel(inter.channel.id).send(embed=error_embed)
        return
    await inter.guild.voice_client.disconnect()

#VC参加通知
@client.event
async def on_voice_state_update(member, before, after): 
    if before.channel != after.channel:
        now = datetime.utcnow() + timedelta(hours=9)
        if before.channel is None:
            #全てのチャンネルを取得
            all_ch = client.get_all_channels()
            
            send_ch_list = []
            act_send_ch_list = []

            #送信先候補を列挙
            for ch in all_ch:
                #ボイスチャットじゃないの
                if str(ch.type) != "voice":
                    #カテゴリー内に該当するチャンネルが存在しない場合の保険
                    act_send_ch_list.append(ch.id)
                    #チャンネルidが一致するやつ
                    if ch.category_id == after.channel.category_id:
                        send_ch_list.append(ch.id)
                        
            #通知もしくは聞き専チャンネルが同一カテゴリー内に存在しない場合
            if len(send_ch_list) == 0:
                #VCと同一カテゴリー内にテキストチャンネルが存在しない場合
                send_ch = client.get_channel(act_send_ch_list[-1])
                join_embed = discord.Embed(title=f"{after.channel.name} へ参加",description=f"{now:%m/%d-%H:%M} に {member.name} が {after.channel.name} に参加しました。",color=discord.Colour.green())
                await send_ch.send(embed=join_embed)
            else:
                #VCと同一カテゴリー内にテキストチャンネルが存在する場合
                send_ch = client.get_channel(send_ch_list[0])
                join_embed = discord.Embed(title=f"{after.channel.name} へ参加",description=f"{now:%m/%d-%H:%M} に {member.name} が {after.channel.name} に参加しました。",color=discord.Colour.green())
                await send_ch.send(embed=join_embed)

            

        elif after.channel is None:
            #全てのチャンネルを取得
            all_ch = client.get_all_channels()

            send_ch_list = []
            act_send_ch_list = []

            #送信先候補を列挙
            for ch in all_ch:
                #ボイスチャットじゃないの
                if str(ch.type) != "voice":
                    #カテゴリー内に該当するチャンネルが存在しない場合の保険
                    act_send_ch_list.append(ch.id)
                    #チャンネルidが一致するやつ
                    if ch.category_id == before.channel.category_id:
                        send_ch_list.append(ch.id)
                        
            #通知もしくは聞き専チャンネルが同一カテゴリー内に存在しない場合
            if len(send_ch_list) == 0:
                #VCと同一カテゴリー内にテキストチャンネルが存在しない場合
                send_ch = client.get_channel(act_send_ch_list[-1])
                exit_embed = discord.Embed(title=f"{before.channel.name} から退出",description=f"{now:%m/%d-%H:%M} に {member.name} が {before.channel.name} から退出しました",color=discord.Colour.red())
                await send_ch.send(embed=exit_embed)
            else:
                #VCと同一カテゴリー内にテキストチャンネルが存在する場合
                send_ch = client.get_channel(send_ch_list[0])
                exit_embed = discord.Embed(title=f"{before.channel.name} から退出",description=f"{now:%m/%d-%H:%M} に {member.name} が {before.channel.name} から退出しました",color=discord.Colour.red())
                await send_ch.send(embed=exit_embed)

client.run(config.discord_token)