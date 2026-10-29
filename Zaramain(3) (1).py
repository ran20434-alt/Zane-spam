#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import os
import re
import sys
import time
import random
import threading
import websocket

from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))

PERMANENT_OWNER = 1238882845322121308
BOT_TOKENS = [
    "token",
  "token",
  "token"

]
DEFAULT_PREFIX = "!"
ALLOWED_FILE = "allowed_ids.json"
SUDO_FILE = "sudo_users.json"

GAMEOVER_GIF = "https://cdn.discordapp.com/attachments/1545663651808018465/1545720560883990548/InShot_20260819_124349115.gif?ex=6aa514f3&is=6aa3c373&hm=97216e1b40e07c84564b283da6f6a4add43f3be45c5cca9845c1c882df8dfda4&"

RAINBOW_COLORS = [
    "\033[38;5;196m", "\033[38;5;202m", "\033[38;5;208m", "\033[38;5;214m",
    "\033[38;5;220m", "\033[38;5;226m", "\033[38;5;190m", "\033[38;5;118m",
    "\033[38;5;82m",  "\033[38;5;46m",  "\033[38;5;51m",  "\033[38;5;45m",
    "\033[38;5;39m",  "\033[38;5;33m",  "\033[38;5;57m",  "\033[38;5;93m",
    "\033[38;5;129m", "\033[38;5;165m", "\033[38;5;201m", "\033[38;5;199m",
]
RESET = "\033[0m"

def rainbow_line(text, offset=0):
    result = ""
    n = len(RAINBOW_COLORS)
    for i, ch in enumerate(text):
        if ch == "\n":
            result += "\n"
        else:
            result += RAINBOW_COLORS[(i + offset) % n] + ch
    return result + RESET

NC_POOLS = {
    "base": ["💤","🎀","💋","💗"],
    "lightning": ["⚡","💫","✨","🌟"],
    "heart": ["🩵","💙","🤍","💜"],
    "keng": ["👑","🔱","⚜️","〽️"],
    "time": ["🕐","🕑","🕒","🕓","⏱️"],
    "animal": ["🦁","🦅","🐺","🦂","🐍","🐆","🦈"],
    "gothic": ["⛓️‍💥","🖤","☠️","⚔️","🥀","🕯️","🎭"],
    "cosmic": ["🌌","🪐","🌟","☄️","🛸","🔮","🌀"],
    "viper": ["🧪","☣️","💚","🔋","🩻","🦠","🧬"],
    "demon": ["👹","🔥","🏮","👁️‍🗨️","🩸","🏛️","🔱"],
    "ocean": ["🌊","🦈","🐙","⚓","🐬","🐳","💧"],
    "frost": ["❄️","🥶","🧊","🏔️","💎","🌨️","🔮"],
    "cyber": ["🤖","💻","💾","📡","👾","⚙️","🔋"],
    "toxic": ["🤢","☣️","☢️","⚠️","🛑","🗑️","🤮"],
    "royal": ["👑","🏰","⚜️","💎","💰","🧝","🦁"],
    "voodoo": ["🔮","🧿","🪄","🧙","🕯️","🎴","🃏"],
    "undead": ["💀","👻","🧟","⚰️","🥀","🖤","🪦"],
    "ninja": ["🥷","🗡️","⚔️","🏮","⛩️","得","💨"],
    "samurai": ["👺","⚔️","🛡️","💮","🗻","🏯","🩸"],
    "arcade": ["🕹️","🎰","👾","🎲","🎟️","💥","🏁"],
    "shadow": ["🥷","🌑","🕷️","🕸️"],
    "hazard": ["☣️","⚠️","🛑"],
    "matrix": ["🟢","📟","🔋","💻"],
    "phantom": ["👻","🌫️","🔮","⛓️"],
    "galaxy": ["🌌","🚀","🪐","🌠"],
    "valiant": ["🛡️","⚔️","🦅","🎖️"],
    "glitch": ["🎛️","🎚️","🔌","📡"],
    "inferno": ["🔥","🌋","💥","☄️"],
    "dynasty": ["🏮","⛩️","得","👑"],
    "rebel": ["🏴‍☠️","💣","⚔️","💥"],
}

CUSTOM_NC_PHRASES = ["RANDAL KA PILLA","KUTTE KA LADKA","PAPA BOL","SALUTE KAR","BETICHOD","BSDK","TMKX M"]
NC_MESSAGES = ["ASSHOLE","MG KA BETA","JHATU","RNDYKA","LESBIAN","GAY","CHUTIYA","HIJDA","CHAMMR","MITHA","DICKEATER","RANDAL KA PILLA","KUTTE KA LADKA","PAPA BOL","SALUTE KAR"]
NC_EMOJIS = ["😈","🤣","🤫","🤢","😣","😝","🤩","🤮","🤡","💩","🫦","💦","😖"]

HEART_EMOJIS = ["🇮🇳", "🇺🇸", "🇬🇧", "🇯🇵", "🇨🇦", "🇦🇺", "🇫🇷", "🇩🇪", "🇧🇷", "🇰🇷"]

LONG_SPAM_WORDS = [

    "𝐋ᴜɴ𝐃 𝐂ʜᴜ𝐒 𝐀𝐩ɴᴇ 𝐁ᴀ𝐀𝐩 𝐊𝐀 !! 🔥😂",
    "𝐓ᴍᴋ𝐂 𝐏ᴇ 𝐂ʜᴘᴘ𝐋 𝐇ɪ 𝐂ʜᴘᴘ𝐋 𝐌ᴀʀᴜɴɢ𝐀 !! 🔥😂🩴",
    "𝐀ᴊ𝐀 𝐋ᴜɴ𝐃 𝐓ᴇ 𝐕ᴀᴊ 😈🔥",
    "𝐂ʜʟ 𝐓ᴇ𝐑ɪ 𝐌ᴀ𝐀 𝐑ɴᴅ𝐘 🐄🔥",
    "𝐓ᴇʀ𝐀 𝐃ʜʏᴀ𝐍 𝐊ᴀʜ𝐀 𝐇ᴀ𝐈 𝐓ᴇᴇʀᴇ अब्बू 𝐘ᴀʜᴀ𝐍 𝐇ᴀ𝐈 😎💥🔥",
    "𝑮ᴄ 𝑳ᴇ𝑓𝑻 𝑳ᴇ लंगड़ी 𝐌ᴀ𝐀 𝐊ᴇ 𝐁ᴀᴄʜ𝐄 🤮",
    "𝐆ʀɪʙ 𝐊ᴇ 𝐁ᴀᴄʜʜᴇ😂🖕",
    "𝐆ᴀᴛᴀᴋ 𝐋ᴇ 𝐈ꜱᴋᴏ 8=========𝙳   𝐑ɴᴅʏᴋ😂🖕",
    "𝐋ᴇʜ 𝐓ᴇʀɪ 𝐆ᴀɴᴅ 𝐌ᴇ 𝐒ᴩᴇʀᴍ💦👌",
    "𝐓ᴇʀɪ 𝐁ᴇʜᴇɴ 𝐊ɪ 𝐂ʜᴜᴛ 𝐌ᴇ 𝐓ᴇxᴛ😂🖕",
    "𝐊ɪʟᴀꜱ 𝐌ᴅᴄ😂🖕",
    "𝐀ᴡᴀᴊ 𝐔ᴛʜᴀ 𝐑ᴀɴᴅʏᴋ 😂🖕",
    "𝐓ᴇ𝐑ɪ 🦅🔥 𝐌ᴀA 🦅🔥 RANDY🎀",
]

