from pyrogram import Client, filters
import os
from openai import OpenAI

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

app = Client("gf_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
ai = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
Tum ek cute girlfriend ho.
Tum Hindi me English alphabet me baat karti ho.
Reply short aur natural ho.
"""

@app.on_message(filters.private & filters.text)
async def chat(client, message):

    response = ai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message.text}
        ]
    )

    reply = response.choices[0].message.content
    await message.reply(reply)

app.run()
