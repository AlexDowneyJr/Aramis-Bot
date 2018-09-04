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
import requests

prefix = "."
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
    embed = discord.Embed(title="Zuki - The Currency Bot", description="The Loli accountant who you'd fuck for your money", color=0xF00000)

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
                await asyncio.sleep(15)

async def hentai_thing(ctx):    
    while not bot.is_closed:
        async with aiohttp.ClientSession() as client:
            async with client.get("https://api.reddit.com/r/hentai/random") as image:
                data = await image.json()
                embed = discord.Embed(title=data[0]["data"]["children"][0]["data"]["title"],color=0xF00000)
                embed.set_image(url=data[0]["data"]["children"][0]["data"]["url"])
                embed.set_footer(text=f"REQUESTED BY {ctx.message.author.display_name}")
                await bot.say(embed=embed)
                await asyncio.sleep(15)

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

@bot.command(pass_context = True, aliases=['ud'])
async def urban(ctx, *msg):
    author = ctx.message.author.display_name
    try:
        word = ' '.join(msg)
        api = "http://api.urbandictionary.com/v0/define"
        response = requests.get(api, params=[("term", word)]).json()
        embed = discord.Embed(description="No results found!", colour=0xF00000)
        if len(response["list"]) == 0:
            return await bot.say(embed=embed)
        embed = discord.Embed(title="Word", description=word, colour=embed.colour)
        embed.add_field(name="Top definition:", value=response['list'][0]['definition'])
        embed.add_field(name="Examples:", value=response['list'][0]["example"])
        embed.set_footer(text=f"Requested by {author}")

        await bot.say(embed=embed)

    except:
        bot.say("An error has occured in the bot.")