LONGSPAM2_VARIATIONS = [
    "𝘚𐐛𝔸𝚅𝞔 🚀", "𝑺𐐛𝑨𝑽𝑬 ⚡", "𝙎𐐛𝘼𝙑𝙀 🔥", "𝕾𐐛𝕬𝖁𝕰 🖤", "Ｓ𐐛ＡＶＥ 💫",
    "𝓢𐐛𝓐𝓥𝓔 🥀", "𝗦𐐛𝗔𝗩𝗘 ☠️", "𝚂𐐛𝙰𝚅𝙴 🚀", "𝒮𐐛𝒜𝒱ℰ 🪽", "𝔖𐐛𝔄𝔙𝔈 🌑",
    "𝘚𐐛𝘈𝘝𝘌 ⚡", "𝐒𐐛𝐀𝐕𝐄 🔥", "𝙎𐐛𝘼𝙑𝙀 🥀", "𝕊𐐛𝔸𝕍𝔼 🖤", "𝑆𐐛𝐴𝑉𝐸 💔",
    "𝖲𐐛𝖠𝖵𝖤 🚀", "𝓢𐐛𝓐𝓥𝓔 🌹", "𝕾𐐛𝕬𝖁𝕰 ⚔️", "𝑺𐐛𝑨𝑽𝑬 🦋", "𝙎𐐛𝘼𝙑𝙀 🌌",
    "Ｓ𐐛ＡＶＥ 🥀", "𝗦𐐛𝗔𝗩𝗘 💀", "𝚂𐐛𝙰𝚅𝙴 🖤", "𝒮𐐛𝒜𝒱ℰ 💔", "𝔖𐐛𝔄𝔙𝔈 🔥",
    "𝘚𐐛𝔸𝚅𝞔 🌑", "𝐒𐐛𝐀𝐕𝐄 🚀", "𝑺𐐛𝑨𝑽𝑬 🥶", "𝕊𐐛𝔸𝕍𝔼 ⚡", "𝓢𐐛𝓐𝓥𝓔 🕊️",
    "𝖲𐐛𝖠𝖵𝖤 🥀", "𝙎𐐛𝘼𝙑𝙀 🩶", "𝕾𐐛𝕬𝖁𝕰 🩸", "𝑆𐐛𝐴𝑉𝐸 🌙", "𝒮𐐛𝒜𝒱ℰ 💫",
    "𝗦𐐛𝗔𝗩𝗘 🗿", "𝚂𐐛𝙰𝚅𝙴 🦅", "𝐒𐐛𝐀𝐕𝐄 🐉", "𝙎𐐛𝘼𝙑𝙀 🐺", "𝕾𐐛𝕬𝖁𝕰 🦂",
    "𝓢𐐛𝓐𝓥𝓔 🦋", "𝘚𐐛𝔸𝚅𝞔 🌹", "Ｓ𐐛ＡＶＥ 🌊", "𝖲𐐛𝖠𝖵𝖤 🌪️", "𝑺𐐛𝑨𝑽𝑬 ☄️",
    "𝕊𐐛𝔸𝕍𝔼 🌠", "𝗦𐐛𝗔𝗩𝗘 🎭", "𝙎𐐛𝘼𝙑𝙀 🥷", "𝕾𐐛𝕬𝖁𝕰 🕷️", "𝒮𐐛𝒜𝒱ℰ 🦇",
    "𝓢𐐛𝓐𝓥𝓔 🖤", "𝘚𐐛𝘈𝘝𝘌 💔", "𝐒𐐛𝐀𝐕𝐄 🥀", "𝑺𐐛𝑨𝑽𝑬 🕊️", "𝙎𐐛𝘼𝙑𝙀 🌑",
    "𝕾𐐛𝕬𝖁𝕰 ☠︎", "Ｓ𐐛ＡＶＥ ⚡", "𝗦𐐛𝗔𝗩𝗘 🔱", "𝚂𐐛𝙰𝚅𝙴 🛡️", "𝒮𐐛𝒜𝒱ℰ 👑",
    "𝓢𐐛𝓐𝓥𝓔 💎", "𝖲𐐛𝖠𝖵𝖤 🧊", "𝘚𐐛𝔸𝚅𝞔 🌙", "𝐒𐐛𝐀𝐕𝐄 ☁️", "𝑆𐐛𝐴𝑉𝐸 🌫️",
    "𝙎𐐛𝘼𝙑𝙀 🌧️", "𝕊𐐛𝔸𝕍𝔼 🌹", "𝕾𐐛𝕬𝖁𝕰 🩶", "𝒮𐐛𝒜𝒱ℰ 🫀", "𝓢𐐛𝓐𝓥𝓔 💧",
    "𝗦𐐛𝗔𝗩𝗘 🫥", "𝚂𐐛𝙰𝚅𝙴 😶", "𝘚𐐛𝘈𝘝𝘌 🥺", "𝑺𐐛𝑨𝑽𝑬 😈", "𝙎𐐛𝘼𝙑𝙀 👿",
    "𝕾𐐛𝕬𝖁𝕰 🐍", "𝖲𐐛𝖠𝖵𝖤 🐲", "𝕊𐐛𝔸𝕍𝔼 🦁", "𝐒𐐛𝐀𝐕𝐄 🐯", "𝒮𐐛𝒜𝒱ℰ 🦋",
    "𝓢𐐛𝓐𝓥𝓔 🌸", "Ｓ𐐛ＡＶＥ 🌺", "𝘚𐐛𝔸𝚅𝞔 🌻", "𝑺𐐛𝑨𝑽𝑬 🍂", "𝙎𐐛𝘼𝙑𝙀 🍁",
    "𝕾𐐛𝕬𝖁𝕰 🌲", "𝗦𐐛𝗔𝗩𝗘 🌴", "𝚂𐐛𝙰𝚅𝙴 🌵", "𝒮𐐛𝒜𝒱ℰ 🌿", "𝓢𐐛𝓐𝓥𝓔 🍃",
    "𝖲𐐛𝖠𝖵𝖤 🌊", "𝕊𐐛𝔸𝕍𝔼 🔥", "𝐒𐐛𝐀𝐕𝐄 ⚡", "𝑺𐐛𝑨𝑽𝑬 🚀", "𝙎𐐛𝘼𝙑𝙀 💥",
    "𝕾𐐛𝕬𝖁𝕰 🖤", "𝘚𐐛𝔸𝚅𝞔 🥀", "𝒮𐐛𝒜𝒱ℰ 💔", "𝓢𐐛𝓐𝓥𝓔 🕊️",
]

LONGSPAM2_COUNT = 10

# ═══════════════════════════════════════════════════════════════
#        🆕 LONGSPAM3 — 7 UNIQUE MESSAGES (auto target fill)
# ═══════════════════════════════════════════════════════════════

LONGSPAM3_TEMPLATES = [
    "✩ ˚₊‧୨୧‧₊˚ ✩ ˚₊‧🫧‧₊˚ ✩ ˚₊‧୨୧‧₊˚ 🖇️🎧『 {TARGET} 』𝐓ᴀʀɪ 𝐌ᴀʏɪ 𝐊ᴀ 𝐂ʜᴏᴅᴏ 🌷♡⊹˚₊‧✩",
    "➛. ׂׂૢ : ‌‌➛. ׂׂૢ : ‌‌➛. ׂׂૢ : ‌‌➛. ׂׂૢ : ‌‌➛. ׂׂૢ : ‌‌➛. ׂׂૢ : ‌‌➛. ׂׂૢ : l ׂׂૢ『 {TARGET} 』𝐓ᴇʀɪ 𝐑🔺ɴᴅɪ 𝐌ᴀᴀ 𝐊ɪ 𝐂ʜᴜ𝐓 𝐁ᴀᴊᴀᴜ 🥁🔥🥁🔥⋅˚₊‧ 𐙚 ‧₊˚ ⋅⋆ ˚｡⋆‧₊˚ ⋅⋆ ˚｡‧₊˚ ⋅⋆ ˚｡୨୧",
    "『 {TARGET} 』 𝐈 #𝗙ꪊᴄᴋ ʏᴏᴜʀ 𝐌ᴏᴍᴍʏ ⃟🌷꙰⃟",
    "˚₊‧♡⊹˚₊ ✩ ˚₊‧♡⊹˚₊ ✩ ˚₊‧♡⊹˚₊ ✩ ˚₊‧♡⊹˚₊ ✩ ˚₊‧♡⊹˚₊ ✩ ˚₊‧ ‧₊˚🖇️✩ ₊˚🎧⊹♡『 {TARGET} 』𝐓ᴇʀɪ 𝐌ᴀ𝐀 𝐂ʜ⭕𝐃 𝐃△ʟᴇɴɢ𝐄 ♡⊹🎧˚₊ 🖇️✩ ˚₊𓆩♡𓆪˖",
    "˚₊‧꒰ა 🖇️ ໒꒱ ‧₊˚『 {TARGET} 』𝐁ʜᴀᴜᴋɴᴀ 𝐁ᴀɴᴅ 𝐊ᴀʀᴏ 🎧🫧",
    "𓆩♡𓆪 ˚₊‧꒰ა 🥀 ໒꒱‧₊˚ 『 {TARGET} 』𝐁ʜᴇɴ 𝐊ᴇ 𝐋ᴏᴅᴇ ⃟🔥꙰⃟ 𓆩♡𓆪",
    "𓆩♡𓆪 ˚₊‧꒰ა 🥀 ໒꒱‧₊˚ 『 {TARGET} 』𝐉ʜᴜɴᴅ 𝐌ᴇɪɴ 𝐒ʜᴇʀ 𝐇ᴜɴ 𝐌ᴀɪɴ ⃟🐺꙰⃟ 𓆩♡𓆪",
    "꧁ ᥫᩣ ︻╦デ╤━╼ ❃ ♡♫ 𝐍ᴀᴅɪ 𝐊ɪɴᴀʀᴇ 𝐒ᴀᴀɴᴩ 𝐇ᴀɪ 🐍『 {TARGET} 』𝐊ɪ 𝐌ᴀᴀ 𝐊ᴏ 𝐂ʜᴏᴅɴᴀ 𝐏ᴀᴀᴩ 𝐇ᴀɪ 💦 ══════ •『 ♡ 』• ══════ ♬ ♡ ❃ ᥫᩣ ꧂",
    "➛ ᚛『 {TARGET} 』𝐎ʏᴇ 𝐒ᴜɴ 𝐓ᴇʀɪ 𝐌ᴏᴍ रंडी — ⬱⬱⬱⬱⬱⬱⬱⬱⬱⬱⬱: ̗̀➛ ᚛᚜ 𝐓ᴇʀɪ 𝐌ᴀᴀ 𝐊ᴀ बुर 𝐌ᴀᴅᴀʀᴄʜ⭕ᴅ  જ⁀➴જ⁀➴જ⁀➴- 😂✋",
    "𓂃☁︎ 𓂃『 {TARGET} 』𝐒ɪᴅᴇ 𝐇ᴀᴛ 𝐆ᴜʟᴀᴍ 𝐓ᴇʀɪ 𝐌ᴀᴀ 𝐊ᴏ 𝐂ʜᴏᴅɴᴇ मेरी रेलगाड़ी आ रही .-‘🚂-‘.ᯓᡣ𐭩__ 𓂃☁︎ 𓂃",
    "❖ ── ✦ ──『 {TARGET} 』𝐏ɪʏᴇ पानी 𝐔sᴋɪ 𝐌ᴀᴀʀᴇ 𝐀ᴍʙᴀɴɪ 🎐 ── ✦ ── ❖",
]

NC_PATTERNS = [
    "𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫",
    "𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷",
    "🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫",
    "𒐫🩵𒐫💙𒐫🤍𒐫💜𒐫🩷𒐫❤️𒐫💖𒐫💗𒐫💓𒐫💘𒐫💝𒐫💞𒐫💕𒐫💚𒐫🩵𒐫💙𒐫🤍𒐫💜𒐫🩷𒐫❤️"
]

AUTOREPLY_REPLY_TEXTS = [
    "𝐖ᴏ ʙʜɪ ᴋʏᴀ ᴅɪɴ ᴛʜᴇ ᴊᴀʙ ᴛʀʏ ᴍᴀᴀ ᴍᴜᴊʜᴇ 𝐀ᴘɴᴀ 𝐂ʜᴜᴛ 𝐃ᴇᴛɪ ᴛʜɪ ʏᴀᴀʀ 💔🥀👌🏻",
    "𝐀ᴡᴀᴢ 𝐍ɪᴄʜᴇ 𝐆ᴜʟᴀᴀᴍ 🤢👇🏻",
    "𝐓ʀʏ 𝐌ᴀᴀ ɴᴇ 𝐂ʜᴜᴅɴᴇ 𝐌ᴀɪ ɢᴏʟᴅ 𝐌ᴇᴅᴀʟ 𝐉ᴇᴇᴛᴀ ᴇʏ 𝐃ᴏꜱᴛ 🤩👑",
    "𝐓ᴇʀɪ 𝐌ᴀᴀ ᴋɪ 𝐂ʜᴜᴛ 𝐌ᴇ 𝐌ᴇʀᴀ 𝐋ᴜɴᴅ 🖕🏻😈",
    "𝐁ʜᴏꜱᴀᴅɪᴋᴇ 𝐀ᴘɴɪ 𝐁ᴇʜᴇɴ 𝐂ʜᴜᴅᴀ 🖕🏻😈",
    "𝐑ᴀɴᴅɪ ᴋᴇ 𝐁ᴀᴄᴄʜᴇ 𝐀ᴜᴋᴀᴛ 𝐌ᴇ 𝐑ᴇʜ 🖕🏻😈",
    "𝐌ᴀᴅᴀʀᴄʜᴏᴅ 𝐓ᴇʀɪ 𝐌ᴀᴀ ᴋɪ 𝐂ʜᴜᴛ 🖕🏻😈",
    "𝐁ʜᴇɴᴄʜᴏᴅ 𝐀ᴘɴɪ 𝐀ᴜᴋᴀᴛ 𝐌ᴇ 𝐑ᴇʜ 🤡💩",
    "𝐓𝐌𝐊𝐂 ᴘᴇ 𝐂ʜᴀᴘᴘᴀʟ 𝐌ᴀᴀʀᴜɴɢᴀ 👟💥",
    "𝐁𝐊𝐂 🦴🐕",
]

