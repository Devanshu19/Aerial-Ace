from discord.ext import commands

from cog_helpers import utility_helper
from cog_helpers.general_helper import get_info_embd

class Utility(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    """Get bot's latency"""

    @commands.guild_only()
    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send(f"Bot Latency (aka Ping) is : `{round(self.bot.latency * 1000, 2)}`ms")

    """Get roll"""

    @commands.guild_only()
    @commands.command()
    async def roll(self, ctx, max_value : int = 100):
        reply = await utility_helper.roll(max_value, ctx.author)
        await ctx.send(reply)

    @roll.error
    async def roll_handler(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.reply(f"Gib a interger as an argument like `{ctx.prefix}roll 69`")
        else:
            await ctx.reply(error)

    """Get links to support servers"""

    @commands.command(name="support_server", aliases=["ss"])
    async def support_server(self, ctx):
        reply = await utility_helper.get_support_server_embed()
        await ctx.send(embed=reply)

    """Get about the bot embed"""

    @commands.command(name="about")
    async def about(self, ctx):
        reply = await utility_helper.get_about_embed(ctx)
        await ctx.send(embed=reply)

    """Get vote links for the vote"""

    @commands.command(name="vote")
    async def vote(self, ctx):
        reply = await utility_helper.get_vote_embed()
        await ctx.send(embed=reply)

    """Get Invite links for the bot"""

    @commands.command(name="invite", aliases=["inv"])
    async def invite(self, ctx):
        reply = await utility_helper.get_invite_embed()
        await ctx.send(embed=reply)
            
def setup(bot):
    bot.add_cog(Utility(bot))