# https://www.devdungeon.com/content/make-discord-bot-python
# https://www.devdungeon.com/content/make-discord-bot-python-part-2
# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import os

import discord

TOKEN = os.environ.get('DDBOT_DISCORD_TOKEN')

client = discord.Client()

# will work horirbly for tons of servers FIXME many collisions
vote_db = {}
passed_votes = []

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!passed'):
        await client.send_message(message.channel, str(passed_votes))
    elif message.content.startswith('!status'):
        arguments = message.content.split(';')[1:]
        vote_key = arguments[0]
        await client.send_message(message.channel, str(vote_db[vote_key]))
    elif message.content.startswith('!vote'):
        arguments = message.content.split(';')[1:]
        vote_key = arguments[0]
        vote_option = int(arguments[1])

        vote_db[vote_key][vote_option] += 1

        #if vote_db[vote_key][vote_option] > (total_members / 4):
        if vote_db[vote_key][vote_option] > 1:
            await client.send_message(message.channel, vote_key + ' passes!')
            passed_votes.append(vote_key)
    elif message.content.startswith('!propose'):
        arguments = message.content.split(';')[1:]
        vote_server = arguments[0]
        vote_channel = arguments[1]
        vote_key = arguments[2]
        vote_text = arguments[3]
        arguments = arguments[4:]

        # formulate the vote entry
        vote_db[vote_key] = [0 for arg in arguments]

        #msg = 'Hello {0.author.mention}'.format(message)
        vote_options = ', '.join(['%d: %s' % (i,a) for i,a in enumerate(arguments)])
        msg = (
            'VOTING TIME!\n\nProposal: %s (vote key: %s)\n\nOptions: %s'
            % (vote_text, vote_key, vote_options)
        )
        print(message.channel)

        # Get correct channel
        # FIXME: what if two servers have same channel name owo
        for server in client.servers:
            if server.name == vote_server:
                vote_server = server
                break
        else:
            await client.send_message(message.channel, "I could not find the server %s..." % vote_server)
            return  # maybe this isnt right way with async

        for channel in vote_server.channels:
            if channel.name == vote_channel:
                vote_channel = channel
                break
        else:
            await client.send_message(message.channel, "I could not find the channel %s..." % vote_channel)
            return

        await client.send_message(vote_channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
