import os
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
load_dotenv()
TOKEN=os.getenv("token")
bot = commands.Bot(command_prefix=">", case_sensitive=False)
bot.remove_command("help")
@bot.event
async def on_ready():
     print("Bot logged in")

@bot.command()
async def giveaway(ctx,winner:discord.Member,duration,*, msg):
      await ctx.message.delete()
      int_dur=int(duration)
      dur_mins=int_dur/60
      dur_hrs=dur_mins/60
      giveaway_embed=discord.Embed()
      giveaway_embed.title="Giveaway"
      giveaway_embed.description=f"""{msg}
      React with :tada: to participate, ends in {dur_hrs} hours
      """
      gw_msg=await ctx.send(embed=giveaway_embed)
      await gw_msg.add_reaction("🎉")
      await asyncio.sleep(int_dur)
      winner_embed=discord.Embed()
      winner_embed.title="Winner"
      winner_embed.description=f"<@{winner.id}> won **{msg}**"
      await ctx.send(f"<@{winner.id}>")
      await ctx.send(embed=winner_embed)

bot.run(TOKEN)