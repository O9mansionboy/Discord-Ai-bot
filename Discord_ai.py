import discord
from discord.ext import commands
from ollama import chat
from ollama import ChatResponse
import asyncio

#Lists
chat_store_buffer = []
chat_remember_buffer = [] # for the ai to use to remember chats they are having with people as context or somthing

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

#Ai settings
OLLAMA_MODEL = "llama2-uncensored"
Is_running = False
# Initialize the bot with intents
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")
    print("Connected servers:", [guild.name for guild in bot.guilds])

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    user_data = {
        "message": message.content,
        "user_id": message.author.id,
        "username": message.author.name,
        "channel_id": message.guild.id
    }

    #add mesage into buffer
    chat_store_buffer.append(user_data)
    print(chat_store_buffer)
    ctx = await bot.get_context(message)
    if len(chat_store_buffer) >= 5:
        print("buffer reached max size of 5 running chat ai")
        run_command = bot.get_command("run")

        if run_command:
            await ctx.invoke(run_command)

    await bot.process_commands(message)
        

@bot.command()
async def run(ctx):
    await ctx.send(f"{ctx.author.mention}, Hmmmm... Let me think!")
    try:
        response = await asyncio.to_thread(
            chat,
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": "You're a helpful assistant. Tasked to help with anyones qustions, or have a friendly chat with people! for people to get your attension they will say <@1331609725132865617> in thair message, aswell you can get peoples attension by including in your meassage <@(user_id)>. You cant do anything in this world without ussing COMMANDS! They connect you to the chat world so you will need to use them, command 1 !say(channel_id, message) eg ussage of command !say(1142351742143582258,'Hello!') !"},
                {"role": "user", "content": str(chat_store_buffer)},
            ],
        )
        print(f"AI response: {response['message']['content']}")
        await ctx.send(response['message']['content'])
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
    
    
bot.run("Your Token")