@bot.command(pass_context=True)
async def insult(ctx, username : discord.Member = None):
    author = ctx.message.author
    
    insults = [   "If laughter is the best medicine, your face must be curing the world.",
    "It's better to let someone think you are an idiot than to open your mouth and prove it.", 
    "If I had a face like yours, I'd sue my parents.", 
    "You're so ugly, when your mom dropped you off at school she got a fine for littering.", 
    "If I wanted to kill myself I'd climb your ego and jump down to your IQ.", 
    "Brains aren't everything. In your case they're nothing.", 
    "Are you always this stupid or is today a special occasion?", 
    "Don't you have a terribly empty feeling - in your skull?", 
    "How did you get here? Did someone leave your cage open?", 
    "I'd like to see things from your point of view but I can't seem to get my head that far up my ass.", 
    "Have you been shopping lately? They're selling lives, you should go get one.", 
    "The last time I saw something like you, I flushed it.", 
    "If ugliness was measured in bricks, you would be the Great Wall of China.", 
    "You want an insult? Look in the mirror!", 
    "The story of your life is more insulting than anything I have to say.", 
    "Did a thought cross your mind? It must have been a long and lonely journey...", 
    "You'd better hide; the garbage man is coming.", 
    "Roses are red, violets are blue, I have five fingers, the middle one's for you.", 
    "I have a text file bigger than your brain in my database. It's 0KB in size.", 
    "You're old enough to remember when emojis were called 'hieroglyphics.'", 
    "I don't engage in mental combat with the unarmed.", 
    "Is your ass jealous of the amount of shit that comes out of your mouth?", 
    "Your face looks like it caught fire and someone tried to put it out with a fork.", 
    "Hey, you have something on your third chin.", 
    "I thought a little girl from Kansas dropped a house on you…", 
    "I'm jealous of people that don't know you.", 
    "You bring everyone a lot of joy, when you leave the room.", 
    "If you are going to be two faced, at least make one of them pretty.", 
    "If you're going to be a smartarse, first you have to be smart. Otherwise you're just an arse.", 
    "Somewhere out there is a tree, tirelessly producing oxygen so you can breathe. I think you owe it an apology.", 
    "I don't exactly hate you, but if you were on fire and I had water, I'd drink it.", 
    "If you were on TV, I would change the channel.", 
    "You have Diarrhea of the mouth; constipation of the ideas.", 
    "If ugly were a crime, you'd get a life sentence.", 
    "There is no vaccine for stupidity.", 
    "Did your parents ever ask you to run away from home?", 
    "Any similarity between you and a human is purely coincidental.", 
    "Keep talking – someday you’ll say something intelligent.", 
    "Don’t you love nature, despite what it did to you?", 
    "I'm sure if you studied harder you could get enough qualifications to work as a McDonalds' cleaner.", 
    "If I knew you were this much of a cock I would have fed you corn.",
    "Yo Mama so fat she sued Xbox 360 for guessing her weight.",
    "You're so fat that when you were diagnosed with a flesh eating bacteria - the doctors gave you 87 years to live.",
    "You're so fat you've got more chins than a Hong Kong phone book.",
    "Yo Mama so fat she's on both sides of the family.",
    "Yo Mama so fat that even Dora couldn't explore her.",
    "Yo Mama so fat that she doesn't need the internet; she's already world wide.",
    "You're so fat that when you farted you started global warming.",
    "You're so fat the back of your neck looks like a pack of hot-dogs.",
    "You're so fat that when you fell from your bed you fell from both sides.",
    "You're so fat when you get on the scale it says \"To be continued.\"",
    "You're so fat when you go swimming the whales start singing \"We Are Family\".",
    "You're so fat when you stepped on the scale, Buzz Lightyear popped out and said \"To infinity and beyond!\"",
    "You're so fat when you turn around, people throw you a welcome back party.",
    "You're so fat when you were in school you sat by everybody.",
    "You're so fat when you went to the circus the little girl asked if she could ride the elephant.",
    "You're so fat when you go on an airplane, you have to pay baggage fees for your ass.",
    "You're so fat whenever you go to the beach the tide comes in.",
    "You're so fat I could slap your butt and ride the waves.",
    "You're so fat I'd have to grease the door frame and hold a Twinkie on the other side just to get you through.",
    "Yo Mama so dumb I told her Christmas was around the corner and she went looking for it.",
    "You're so dumb it took you 2 hours to watch 60 minutes.",
    "Yo Mama so dumb she bought tickets to Xbox Live.",
    "You're so dumb that you thought The Exorcist was a workout video.",
    "You're so ugly that you went to the salon and it took 3 hours just to get an estimate.",
    "You're so ugly that even Scooby Doo couldn't solve that mystery.",
    "What is the weighted center between Planet X and Planet Y? Oh it's YOU!",
    ":eggplant: :eggplant: :eggplant:",
    "Your birth certificate is an apology letter from the condom factory.",
    "I wasn't born with enough middle fingers to let you know how I feel about you.",
    "You must have been born on a highway because that's where most accidents happen.",
    "I'm jealous of all the people that haven't met you.",
    "I bet your brain feels as good as new, seeing that you never use it.",
    "I'm not saying I hate you, but I would unplug your life support to charge my phone.",
    "You're so ugly, when your mom dropped you off at school she got a fine for littering.",
    "You bring everyone a lot of joy, when you leave the room.",
    "What's the difference between you and eggs? Eggs get laid and you don't.",
    "You're as bright as a black hole, and twice as dense.",
    "I tried to see things from your perspective, but I couldn't seem to shove my head that far up my ass.",
    "Two wrongs don't make a right, take your parents as an example.",
    "You're the reason the gene pool needs a lifeguard.",
    "If laughter is the best medicine, your face must be curing the world.",
    "You're so ugly, when you popped out the doctor said \"Aww what a treasure\" and your mom said \"Yeah, lets bury it.\"",
    "I have neither the time nor the crayons to explain this to you.",
    "You have two brains cells, one is lost and the other is out looking for it.",
    "How many times do I have to flush to get rid of you?",
    "I don't exactly hate you, but if you were on fire and I had water, I'd drink it.",
    "You shouldn't play hide and seek, no one would look for you.",
    "Some drink from the fountain of knowledge; you only gargled.",
    "Roses are red violets are blue, God made me pretty, what happened to you?",
    "It's better to let someone think you are an Idiot than to open your mouth and prove it.",
    "Somewhere out there is a tree, tirelessly producing oxygen so you can breathe. I think you owe it an apology.",
    "The last time I saw a face like yours I fed it a banana.",
    "The only way you'll ever get laid is if you crawl up a chicken's ass and wait.",
    "Which sexual position produces the ugliest children? Ask your mother.",
    "If you really want to know about mistakes, you should ask your parents.",
    "At least when I do a handstand my stomach doesn't hit me in the face.",
    "If I gave you a penny for your thoughts, I'd get change.",
    "If I were to slap you, it would be considered animal abuse.",
    "Do you know how long it takes for your mother to take a crap? Nine months.",
    "What are you going to do for a face when the baboon wants his butt back?",
    "Well I could agree with you, but then we'd both be wrong.",
    "You're so fat, you could sell shade.",
    "It looks like your face caught on fire and someone tried to put it out with a hammer.",
    "You're not funny, but your life, now that's a joke.",
    "You're so fat the only letters of the alphabet you know are KFC.",
    "Oh my God, look at you. Was anyone else hurt in the accident?",
    "What are you doing here? Did someone leave your cage open?",
    "You're so ugly, the only dates you get are on a calendar.",
    "I can explain it to you, but I can't understand it for you.",
    "You are proof that God has a sense of humor.",
    "If you spoke your mind, you'd be speechless.",
    "Why don't you check eBay and see if they have a life for sale.",
    "If I wanted to hear from an asshole, I'd fart.",
    "You're so fat you need cheat codes to play Wii Fit",
    "You're so ugly, when you got robbed, the robbers made you wear their masks.",
    "Do you still love nature, despite what it did to you?",
    "You are proof that evolution CAN go in reverse.",
    "I'll never forget the first time we met, although I'll keep trying.",
    "Your parents hated you so much your bath toys were an iron and a toaster",
    "Don't feel sad, don't feel blue, Frankenstein was ugly too.",
    "You're so ugly, you scared the crap out of the toilet.",
    "It's kinda sad watching you attempt to fit your entire vocabulary into a sentence.",
    "I fart to make you smell better.",
    "You're so ugly you make blind kids cry.",
    "You're a person of rare intelligence. It's rare when you show any.",
    "You're so fat, when you wear a yellow rain coat people scream ''taxi''.",
    "I heard you went to a haunted house and they offered you a job.",
    "You look like a before picture.",
    "If your brain was made of chocolate, it wouldn't fill an M&M.",
    "Aww, it's so cute when you try to talk about things you don't understand.",
    "I heard your parents took you to a dog show and you won.",
    "You stare at frozen juice cans because they say, \"concentrate\".",
    "You're so stupid you tried to wake a sleeping bag.",
    "Am I getting smart with you? How would you know?",
    "We all sprang from apes, but you didn't spring far enough.",
    "I'm no proctologist, but I know an asshole when I see one.",
    "When was the last time you could see your whole body in the mirror?",
    "You must have a very low opinion of people if you think they are your equals.",
    "So, a thought crossed your mind? Must have been a long and lonely journey.",
    "You're the best at all you do - and all you do is make people hate you.",
    "Looks like you fell off the ugly tree and hit every branch on the way down.",
    "Looks aren't everything; in your case, they aren't anything.",
    "You have enough fat to make another human.",
    "You're so ugly, when you threw a boomerang it didn't come back.",
    "You're so fat a picture of you would fall off the wall!",
    "Your hockey team made you goalie so you'd have to wear a mask.",
    "Ordinarily people live and learn. You just live.",
    "Did your parents ever ask you to run away from home?",
    "I heard you took an IQ test and they said your results were negative.",
    "You're so ugly, you had tinted windows on your incubator.",
    "Don't you need a license to be that ugly?",
    "I'm not saying you're fat, but it looks like you were poured into your clothes and someone forgot to say \"when\"",
    "I've seen people like you, but I had to pay admission!",
    "I hear the only place you're ever invited is outside.",
    "Keep talking, someday you'll say something intelligent!",
    "You couldn't pour water out of a boot if the instructions were on the heel.",
    "Even if you were twice as smart, you'd still be stupid!",
    "You're so fat, you have to use a mattress as a maxi-pad.",
    "I may be fat, but you're ugly, and I can lose weight.",
    "I was pro life before I met you.",
    "What's the difference between you and Hitler? Hitler knew when to kill himself.",
    "You're so fat, your double chin has a double chin.",
    "If ignorance is bliss, you must be the happiest person on earth.",
    "You're so stupid, it takes you an hour to cook minute rice.",
    "Is that your face? Or did your neck just throw up?",
    "You're so ugly you have to trick or treat over the phone.",
    "I'd hit you but we don't hit girls around here.",
    "Dumbass.",
    "Bitch.",
    "I'd give you a nasty look but you've already got one.",
    "If I wanted a bitch, I'd have bought a dog.",
    "Scientists say the universe is made up of neutrons, protons and electrons. They forgot to mention morons.",
    "Why is it acceptable for you to be an idiot but not for me to point it out?",
    "Did you know they used to be called \"Jumpolines\" until your mum jumped on one?",
    "You're not stupid; you just have bad luck when thinking.",
    "I thought of you today. It reminded me to take the garbage out.",
    "I'm sorry I didn't get that - I don't speak idiot.",
    "Hey, your village called they want their idiot back.",
    "I just stepped in something that was smarter than you :poop: and smelled better too.",
    "You're so fat that at the zoo the elephants started throwing you peanuts.",
    "You're so fat every time you turn around, it's your birthday.",
    "You're so fat your idea of dieting is deleting the cookies from your internet cache.",
    "You're so fat your shadow weighs 35 pounds.",
    "You're so fat I could tell you to haul ass and you'd have to make two trips.",
    "You're so fat I took a picture of you at Christmas and it's still printing.",
    "You're so fat I tried to hang a picture of you on my wall, and my wall fell over.",
    "You're so fat Mount Everest tried to climb you.",
    "You're so fat you can't even jump to a conclusion.",
    "You're so fat you can't fit in any timeline.",
    "You're so fat you can't fit in this joke.",
    "You're so fat you don't skinny dip, you chunky dunk.",
    "You're so fat you fell in love and broke it.",
    "You're so fat you go to KFC and lick other peoples' fingers.",
    "You're so fat you got arrested at the airport for ten pounds of crack.",
    "You're so fat you'd have to go to Sea World to get baptized.",
    "You're so fat you have your own zip code.",
    "You're so fat you have more rolls than a bakery.",
    "You're so fat you don't have got cellulite, you've got celluheavy.",
    "You're so fat you influence the tides.",
    "You're so fat you jumped off the Grand Canyon and got stuck.",
    "You're so fat that you laid on the beach and Greenpeace tried to push you back in the water.",
    "You're so fat you leave footprints in concrete.",
    "You're so fat you need GPS to find your asshole.",
    "You're so fat you pull your pants down and your ass is still in them.",
    "You're so fat you show up on radar.",
    "If you were any less intelligent we'd have to water you three times a week..",
    "If your IQ was 3 points higher, you'd be a rock.",
    "I would insult you but nature did a better job.",
    "Does your ass get jealous of all the shit that comes out of your mouth?",
    "If I ate a bowl of alphabet soup, I could shit out a smarter sentence than any of yours.",
    "You're not pretty enough to be this stupid.",
    "That little voice in the back of your head, telling you you'll never be good enough? It's right.",
    "You look like you're going to spend your life having one epiphany after another, always thinking you've finally figured out what's holding you back, and how you can finally be productive and creative and turn your life around. But nothing will ever change. That cycle of mediocrity isn't due to some obstacle. It's who you *are*. The thing standing in the way of your dreams is; that the person having them is *you*.",
    "May your day and future be as pleasant as you are.",
    "I would agree with you but then we would both be wrong.",
    "I bite my thumb at you, sir.",
    "I'd call you a tool, but that would imply you were useful in at least one way.",
    "I hope you outlive your children.",
    "Are you and your dick having a competition to see who can disappoint me the most?",
    "Yo mamma is so ugly her portraits hang themselves.",
    "Your birth certificate is an apology from the abortion clinic.",
    "If you were anymore inbred you'd be a sandwich.",
    "Say hello to your wife and my kids for me." ]
    
    if username == None:
        await bot.say("Who am I supposed to insult again?")
    elif username == bot.user:
        await bot.say("How original. No one else had thought of trying to get the bot to insult itself. I applaud your creativity. *Yawn*. Perhaps this is why you don't have friends. You don't add anything new to any conversation. You are more of a bot than me, predictable answers, and absolutely dull to have an actual conversation with.")
    elif username == author:
        await bot.say("Can't be that harsh on ya. :frowning:")
    else:
        await bot.say(username.mention + " " + random.choice(insults))

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
    embed.add_field(name="?urban", value="Searches the Urban dictionary for definitions", inline=False)

    await bot.say(embed=embed)
