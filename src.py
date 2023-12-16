# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 20:30:15 2023

@author: ketch
"""

import nest_asyncio
nest_asyncio.apply()

import discord
from transformers import pipeline, Conversation

TOKEN = 'MTE4NTI0NzkxNTAyODAwNDkyNA.Gh0GQh.vEdMN6-gvazRv7o6fa-M3aaGbdplXV5y4LFtyc'
autoreply = False

intents = discord.Intents(guilds = True, dm_messages = True, members = True, messages = True, guild_messages = True, invites = True, message_content = True)
client = discord.Client(chunk_guilds_at_startup = True, intents = intents)

model = pipeline('conversational', model = 'microsoft/DialoGPT-small')
captioner = pipeline('image-to-text', model = 'Salesforce/blip-image-captioning-base')

@client.event
async def on_ready() :
    print('Bot is ready to roll!')
    return

@client.event
async def on_message(message) :
    global autoreply
    
    if message.content == '$$stop_autoreply' :
        autoreply = False
        await message.reply('[SYSTEM] Autoreply turned off!')
        return
    if message.content == '$$start_autoreply' :
        autoreply = True
        await message.reply('[SYSTEM] Autoreply turned on!')
        return
    if message.author.bot : return
    print(f'User sent a message: {message.content}')
    
    if autoreply :
        await message.channel.typing()
        attachment_info = '. '.join([captioner(attachment.url)[0]['generated_text'] for attachment in message.attachments])
        prompt = Conversation(attachment_info + message.content)
        response = list(model.predict(prompt).iter_texts())[1][1]
        await message.reply(response)
    return

if __name__ == '__main__' :
    client.run(TOKEN)