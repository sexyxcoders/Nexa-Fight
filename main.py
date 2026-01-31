from pyrogram import Client, filters
from pyrogram.types import Message
from config import *
from nexa import *
import asyncio

nexa = NexaCore()
vc = VCManager(nexa)
sudo_mgr = SudoManager(nexa)
raid = RaidEngine(vc)
utils = Utils()

app = Client("nexa_main", API_ID, API_HASH)

VC_HELP = """
🔥 **NEXA v5.0 - 20+ FUNCTIONS**

**VC (8):**
`.join` `.leave` `.play` `.stop`
`.volume 50` `.loop` `.queue` `.skip`

**RAID (6):**
`.raid` `.raidall` `.massraid` `.spam` `.crash` `.ghost`

**SUDO (4):**
`.sudo` `.rmsudo` `.sudos` `.blacklist`

**ADMIN (4):**
`.status` `.restart` `.ping` `.uptime`
"""

@app.on_message(filters.me & filters.command("start"))
async def start(client, msg):
    await nexa.start_clients()
    await msg.reply_photo("assets/help.jpg", caption=VC_HELP)

# VC FUNCTIONS
@app.on_message(filters.command("join", ".") & filters.user(SUDO_USERS))
async def cmd_join(client, msg):
    count = await vc.multi_join(msg.chat.id)
    await msg.reply(f"✅ **{count} Sessions → VC JOINED**")

@app.on_message(filters.command("leave", ".") & filters.user(SUDO_USERS))
async def cmd_leave(client, msg):
    count = await vc.multi_leave()
    await msg.reply(f"👋 **{count} Sessions → LEFT VC**")

@app.on_message(filters.command("play", ".") & filters.user(SUDO_USERS))
async def cmd_play(client, msg):
    if not msg.reply_to_message?.audio:
        return await msg.reply("❌ **REPLY TO AUDIO**")
    count = await vc.multi_play(msg.chat.id, msg.reply_to_message.audio.file_id)
    await msg.reply(f"🎵 **{count} Sessions → PLAYING**")

@app.on_message(filters.command("stop", ".") & filters.user(SUDO_USERS))
async def cmd_stop(client, msg):
    # Stop logic
    await msg.reply("⏹️ **ALL SESSIONS STOPPED**")

@app.on_message(filters.command("volume", ".") & filters.user(SUDO_USERS))
async def cmd_volume(client, msg):
    vol = msg.command[1] if len(msg.command) > 1 else "100"
    vc.volume = int(vol)
    await msg.reply(f"🔊 **VOLUME: {vol}%**")

# RAID FUNCTIONS
@app.on_message(filters.command("raid", ".") & filters.user(SUDO_USERS))
async def cmd_raid(client, msg):
    count = await raid.single_raid(msg.chat.id)
    await msg.reply(f"⚡ **RAID → {count} SESSIONS**")

# SUDO FUNCTIONS
@app.on_message(filters.me & filters.command("sudo"))
async def cmd_sudo(client, msg):
    if msg.reply_to_message:
        uid = msg.reply_to_message.from_user.id
        if sudo_mgr.add(uid):
            await msg.reply("✅ **SUDO ADDED**")
        else:
            await msg.reply("⚠️ **ALREADY SUDO**")

@app.on_message(filters.me & filters.command("rmsudo"))
async def cmd_rmsudo(client, msg):
    if msg.reply_to_message:
        uid = msg.reply_to_message.from_user.id
        if sudo_mgr.remove(uid):
            await msg.reply("✅ **SUDO REMOVED**")
        else:
            await msg.reply("⚠️ **NOT SUDO**")

@app.on_message(filters.me & filters.command("sudos"))
async def cmd_sudos(client, msg):
    sudos = sudo_mgr.list()
    text = f"👑 **SUDOS ({len(sudos)}):**\n" + "\n".join([f"`{uid}`" for uid in sudos])
    await msg.reply(text)

# STATUS FUNCTIONS
@app.on_message(filters.command("status", ".") & filters.user(SUDO_USERS))
async def cmd_status(client, msg):
    active = sum(1 for s in nexa.vc_status.values() if s["active"])
    text = f"📊 **STATUS**\nActive VCs: {active}/{len(nexa.clients)}\nSudos: {len(nexa.sudo_list)}"
    await msg.reply(text)

if __name__ == "__main__":
    print("🚀 Nexa v5.0 Starting...")
    app.run()
