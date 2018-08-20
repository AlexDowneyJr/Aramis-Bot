import discord
from discord.ext import commands
import random
import numbers
import time
import os
import datetime
import aiohttp
import asyncio
from itertools import cycle
import json
import timeit
import traceback

prefix = "?"
bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    print(f"{discord.__name__.upper()} | {discord.__version__}")
    print("ONLINE")
    await bot.change_presence(game=discord.Game(name="Stuff", type=2))
    global accounts
    try:
        with open('accounts.json') as f:             
            accounts = json.load(f)
    except:
        pass

bot.owner = "270240582851493888"

@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say("Pong!")

@bot.command(pass_context=True)
async def shutdown(ctx):
    if ctx.message.author.id == bot.owner:
        await bot.say("Cya later peeps!")
        await bot.close()
    else:
        await bot.say("Owner only command.")

@bot.command()
async def punch(username : discord.Member):
    e = discord.Embed(color=0xF00000)
    f = discord.Embed(color=0xF00000)
    e.set_image(url="https://cdn.discordapp.com/attachments/358587036678225920/471581454116192266/giphy_1.gif")
    f.set_image(url="https://cdn.discordapp.com/attachments/358587036678225920/471581540858724383/giphy_2.gif")
    if username == bot.user :
        await bot.say("Think this is funny? **WAPOW** ლ(ಠ益ಠლ) NOW WHO'S BEGGING FOR MERCY?")
        await bot.say(embed=f)
    else:
        while not bot.is_closed:
            await bot.say(f"ONE PUNCH!! and {username.mention} is out! ლ(ಠ益ಠლ)")
            await bot.say(embed=e)

@bot.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, username : discord.Member, reason : str = None):
    author = ctx.message.author
    e=discord.Embed(color=0xF00000)
    e.set_image(url="https://cdn.discordapp.com/attachments/460839454358372353/469886770754879488/ezgif-5-bda5e8d79b.gif")

    if author == username:
        await bot.say("I can't let you do that, Self harm is wrong :frowning:")
        return

    if reason is None:
        reason = "The Ban Hammer has spoken."
        try:
            await bot.ban(username)
            await bot.say(embed=e)
            await bot.say(f"HAMMER! **Wapow** {username} is now banned!")
        except discord.errors.Forbidden:
            await bot.say("Either I or you don't have the powers to summon the Hammer right now.")        

@bot.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def unban(ctx, user : str):
    try:
        banlist = await bot.get_bans(ctx.message.server)
    except discord.errors.Forbidden:
        await bot.say("I don't have the power to do so")
        return

    username = discord.utils.get(banlist, name = user)
    if username is None:
        await bot.say("My ocular powers cannot find {0}".format(user))
        return

    bot.unban(ctx.message.server, username)
    await bot.say("I have unbanned this mortal.")

@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, username : discord.Member, reason : str = None):
    author = ctx.message.author
    e=discord.Embed(color=0xF00000)
    e.set_image(url="https://cdn.discordapp.com/attachments/358587036678225920/469917097498116106/tumblr_mulauefSzX1sl0k4to1_500.gif")

    if author == username:
        await bot.say("I can't let you do that, Self Harm is wrong :frowning:")
        return
        
    if reason is None:
        reason = "The Mod/Admin thought of this person to be a disgusting creature."
        try:
            await bot.kick(username)
            await bot.say(embed=e)
            await bot.say(f"**Diable Jambe! Concasse** :boot::boom: {username} was kicked!")
        except discord.errors.Forbidden:
            await bot.say("Either you or I don't have the power to kick this mortal.")    

@bot.command(pass_context=True)
async def info(ctx):
    embed = discord.Embed(title="Aramis - The Official Bot", description="The Bot that sees all, hears all and knows all. Don't piss it off.", color=0xF00000)

    embed.add_field(name="Author", value="Alex Downey Jr.")
    
    embed.add_field(name="Server count", value=f"{len(bot.servers)}")

    await bot.say(embed=embed)
    
    await bot.say("Thats about it.")

@bot.command(pass_context=True)
async def add(ctx,a, b):
    try:
        try:
            a = int(a)
            b = int(b)
        except:
            a = float(a)
            b = float(b)
        await bot.say(a + b)
    except:
        await bot.say("Whatcha tryna do, mate?")
    
@bot.command(pass_context=True)
async def multiply(ctx,a : float, b : float):
    await bot.say(a * b)