allowed_ids = set()
allowed_lock = threading.RLock()

def load_allowed_ids():
    global allowed_ids
    if os.path.exists(ALLOWED_FILE):
        try:
            with open(ALLOWED_FILE) as f:
                allowed_ids = set(json.load(f))
        except: pass
    allowed_ids.add(PERMANENT_OWNER)
    save_allowed_ids()

def save_allowed_ids():
    with allowed_lock:
        with open(ALLOWED_FILE, "w") as f:
            json.dump(list(allowed_ids), f)

def load_sudo_file():
    if os.path.exists(SUDO_FILE):
        try:
            with open(SUDO_FILE) as f:
                return json.load(f)
        except: pass
    return []

def save_sudo_file(lst):
    with open(SUDO_FILE, "w") as f:
        json.dump(lst, f)

SESSION = requests.Session()

def api_request(method, url, token, **kwargs):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    if "headers" in kwargs:
        headers.update(kwargs.pop("headers"))
    for _ in range(12):
        try:
            resp = getattr(SESSION, method.lower())(url, headers=headers, **kwargs)
            if resp.status_code == 429:
                wait = resp.json().get("retry_after", 2.0)
                time.sleep(wait + random.uniform(0.1, 0.5))
                continue
            return resp
        except: time.sleep(0.5)
    return None

def send_message(channel_id, token, content, reply_to=None):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    payload = {"content": content}
    if reply_to:
        payload["message_reference"] = {"channel_id": channel_id, "message_id": reply_to}
    resp = api_request("POST", url, token, json=payload)
    return resp.json() if resp and resp.status_code == 200 else None

def get_bot_info(token):
    resp = api_request("GET", "https://discord.com/api/v9/users/@me", token)
    return resp.json() if resp and resp.status_code == 200 else None

# ═══════════════════════════════════════════════════════════════
#        🆕 GC MAKER + FRIEND REQUEST HELPERS (FIXED)
# ═══════════════════════════════════════════════════════════════

def create_group_dm(token, recipient_ids):
    """Create a new group DM. Returns (channel_id, status_message)."""
    url = "https://discord.com/api/v9/users/@me/channels"
    clean_ids = [str(x).strip() for x in recipient_ids if str(x).strip()]
    if not clean_ids:
        return None, "no-recipients"
    payload = {"recipients": clean_ids}
    resp = api_request("POST", url, token, json=payload)
    if resp is None:
        return None, "no-response"
    if resp.status_code in (200, 201):
        try:
            cid = resp.json().get("id")
            return cid, "ok"
        except Exception as e:
            return None, f"bad-json: {e}"
    err_msg = ""
    try:
        j = resp.json()
        err_msg = j.get("message", "") or str(j)[:120]
    except:
        err_msg = f"http-{resp.status_code}"
    return None, f"HTTP {resp.status_code}: {err_msg}"

def add_user_to_group(token, channel_id, user_id):
    url = f"https://discord.com/api/v9/channels/{channel_id}/recipients/{user_id}"
    resp = api_request("PUT", url, token, json={})
    return resp and resp.status_code in (200, 201, 204)

def send_friend_request(token, user_id):
    """Send a friend request. Returns (ok, status)."""
    url = f"https://discord.com/api/v9/users/@me/relationships/{user_id}"
    resp = api_request("PUT", url, token, json={})
    if resp is None:
        return False, "no-resp"
    return resp.status_code in (200, 201, 204), resp.status_code

def accept_friend_request(token, user_id):
    """Accept an incoming friend request. Returns (ok, status)."""
    uid_str = str(user_id).strip()
    resp = api_request("GET", "https://discord.com/api/v9/users/@me/relationships", token)
    if resp is None:
        return False, "no-response"
    if resp.status_code != 200:
        return False, f"http-{resp.status_code}"
    try:
        relationships = resp.json()
    except:
        return False, "bad-json"

    # Look for incoming FR (type 3) — check both top-level id and nested user.id
    found = False
    for r in relationships:
        if not isinstance(r, dict):
            continue
        if r.get("type") != 3:
            continue
        top_id = str(r.get("id", "")).strip()
        nested_id = str((r.get("user") or {}).get("id", "")).strip()
        if top_id == uid_str or nested_id == uid_str:
            found = True
            break

    if not found:
        return False, "no-fr"

    put = api_request("PUT", f"https://discord.com/api/v9/users/@me/relationships/{uid_str}", token, json={})
    if put is None:
        return False, "no-resp-put"
    return put.status_code in (200, 201, 204), put.status_code

def change_gc_name(channel_id, token, name):
    return api_request("PATCH", f"https://discord.com/api/v9/channels/{channel_id}", token, json={"name": name})

