import discord
from discord.ext import commands
import asyncio
from discord.ui import View, Button
import datetime
import os
import random
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('token')
bot  = commands.Bot(command_prefix='>', intents=discord.Intents.all())

class GiveawayButtons(View):
    def __init__(self, ctx, end_time, winners):
        super().__init__()
        self.ctx = ctx
        self.end_time = end_time
        self.winners = winners
        self.entries = 0

        # Use primary style (CTA) for the button
        self.add_item(Button(style=discord.ButtonStyle.primary, label="🎉", custom_id="enter_giveaway"))

    async def interaction_handler(self, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            await interaction.response.send_message("You cannot interact with the buttons.")
            return

        if interaction.custom_id == "enter_giveaway":
            self.entries += 1
            await interaction.response.send_message(f"{interaction.user.mention} entered the giveaway!")

        elif interaction.custom_id == "check_winners":
            winners_list = await get_giveaway_winners(self.ctx, self.winners)
            winner_mentions = [f"<@{winner.id}>" for winner in winners_list]
            await interaction.response.send_message(f"Winners: {', '.join(winner_mentions)}", ephemeral=True)

    async def on_timeout(self):
        await self.ctx.send("Giveaway has ended!")

@bot.command(name='giveaway', help='Create a giveaway')
@commands.has_permissions(administrator=True)
async def giveaway(ctx, duration: str, winners: int, *, prize):
    await ctx.message.delete()

    UTC_now = datetime.datetime.utcnow()
    end_time = UTC_now + await convert_duration(duration)

    giveaway_embed = discord.Embed()
    giveaway_embed.title = "Nitro Classic"
    giveaway_embed.description = f"Ends: in {duration} ({end_time.strftime('%d %B %Y %H:%M')})\nHosted by: {ctx.author.mention}\nEntries: **0**\nWinners: **{winners}**"
    giveaway_embed.set_footer(text=f"Today at {end_time.strftime('%H:%M')}")
    giveaway_embed.colour = discord.Colour(0x5865F2)  # Set the color

    giveaway_buttons = GiveawayButtons(ctx, end_time, winners)
    giveaway_msg = await ctx.send(embed=giveaway_embed, view=giveaway_buttons)

    view = giveaway_buttons
    view.timeout = (end_time - UTC_now).total_seconds()

    await view.wait()
    await asyncio.sleep(view.timeout)

    winners_list = await get_giveaway_winners(ctx, winners)

    winner_embed = discord.Embed()
    winner_embed.title = "🏆 **Winners** 🏆"
    winner_embed.colour = discord.Colour(0x5865F2)  # Set the color

    for winner in winners_list:
        winner_embed.add_field(name=f"Winner {winners_list.index(winner) + 1}", value=f"<@{winner.id}>", inline=False)

    await ctx.send(embed=winner_embed)

async def convert_duration(duration):
    units = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
    unit = duration[-1].lower()
    amount = int(duration[:-1])
    return datetime.timedelta(seconds=amount * units[unit])

async def get_giveaway_winners(ctx, winners):
    # Implement your logic to get giveaway winners
    # This function should return a list of discord.User objects
    pass

bot.run(TOKEN)