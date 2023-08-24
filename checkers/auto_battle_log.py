from discord import AutoShardedBot, Message, Member, Reaction
from asyncio import TimeoutError

from managers import mongo_manager
from helpers import battle_helper
import config


async def determine_battle_message(bot: AutoShardedBot, message: Message):
    bot_member: Member = message.guild.get_member(bot.user.id)

    # return if bot is not allowed to send messages in this channel
    if message.channel.permissions_for(bot_member).send_messages is False:
        return

    initiation_content = message.content

    if not initiation_content.strip().startswith(f"<@{config.POKETWO_ID}>"):
        return
    else:
        initiation_content = initiation_content.removeprefix(f"<@{config.POKETWO_ID}>")

    if not message.content.strip().endswith(">"):
        return

    initiation_content = initiation_content.replace("<@", "").replace(">", "").replace("&", "")

    battle_initiation_keywords = ["duel ", "battle "]

    for keyword in battle_initiation_keywords:
        if keyword in initiation_content:
            initiation_content = initiation_content.replace(keyword, "")
            break
    else:
        return

    # Check whether this server has Auto Battle Logging Enabled or Not.
    data_cursor = await mongo_manager.manager.get_all_data("servers", {"server_id": str(message.guild.id)})

    if data_cursor[0].get("auto_battle_log", 1) != 1:
        return

    challenger_id = message.author.id
    challenger_name = message.author.name
    target_id = int(initiation_content.strip())
    target_name = ""

    if challenger_id == target_id:
        return

    def get_confirmation_on_battle_invitation(reaction: Reaction, user: Member):

        nonlocal target_name

        msg: Message = reaction.message

        if msg.author.id != int(config.POKETWO_ID):
            return False

        battle_invitation_keywords = ["Challenging", "battle", "checkmark"]

        for _keyword in battle_invitation_keywords:
            if _keyword not in msg.content:
                return False

        if msg.mentions[0].id != target_id:
            return False

        if reaction.emoji != "✅":
            return False

        if user.id != target_id:
            return False

        target_name = user.name

        return True

    try:
        await bot.wait_for("reaction_add", check=get_confirmation_on_battle_invitation, timeout=20)

    except TimeoutError:
        return await message.channel.send("> Auto Battle Log Session Timed out! Please accept the battle invitation.")

    else:
        await message.channel.send(
            "> Auto Battle Log Session Started! \n**NOTE: **Auto Battle Logging Module is coming out of beta and will be released as a premium feature! If you want to continue using it, please support aerial ace on patron.")

    conclusion_type = None
    winner = None
    loser = None

    def get_battle_cancel_message(msg: Message):

        nonlocal conclusion_type

        if not msg.content.strip().startswith(f"<@{config.POKETWO_ID}>"):
            return False

        if msg.author.id != challenger_id and msg.author.id != target_id:
            return False

        if "x" not in msg.content.lower() and "cancel" not in msg.content.lower():
            return False

        battle_cancel_keywords = ["duel ", "battle "]

        for _keyword in battle_cancel_keywords:
            if _keyword in msg.content:
                break
        else:
            return

        conclusion_type = "CANCEL"

        return True

    def get_battle_end_message(msg: Message):

        nonlocal conclusion_type, winner, loser

        if msg.author.id != int(config.POKETWO_ID):
            return False

        if "won the battle!" in msg.content:
            winner = msg.mentions[0].id
        else:
            if "has won." in msg.content:
                winner = int(msg.content.removesuffix("> has won.").split()[-1].removeprefix("<@"))
            else:
                return False

        if winner != challenger_id and winner != target_id:
            return False

        conclusion_type = "FINISH"

        loser = (target_id if winner == challenger_id else challenger_id)

        return True

    def get_battle_conclusion(msg: Message):

        if get_battle_cancel_message(msg) is not False:
            return True

        if get_battle_end_message(msg) is not False:
            return True

        return False

    try:
        await bot.wait_for("message", check=get_battle_conclusion, timeout=10 * 60)

    except TimeoutError:
        await message.channel.send(
            "> Auto Battle Logging session ended with a timeout. Make sure to register your battle manually.")

    if conclusion_type == "CANCEL":
        return await message.channel.send("> Auto Log Session Cancelled!")

    elif conclusion_type == "FINISH":
        await message.channel.send("> Logging Battle. Please Wait!")

        winner_name = (challenger_name if challenger_id == winner else target_name)
        loser_name = (challenger_name if challenger_id == loser else target_name)

        reply = await battle_helper.register_battle_log(message.guild.id, str(winner), str(loser), winner_name,
                                                        loser_name)

        await message.channel.send(reply)