def nc_worker(bot, g_id, pool_key, text_content=""):
    pattern_idx = 0
    while bot.active_nc.get(g_id, False):
        try:
            if pool_key == "CUSTOM":
                phrase = random.choice(CUSTOM_NC_PHRASES)
                base = f"{text_content} {phrase}".strip()
            elif pool_key == "TIME":
                all_e = [e for pool in NC_POOLS.values() for e in pool]
                t_str = datetime.now(IST).strftime("%H:%M:%S")
                base = f"{text_content} {t_str} {random.choice(all_e)}".strip()
            elif pool_key == "ALL":
                all_e = [e for pool in NC_POOLS.values() for e in pool]
                base = f"{text_content} {random.choice(all_e)}".strip()
            else:
                pool = NC_POOLS.get(pool_key, NC_POOLS["base"])
                base = f"{text_content} {random.choice(pool)}".strip()
            roast = random.choice(NC_MESSAGES)
            base = f"{base} {roast}".strip()
            pattern = NC_PATTERNS[pattern_idx % len(NC_PATTERNS)]
            pattern_idx += 1
            current = base
            if len(current) > 100:
                current = current[:100]
            elif len(current) < 100:
                needed = 100 - len(current)
                current += pattern * (needed // len(pattern)) + pattern[:needed % len(pattern)]
            change_gc_name(g_id, bot.token, current)
            time.sleep(bot.nc_delay)
        except: time.sleep(0.05)

def fast_nc_worker(bot, g_id, text_content, num_threads=5):
    stop_event = threading.Event()
    bot.fast_nc_stop_evts[g_id] = stop_event
    pool_names = list(NC_POOLS.keys())
    chunk = max(1, len(pool_names) // num_threads)
    threads = []
    for i in range(num_threads):
        assigned = pool_names[i * chunk:(i + 1) * chunk] or [pool_names[i % len(pool_names)]]
        def sub_worker(assigned_pools, stop_ev):
            pool_idx = 0
            pattern_idx = 0
            while not stop_ev.is_set():
                try:
                    pool = NC_POOLS.get(assigned_pools[pool_idx % len(assigned_pools)], NC_POOLS["base"])
                    emoji = random.choice(pool)
                    roast = random.choice(NC_MESSAGES)
                    base = f"{text_content} {emoji} {roast}".strip()
                    pattern = NC_PATTERNS[pattern_idx % len(NC_PATTERNS)]
                    pattern_idx += 1
                    if len(base) > 100:
                        base = base[:100]
                    elif len(base) < 100:
                        needed = 100 - len(base)
                        base += pattern * (needed // len(pattern)) + pattern[:needed % len(pattern)]
                    change_gc_name(g_id, bot.token, base)
                    pool_idx += 1
                except: time.sleep(0.05)
        t = threading.Thread(target=sub_worker, args=(assigned, stop_event), daemon=True)
        t.start()
        threads.append(t)
    bot.fast_nc_threads[g_id] = threads

def gc_nc_matrix_worker(bot, group_id, base_text):
    idx = 0
    pattern_idx = 0
    while bot.gc_name_tasks.get(group_id) is not None:
        try:
            msg_txt = NC_MESSAGES[idx % len(NC_MESSAGES)]
            possible = [e for e in NC_EMOJIS if e != bot.last_emoji_used.get(group_id)]
            emoji = random.choice(possible if possible else NC_EMOJIS)
            bot.last_emoji_used[group_id] = emoji
            base = f"{base_text} - {msg_txt} {emoji}"
            pattern = NC_PATTERNS[pattern_idx % len(NC_PATTERNS)]
            pattern_idx += 1
            if len(base) > 100:
                base = base[:100]
            elif len(base) < 100:
                needed = 100 - len(base)
                base += pattern * (needed // len(pattern)) + pattern[:needed % len(pattern)]
            change_gc_name(group_id, bot.token, base)
            idx += 1
        except: pass
        time.sleep(0)

def server_nc_worker(bot, guild_id, base_text):
    idx = 0
    pattern_idx = 0
    while bot.server_name_tasks.get(guild_id) is not None:
        try:
            msg_txt = NC_MESSAGES[idx % len(NC_MESSAGES)]
            possible = [e for e in NC_EMOJIS if e != bot.last_emoji_used.get(guild_id)]
            emoji = random.choice(possible if possible else NC_EMOJIS)
            bot.last_emoji_used[guild_id] = emoji
            base = f"{base_text} - {msg_txt} {emoji}"
            pattern = NC_PATTERNS[pattern_idx % len(NC_PATTERNS)]
            pattern_idx += 1
            if len(base) > 100:
                base = base[:100]
            elif len(base) < 100:
                needed = 100 - len(base)
                base += pattern * (needed // len(pattern)) + pattern[:needed % len(pattern)]
            change_gc_name(guild_id, bot.token, base)
            idx += 1
        except: pass
        time.sleep(0)

def long_spam_worker(bot, channel_id, mention, stop_event):
    word_idx = 0
    while not stop_event.is_set():
        try:
            word = LONG_SPAM_WORDS[word_idx % len(LONG_SPAM_WORDS)]
            heart = random.choice(HEART_EMOJIS)
            block = ""
            current_length = 0
            while current_length < 1950:
                line = f"# {mention} {word} 𓆩{heart}𓆪\n"
                if current_length + len(line) > 1950:
                    break
                block += line
                current_length += len(line)
            if block.strip():
                send_message(channel_id, bot.token, block.strip())
            word_idx += 1
        except: pass
        time.sleep(0.05)

def long_spam2_worker(bot, channel_id, mention, stop_event):
    m = re.match(r"<@!?(\d+)>", mention)
    if m:
        target_display = m.group(1)
    else:
        target_display = mention.strip("@")

     
    while not stop_event.is_set():
        try:
            block = ""
            for _ in range(LONGSPAM2_COUNT):
                suffix = random.choice(LONGSPAM2_VARIATIONS)
                block += f"# {target_display} {suffix}\n\n"
            if len(block) > 1990:
                block = block[:1990]
            if block.strip():
                send_message(channel_id, bot.token, block.strip())
        except Exception as e:
            print(f"[LONGSPAM2] err: {e}")
        time.sleep(0.05)



def long_spam3_worker(bot, channel_id, target_name, stop_event):
    idx = 0
    while not stop_event.is_set():
        try:
            template = LONGSPAM3_TEMPLATES[idx % len(LONGSPAM3_TEMPLATES)]
            msg = template.replace("{TARGET}", target_name)
            block = ""
            i = 0
            while len(block) + len(msg) + 1 < 1990:
                block += msg + "\n"
                i += 1
                if i >= 3:
                    break
            if block.strip():
                send_message(channel_id, bot.token, block.strip())
            idx += 1
        except Exception as e:
            print(f"[LONGSPAM3] err: {e}")
        time.sleep(0.05)


def mention_spam_worker(bot, channel_id, mention, stop_event):
    while not stop_event.is_set():
        try:
            send_message(channel_id, bot.token, mention)
        except: pass
        time.sleep(0.0)

def spam_worker_matrix(bot, channel_id, text):
    idx = 0
    custom_msgs = ["😺","😸","😹","😻","😼","😽","🙀","😈","🤣","😝","🤩","🤢","🤮","🤡","💩","🫦","💦","😖"]
    while bot.spam_tasks.get(channel_id) is not None:
        try:
            content = f"{text} {custom_msgs[idx % len(custom_msgs)]}".replace("@","@")
            send_message(channel_id, bot.token, content)
            idx += 1
        except: pass
        time.sleep(bot.spam_delay)

def extract_user_id_from_mention(mention):
    if mention.startswith('<@') and mention.endswith('>'):
        mention = mention[2:-1]
        if mention.startswith('!'):
            mention = mention[1:]
    else:
        if mention.startswith('@'):
            mention = mention[1:]
    match = re.search(r'\d+', mention)
    if match:
        return match.group()
    return None

def add_reaction(channel_id, message_id, emoji, token):
    encoded_emoji = requests.utils.quote(emoji)
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{encoded_emoji}/@me"
    api_request("PUT", url, token)

class BotInstance:
    def __init__(self, token, owner_id, bot_index):
        self.token = token
        self.owner_id = owner_id
        self.bot_index = bot_index
        self.prefix = DEFAULT_PREFIX
        self.start_time = time.time()
        self.my_id = None
        self.ws = None
        self.running = True
        self.spam_tasks = {}
        self.spam_delay = 0.1
        self.active_longspam = {}
        self.active_longspam2 = {}
        self.active_longspam3 = {}
        self.active_mentionspam = {}
        self.active_nc = {}
        self.nc_delay = 0.0
        self.gc_name_tasks = {}
        self.gc_name_content = {}
        self.last_emoji_used = {}
        self.server_name_tasks = {}
        self.fast_nc_stop_evts = {}
        self.fast_nc_threads = {}
        self.target_user_id = None
        self.echo_targets = {}
        self.sudo_users = load_sudo_file()
        self.autoreply_targets = {}
        self.autoreact_emojis = {}
        self.last_heartbeat_sent = 0
        self.gateway_ping = 0
        self.gc_make_stop = {}
        self.gc_make_stats = {}
        self.current_streaming = None

    def get_my_id(self):
        if self.my_id is None:
            info = get_bot_info(self.token)
            if info:
                self.my_id = int(info["id"])
        return self.my_id

    def send(self, channel_id, content, reply_to=None):
        return send_message(channel_id, self.token, content, reply_to)

    def is_authorized(self, author_id_int):
        with allowed_lock:
            if author_id_int in allowed_ids:
                return True
        if str(author_id_int) in self.sudo_users:
            return True
        return False

    def set_presence(self, act_type, name, url=None):
        if not self.ws:
            return False
        activity = {"name": name, "type": act_type}
        if act_type == 1:
            activity["url"] = url or "https://twitch.tv/dark"
        payload = {
            "op": 3,
            "d": {
                "since": 0,
                "activities": [activity],
                "status": "online",
                "afk": False
            }
        }
        try:
            self.ws.send(json.dumps(payload))
            return True
        except Exception as e:
            print(f"[Bot {self.bot_index}] presence error: {e}")
            return False

    def clear_presence(self):
        if not self.ws:
            return False
        payload = {"op": 3, "d": {"since": 0, "activities": [], "status": "online", "afk": False}}
        try:
            self.ws.send(json.dumps(payload))
            return True
        except:
            return False
def make_help(prefix, page=1):
    p = prefix
    if page == 1:
        return (
            "```ansi\n"
            "\u001b[1;31m╔══════════════════════════════════════════════╗\u001b[0m\n"
            "\u001b[1;33m║\u001b[0m   \u001b[1;35m🌈 DIRECTOR SELFBOT V19\u001b[0m  \u001b[1;36m⚡ GODMODE ⚡\u001b[0m   \u001b[1;33m║\u001b[0m\n"
            "\u001b[1;31m╚══════════════════════════════════════════════╝\u001b[0m\n"
            "```\n"
            "> 🎯 **GC NAMES (NC)**\n"
            f"```\n"
            f" {p}nc              {p}lightningnc     {p}heartnc\n"
            f" {p}kengnc          {p}timenc          {p}animalnc\n"
            f" {p}gothicnc        {p}cosmicnc        {p}vipernc\n"
            f" {p}demonnc         {p}oceannc         {p}frostnc\n"
            f" {p}cybernc         {p}toxicnc         {p}royalnc\n"
            f" {p}voodoonc        {p}undeadnc        {p}ninjanc\n"
            f" {p}samurainc       {p}arcadenc        {p}shadownc\n"
            f" {p}hazardnc        {p}matrixnc        {p}phantomnc\n"
            f" {p}galaxync        {p}valiantnc       {p}glitchnc\n"
            f" {p}infernonc       {p}dynastync       {p}rebelnc\n"
            f" {p}allnc <txt>     {p}customnc <txt>\n"
            f" {p}gcnc <txt>      {p}gcncstop\n"
            f" {p}servernc <txt>  {p}serverncstop\n"
            f" {p}fastnc <txt>    {p}fastncstop\n"
            f" {p}stopnc         {p}delaync <s>\n"
            "```\n"
            "> 💥 **SPAM**\n"
            f"```\n"
            f" {p}longspam <user>       {p}longspamstop\n"
            f" {p}longspam2 <user>      {p}longspam2stop   💀 SLAVE\n"
            f" {p}longspam3 <user>      {p}longspam3stop   🌷 VIP\n"
            f" {p}mentionspam <user>    {p}mentionspamstop\n"
            f" {p}dualspam <user>       {p}dualspamstop\n"
            f" {p}spam <txt>            {p}stopspam\n"
            f" {p}stopall\n"
            "```\n"
            "> 🎥 **ACTIVITY**\n"
            f"```\n"
            f" {p}streaming <txt> | <url>   {p}playing <txt>\n"
            f" {p}watching <txt>            {p}listening <txt>\n"
            f" {p}competing <txt>           {p}clearactivity\n"
            "```\n"
            "> 💀 **GC MAKER + FRIEND REQ**\n"
            f"```\n"
            f" {p}gcmake <n> <name> @users   {p}stopgc\n"
            f" {p}gcmake @user (unlimited)\n"
            f" {p}sendfr @user              {p}acceptfr @user\n"
            "```\n"
            f"📖 **Page 1/2** ─ Type `{p}help2` for next ➡️"
        )
    else:
        return (
            "```ansi\n"
            "\u001b[1;36m╔══════════════════════════════════════════════╗\u001b[0m\n"
            "\u001b[1;33m║\u001b[0m   \u001b[1;35m🎮 FUN & UTILITY COMMANDS\u001b[0m  \u001b[1;32m✨ V19\u001b[0m   \u001b[1;33m║\u001b[0m\n"
            "\u001b[1;36m╚══════════════════════════════════════════════╝\u001b[0m\n"
            "```\n"
            "> 🤖 **AUTOREPLY**\n"
            f"```\n"
            f" {p}autoreply @user        {p}removeautoreply @user\n"
            f" {p}stopautoreply         {p}showautoreply\n"
            "```\n"
            "> 📨 **FUN**\n"
            f"```\n"
            f" {p}dog       {p}cat       {p}meme\n"
            f" {p}joke      {p}darkjoke  {p}fact\n"
            f" {p}quote     {p}avatar @user\n"
            "```\n"
            "> 🚪 **LEAVE / DESTROY**\n"
            f"```\n"
            f" {p}leave / {p}gcleft / {p}disband    → Leave GC/Server\n"
            f" {p}gcleftall                        → Leave ALL GCs\n"
            f" {p}gameover / {p}go                 → 💀 GAME OVER 💀\n"
            f" {p}autoreact <emoji>                {p}stopautoreact\n"
            "```\n"
            "> ⚙️ **SYSTEM**\n"
            f"```\n"
            f" {p}ping          {p}uptime         {p}status\n"
            f" {p}shutdown      {p}changeprefix <new>\n"
            f" {p}delay <s>     {p}delaync <s>\n"
            f" {p}target @user  {p}stoptarget\n"
            f" {p}echo on @user {p}echo off\n"
            "```\n"
            "> 👑 **ACCESS CONTROL**\n"
            f"```\n"
            f" {p}access @user         {p}unaccess @user\n"
            f" {p}cokeng @user         {p}removecokeng @user\n"
            "```\n"
            f"📖 **Page 2/2** ─ Type `{p}help` for previous ⬅️"
        )
def handle_command(bot, msg):
    channel_id = msg["channel_id"]
    author_id = int(msg["author"]["id"])
    content = msg.get("content", "").strip()
    message_id = msg["id"]
    guild_id = msg.get("guild_id")

    if author_id in bot.echo_targets:
        if content and not msg["author"].get("bot", False):
            try:
                bot.send(channel_id, content)
            except:
                pass

    if not content.startswith(bot.prefix):
        return
    if not bot.is_authorized(author_id):
        bot.send(channel_id, "𝐌𝐆 𝐒𝐁 𝐔𝐒𝐄 𝐊𝐑𝐄𝐆𝐀 𝐁𝐄𝐓𝐈𝐂𝐇𝐎𝐃 𝐆𝐔𝐋𝐀𝐌 🤣", reply_to=message_id)
        return
    cmd_part = content[len(bot.prefix):].strip()
    cmd_lower = cmd_part.lower()
    def reply(text):
        bot.send(channel_id, text, reply_to=message_id)

    # ══════════ HELP ══════════
    if cmd_lower in ("help", "help1"):
        reply(make_help(bot.prefix, 1))
        return
    if cmd_lower == "help2":
        reply(make_help(bot.prefix, 2))
        return

    # ══════════ PING ══════════
    if cmd_lower == "ping":
        api_start = time.time()
        api_request("GET", "https://discord.com/api/v9/users/@me", bot.token)
        api_ping = round((time.time() - api_start) * 1000, 2)
        gateway_ping = bot.gateway_ping if bot.gateway_ping > 0 else "N/A"
        msg_start = time.time()
        sent = send_message(channel_id, bot.token, "🏓 Pinging...")
        msg_ping = round((time.time() - msg_start) * 1000, 2)

        def quality(ms):
            if ms == "N/A": return "❔"
            try: ms = float(ms)
            except: return "❔"
            if ms < 100: return "🟢"
            if ms < 250: return "🟡"
            if ms < 500: return "🟠"
            return "🔴"

        def bar(ms):
            if ms == "N/A": return "▱▱▱▱▱▱"
            try: ms = float(ms)
            except: return "▱▱▱▱▱▱"
            filled = min(6, max(1, int(ms / 150)))
            return "▰" * filled + "▱" * (6 - filled)

        try:
            avg = (float(api_ping) + (float(gateway_ping) if gateway_ping != "N/A" else float(api_ping))) / 2
        except:
            avg = float(api_ping)
        if avg < 150: verdict = "⚡ EXCELLENT"
        elif avg < 300: verdict = "✅ GOOD"
        elif avg < 500: verdict = "⚠️ OKAY"
        else: verdict = "🐢 SLOW"

        try:
            if sent and sent.get("id"):
                api_request("DELETE", f"https://discord.com/api/v9/channels/{channel_id}/messages/{sent['id']}", bot.token)
        except: pass

        ping_text = (
            "```\n"
            "╔════════════════════════════════════╗\n"
            "║         🏓  DIRECTOR PING  🏓          ║\n"
            "╠════════════════════════════════════╣\n"
            f"║ {quality(api_ping)} API      {bar(api_ping)} {str(api_ping).rjust(7)}ms ║\n"
            f"║ {quality(gateway_ping)} Gateway  {bar(gateway_ping)} {str(gateway_ping).rjust(7)}ms ║\n"
            f"║ {quality(msg_ping)} Message  {bar(msg_ping)} {str(msg_ping).rjust(7)}ms ║\n"
            "╠════════════════════════════════════╣\n"
            f"║ 📊 Status  : {verdict.ljust(20)} ║\n"
            f"║ 🤖 Bot #{bot.bot_index} │ 🕐 {datetime.now(IST).strftime('%H:%M:%S')}           ║\n"
            "╚════════════════════════════════════╝\n"
            "```"
        )
        reply(ping_text)
        return

    # ══════════ AUTOREPLY ══════════
    if cmd_lower.startswith("autoreply "):
        parts = cmd_part.split()
        if len(parts) < 2:
            reply("❌ Usage: !autoreply @user1 @user2 ...")
            return
        user_ids = []
        for mention in parts[1:]:
            uid = extract_user_id_from_mention(mention)
            if uid:
                user_ids.append(uid)
        if not user_ids:
            reply("❌ No valid user mentions")
            return
        if channel_id not in bot.autoreply_targets:
            bot.autoreply_targets[channel_id] = []
        for uid in user_ids:
            if uid not in bot.autoreply_targets[channel_id]:
                bot.autoreply_targets[channel_id].append(uid)
        reply(f"✅ Autoreply targets added: {len(user_ids)} user(s)")
        return

    if cmd_lower.startswith("removeautoreply "):
        parts = cmd_part.split()
        if len(parts) < 2:
            reply("❌ Usage: !removeautoreply @user")
            return
        uid = extract_user_id_from_mention(parts[1])
        if not uid:
            reply("❌ Invalid mention")
            return
        if channel_id in bot.autoreply_targets and uid in bot.autoreply_targets[channel_id]:
            bot.autoreply_targets[channel_id].remove(uid)
            if not bot.autoreply_targets[channel_id]:
                del bot.autoreply_targets[channel_id]
            reply("✅ Removed")
        else:
            reply("ℹ️ Not in list")
        return

    if cmd_lower == "stopautoreply":
        if channel_id in bot.autoreply_targets:
            del bot.autoreply_targets[channel_id]
            reply("✅ Cleared all autoreply targets")
        else:
            reply("ℹ️ No active autoreply targets")
        return

    if cmd_lower == "showautoreply":
        if channel_id in bot.autoreply_targets and bot.autoreply_targets[channel_id]:
            users = ", ".join([f"<@{uid}>" for uid in bot.autoreply_targets[channel_id]])
            reply(f"📋 **Targets:** {users}")
        else:
            reply("ℹ️ No autoreply targets")
        return

    # ══════════ FUN ══════════
    if cmd_lower == "dog":
        try:
            resp = api_request("GET", "https://dog.ceo/api/breeds/image/random", bot.token)
            if resp and resp.status_code == 200:
                reply(resp.json().get("message", "🐶 Woof!"))
            else:
                reply("🐶 Could not fetch dog image.")
        except:
            reply("🐶 Could not fetch dog image.")
        return

    if cmd_lower == "cat":
        reply("https://cataas.com/cat")
        return

    if cmd_lower == "meme":
        meme_gifs = [
            "https://media.giphy.com/media/3o6Zt6LgVK6MZ0Kt3m/giphy.gif",
            "https://media.giphy.com/media/LmNwrBhejkK9EFP504/giphy.gif",
            "https://media.giphy.com/media/3o7btPCcdNniyf0ArS/giphy.gif",
        ]
        reply(random.choice(meme_gifs))
        return

    if cmd_lower == "joke":
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything.",
            "What do you call a fish with no eyes? A fsh.",
            "I'm reading a book on anti-gravity. It's impossible to put down.",
        ]
        reply(f"😂 {random.choice(jokes)}")
        return

    if cmd_lower == "darkjoke":
        dark_jokes = [
            "What's the difference between a pizza and a Jew? A pizza doesn't scream when you put it in the oven.",
            "My girlfriend's gone to the West Indies... Jamaica? No, she wanted to.",
            "What's red and bad for your teeth? A brick.",
        ]
        reply(f"🖤 **Dark Humor:** {random.choice(dark_jokes)}")
        return

    if cmd_lower == "fact":
        facts = [
            "Octopuses have three hearts.",
            "Honey never spoils.",
            "Bananas are berries, but strawberries aren't.",
        ]
        reply(f"📚 {random.choice(facts)}")
        return

    if cmd_lower == "quote":
        quotes = [
            "The only way to do great work is to love what you do.",
            "In the middle of difficulty lies opportunity.",
            "Success is not final, failure is not fatal.",
        ]
        reply(f"📝 {random.choice(quotes)}")
        return

    if cmd_lower.startswith("avatar "):
        parts = cmd_part.split()
        if len(parts) < 2:
            reply("❌ Usage: !avatar @user")
            return
        user_id = extract_user_id_from_mention(parts[1])
        if not user_id:
            reply("❌ Invalid user mention.")
            return
        resp = api_request("GET", f"https://discord.com/api/v9/users/{user_id}", bot.token)
        if resp and resp.status_code == 200:
            data = resp.json()
            avatar_hash = data.get('avatar')
            if avatar_hash:
                avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png"
            else:
                avatar_url = "https://cdn.discordapp.com/embed/avatars/0.png"
            reply(avatar_url)
        else:
            reply("❌ Could not fetch avatar.")
        return

    # ══════════ LEAVE / GCLEFT / DISBAND ══════════
    if cmd_lower in ("leave", "gcleft", "disband"):
        goodbye_msg = "𝘾𝙃𝙐𝘿𝘼𝙄 𝘿𝙊𝙉𝙀 𝙃𝙊𝙂𝙔𝙄 𝙈𝘼𝙇𝙄𝙆 𝘼𝘽 𝙈𝙀 𝙅𝘼𝙍𝘼 𝙃𝙐 🤣💋✌🏼"
        try:
            reply(goodbye_msg)
        except: pass
        time.sleep(0.5)
        my_id = bot.get_my_id()
        if not my_id:
            info = get_bot_info(bot.token)
            if info:
                my_id = int(info["id"])
                bot.my_id = my_id
        if not my_id:
            print(f"\033[91m[Bot {bot.bot_index}] ❌ Could not fetch own user ID\033[0m")
            return
        if guild_id:
            url = f"https://discord.com/api/v9/guilds/{guild_id}/members/@me"
            resp = api_request("DELETE", url, bot.token)
            if resp and resp.status_code in (200, 204):
                print(f"\033[92m[Bot {bot.bot_index}] ✅ Left server {guild_id}\033[0m")
            else:
                code = resp.status_code if resp else "NO-RESP"
                print(f"\033[91m[Bot {bot.bot_index}] ❌ Server leave failed ({code})\033[0m")
            return
        url = f"https://discord.com/api/v9/channels/{channel_id}/recipients/{my_id}"
        resp = api_request("DELETE", url, bot.token)
        if resp and resp.status_code in (200, 204):
            print(f"\033[92m[Bot {bot.bot_index}] ✅ Left GC {channel_id}\033[0m")
        else:
            code = resp.status_code if resp else "NO-RESP"
            print(f"\033[91m[Bot {bot.bot_index}] ❌ GC leave failed ({code})\033[0m")
            try:
                fb = api_request("DELETE", f"https://discord.com/api/v9/channels/{channel_id}", bot.token)
                if fb and fb.status_code in (200, 204):
                    print(f"\033[92m[Bot {bot.bot_index}] ✅ GC closed (fallback)\033[0m")
            except: pass
        return

    # ══════════ GCLEFTALL ══════════
    if cmd_lower == "gcleftall":
        try:
            resp = api_request("GET", "https://discord.com/api/v9/users/@me/channels", bot.token)
            if not resp or resp.status_code != 200:
                reply("❌ Could not fetch channels.")
                return
            my_id = bot.get_my_id()
            groups = [c for c in resp.json() if c.get("type") == 3]
            reply(f"🚪 Leaving {len(groups)} GCs...")
            left = 0
            for c in groups:
                r = api_request("DELETE", f"https://discord.com/api/v9/channels/{c['id']}/recipients/{my_id}", bot.token)
                if r and r.status_code in (200, 204):
                    left += 1
                time.sleep(0.5)
            reply(f"✅ Left {left}/{len(groups)} GCs.")
        except Exception as e:
            reply(f"❌ Error: {e}")
        return

    # ══════════ GAMEOVER ══════════
    if cmd_lower in ("gameover", "go"):
        gameover_text = "```\n╔═══════════════════════════════╗\n║       💀 GAME OVER 💀         ║\n╚═══════════════════════════════╝\n```"
        reply(gameover_text)
        time.sleep(0.4)
        reply(GAMEOVER_GIF)
        return

    # ══════════ AUTOREACT ══════════
    if cmd_lower.startswith("autoreact "):
        parts = cmd_part.split()
        if len(parts) < 2:
            reply("❌ Usage: !autoreact <emoji>")
            return
        bot.autoreact_emojis[channel_id] = parts[1]
        reply(f"✅ Autoreact set to {parts[1]}")
        return

    if cmd_lower == "stopautoreact":
        if channel_id in bot.autoreact_emojis:
            del bot.autoreact_emojis[channel_id]
            reply("✅ Stopped auto-react")
        else:
            reply("ℹ️ No active auto-react")
        return

    # ══════════ SYSTEM ══════════
    if cmd_lower == "uptime":
        u = time.time() - bot.start_time
        d,r = divmod(int(u), 86400)
        h,r = divmod(r, 3600)
        m,s = divmod(r, 60)
        reply(f"⏱️ Uptime: **{d}d {h}h {m}m {s}s**")
        return

    if cmd_lower == "status":
        autoreply_count = len(bot.autoreply_targets.get(channel_id, []))
        reply(
            f"```\n"
            f"╔══════ DIRECTOR V19 STATUS ══════╗\n"
            f" UPTIME : {round(time.time()-bot.start_time,1)}s\n"
            f" SPAM DELAY : {bot.spam_delay}s\n"
            f" NC DELAY : {bot.nc_delay}s\n"
            f" PREFIX : {bot.prefix}\n"
            f" GATEWAY PING : {bot.gateway_ping}ms\n"
            f" TARGET : {bot.target_user_id if bot.target_user_id else 'None'}\n"
            f" AUTOREPLY : {autoreply_count} user(s)\n"
            f"╚════════════════════════════════╝\n"
            f"```"
        )
        return

    if cmd_lower == "shutdown":
        reply("Shutting down...")
        bot.running = False
        if bot.ws: bot.ws.close()
        return

    if cmd_lower.startswith("changeprefix "):
        bot.prefix = cmd_part.split(maxsplit=1)[1].strip()
        reply(f"Prefix changed to `{bot.prefix}`")
        return

    if cmd_lower.startswith("delay "):
        try:
            bot.spam_delay = max(0.0, float(cmd_part.split()[1]))
            reply(f"Global delay set to **{bot.spam_delay}s**")
        except: pass
        return

    if cmd_lower.startswith("delaync "):
        try:
            bot.nc_delay = max(0.0, float(cmd_part.split()[1]))
            reply(f"NC delay set to **{bot.nc_delay}s**")
        except: pass
        return

    if cmd_lower.startswith("target "):
        m = re.search(r"<@!?(\d+)>", cmd_part)
        if m:
            bot.target_user_id = m.group(1)
            reply(f"🎯 Target locked: `<@{bot.target_user_id}>`")
        return

    if cmd_lower == "stoptarget":
        bot.target_user_id = None
        reply("Target cleared.")
        return

    if cmd_lower.startswith("echo "):
        parts = cmd_part.split()
        if len(parts) < 2:
            reply("❌ Usage: `!echo on @user` or `!echo off`")
            return
        mode = parts[1].lower()
        if mode == "on":
            m = re.search(r"<@!?(\d+)>", cmd_part)
            if not m and len(parts) > 2 and parts[2].isdigit():
                uid = int(parts[2])
            elif m:
                uid = int(m.group(1))
            else:
                reply("❌ Mention a user: `!echo on @user`")
                return
            bot.echo_targets[uid] = True
            reply(f"✅ Echo ON for <@{uid}>")
        elif mode == "off":
            bot.echo_targets.clear()
            reply("✅ Echo OFF.")
        return

    # ══════════ ACCESS ══════════
    if cmd_lower.startswith("access "):
        if author_id not in (bot.owner_id, PERMANENT_OWNER):
            reply("Only the owner can grant access."); return
        raw = cmd_part[7:].strip()
        m = re.search(r"<@!?(\d+)>", raw)
        tid = int(m.group(1)) if m else (int(raw) if raw.isdigit() else None)
        if tid is None: reply("❌ Invalid user."); return
        with allowed_lock:
            if tid in allowed_ids:
                reply(f"<@{tid}> **already an sudo**")
            else:
                allowed_ids.add(tid); save_allowed_ids()
                reply(f"**Le bsdk** <@{tid}>")
        return

    if cmd_lower.startswith("unaccess "):
        if author_id not in (bot.owner_id, PERMANENT_OWNER):
            reply("Only the owner can remove access."); return
        raw = cmd_part[9:].strip()
        m = re.search(r"<@!?(\d+)>", raw)
        tid = int(m.group(1)) if m else (int(raw) if raw.isdigit() else None)
        if tid is None: reply("Invalid user."); return
        if tid == PERMANENT_OWNER: reply("Cannot remove permanent owner."); return
        with allowed_lock:
            if tid in allowed_ids:
                allowed_ids.discard(tid); save_allowed_ids()
                reply(f"Access removed from <@{tid}>")
            else:
                reply("That user has no access.")
        return

    if cmd_lower.startswith("cokeng "):
        raw = cmd_part[7:].strip()
        m = re.search(r"<@!?(\d+)>", raw)
        tid = m.group(1) if m else (raw if raw.isdigit() else None)
        if tid and tid not in bot.sudo_users:
            bot.sudo_users.append(tid)
            save_sudo_file(bot.sudo_users)
            with allowed_lock:
                allowed_ids.add(int(tid)); save_allowed_ids()
            reply(f"**CO KENG ADDED <@{tid}>**")
        return

    if cmd_lower.startswith("removecokeng "):
        raw = cmd_part[13:].strip()
        m = re.search(r"<@!?(\d+)>", raw)
        tid = m.group(1) if m else (raw if raw.isdigit() else None)
        if tid and tid in bot.sudo_users:
            bot.sudo_users.remove(tid)
            save_sudo_file(bot.sudo_users)
            reply(f"**CO-KENG REMOVED: <@{tid}>**")
        return

    # ══════════ NC COMMANDS ══════════
    nc_map = {
        "nc":"base","lightningnc":"lightning","heartnc":"heart","kengnc":"keng",
        "timenc":"TIME","animalnc":"animal","gothicnc":"gothic","cosmicnc":"cosmic",
        "vipernc":"viper","demonnc":"demon","oceannc":"ocean","frostnc":"frost",
        "cybernc":"cyber","toxicnc":"toxic","royalnc":"royal","voodoonc":"voodoo",
        "undeadnc":"undead","ninjanc":"ninja","samurainc":"samurai","arcadenc":"arcade",
        "shadownc":"shadow","hazardnc":"hazard","matrixnc":"matrix","phantomnc":"phantom",
        "galaxync":"galaxy","valiantnc":"valiant","glitchnc":"glitch","infernonc":"inferno",
        "dynastync":"dynasty","rebelnc":"rebel","allnc":"ALL","customnc":"CUSTOM","slownc":"SLOW",
    }
    matched_nc_key = None
    for cmd_key, pool_key in nc_map.items():
        if cmd_lower == cmd_key or cmd_lower.startswith(cmd_key + " "):
            matched_nc_key = pool_key
            text_part = cmd_part[len(cmd_key):].strip()
            break
    if matched_nc_key is not None:
        bot.active_nc[channel_id] = True
        threading.Thread(target=nc_worker, args=(bot, channel_id, matched_nc_key, text_part), daemon=True).start()
        reply(f"✅ NC started [{matched_nc_key}]")
        return

    if cmd_lower == "stopnc":
        bot.active_nc[channel_id] = False
        reply("NC stopped.")
        return

    if cmd_lower.startswith("fastnc") and (cmd_lower == "fastnc" or cmd_lower.startswith("fastnc ")):
        text = cmd_part[6:].strip()
        if channel_id in bot.fast_nc_stop_evts:
            bot.fast_nc_stop_evts[channel_id].set()
        threading.Thread(target=fast_nc_worker, args=(bot, channel_id, text, 5), daemon=True).start()
        reply("⚡ FAST NC started — 5 threads!")
        return

    if cmd_lower == "fastncstop":
        ev = bot.fast_nc_stop_evts.get(channel_id)
        if ev: ev.set()
        reply("⚡ FAST NC stopped.")
        return

    if cmd_lower.startswith("gcnc "):
        text = cmd_part[5:]
        if channel_id in bot.gc_name_tasks:
            bot.gc_name_tasks[channel_id] = None
        bot.gc_name_content[channel_id] = text
        t = threading.Thread(target=gc_nc_matrix_worker, args=(bot, channel_id, text), daemon=True)
        bot.gc_name_tasks[channel_id] = t
        t.start()
        reply("✅ GC name changer started.")
        return

    if cmd_lower == "gcncstop":
        bot.gc_name_tasks.pop(channel_id, None)
        bot.gc_name_content.pop(channel_id, None)
        bot.last_emoji_used.pop(channel_id, None)
        reply("✅ GC NC stopped.")
        return

    if cmd_lower.startswith("servernc "):
        text = cmd_part[9:]
        resp = api_request("GET", f"https://discord.com/api/v9/channels/{channel_id}", bot.token)
        if resp and resp.status_code == 200:
            gid = resp.json().get("guild_id")
            if gid:
                if gid in bot.server_name_tasks:
                    bot.server_name_tasks[gid] = None
                t = threading.Thread(target=server_nc_worker, args=(bot, gid, text), daemon=True)
                bot.server_name_tasks[gid] = t
                t.start()
                reply("✅ Server NC started.")
            else:
                reply("Not a server channel.")
        return

    if cmd_lower == "serverncstop":
        resp = api_request("GET", f"https://discord.com/api/v9/channels/{channel_id}", bot.token)
        if resp and resp.status_code == 200:
            gid = resp.json().get("guild_id")
            if gid and gid in bot.server_name_tasks:
                bot.server_name_tasks.pop(gid, None)
                reply("✅ Server NC stopped.")
            else:
                reply("No active server NC.")
        return

    # ══════════ SPAM ══════════
    if cmd_lower.startswith("longspam "):
        raw = cmd_part[9:].strip()
        m = re.search(r"<@!?(\d+)>", raw)
        if m:
            mention = f"<@{m.group(1)}>"
        else:
            mention = raw if raw else "@everyone"
        ev = bot.active_longspam.get(channel_id)
        if ev: ev.set()
        stop_ev = threading.Event()
        bot.active_longspam[channel_id] = stop_ev
        threading.Thread(target=long_spam_worker, args=(bot, channel_id, mention, stop_ev), daemon=True).start()
        reply(f"💬 Long spam started on {mention}")
        return

    if cmd_lower == "longspamstop":
        ev = bot.active_longspam.get(channel_id)
        if ev: ev.set()
        reply("💬 Long spam stopped.")
        return

    if cmd_lower.startswith("longspam2 "):
        raw = cmd_part[10:].strip()
        m = re.search(r"<@!?(\d+)>", raw)
        if m:
            mention = f"<@{m.group(1)}>"
        else:
            mention = raw if raw else "@everyone"
        ev = bot.active_longspam2.get(channel_id)
        if ev: ev.set()
        stop_ev = threading.Event()
        bot.active_longspam2[channel_id] = stop_ev
        threading.Thread(target=long_spam2_worker, args=(bot, channel_id, mention, stop_ev), daemon=True).start()
        reply(f"💀 LONGSPAM2 started on {mention}")
        return

    if cmd_lower == "longspam2stop":
        ev = bot.active_longspam2.get(channel_id)
        if ev: ev.set()
        reply("💀 LONGSPAM2 stopped.")
        return
        
        # ══════════ LONGSPAM3 ══════════
    if cmd_lower.startswith("longspam3 "):
        raw = cmd_part[10:].strip()
        m = re.search(r"<@!?(\d+)>", raw)
        if m:
            target_name = m.group(1)
        else:
            target_name = raw if raw else "everyone"
        ev = bot.active_longspam3.get(channel_id)
        if ev: ev.set()
        stop_ev = threading.Event()
        bot.active_longspam3[channel_id] = stop_ev
        threading.Thread(
            target=long_spam3_worker,
            args=(bot, channel_id, target_name, stop_ev),
            daemon=True
        ).start()
        reply(f"🌷 LONGSPAM3 started — target: **{target_name}**")
        return

    if cmd_lower == "longspam3stop":
        ev = bot.active_longspam3.get(channel_id)
        if ev: ev.set()
        reply("🌷 LONGSPAM3 stopped.")
        return


    if cmd_lower.startswith("mentionspam "):
        raw = cmd_part[12:].strip()
        m = re.search(r"<@!?(\d+)>", raw)
        if not m:
            reply("Usage: mentionspam <user>")
            return
        mention = f"<@{m.group(1)}>"
        ev = bot.active_mentionspam.get(channel_id)
        if ev: ev.set()
        stop_ev = threading.Event()
        bot.active_mentionspam[channel_id] = stop_ev
        threading.Thread(target=mention_spam_worker, args=(bot, channel_id, mention, stop_ev), daemon=True).start()
        reply(f"🔔 Mention spam started on {mention}!")
        return

    if cmd_lower == "mentionspamstop":
        ev = bot.active_mentionspam.get(channel_id)
        if ev: ev.set()
        reply("🔔 Mention spam stopped.")
        return

    if cmd_lower.startswith("dualspam "):
        raw = cmd_part[9:].strip()
        m = re.search(r"<@!?(\d+)>", raw)
        if not m:
            reply("Usage: dualspam <user>")
            return
        mention = f"<@{m.group(1)}>"
        for ev in [bot.active_mentionspam.get(channel_id), bot.active_longspam.get(channel_id)]:
            if ev: ev.set()
        ms_ev = threading.Event()
        ls_ev = threading.Event()
        bot.active_mentionspam[channel_id] = ms_ev
        bot.active_longspam[channel_id] = ls_ev
        threading.Thread(target=mention_spam_worker, args=(bot, channel_id, mention, ms_ev), daemon=True).start()
        threading.Thread(target=long_spam_worker, args=(bot, channel_id, mention, ls_ev), daemon=True).start()
        reply(f"💥 DUAL SPAM started on {mention}!")
        return

    if cmd_lower == "dualspamstop":
        for ev in [bot.active_mentionspam.get(channel_id), bot.active_longspam.get(channel_id)]:
            if ev: ev.set()
        reply("💥 DUAL SPAM stopped.")
        return

    if cmd_lower.startswith("spam "):
        text = cmd_part[5:]
        if channel_id in bot.spam_tasks:
            bot.spam_tasks[channel_id] = None
        t = threading.Thread(target=spam_worker_matrix, args=(bot, channel_id, text), daemon=True)
        bot.spam_tasks[channel_id] = t
        t.start()
        reply("✅ Spam started.")
        return

    if cmd_lower == "stopspam":
        bot.spam_tasks.pop(channel_id, None)
        reply("✅ Spam stopped.")
        return

    # ══════════ STREAMING / PRESENCE ══════════
    if cmd_lower.startswith("streaming "):
        raw = cmd_part[10:].strip()
        if "|" in raw:
            parts = raw.split("|", 1)
            text = parts[0].strip()
            url = parts[1].strip()
        else:
            parts = raw.split()
            if not parts:
                reply("❌ Usage: `!streaming <text> | <twitch_url>`")
                return
            text = raw
            url = "https://twitch.tv/dark"
        if not url.startswith("https://twitch.tv/"):
            reply("❌ URL must be a twitch.tv link (Discord requires it for streaming).")
            return
        if bot.set_presence(1, text, url):
            bot.current_streaming = (text, url)
            reply(f"🎥 Now streaming: **{text}**\n🔗 {url}")
        else:
            reply("❌ Failed to set streaming status.")
        return

    if cmd_lower.startswith("playing "):
        text = cmd_part[8:].strip()
        if bot.set_presence(0, text):
            reply(f"🎮 Now playing: **{text}**")
        else:
            reply("❌ Failed.")
        return

    if cmd_lower.startswith("watching "):
        text = cmd_part[9:].strip()
        if bot.set_presence(3, text):
            reply(f"📺 Now watching: **{text}**")
        else:
            reply("❌ Failed.")
        return

    if cmd_lower.startswith("listening "):
        text = cmd_part[10:].strip()
        if bot.set_presence(2, text):
            reply(f"🎧 Now listening to: **{text}**")
        else:
            reply("❌ Failed.")
        return

    if cmd_lower.startswith("competing "):
        text = cmd_part[10:].strip()
        if bot.set_presence(5, text):
            reply(f"🏆 Now competing in: **{text}**")
        else:
            reply("❌ Failed.")
        return

    if cmd_lower in ("clearactivity", "clearstream", "stopstream"):
        if bot.clear_presence():
            bot.current_streaming = None
            reply("✅ Activity cleared.")
        else:
            reply("❌ Failed.")
        return

    if cmd_lower == "stopall":
        bot.spam_tasks.pop(channel_id, None)
        bot.active_nc[channel_id] = False
        ev = bot.active_longspam.get(channel_id)
        if ev: ev.set()
        ev = bot.active_longspam2.get(channel_id)
        if ev: ev.set()
        ev = bot.active_longspam3.get(channel_id)
        if ev: ev.set()
        ev = bot.active_mentionspam.get(channel_id)
        if ev: ev.set()
        ev = bot.fast_nc_stop_evts.get(channel_id)
        if ev: ev.set()
        bot.gc_name_tasks.pop(channel_id, None)
        if channel_id in bot.autoreply_targets:
            del bot.autoreply_targets[channel_id]
        reply("⛔ ALL COMMANDS STOPPED.")
        return

    # ═══════════════════════════════════════════════════════════════
    #              🆕 GC MAKER  (!gcmake  /  !stopgc) — FIXED
    # ═══════════════════════════════════════════════════════════════
    if cmd_lower.startswith("gcmake"):
        parts = cmd_part.split()
        count = 0
        arg_start = 1
        if len(parts) > 1 and parts[1].isdigit():
            count = int(parts[1])
            arg_start = 2

        mentions = re.findall(r"<@!?(\d+)>", cmd_part)
        if not mentions:
            reply("❌ Usage: `!gcmake <n> <name> @users` or `!gcmake @users`")
            return

        name_tokens = []
        for tok in parts[arg_start:]:
            if not re.match(r"<@!?\d+>", tok) and not tok.isdigit():
                name_tokens.append(tok)
        target_name = " ".join(name_tokens).strip()
        if not target_name:
            target_name = "DARK MAFIA"

        unlimited = (count == 0)

        ev = bot.gc_make_stop.get(channel_id)
        if ev: ev.set()
        stop_ev = threading.Event()
        bot.gc_make_stop[channel_id] = stop_ev

        bot.gc_make_stats[channel_id] = {
            "created": 0, "target": count, "unlimited": unlimited,
            "name": target_name, "users": mentions, "start": time.time(),
        }

        def gc_make_worker(b, ch_id, uids, nm, cnt, unlim, stop_ev):
            pattern_idx = 0
            created = 0
            consecutive_fails = 0

            my_id = b.get_my_id()
            uids = [u for u in uids if str(u) != str(my_id)]
            if not uids:
                send_message(ch_id, b.token, "❌ No valid recipients (bot excluded)")
                return

            while not stop_ev.is_set():
                if not unlim and created >= cnt:
                    break

                gc_id, status = create_group_dm(b.token, uids)
                if not gc_id:
                    consecutive_fails += 1
                    print(f"\033[91m[GC MAKER] Fail #{consecutive_fails}: {status}\033[0m")
                    if consecutive_fails >= 5:
                        send_message(ch_id, b.token,
                            f"```\n⛔ GC MAKER STOPPED\nReason: {status}\nCreated: {created}\n```")
                        break
                    time.sleep(2.0)
                    continue

                consecutive_fails = 0

                for uid in uids:
                    add_user_to_group(b.token, gc_id, uid)
                    time.sleep(0.15)

                heart = random.choice(HEART_EMOJIS)
                emoji = random.choice(NC_EMOJIS)
                roast = random.choice(NC_MESSAGES)
                base = f"{nm} {heart} {emoji} {roast}".strip()
                pattern = NC_PATTERNS[pattern_idx % len(NC_PATTERNS)]
                pattern_idx += 1
                if len(base) > 100:
                    base = base[:100]
                elif len(base) < 100:
                    needed = 100 - len(base)
                    base += pattern * (needed // len(pattern)) + pattern[:needed % len(pattern)]

                r = change_gc_name(gc_id, b.token, base)
                if not r or r.status_code != 200:
                    print(f"\033[93m[GC MAKER] Rename failed on GC #{created+1}\033[0m")

                created += 1
                b.gc_make_stats[ch_id]["created"] = created
                print(f"\033[92m[Bot {b.bot_index}] ✅ GC #{created}{'' if unlim else '/'+str(cnt)}\033[0m")

                time.sleep(0.8)

            stats = b.gc_make_stats.get(ch_id, {})
            duration = int(time.time() - stats.get("start", time.time()))
            report = (
                "```\n"
                "╔══════ GC MAKER REPORT ══════╗\n"
                f"  Created : {created}\n"
                f"  Name    : {nm}\n"
                f"  Users   : {len(uids)}\n"
                f"  Time    : {duration}s\n"
                "╚═════════════════════════════╝\n"
                "```"
            )
            send_message(ch_id, b.token, report)

        t = threading.Thread(
            target=gc_make_worker,
            args=(bot, channel_id, mentions, target_name, count, unlimited, stop_ev),
            daemon=True,
        )
        t.start()
        reply(
            f"🔥 **GC MAKER STARTED**\n"
            f"Name: `{target_name}`\n"
            f"Users: {len(mentions)}\n"
            f"Count: {'∞ unlimited' if unlimited else count}\n"
            f"Stop: `{bot.prefix}stopgc`"
        )
        return

    if cmd_lower == "stopgc":
        ev = bot.gc_make_stop.get(channel_id)
        if ev:
            ev.set()
            reply("⛔ GC MAKER STOPPED.")
        else:
            reply("ℹ️ No active GC maker.")
        return

    # ═══════════════════════════════════════════════════════════════
    #           🆕 FRIEND REQUEST — FIXED
    # ═══════════════════════════════════════════════════════════════
    if cmd_lower.startswith("sendfr"):
        m = re.search(r"<@!?(\d+)>", cmd_part)
        if not m:
            reply("❌ Usage: `!sendfr @user`")
            return
        target_uid = m.group(1)

        all_bots = getattr(handle_command, "_all_bots", None) or [bot]
        reply(f"📨 Sending FR to <@{target_uid}> from {len(all_bots)} bot(s)...")

        def fr_worker(bots, uid, ch_id):
            sent = 0; already = 0; failed = 0
            details = []
            for idx, b in enumerate(bots, 1):
                if str(b.get_my_id()) == str(uid):
                    continue
                ok, status = send_friend_request(b.token, uid)
                if ok:
                    sent += 1
                    details.append(f"  Bot {idx}: ✅ sent")
                elif status == 400:
                    already += 1
                    details.append(f"  Bot {idx}: ⚠️ already")
                else:
                    failed += 1
                    details.append(f"  Bot {idx}: ❌ {status}")
                print(f"[SENDFR Bot {idx}] status={status}")
                time.sleep(1.5)
            report = (
                "```\n"
                "╔══════ FR REPORT ══════╗\n"
                f"  Sent    : {sent}\n"
                f"  Already : {already}\n"
                f"  Failed  : {failed}\n"
                "╠═══════════════════════╣\n"
                + "\n".join(details[:10]) +
                "\n╚═══════════════════════╝\n"
                "```"
            )
            send_message(ch_id, bot.token, report)

        threading.Thread(target=fr_worker, args=(all_bots, target_uid, channel_id), daemon=True).start()
        return

    if cmd_lower.startswith("acceptfr"):
        m = re.search(r"<@!?(\d+)>", cmd_part)
        if not m:
            reply("❌ Usage: `!acceptfr @user`")
            return
        target_uid = m.group(1)

        all_bots = getattr(handle_command, "_all_bots", None) or [bot]
        reply(f"📨 Accepting FR from <@{target_uid}> on {len(all_bots)} bot(s)...")

        def accept_worker(bots, uid, ch_id):
            ok_count = 0; no_fr = 0; failed = 0
            details = []
            for idx, b in enumerate(bots, 1):
                ok, status = accept_friend_request(b.token, uid)
                if ok:
                    ok_count += 1
                    details.append(f"  Bot {idx}: ✅ accepted")
                elif status == "no-fr":
                    no_fr += 1
                    details.append(f"  Bot {idx}: ⚠️ no FR")
                else:
                    failed += 1
                    details.append(f"  Bot {idx}: ❌ {status}")
                print(f"[ACCEPTFR Bot {idx}] status={status}")
                time.sleep(1.5)
            report = (
                "```\n"
                "╔══════ ACCEPT FR REPORT ══════╗\n"
                f"  Accepted : {ok_count}\n"
                f"  No FR    : {no_fr}\n"
                f"  Failed   : {failed}\n"
                "╠══════════════════════════════╣\n"
                + "\n".join(details[:10]) +
                "\n╚══════════════════════════════╝\n"
                "```"
            )
            send_message(ch_id, bot.token, report)

        threading.Thread(target=accept_worker, args=(all_bots, target_uid, channel_id), daemon=True).start()
        return


def run_bot(bot):
    print(f"\033[93m[Bot {bot.bot_index}] Starting...\033[0m")
    while bot.running:
        try:
            ws = websocket.WebSocketApp(
                "wss://gateway.discord.gg/?v=9&encoding=json",
                on_open=lambda ws: print(f"\033[92m[Bot {bot.bot_index}] Connected\033[0m"),
                on_message=lambda ws, msg: on_ws_message(ws, msg, bot),
                on_error=lambda ws, err: print(f"[Bot {bot.bot_index}] Error: {err}"),
                on_close=lambda ws, code, txt: print(f"[Bot {bot.bot_index}] Closed: {code}")
            )
            bot.ws = ws
            ws.run_forever()
        except Exception as e:
            print(f"[Bot {bot.bot_index}] Gateway error: {e}")
        if not bot.running:
            break
        print(f"[Bot {bot.bot_index}] Reconnecting in 5s...")
        time.sleep(5)


def on_ws_message(ws, message, bot):
    try:
        data = json.loads(message)
        op = data.get("op")
        t = data.get("t")
        if op == 10:
            interval = data["d"]["heartbeat_interval"] / 1000
            def hb_loop():
                while bot.running:
                    time.sleep(interval)
                    try:
                        if ws.sock and ws.sock.connected:
                            bot.last_heartbeat_sent = time.time()
                            ws.send(json.dumps({"op": 1, "d": None}))
                    except:
                        break
            threading.Thread(target=hb_loop, daemon=True).start()
            ws.send(json.dumps({
                "op": 2,
                "d": {"token": bot.token, "properties": {"$os": "windows", "$browser": "chrome", "$device": "pc"}}
            }))
        elif op == 11:
            if bot.last_heartbeat_sent > 0:
                bot.gateway_ping = round((time.time() - bot.last_heartbeat_sent) * 1000, 2)
        elif t == "READY":
            user = data["d"]["user"]
            bot.my_id = int(user["id"])
            print(f"\033[92m[Bot {bot.bot_index}] Ready as {user['username']} (ID: {bot.my_id})\033[0m")
            if getattr(bot, "current_streaming", None):
                text, url = bot.current_streaming
                time.sleep(1.5)
                if bot.set_presence(1, text, url):
                    print(f"\033[92m[Bot {bot.bot_index}] ♻️ Streaming re-applied: {text}\033[0m")
        elif op == 9:
            print(f"\033[91m[Bot {bot.bot_index}] Invalid session\033[0m")
            bot.running = False
            ws.close()
        elif t == "MESSAGE_CREATE":
            msg = data["d"]
            author_id = int(msg["author"]["id"])
            channel_id = msg["channel_id"]
            content = msg.get("content", "")
            message_id = msg["id"]

            if channel_id in bot.autoreply_targets:
                if str(author_id) in bot.autoreply_targets[channel_id]:
                    if bot.my_id and author_id != bot.my_id:
                        if not msg["author"].get("bot", False):
                            reply_text = random.choice(AUTOREPLY_REPLY_TEXTS)
                            try:
                                send_message(channel_id, bot.token, reply_text, reply_to=message_id)
                            except: pass

            if channel_id in bot.autoreact_emojis:
                if bot.my_id and author_id != bot.my_id:
                    if not msg["author"].get("bot", False):
                        try:
                            emoji = bot.autoreact_emojis[channel_id]
                            add_reaction(channel_id, message_id, emoji, bot.token)
                        except: pass

            if author_id in bot.echo_targets:
                if content and not msg["author"].get("bot", False):
                    try:
                        bot.send(channel_id, content)
                    except: pass
            handle_command(bot, msg)
    except Exception as e:
        print(f"[Bot {bot.bot_index}] WS error: {e}")


def print_rainbow_banner():
    director = [
        "██████╗ ██╗██████╗ ███████╗ ██████╗████████╗ ██████╗ ██████╗ ",
        "██╔══██╗██║██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗",
        "██║  ██║██║██████╔╝█████╗  ██║        ██║   ██║   ██║██████╔╝",
        "██║  ██║██║██╔══██╗██╔══╝  ██║        ██║   ██║   ██║██╔══██╗",
        "██████╔╝██║██║  ██║███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║",
        "╚═════╝ ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝",
    ]
    offset = 0
    for line in director:
        print(rainbow_line(line, offset))
        offset += 4
    print("")
    print(rainbow_line("           V19  🌈  G O D M O D E  🌈  EDITION", 8))
    print(rainbow_line("       ⚡ The Ultimate Speed – Never Stops ⚡", 12))
    print(rainbow_line("=" * 60, 20))
    print("")


def main():
    sys.stdout.reconfigure(line_buffering=True)
    print_rainbow_banner()
    load_allowed_ids()

    ALL_BOTS = [BotInstance(tok, PERMANENT_OWNER, i+1) for i, tok in enumerate(BOT_TOKENS) if tok and tok.strip()]
    handle_command._all_bots = ALL_BOTS
    print(f"\033[93m[+] Owner ID: {PERMANENT_OWNER}")
    print(f"[+] Total bots: {len(ALL_BOTS)}\033[0m")

    for bot in ALL_BOTS:
        threading.Thread(target=run_bot, args=(bot,), daemon=True).start()
        time.sleep(2)

    print(f"\033[92m[+] All bots running! Use '{DEFAULT_PREFIX}help' \033[0m")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\033[91m[!] Shutdown\033[0m")


if __name__ == "__main__":
    main()