@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        x = error.retry_after
        await bot.send_message(ctx.message.channel, content='Command on cooldown bud, Come back after %.2fs :smile:' % x)

@bot.event
async def on_message(message):
    author = message.author

    partner_channel = bot.get_channel("433746345828810783")
    if message.channel == partner_channel:
        if message.author.id in accounts:
            accounts[message.author.id] += 50
            await bot.send_message(message.channel, "Congrats, You just got 50 :dollar: for bringing in another partner. :smile:")
            with open('accounts.json', 'w') as f:
                json.dump(accounts, f)
    
    if bot.user.id != message.author.id:
        gae_stuff = [
            "gae", "gay", "gae bot", "You're gae Zuki", "Zuki is gae", "gay bot", 
            "You're gay Zuki", "Zuki is gay", "you're gae {}".format(author.mention)
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
        
        if "i'm sick" in message.content.lower():
            await bot.add_reaction(message, emoji='🤧')
            await bot.send_message(message.channel,'Get well soon :smile:')
        
        if 'got sick' in message.content.lower():
            await bot.add_reaction(message, emoji='🤧')
            await bot.send_message(message.channel,'Get well soon :smile:')

        if "weird" in message.content.lower():
            await bot.send_message(message.channel, "Weird indeed")

        if "RIP" in message.content:
            await bot.send_message(message.channel, "RIP indeed, Welp . . . What can bots do to help? :shrug:")

        howdy = ["how are you zuki?", "How are you zuki", "zuki, how are you?"]
        
        for how in howdy:
            if how == message.content.lower():
                await bot.send_message(message.channel, "I'm feeling good, How about you?")
                    
    await bot.process_commands(message)

bot.run(os.environ["bot_token"])
