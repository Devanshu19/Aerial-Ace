from discord.ext import commands

import config
from views.GeneralView import GeneralView
from cog_helpers import pokemon_info_helper
from cog_helpers import general_helper

class Pokemon_Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """For getting the duel stats"""

    @commands.guild_only()
    @commands.command()
    async def stats(self, ctx, poke:str):
        reply = await pokemon_info_helper.get_stats_embed(poke)

        view = GeneralView(200, True, True, False, False)

        await ctx.send(embed=reply, view=view)

    @stats.error
    async def stats_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Gib pokemon name as a param when :/", f"A pokemon name is required for this command. Try this ```{ctx.prefix}stats Solgaleo\n{ctx.prefix}stats raichu-alola```", config.ERROR_COLOR)
            view = GeneralView(200, True, True, False, False)

            await ctx.send(embed=reply, view=view)
        else:
            await ctx.send(error)

    """For getting the duel moveset"""

    @commands.guild_only()
    @commands.command(name="moveset", aliases=["ms"])
    async def moveset(self, ctx, poke : str):
        reply = await pokemon_info_helper.get_moveset_embed(poke)
        view = GeneralView(200, True, True, False, False)

        await ctx.send(embed=reply, view=view)

    @moveset.error
    async def moveset_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Gib pokemon name as a param when :/", f"A pokemon name is required for this command, try this ```{ctx.prefix}moveset Zekrom\n{ctx.prefix}moveset raichu-alola```", config.ERROR_COLOR)
            view = GeneralView(200, True, True, False, False)

            await ctx.send(embed=reply, view=view)
        else:
            await ctx.send(error)

    """For getting the duel nature"""

    @commands.guild_only()
    @commands.command()
    async def nature(self, ctx, poke : str):
        reply = await pokemon_info_helper.get_nature_embed(poke)
        view = GeneralView(200, True, True, False, False)

        await ctx.send(embed=reply, view=view)

    @nature.error
    async def nature_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Gib pokemon name as a param when :/", f"A pokemon name is required for this command, try this ```{ctx.prefix}nature Nihilego\n{ctx.prefix}nature raichu-alola```", config.ERROR_COLOR)
            view = GeneralView(200, True, True, False, False)

            await ctx.send(embed=reply, view=view)
        else:
            await ctx.send(error)

    """For getting the tierlists"""

    @commands.guild_only()
    @commands.command(name="tierlist", aliases=["tl"])
    async def tierlist(self, ctx, tier : str):
        try:
            tier_link = config.TIER_LINK[tier.lower()]
        except:
            await ctx.reply(f"That is not a tier. Enter a good tier like `rare`, `mega`, `common`, `steel`, `fighting`")
            return

        await ctx.send(tier_link)

    @tierlist.error
    async def tierlist_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply("Give a tier name as a parameter :/ Like `rare`, `common`, `mega`, `steel`, `fighting`")
        else:
            await ctx.send(error)

    """For getting the weakness"""

    @commands.guild_only()
    @commands.command(name="weakness", aliases=["weak"])
    async def get_weakness(self, ctx, *params):

        reply = await pokemon_info_helper.get_weakness_embed(params)
        view = GeneralView(200, True, True, False, False)

        await ctx.send(embed=reply, view=view)

def setup(bot):
    bot.add_cog(Pokemon_Info(bot))