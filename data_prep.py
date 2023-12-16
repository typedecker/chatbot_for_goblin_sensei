# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 23:27:46 2023

@author: ketch
"""

# from transformers import pipeline, Conversation

# from transformers import AutoTokenizer

# tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-small')
# print(tokenizer)

# response1_encoded = tokenizer('hey sup')
# print(response1_encoded)

# response1_decoded = tokenizer.decode(response1_encoded['input_ids'])
# print(response1_decoded)

import nest_asyncio
nest_asyncio.apply()

# Data Retrieval

import discord, os

lim = 1000
TOKEN = 'BOT_TOKEN'

intents = discord.Intents(guilds = True, dm_messages = True, members = True, messages = True, guild_messages = True, invites = True, message_content = True)
client = discord.Client(chunk_guilds_at_startup = True, intents = intents)

@client.event
async def on_ready() :
    print('Ready to collect data')
    return

@client.event
async def on_message(message) :
    global lim
    
    if message.content == '$$collect_data' :
        response_msg = await message.reply('Starting data collection...')
        print('Data collection is about to start....')
        
        data = {}
        
        count = 0
        async for _msg in message.channel.history(limit = lim) :
            try :
                if _msg.author.name == 'typedecker' and _msg.reference != None and not _msg.is_system() :
                    reference_msg = await message.channel.fetch_message(_msg.reference.message_id)
                    data[reference_msg.content] = _msg.content
                    await response_msg.edit(content = f'Collecting data... ({count}/{lim})')
            except discord.NotFound :
                continue
            count += 1
            continue
        
        print(f'Data fetched: {len(data)} samples')
        await response_msg.edit(content = f'Data collection ended. {len(data)} number of samples collected!')
        
        print('Saving data in a tsv file....')
        with open('data.tsv', 'w', encoding = 'utf-8') as f :
            lines = [key + '\t' + data[key] for key in data]
            f.write('\n'.join(lines))
            print('Data saved in file: [data.tsv]')
    elif message.content == '$$append_data' :
        response_msg = await message.reply('Starting data collection...')
        print('Data collection is about to start....')
        
        data = {}
        
        count = 0
        async for _msg in message.channel.history(limit = lim) :
            try :
                if _msg.author.name == 'typedecker' and _msg.reference != None and not _msg.is_system() :
                    reference_msg = await message.channel.fetch_message(_msg.reference.message_id)
                    data[reference_msg.content] = _msg.content
                    await response_msg.edit(content = f'Collecting data... ({count}/{lim})')
            except discord.NotFound :
                continue
            count += 1
            continue
        
        print(f'Data fetched: {len(data)} samples')
        await response_msg.edit(content = f'Data collection ended. {len(data)} number of samples collected!')
        
        print('Saving data in a tsv file....')
        with open('data.tsv', 'a', encoding = 'utf-8') as f :
            lines = [key + '\t' + data[key] for key in data]
            f.write('\n'.join(lines))
            print('Data appended in file: [data.tsv]')
    elif message.content == '$$clear_data' :
        os.remove('data.tsv')
        print('Data cleared.')
        await message.reply('Data cleared.')
    elif message.content.startswith('$$set_limit ') :
        lim = int(message.content[len('$$set_limit ') : ].strip())
        await message.reply(f'Limit set to {lim}!')
    return

if __name__ == '__main__' :
    client.run(TOKEN)