from YoneRobot import telethn as bot
from YoneRobot import telethn as tbot
from YoneRobot.events import register
from telethon import *
from telethon import Button, custom, events, functions
from YoneRobot.helper_extra.badmedia import is_nsfw
import requests
import string 
import random 
from YoneRobot.modules.sql_extended.nsfw_watch_sql import add_nsfwatch, rmnsfwatch, get_all_nsfw_enabled_chat, is_nsfwatch_indb
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChatAdminRights,
    ChatBannedRights,
    MessageEntityMentionName,
    MessageMediaPhoto,
)
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
async def can_change_info(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.change_info
    )
@register(pattern="^/defence")
async def nsfw(event):
    if event.is_private:
       return
    if is_nsfwatch_indb(str(event.chat_id)):
        await event.reply("`This Chat has Enabled NSFW watch`")
    else:
        await event.reply("`NSfw Watch is off for this chat`")

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
@register(pattern="^/addshield")
async def nsfw_watch(event):
    if event.is_private:
       return
    if event.is_group and not await can_change_info(message=event):
        return
    if is_nsfwatch_indb(str(event.chat_id)):
        await event.reply("`This Chat Has Already Enabled Nsfw Watch.`")
        return
    add_nsfwatch(str(event.chat_id))
    await event.reply(f"**Added Chat {event.chat.title} With Id {event.chat_id} To Database. This Groups Nsfw Contents Will Be Deleted And Logged in Logging Group**")

@register(pattern="^/rmshield ?(.*)")
async def disable_nsfw(event):
    if event.is_private:
       return
    if event.is_group and not await can_change_info(message=event):
        return
    if not is_nsfwatch_indb(str(event.chat_id)):
        await event.reply("This Chat Has Not Enabled Nsfw Watch.")
        return
    rmnsfwatch(str(event.chat_id))
    await event.reply(f"**Removed Chat {event.chat.title} With Id {event.chat_id} From Nsfw Watch**")
    
@bot.on(events.NewMessage())
async def ws(event):
    warner_starkz = get_all_nsfw_enabled_chat()
    if len(warner_starkz) == 0:
        return
    if not is_nsfwatch_indb(str(event.chat_id)):
        return
    if not event.media:
        return
    if not (event.gif or event.video or event.video_note or event.photo or event.sticker):
        return
    hmmstark = await is_nsfw(event)
    his_id = event.sender_id
    if hmmstark is True:
        try:
            await event.delete()
            await event.client(EditBannedRequest(event.chat_id, his_id, MUTE_RIGHTS))
        except:
            pass
        lolchat = await event.get_chat()
        ctitle = event.chat.title
        hehe = lolchat.username or event.chat_id
        wstark = await event.client.get_entity(his_id)
        ujwal = wstark.username or wstark.id
        try:
            await tbot.send_message(event.chat_id, f"**#ANTI_NSFW_SHIELD** \n**Chat :** `{hehe}` \n**Nsfw Sender - User / Bot :** `{ujwal}` \n**Chat Title:** `{ctitle}`")  
            return
        except:
            return

__mod_name__ = "A-Shield"

__help__ = """
*Nsfw Watch Helps to Protect Your Group From Nudety*
 ❍ /defence*:* Check NSFW WATCH status in group
 ❍ /addshield*:* Adds The Group to nsfw Watch List
 ❍ /rmshield*:* Removes The Group From nsfw Watch List
"""