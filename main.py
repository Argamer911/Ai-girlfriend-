import random
import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from openai import OpenAI

# ================= CONFIG =================

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OWNER_ID = 8444148014  # 👈 YAHAN APNA TELEGRAM USER ID DAALO

app = Client("ai-gf-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
ai = OpenAI(api_key=OPENAI_API_KEY)

BASE_PROMPT = """
You are a cute, romantic, playful AI girlfriend.
Reply short.
Speak Hindi in English letters.
Be fun and engaging.
"""

OWNER_PROMPT = """
You are a respectful AI assistant.
User is the Owner.
Call them 'Owner'.
Talk respectfully using 'aap'.
Be loyal and polite.
"""

# ================= MEMORY + LEADERBOARD =================

leaderboard = {}

async def ai_reply(prompt, is_owner=False):
    system_prompt = OWNER_PROMPT if is_owner else BASE_PROMPT

    response = ai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# ================= START =================

@app.on_message(filters.command("start"))
async def start(client, message: Message):

    text = """
💖 𝐀𝐈 𝐆𝐢𝐫𝐥𝐟𝐫𝐢𝐞𝐧𝐝 💖

Hey baby 😘  
Main tumhari AI girlfriend hoon 💕

Neeche se choose karo 👇
"""

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("💘 Love %", switch_inline_query_current_chat="/love")],
        [
            InlineKeyboardButton("😂 Joke", switch_inline_query_current_chat="/joke"),
            InlineKeyboardButton("🤫 Truth", switch_inline_query_current_chat="/truth")
        ],
        [InlineKeyboardButton("🔥 Dare", switch_inline_query_current_chat="/dare")],
        [InlineKeyboardButton("🏆 Leaderboard", switch_inline_query_current_chat="/leaderboard")]
    ])

    await message.reply(text, reply_markup=buttons)

# ================= COMMANDS =================

@app.on_message(filters.command("joke"))
async def joke(client, message: Message):
    reply = await ai_reply("Ek funny romantic joke bolo", message.from_user.id == OWNER_ID)
    await message.reply(reply)

@app.on_message(filters.command("truth"))
async def truth(client, message: Message):
    reply = await ai_reply("Ek interesting truth question pucho", message.from_user.id == OWNER_ID)
    await message.reply(reply)

@app.on_message(filters.command("dare"))
async def dare(client, message: Message):
    reply = await ai_reply("Ek funny dare do", message.from_user.id == OWNER_ID)
    await message.reply(reply)

@app.on_message(filters.command("love"))
async def love(client, message: Message):
    percent = random.randint(1, 100)
    explanation = await ai_reply(
        f"Love percentage {percent}% hai. Ek cute line bolo.",
        message.from_user.id == OWNER_ID
    )
    await message.reply(f"💖 Love: {percent}%\n{explanation}")

# ================= LEADERBOARD =================

@app.on_message(filters.command("leaderboard"))
async def show_leaderboard(client, message: Message):

    if not leaderboard:
        return await message.reply("Abhi tak koi top lover nahi bana 😅")

    sorted_users = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)[:10]

    text = "🏆 Top 10 Lovers 💕\n\n"
    for i, (user_id, count) in enumerate(sorted_users, 1):
        user = await app.get_users(user_id)
        text += f"{i}. {user.first_name} — {count} msgs\n"

    await message.reply(text)

# ================= AI CHAT =================

@app.on_message(filters.text & ~filters.command(
    ["start", "joke", "truth", "dare", "love", "leaderboard"]
))
async def chat(client, message: Message):

    if not message.from_user:
        return

    user_id = message.from_user.id
    is_owner = user_id == OWNER_ID

    # Group me sirf mention ya reply pe bolega
    if message.chat.type != "private":
        me = await app.get_me()
        if not (message.mentioned or 
                (message.reply_to_message and 
                 message.reply_to_message.from_user and 
                 message.reply_to_message.from_user.id == me.id)):
            return

    leaderboard[user_id] = leaderboard.get(user_id, 0) + 1

    reply = await ai_reply(message.text, is_owner)
    await message.reply(reply)

# ================= RUN =================

print("AI Girlfriend Bot Running 💖")
app.run()
