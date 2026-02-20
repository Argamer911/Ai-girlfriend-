import random
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from openai import OpenAI

# ================= CONFIG =================

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = Client("ai-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
ai = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are a fun, romantic, playful Telegram bot.
Reply short, natural, Gen-Z style.
No long paragraphs.
Make it entertaining.
"""

# ================= AI FUNCTION =================

async def ai_reply(prompt):
    response = ai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# ================= JOKE =================

@app.on_message(filters.command("joke"))
async def joke(client, message: Message):
    text = await ai_reply("Ek funny romantic joke bolo")
    await message.reply(text)

# ================= TRUTH =================

@app.on_message(filters.command("truth"))
async def truth(client, message: Message):
    text = await ai_reply("Ek interesting truth question pucho group game ke liye")
    await message.reply(text)

# ================= DARE =================

@app.on_message(filters.command("dare"))
async def dare(client, message: Message):
    text = await ai_reply("Ek funny dare do group ke liye")
    await message.reply(text)

# ================= LOVE % =================

@app.on_message(filters.command("love"))
async def love(client, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply karke use karo 😅")

    user1 = message.from_user.first_name
    user2 = message.reply_to_message.from_user.first_name

    percent = random.randint(1, 100)

    explanation = await ai_reply(
        f"{user1} aur {user2} ka love percentage {percent}% hai. Ek cute funny line bolo."
    )

    await message.reply(f"💖 Love: {percent}%\n\n{explanation}")

# ================= SLAP =================

@app.on_message(filters.command("slap"))
async def slap(client, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply karo kisi ko 😤")

    user1 = message.from_user.mention
    user2 = message.reply_to_message.from_user.mention

    text = await ai_reply(f"{user1} ne {user2} ko funny style me slap kiya. Ek dramatic line bolo.")
    await message.reply(text)

# ================= HUG =================

@app.on_message(filters.command("hug"))
async def hug(client, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply karo kisi ko 🤗")

    user1 = message.from_user.mention
    user2 = message.reply_to_message.from_user.mention

    text = await ai_reply(f"{user1} ne {user2} ko cute hug diya. Ek sweet line bolo.")
    await message.reply(text)

# ================= KISS =================

@app.on_message(filters.command("kiss"))
async def kiss(client, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply karo kisi ko 😘")

    user1 = message.from_user.mention
    user2 = message.reply_to_message.from_user.mention

    text = await ai_reply(f"{user1} ne {user2} ko cute kiss diya. Ek romantic funny line bolo.")
    await message.reply(text)

# ================= DIVORCE =================

@app.on_message(filters.command("divorce"))
async def divorce(client, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply karo jis se divorce lena hai 💔")

    user1 = message.from_user.mention
    user2 = message.reply_to_message.from_user.mention

    text = await ai_reply(f"{user1} ne {user2} se funny dramatic divorce liya. Ek savage line bolo.")
    await message.reply(text)

# ================= START =================

print("Bot Started 🚀")
app.run()
