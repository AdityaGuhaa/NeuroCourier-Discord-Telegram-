import discord
import asyncio
import os
import time
from llm_backend import run_llm, log

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

from dotenv import load_dotenv
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

def split_message(text, limit=1900):
    chunks = []
    while len(text) > limit:
        split_at = text.rfind('\n', 0, limit)
        if split_at == -1:
            split_at = limit
        chunks.append(text[:split_at])
        text = text[split_at:].lstrip('\n')
    chunks.append(text)
    return chunks


@client.event
async def on_ready():
    print("\n" + "=" * 60)
    print(f"Discord bot connected as {client.user}")
    print("=" * 60)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    log("DISCORD RECEIVED", message.content)

    thinking = await message.channel.send("Thinking...")

    try:
        image_path = None

        # Download image if attached
        if message.attachments:
            attachment = message.attachments[0]
            if attachment.content_type and attachment.content_type.startswith("image"):
                timestamp = int(time.time())
                image_path = os.path.join(DATA_DIR, f"discord_image_{timestamp}.jpg")
                await attachment.save(image_path)
                log("DISCORD IMAGE", image_path)
            else:
                await thinking.edit(content="Unsupported attachment type.")
                return

        # Determine prompt
        if message.content and image_path:
            # Both text and image
            prompt = message.content
        elif message.content:
            # Text only
            prompt = message.content
        elif image_path:
            # Image only, no caption
            prompt = "Analyze this image."
        else:
            await thinking.delete()
            return

        reply = await run_llm(prompt=prompt, image_path=image_path)

        chunks = split_message(reply)
        await thinking.edit(content=chunks[0])
        for chunk in chunks[1:]:
            await message.channel.send(chunk)

    except Exception as e:
        log("DISCORD ERROR", str(e))
        await thinking.edit(content="Error processing request.")


client.run(DISCORD_TOKEN)