@bot.command()
async def cat():
    catlist = ["https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif",
    "https://giphy.com/gifs/funny-cat-mlvseq9yvZhba",
    "https://giphy.com/gifs/transparent-baby-shake-nNxT5qXR02FOM",
    "https://giphy.com/gifs/facepalm-yFQ0ywscgobJK",
    "https://giphy.com/gifs/cat-moment-remember-8vQSQ3cNXuDGo", 
    "https://giphy.com/gifs/cat-funny-WXB88TeARFVvi",
    "https://giphy.com/gifs/reaction-Nm8ZPAGOwZUQM",
    "https://giphy.com/gifs/cat-hello-oh-MWSRkVoNaC30A",
    "https://giphy.com/gifs/cat-weird-bra-p4xp4BjHIdane"]

    await bot.say(random.choice(catlist))

@bot.command()
async def greet():
    await bot.say(":wave::smile: Hello there!")

@bot.command()
async def choose(*choices):
    if len(choices) < 2:
        await bot.say("Umm . . . Where are the other options?")
    else:
        await bot.say(random.choice(choices))

@bot.command(name = "8", aliases=["8ball"])
async def _8ball(* ,question : str):
    answers = ["As I see it, yes", "It is certain", "It is decidedly so", "Most likely", "Outlook good",
    "Signs point to yes", "Without a doubt", "Yes", "Yes – definitely", "You may rely on it", "Reply hazy, try again",
    "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
    "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]
    if question.endswith("?") and question != "?":
        await bot.say(":8ball: : `" + random.choice(answers) + "`")
    else:
        await bot.say("This is not a question. Ask me a question next time.")

@bot.command(pass_context=True)
async def hug(ctx, username: discord.Member):
    author = ctx.message.author.display_name
    person = username.display_name
    hugs = [
        "https://cdn.discordapp.com/attachments/358587036678225920/470598370390704142/to_all_of_those_who_need_a_hug_have_a_ghost_hug_-_Imgur.gif",
        "https://cdn.discordapp.com/attachments/358587036678225920/470600283144060948/Monkey_Hug_-_Imgur.gif",
        "https://cdn.discordapp.com/attachments/432559393859698691/471236787285655552/giphy.gif",
        "https://cdn.discordapp.com/attachments/432559393859698691/471237107864829952/tenor.gif",
        "https://cdn.discordapp.com/attachments/432559393859698691/471238143752929280/655d65d49a2981f2fcfc6d94a397db884c703779_hq.gif",
        "https://cdn.discordapp.com/attachments/432559393859698691/471238255581331477/Anime-hug-GIF-Image-Download-24.gif",
        ]
    embed=discord.Embed(title=f"{author} has given a hug to {person} :heart:", color=0xF00000)
    embed.set_image(url=random.choice(hugs))
    
    if author == username:
        await bot.say("Aww . . . Thats sad, Hope you find someone soon. :smile:")
    else:
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def cumshot(ctx, username : discord.Member):
    author = ctx.message.author
    e=discord.Embed(color=0xF00000)
    e.set_image(url="https://cdn.discordapp.com/attachments/358587036678225920/470971020279414784/tumblr_nglyzhkIRs1qfap4co7_250.gif")

    if author == username:
        await bot.say("Umm . . . Dude, I didn't know that you had that kinda fetish :rolling_eyes:")
        return
    if username == bot.user:
        await bot.say("Yeah, Not funny. What made you think this would work? :expressionless:")
        return
    await bot.say(f"I'M GONNA DO IT!! HERE IT COMES!\n\n" + "~Agh, that felt good.")
    await bot.say(embed=e)

@bot.command(pass_context=True)
async def dankmeme(ctx):
    async with aiohttp.ClientSession() as client:
        async with client.get("https://api.reddit.com/r/dankmemes/random") as image:
            data = await image.json()
            embed = discord.Embed(
            title=data[0]["data"]["children"][0]["data"]["title"],
            color=0xF00000
            )
            embed.set_image(url=data[0]["data"]["children"][0]["data"]["url"])
            embed.set_footer(text=f"REQUESTED BY {ctx.message.author.display_name}")
            await bot.say(embed=embed)

async def porn_thing(ctx):    
    while not bot.is_closed:
        async with aiohttp.ClientSession() as client:
            async with client.get("https://api.reddit.com/r/nsfw/random") as image:
                data = await image.json()
                embed = discord.Embed(title=data[0]["data"]["children"][0]["data"]["title"],color=0xF00000)
                embed.set_image(url=data[0]["data"]["children"][0]["data"]["url"])
                embed.set_footer(text=f"REQUESTED BY {ctx.message.author.display_name}")
                await bot.say(embed=embed)
                await asyncio.sleep(1800)

async def hentai_thing(ctx):    
    while not bot.is_closed:
        async with aiohttp.ClientSession() as client:
            async with client.get("https://api.reddit.com/r/hentai/random") as image:
                data = await image.json()
                embed = discord.Embed(title=data[0]["data"]["children"][0]["data"]["title"],color=0xF00000)
                embed.set_image(url=data[0]["data"]["children"][0]["data"]["url"])
                embed.set_footer(text=f"REQUESTED BY {ctx.message.author.display_name}")
                await bot.say(embed=embed)
                await asyncio.sleep(1800)

@bot.command(pass_context=True)
async def autoporn(ctx):
    channel = ctx.message.channel
    author = ctx.message.author.id
    if author == bot.owner:
        await bot.send_message(await porn_thing(ctx), channel)
    else:
        await bot.say("This command is deleted. Sign a petition and send it to Alex to bring it back.")

@bot.command(pass_context=True)
async def autohentai(ctx):
    channel = ctx.message.channel
    author = ctx.message.author.id
    if author == bot.owner:
        await bot.send_message(await hentai_thing(ctx), channel)
    else:
        await bot.say("This command is deleted. Sign a petition and send it to Alex to bring it back.")

@bot.command(pass_context=True)
async def avatar(ctx, user : discord.Member = None):
    author = ctx.message.author
    if not user:
        user = author
    avatar = user.avatar_url
    await bot.say("{0}".format(avatar))

@bot.command(pass_context=True)
async def userinfo(ctx, *, user: discord.Member=None):
    author = ctx.message.author
    server = ctx.message.server

    if not user:
        user = author

    roles = [x.name for x in user.roles if x.name != "@everyone"]

    joined_at = fetch_joined_at(user, server)
    since_created = (ctx.message.timestamp - user.created_at).days
    since_joined = (ctx.message.timestamp - joined_at).days
    user_joined = joined_at.strftime("%d %b %Y %H:%M")
    user_created = user.created_at.strftime("%d %b %Y %H:%M")
    member_number = sorted(server.members, key=lambda m: m.joined_at).index(user) + 1

    created_on = "{}\n({} days ago)".format(user_created, since_created)
    joined_on = "{}\n({} days ago)".format(user_joined, since_joined)

    game_list = [
        "Following the Cult of Satan in His **{}** Service Centre".format(user.status) ,
        "Applying for a job while being **{}**".format(user.status) ,
        "Making your **{}** type parents proud".format(user.status) ,
        "Disgracing your Dance teacher with your **{}** type moves".format(user.status),
        "Taking in the **{}** kinda stuff.*Police arriving any minute*".format(user.status),
        "Changing genders without the permission of your **{}** type parents".format(user.status),
        "Robbing the Bank **{}**".format(user.status)
    ]
    
    game = random.choice(game_list)

    if user.game is None:
        pass
    elif user.game.url is None:
        game = "Playing {}".format(user.game)
    else:
        game = "Streaming: [{}]({})".format(user.game, user.game.url)

    if roles:
        roles = sorted(roles, key=[x.name for x in server.role_hierarchy if x.name != "@everyone"].index)
        roles = ", ".join(roles)
    else:
        roles = "None"

    data = discord.Embed(description=game, colour=user.colour)
    data.add_field(name="Joined Discord on", value=created_on)
    data.add_field(name="Joined this server on", value=joined_on)
    data.add_field(name="Roles", value=roles, inline=False)
    data.set_footer(text="Member #{} | User ID:{}".format(member_number, user.id))

    name = str(user)
    name = " ~ ".join((name, user.nick)) if user.nick else name

    if user.avatar_url:
        data.set_author(name=name, url=user.avatar_url)
        data.set_thumbnail(url=user.avatar_url)
    else:
        data.set_author(name=name)

    try:
        await bot.say(embed=data)
    except:
        pass

def fetch_joined_at(user, server):
    if user.id == "96130341705637888" and server.id == "133049272517001216":
        return datetime.datetime(2016, 1, 10, 6, 8, 4, 443000)
    else:
        return user.joined_at

@bot.command(pass_context=True)
async def balance(ctx):
    id = ctx.message.author.id
    if id in accounts:
        await bot.say("You have {}:dollar: in the bank. WOOHOO! :smile:".format(accounts[id]))
    else:
        await bot.say("You do not have an account in the bank. *Whats with the beggars tryna act smart.*")

@bot.command(pass_context=True)
async def register(ctx):
    id = ctx.message.author.id
    if id not in accounts:
        accounts[id] = 100
        await bot.say("You are now registered in the bank. WOOHOO! :smile:")
    else:
        await bot.say("You already have an account. Buddy, You drunk or just acting smart?")
        with open('accounts.json', 'w') as f:
            json.dump(accounts, f)

@bot.command(pass_context=True)
async def transfer(ctx, amount: int, other: discord.Member):
    primary_id = ctx.message.author.id
    other_id = other.id
    if primary_id not in accounts:
        await bot.say("You do not have an account. *Heh Nub* :stuck_out_tongue: ")
    elif other_id not in accounts:
        await bot.say("The other dude does not have an account. Get yourself registered already :face_palm:")
    elif accounts[primary_id] < amount:
        await bot.say("You cannot afford this transaction. Poor kid :stuck_out_tongue:")
    else:
        accounts[primary_id] -= amount
        accounts[other_id] += amount
        await bot.say("Transaction complete.")
        with open('accounts.json', 'w') as f:
            json.dump(accounts, f)

def cooldown(rate, per_sec=0, per_min=0, per_hour=0, type=commands.BucketType.default):
    return commands.cooldown(rate, per_sec + 60 * per_min + 3600 * per_hour, type)

@bot.command(pass_context=True)
@cooldown(1, per_hour=24, type=commands.BucketType.user)
async def payday(ctx):
    id = ctx.message.author.id
    amount = 250
    if id not in accounts:
        await bot.say("How do I give you money if you don't have a bank account? :thinking:")
    else:
        accounts[id] += amount
        await bot.say("Enjoy your free 250:dollar: :smile:.")
        with open('accounts.json', 'w') as f:
            json.dump(accounts, f)
    
@bot.command(pass_context=True)
@commands.has_permissions(administrator = True)
async def set(ctx, amount : int ,user : discord.Member):
    user = user.id
    if user not in accounts:
        await bot.say("How do I give you money if you don't have a bank account? :thinking:")
    else:
        accounts[user] = amount
        await bot.say(":dollar: has been successfully set. :smile: WOOHOO!")
        with open('accounts.json', 'w') as f:
            json.dump(accounts, f)

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def donate(ctx, amount : int, user : discord.Member):
    userid = user.id
    if userid not in accounts:
        await bot.say("How do I give you money if you don't have a bank account? :thinking:")
    else:
        accounts[userid] += amount
        await bot.say("Congratulations {}, you got {} from the Staff. WOOHOO! :smile: ".format(user, amount))
        with open('accounts.json', 'w') as f:
            json.dump(accounts, f)

items = [
        "Dark Shadow",
        "Dark Knight",
        "Grand Blue",
        "Apollo's Wrath",
        "Sweet Cotton",
        "Ice Age",
        "Burning Blood",
        "Witch Hazel",
    ]

@bot.command(pass_context=True)
async def shop(ctx):
    for role in items:
        role = discord.utils.get(ctx.message.server.roles, name = role)
        shop = discord.Embed(title = "Shop", description = "Purchase your roles here", color = 0xF00000)
        shop.add_field(name = role.name, value = role.mention, inline = False)
        shop.add_field(name = "Price :", value = "10,000 :dollar:", inline = False)
        
        await bot.say(embed = shop)

@bot.command(pass_context=True)
async def buy(ctx, *,role : discord.Role):
    author = ctx.message.author
    price = 10000
    
    if author.id in accounts:
        if accounts[author.id] >= price:
            if role.name in items:
                accounts[author.id] -= price
                await bot.add_roles(author, role) 
                await bot.say("Congrats {}, you just purchased {}. :smile:".format(author.mention, role))
                with open('accounts.json', 'w') as f:
                    json.dump(accounts, f)
            else:
                await bot.say("Can't find this role :shrug: .")
        else:
            await bot.say("You don't have enough :dollar: to complete this transaction. *lel nub* :stuck_out_tongue:")
    else:
        await bot.say("Ain't got an account bud, type `?register` to get one. :stuck_out_tongue:")

@bot.command(pass_context = True)
async def leaderboard(ctx):
    leaderbo = sorted(accounts, key = lambda x : accounts[x], reverse = True)
    list_lb = ''
    for number, dude in enumerate(leaderbo):
        list_lb += "{}. `<@{}>`  :  {} :dollar:\n".format(number + 1, dude, accounts[dude])
    await bot.send_message(ctx.message.channel, list_lb)

bot.remove_command("help")

@bot.command()
async def help():
    embed = discord.Embed(title="Aramis - The Official Bot", description="The Bot that sees all, hears all and knows all. List of commands are:", color=0xF00000)

    embed.add_field(name="?add X Y", value="Gives the addition of **X** and **Y**", inline=False)
    embed.add_field(name="?multiply X Y", value="Gives the multiplication of **X** and **Y**", inline=False)
    embed.add_field(name="?greet", value="Gives a nice greet message", inline=False)
    embed.add_field(name="?cat", value="Gives a cute cat gif to lighten up the mood.", inline=False)
    embed.add_field(name="?info", value="Gives a little info about the bot", inline=False)
    embed.add_field(name="?help", value="Gives this message", inline=False)
    embed.add_field(name="?shutdown", value="Shuts down the Bot", inline=False)
    embed.add_field(name="?ping", value="Ping-pong", inline=False)
    embed.add_field(name="?punch", value="Punch a user", inline=False)
    embed.add_field(name="?ban", value="Ban a user", inline=False)
    embed.add_field(name="?unban", value="Unban a banned user", inline=False)
    embed.add_field(name="?kick", value="Kick a user", inline=False)
    embed.add_field(name="?choose", value="Chooses between a given set of choices", inline=False)
    embed.add_field(name="?8ball", value="Ask 8ball something", inline=False)
    embed.add_field(name="?hug", value="Hug a user, Show them the love they deserve :smiling:", inline=False)
    embed.add_field(name="?avatar", value="Displays the avatar of the person", inline=False)
    embed.add_field(name="?userinfo", value="Displays information relating to the user", inline=False)

    await bot.say(embed=embed)
@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        x = error.retry_after
        await bot.send_message(ctx.message.channel, content='Command on cooldown bud, Come back after %.2fs :smile:' % x)

@bot.event
async def on_message(message):
    author = message.author

    partner_channel = bot.get_channel("375325934888157194")
    if message.channel == partner_channel:
        if message.author.id in accounts:
            accounts[message.author.id] += 50
            await bot.send_message(message.channel, "Congrats, You just got 50 :dollar: for bringing in another partner. :smile:")
            with open('accounts.json', 'w') as f:
                json.dump(accounts, f)
    
    if bot.user.id != message.author.id:
        gae_stuff = [
            "gae", "gay", "gae bot", "You're gae Aramis", "Aramis is gae", "gay bot", 
            "You're gay Aramis", "Aramis is gay", "you're gae {}".format(author.mention)
        ] 
        
        for x in gae_stuff:
            if x in message.content:
                if x is "gae" or x is "gay":
                    await bot.send_message(message.channel, "lul, gae boii.")
                    await bot.add_reaction(message, emoji='👌')
                    await bot.add_reaction(message, emoji='🏳️‍🌈')
                else:
                    await bot.send_message(message.channel, "But, nah my young padawan, . . . you're gae")
        
        if "🤔" in message.content.lower():
            await bot.add_reaction(message, emoji='🤔')
        
        if "👌" in message.content.lower():
            await bot.add_reaction(message, emoji='👌')
        
        if 'bye' in message.content.lower():
            await bot.add_reaction(message, emoji='👋')
            
        if 'sleep' in message.content.lower():
            await bot.add_reaction(message, emoji='💤')
        
        if "I'm sick" in message.content:
            await bot.add_reaction(message, emoji='🤧')
            await bot.send_message(message.channel,'Get well soon :smile:')
        
        if 'got sick' in message.content.lower():
            await bot.add_reaction(message, emoji='🤧')
            await bot.send_message(message.channel,'Get well soon :smile:')
                    
    await bot.process_commands(message)

bot.run("NDgxMDcyMjUyMjg5Mjg2MTU0.DlxBPQ.6_erXKpMtyTx73_JapCciUnou3Q")    
