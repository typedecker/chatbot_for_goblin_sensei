# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 23:27:46 2023

@author: ketch
"""

import nest_asyncio
nest_asyncio.apply()

# Data Retrieval

import discord, os

lim = 1000
TOKEN = 'BOT_TOKEN'
messages = []

intents = discord.Intents(guilds = True, dm_messages = True, members = True, messages = True, guild_messages = True, invites = True, message_content = True)
client = discord.Client(chunk_guilds_at_startup = True, intents = intents)

class Message :
    def __init__(self, author, content, timestamp, discord_obj) :
        self.author, self.content, self.timestamp = author, content, timestamp
        self.reference = None
        if discord_obj.reference :
            try :
                ref_obj = await discord_obj.channel.fetch_message(discord_obj.reference.message_id)
                self.reference = Message(ref_obj.author, ref_obj.content, ref_obj.created_at, ref_obj)
            except discord.NotFound :
                pass
        return
    
    pass

@client.event
async def on_ready() :
    print('Ready to collect data')
    return

@client.event
async def on_message(message) :
    global lim, messages
    
    if message.content == '$$collect_data' :
        response_msg = await message.reply('Starting data collection...')
        print('Data collection is about to start....')
        
        count = 0
        async for _msg in message.channel.history(limit = lim) :
            try :
                messages.append(Message(_msg.author, _msg.content, _msg.created_at, _msg))
                if count % 31 == 0 : await response_msg.edit(content = f'Collecting data... ({count}/{lim})')
            except discord.NotFound :
                continue
            count += 1
            continue
        
        print(f'Data fetched: {count} samples')
        await response_msg.edit(content = f'Data collection ended. {count} number of samples collected!')
    elif message.content == '$$append_data' :
        response_msg = await message.reply('Starting data collection...')
        print('Data collection is about to start....')
        
        count = 0
        async for _msg in message.channel.history(limit = lim) :
            try :
                messages.append(Message(_msg.author, _msg.content, _msg.created_at, _msg))
                if count % 31 == 0 : await response_msg.edit(content = f'Collecting data... ({count}/{lim})')
            except discord.NotFound :
                continue
            count += 1
            continue
        
        print(f'Data fetched: {count} samples')
        await response_msg.edit(content = f'Data collection ended. {count} number of samples collected!')
    elif message.content == '$$clear_data' :
        messages = []
        print('Data cleared.')
        await message.reply('Data cleared.')
    elif message.content.startswith('$$set_limit ') :
        lim = int(message.content[len('$$set_limit ') : ].strip())
        await message.reply(f'Limit set to {lim}!')
    elif message.content == '$$collect_all_data' :
        guild = message.channel.guild
        guild_channels = await guild.fetch_channels()
        
        response_msg = await message.reply('Starting data collection...')
        print('Data collection is about to start....')
        
        count = 0
        for channel in guild_channels :
            async for _msg in channel.history(limit = lim) :
                messages.append(Message(_msg.author, _msg.content, _msg.created_at, _msg))
                if count % 73 == 0 : await response_msg.edit(content = f'Collecting data... ({count}/{lim})')
                count += 1
                continue
            continue
        
        print(f'Data fetched: {count} samples')
        await response_msg.edit(content = f'Data collection ended. {count} number of samples collected!')
    # elif message.content == '$$save_data' :
    #     print('Saving data in a tsv file....')
    #     with open('data.tsv', 'a', encoding = 'utf-8') as f :
    #         lines = [key + '\t' + data[key] for key in data]
    #         f.write('\n'.join(lines))
    #         print('Data appended in file: [data.tsv]')
    return

if __name__ == '__main__' :
    client.run(TOKEN)