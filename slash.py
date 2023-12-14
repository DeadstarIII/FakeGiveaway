import discord
import interactions

bot = interactions.Client(token="")

@bot.command(
    name="my_first_command",
    description="This is the first command I made!",
    scope=866981796310679572,
)
async def my_first_command(ctx: interactions.CommandContext):
    await ctx.send("Hi there!")


bot.start()