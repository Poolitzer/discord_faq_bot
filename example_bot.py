from discord.ext import commands
import json
import re
import logging

logging.basicConfig(filename="log.log", level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
data_file = open('./database.json')
database = json.load(data_file)
bot = commands.Bot(command_prefix='!')
idlist = [296280946813173761]


async def is_allowed(ctx):
    skip = False
    idlist.append(ctx.guild.owner_id)
    for ids in idlist:
        if ctx.author.id == ids:
            skip = True
            break
    idlist.pop()
    if ctx.author.top_role.name == "mods" or skip:
        return True


@bot.command(name="bot")
async def bot2(ctx, arg=None):
    if not arg:
        temp = []
        for item in database:
            temp.append(item)
        await ctx.send("These are my current commands: {}".format(", ".join(temp)))
    else:
        skip = False
        for item in database:
            if item == arg.lower():
                skip = True
                await ctx.send(database[item])
                break
        if not skip:
            await ctx.send("Command not known. Say what?")


@bot.command()
@commands.check(is_allowed)
async def add(ctx, *, arg):
    pattern = re.match("(\w+) (.+)", arg)
    if pattern:
        database[pattern.group(1).lower()] = pattern.group(2)
        with open('./database.json', 'w') as outfile:
            json.dump(database, outfile, indent=4, sort_keys=True)
            await ctx.send("I saved the command **{}**".format(pattern.group(1).lower()))
    else:
        await ctx.send("You need to give me a command name and a value. Like `!add {} IsStupid`, if you want to have "
                       "your own name there and then get IsStupid as return".format(ctx.author.name))


@add.error
async def info_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("I'm sorry, you can't do this :(")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You need to give me a command name and a value. Like `!add {} IsStupid`, if you want to have "
                       "your own name there and then get IsStupid as return".format(ctx.author.name))


@bot.command()
@commands.check(is_allowed)
async def delete(ctx, arg):
    try:
        del database[arg]
        with open('./database.json', 'w') as outfile:
            json.dump(database, outfile, indent=4, sort_keys=True)
            await ctx.send("Deleting successful. Good job :)")
    except KeyError:
        await ctx.send("Can't find this entry. Sad face.")


@delete.error
async def info_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("I'm sorry, you can't do this :(")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You need to give me an entry. Type it like `!delete IAmStupid`, if IAmStupid is the entry "
                       "you want to delete.")


bot.run('token')
