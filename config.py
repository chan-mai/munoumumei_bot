# coding: utf-8
import configparser

class config():
    #トークン周り
    bot_token = configparser.ConfigParser()
    bot_token.read('bot_token.ini')

    data = 'data'
    print(f"discord_token : {bot_token.get(data, 'discord_token')}")
    discord_token = bot_token.get(data, 'discord_token')