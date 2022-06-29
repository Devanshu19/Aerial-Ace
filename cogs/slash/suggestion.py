from discord.ext import commands
from discord import ApplicationContext
from discord.commands import slash_command, Option

from cog_helpers import suggestion_helper
from views.GeneralView import GeneralView

class SuggestionSlash(commands.Cog):

    @slash_command(name="suggest", description="Suggest something to the developers")
    async def suggest(self, ctx:ApplicationContext, suggestion:Option(str, description="Suggestion Goes Here", required=True)):
        
        reply = await suggestion_helper.send_suggestion(ctx.guild, ctx.author, suggestion)
        view = GeneralView(200, True, True, False, False)

        await ctx.respond(reply, view=view)

def setup(bot:commands.Bot):
    bot.add_cog(SuggestionSlash())
