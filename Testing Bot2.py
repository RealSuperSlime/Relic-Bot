import discord
from discord.ext import commands
import asyncio
from HonkaiBotData import *
from Honkai_Token import TOKEN
from CalculatorFunctions import *

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Boothill is still kickin")
    print("------------------------")


@client.command()
async def relic(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    substats = ["HP", "FLAT_HP", "ATK", "FLAT_ATK", "DEF", "FLAT_DEF", "SPD", "CR", "CD", "EHR", "RES", "BE"]
# maybe try substats as lowercase = ["hp", "flat_hp", "atk", "flat_atk", "def", "flat_def", "spd", "cr", "cd", "ehr", "res", "be"] in the future?
    stats =  {}
    await ctx.send("Please enter the character's name:")
    try:
        msg = await client.wait_for("message", check=check, timeout=60.0)
        character = msg.content.strip().lower()
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond! Please try the command again.")
        return

    await ctx.send("Please enter your four relic substats one by one from the following options:\n" + ", ".join(substats))
    
    for i in range(4):
        await ctx.send(f"Enter substat {i+1}:")
        try:
            msg = await client.wait_for("message", check=check, timeout=60.0)
            substat = msg.content.strip()
            if substat not in [stat for stat in substats]:
                await ctx.send(f"{substat} is not a valid substat. Please enter a valid substat from the list.")
                return

            
            await ctx.send(f"Enter the value for {substat}:")
            msg = await client.wait_for("message", check=check, timeout=60.0)
            try:
                value = float(msg.content.strip())
            except ValueError:
                await ctx.send("Invalid value. Please enter a numerical value.")
                return

            stats[substat] = value

        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond! Please try the command again.")
            return

    total_score = calculate_total_score(stats)
    rounded_score = round(total_score, 1)

    # Determine the grade based on the total score
    if rounded_score >= 45:
        grade = "GOATED"
    elif 45 > rounded_score >= 40:
        grade = "SSS"
    elif 40 > rounded_score >= 35:
        grade = "SS"
    elif 35 > rounded_score >= 30:
        grade = "S"
    elif 30 > rounded_score >= 28:
        grade = "A+"
    elif 28 > rounded_score >= 25:
        grade = "A"
    elif 25 > rounded_score >= 22:
        grade = "B+"
    elif 22 > rounded_score >= 20:
        grade = "B"
    elif 20 > rounded_score >= 18:
        grade = "C+"
    elif 18 > rounded_score >= 15:
        grade = "C"
    elif 15 > rounded_score >= 10:
        grade = "D"
    else:
        grade = "F"

    await ctx.send(f"The total score for {character}'s relic stats is {rounded_score}. Your grade is {grade}.")


client.run(TOKEN)
