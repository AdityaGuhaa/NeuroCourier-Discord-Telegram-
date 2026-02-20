import discord
import asyncio
import os
import time

from llm_backend import run_llm, log

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

DISCORD_TOKEN = ""

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


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

        # TEXT
        if message.content:

            reply = await run_llm(
                prompt=message.content
            )

            await thinking.edit(content=reply)

        # IMAGE
        elif message.attachments:

            attachment = message.attachments[0]

            if attachment.content_type.startswith("image"):

                timestamp = int(time.time())

                file_path = os.path.join(
                    DATA_DIR,
                    f"discord_image_{timestamp}.jpg"
                )

                await attachment.save(file_path)

                reply = await run_llm(
                    prompt="Analyze this image.",
                    image_path=file_path
                )

                await thinking.edit(content=reply)

    except Exception as e:

        log("DISCORD ERROR", str(e))

        await thinking.edit(content="Error processing request.")


client.run(DISCORD_TOKEN)