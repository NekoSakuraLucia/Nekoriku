import discord
from discord import app_commands
from discord.ext import commands
from ..colored_logging import get_logger
import wavelink

logger = get_logger('nekoriku_logger')

class Nekoriku_Music_Slash(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        if logger:
            logger.info("[READY] -> Music_Slash plugins is ready")
        else:
            raise RuntimeError('TH: Logger ไม่ได้ถูกติดตั้งอย่างถูกต้อง / EN: Logger is not initialized.')
    
    @app_commands.command(name="ping", description="TH: ทดสอบคำสั่ง | EN: Test commands")
    async def ping_pong(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()

        await interaction.followup.send("Pong.")

    @app_commands.command(name="play", description="TH: ให้หนูเล่นเพลงให้คุณฟัง / EN: Let me play a song for you.")
    @app_commands.describe(song="TH: ป้อน URL ของเพลงเพื่อให้หนูเล่นเพลงให้คุณฟังได้ / EN: Enter the URL of the song so we can play it for you.")
    async def play_music(self, interaction: discord.Interaction, song: str) -> None:
        await interaction.response.defer()

        if not interaction.guild:
            await interaction.followup.send('TH: คำสั่งนี้สามารถใช้ได้เฉพาะในเซิร์ฟเวอร์เท่านั้น\nEN: This command can only be used on the server.')
            return

        player = interaction.guild.voice_client

        if not player:
            try:
                player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
            except AttributeError:
                await interaction.followup.send('TH: กรุณาเข้าร่วมช่องเสียงก่อนที่จะใช้คำสั่งนี้\nEN: Please Join Voice Channel')
                return
            except discord.ClientException:
                await interaction.followup.send('TH: กรุณาเข้าร่วมช่องเสียงก่อนที่จะใช้คำสั่งนี้\nEN: Please Join Voice Channel')
                return
        
        if player.channel != interaction.user.voice.channel:
            await interaction.followup.send('คุณต้องอยู่ในช่องเสียงเดียวกับหนูเพื่อใช้คำสั่งนี้')
            return
        
        tracks: wavelink.Player = await wavelink.Playable.search(song)
        if not tracks:
            await interaction.followup.send(f'{interaction.user.mention} - ไม่พบเพลงใด ๆ ที่ตรงกับคำค้นหานั้น โปรดลองอีกครั้ง')
            return
        
        if isinstance(tracks, wavelink.Playlist):
            added: int = await player.queue.put_wait(tracks)
            await interaction.followup.send(f"เพิ่มเพลลิสต์เพลงแล้ว **`{tracks.name}`** | ({added} เพลงทั้งหมด) เข้าคิวแล้ว")
        else:
            track: wavelink.Playable = tracks[0]
            await player.queue.put_wait(track)
            await interaction.followup.send(f'เพิ่มคิวเพลงแล้ว **`{track.title}`**')
        
        if not player.playing:
            await player.play(
                player.queue.get(),
                volume=60
            )

async def setup(bot: commands.Bot):
    await bot.add_cog(Nekoriku_Music_Slash(bot))