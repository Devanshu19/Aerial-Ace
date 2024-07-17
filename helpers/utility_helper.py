import discord
from discord.ext import commands
import random

from helpers import general_helper
import config


# returns a value for roll
async def roll(max_value, user) -> str:
    if max_value < 0:
        return f"> **{user.name}** rolled and got ||Nothing|| :]"

    random_value = random.randint(0, max_value)
    return f"> **{user.name}** rolled and got {random_value} :game_die: [0 - {max_value}]"


# returns the about the bot embed
async def get_about_embed(ctx) -> discord.Embed:
    embd = discord.Embed(title="__ABOUT - Aerial Ace__", color=config.NORMAL_COLOR)
    embd.description = "Aerial Ace = Pokedex + Poketwo Helper Bot"

    embd.add_field(
        name=f"Prefix",
        value="`-aa ` and `aa.`",
        inline=True
    )
    embd.add_field(
        name=f"Support Server",
        value=f"[Click here]({config.SUPPORT_SERVER_LINK})",
        inline=True
    )
    embd.add_field(
        name=f"Vote Link",
        value=f"[Click Here]({config.VOTE_LINK})",
        inline=True
    )

    embd.add_field(
        name=f"Servers",
        value=len(ctx.bot.guilds),
        inline=True
    )

    embd.add_field(
        name=f"Invite",
        value=f"[Click here]({config.INVITE_LINK})",
        inline=True
    )

    embd.add_field(
        name=f"Ping",
        value=str(round(ctx.bot.latency * 100, 2)),
        inline=True
    )

    embd.add_field(
        name=f"Language",
        value="Python 3.10",
        inline=True
    )

    embd.add_field(
        name=f"Library",
        value="[py-cord](https://github.com/Pycord-Development/pycord)",
        inline=True
    )

    embd.add_field(
        name=f"Repository",
        value=f"[Click here]({config.REPO_LINK})",
        inline=True
    )

    bot: commands.Bot = ctx.bot

    shards = bot.shard_count

    embd.add_field(
        name=f"Shards",
        value="{}".format(shards),
        inline=True
    )

    embd.add_field(
        name=f"Source Details",
        value=f"**Aerial Ace** is an open source project released under GNU GPL v3 license.\nComplete source of the project is available on the github page (links above).\nRepo stars are appreciated :3",
        inline=False
    )

    embd.add_field(
        name=f"Made with  <3  by **Dev**",
        value=f"**Discord** : [DevGa.me]({config.DEVELOPER_PROFILE_LINK})\n**Github** : [Devanshu19]({config.GITHUB_PROFILE_LINK})",
        inline=False
    )

    embd.set_thumbnail(url=config.AVATAR_LINK)

    return embd


# returns the vote embed
async def get_vote_embed() -> discord.Embed:
    embd = discord.Embed(title="__Vote for Aerial Ace__", color=config.NORMAL_COLOR)
    embd.description = f"You can help Aerial Ace by voting for it.\n**Thank you** if you voted :3\n"
    embd.description += f"Vote Link : [Click here]({config.VOTE_LINK})"
    embd.set_thumbnail(url=config.AVATAR_LINK)

    return embd


# returns the support server embed
async def get_support_server_embed() -> discord.Embed:
    embd = discord.Embed(title="__Support Server__", color=config.NORMAL_COLOR)
    embd.description = f"Join the support server for reporting bugs, suggesting features,\ngetting help...you got it.\n[Click here to join]({config.SUPPORT_SERVER_LINK})"
    embd.set_thumbnail(url=config.AVATAR_LINK)

    return embd


# returns the invite embed
async def get_invite_embed() -> discord.Embed:
    embd = discord.Embed(title="__Invite - Aerial Ace__", color=config.NORMAL_COLOR)
    embd.description = "Invite Aerial Ace to your server using this link : \n\n"
    embd.description += f"Link : [Click Here]({config.INVITE_LINK})"
    embd.set_thumbnail(url=config.AVATAR_LINK)

    return embd


# logs the suggestions
async def register_suggestion(ctx, text: list) -> None:
    suggestion_channel: discord.TextChannel = ctx.bot.get_guild(config.SUPPORT_SERVER_ID).get_channel(config.SUGGESTION_LOG_CHANNEL_ID)

    embd = discord.Embed(title="__Suggestion Recieved__", color=discord.Color.green())

    embd.add_field(
        name="Sent by",
        value=ctx.author.name,
        inline=False
    )

    embd.add_field(
        name="Sent from",
        value=ctx.guild.name,
        inline=False
    )
    embd.add_field(
        name="Suggestion",
        value=" ".join(text),
        inline=False
    )

    embd.set_thumbnail(url=config.AVATAR_LINK)

    await suggestion_channel.send(embed=embd)


# returns the donation embed
async def get_premium_embed() -> discord.Embed:
    embd = await general_helper.get_info_embd(title=f"{config.PREMIUM_EMOJI}┃Premium - Aerial Ace", desc="")

    embd.set_image(url=config.PREMIUM_IMAGE)

    return embd
