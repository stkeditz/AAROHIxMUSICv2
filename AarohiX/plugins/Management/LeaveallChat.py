import asyncio
from AarohiX.misc import SUDOERS
from AarohiX.core.userbot import Userbot
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from AarohiX import app

userbot = Userbot()

async def restart_userbot():
    try:
        await userbot.one.stop()
    except Exception as e:
        print(f"Userbot stop error: {e}")
    try:
        await userbot.one.start()
    except Exception as e:
        print(f"Userbot start error: {e}")

@app.on_message(filters.command(["userbotjoin", f"userbotjoin@{app.username}"]) & ~filters.private & ~filters.bot)
async def join_group(client, message):
    chid = message.chat.id
    await restart_userbot()
    try:
        invitelink = await app.export_chat_invite_link(chid)
        await userbot.one.join_chat(invitelink)
        await message.reply_text(
            "🤖 **Userbot has successfully joined the chat!**\n"
            "To manage the userbot, use the available commands."
        )
    except Exception as e:
        print(f"Error joining chat: {e}")
        await message.reply_text("⚠️ **Failed to add Userbot to the chat.**")
    finally:
        await userbot.one.stop()

@app.on_message(filters.command("userbotleave") & filters.group)
async def leave_one(client, message):
    await restart_userbot()
    try:
        await userbot.one.leave_chat(message.chat.id)
        await message.reply_text("✅ **Userbot has successfully left the chat.**")
    except Exception as e:
        print(f"Error leaving chat: {e}")
        await message.reply_text("⚠️ **Failed to remove Userbot from the chat.**")
    finally:
        await userbot.one.stop()

@app.on_message(filters.command(["leaveall", f"leaveall@{app.username}"]) & SUDOERS)
async def leave_all(client, message):
    if message.from_user.id not in SUDOERS:
        await message.reply_text("❌ **You are not authorized to use this command.**")
        return

    left, failed = 0, 0
    notification = await message.reply("🔄 **Userbot is leaving all groups...**")
    await restart_userbot()

    try:
        async for dialog in userbot.one.get_dialogs():
            if dialog.chat.id == -1001733534088:  # Avoid leaving a specific chat
                continue
            try:
                await userbot.one.leave_chat(dialog.chat.id)
                left += 1
            except Exception:
                failed += 1
            await notification.edit_text(
                f"🚪 **Leaving all groups...**\n\n"
                f"✅ Left: `{left}`\n"
                f"❌ Failed: `{failed}`"
            )
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Error during leave all: {e}")
        await notification.edit_text("⚠️ **An error occurred while leaving all chats.**")
    finally:
        await userbot.one.stop()
        await message.reply_text(
            f"✅ **Left:** {left} chats.\n"
            f"❌ **Failed:** {failed} chats.\n\n"
            "Userbot cleanup complete."
        )
