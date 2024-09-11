import discord
from discord.ext import commands
from ..colored_logging import get_logger
import wavelink
from typing import Optional

logger = get_logger('nekoriku_logger')

class Nekoriku_Music_Prefix(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def send_typing(self, ctx: commands.Context, message: str) -> None:
        """
        TH:
        ฟังก์ชัน `send_typing` ทำให้บอทแสดงสถานะการพิมพ์ในระหว่างที่ส่งข้อความ โดยจะใช้ `ctx.typing()` เพื่อแสดงสถานะ และใช้ `ctx.send(message)` เพื่อส่งข้อความนั้นออกไป

        EN:
        The `send_typing` function makes the bot show a typing status while sending a message. It uses `ctx.typing()` to display the typing status and `ctx.send(message)` to send the message.

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        async with ctx.typing():
            await ctx.send(message)

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        if logger:
          logger.info("[READY] -> Music_prefix plugins is ready")
        else:
            raise RuntimeError('TH: Logger ไม่ได้ถูกติดตั้งอย่างถูกต้อง / EN: Logger is not initialized.')

    @commands.command(name="play")
    async def play(self, ctx: commands.Context, *, url: str) -> None:
        if not ctx.guild:
            return

        player: Optional[wavelink.Player] = ctx.voice_client
        if not player:
            try:
                player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            except AttributeError:
                await ctx.send("กรุณาเข้าร่วมช่องเสียงก่อนใช้คำสั่งนี้")
                return
            except discord.ClientException:
                await ctx.send("ขออภัยหนูไม่สามารถเข้าร่วมช่องเสียงของคุณได้ ลองใหม่อีกครั้งสิ")
                return
        
        if player.channel != ctx.author.voice.channel:
            await ctx.send("คุณต้องอยู่ในช่องเดียวกับหนูสิ ลองอีกครั้งนะ")
            return
        
        tracks: wavelink.Playable = await wavelink.Playable.search(url)
        if not tracks:
            await ctx.send(f'{ctx.author.mention} - ไม่พบเพลงใด ๆ ที่ตรงกับคำค้นหานั้น โปรดลองอีกครั้ง')
            return
        
        if isinstance(tracks, wavelink.Playlist):
            added: int = await player.queue.put_wait(tracks)
            await ctx.send(f"เพิ่มเพลลิสต์เพลงแล้ว **`{tracks.name}`** | ({added} เพลงทั้งหมด) เข้าคิวแล้ว")
        else:
            track: wavelink.Playable = tracks[0]
            await player.queue.put_wait(track)
            await self.send_typing(ctx, f'เพิ่มคิวเพลงแล้ว **`{track.title}`**')

        if not player.playing:
            await player.play(
                player.queue.get(),
                volume=60
            )
        
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

    @commands.command(name="leave")
    async def leave_voice(self, ctx: commands.Context) -> None:
        if not ctx.guild:
            return
        
        player: Optional[wavelink.Player] = ctx.voice_client
        if not player or not isinstance(player, wavelink.Player):
            await ctx.send('หนูไม่ได้เชื่อมต่อกับช่องเสียงหรือไม่สามารถเข้าถึง Player ได้')
            return
        
        await player.disconnect()
        await self.send_typing(ctx, 'ออกจากช่องเสียงแล้ว')
    
    @commands.command(name="skip")
    async def skip_voice(self, ctx: commands.Context) -> None:
        if not ctx.guild:
            return
        
        player: Optional[wavelink.Player] = ctx.voice_client
        if not player or not isinstance(player, wavelink.Player):
            await self.send_typing(ctx, 'หนูไม่ได้เชื่อมต่อกับช่องเสียงหรือไม่สามารถเข้าถึง Player ได้')
            return
        
        await player.stop()
        await self.send_typing(ctx, 'ข้ามไปยังเพลงถัดไปแล้ว')

    @commands.command(name="filters", aliases=["nightcore", "karaoke", "reset"])
    async def filter_mode(self, ctx: commands.Context, filter_type: str) -> None:
        if not ctx.guild:
            return

        player: Optional[wavelink.Player] = ctx.voice_client
        if not player or not isinstance(player, wavelink.Player):
            await self.send_typing(ctx, 'หนูไม่ได้เชื่อมต่อกับช่องเสียงหรือไม่สามารถเข้าถึง Player ได้')
            return
        
        if player.channel != ctx.author.voice.channel:
            await self.send_typing('คุณต้องอยู่ในช่องเดียวกับหนูสิ ลองอีกครั้งนะ')
            return
        
        filters: wavelink.Filters = player.filters
        if filter_type == "nightcore":
            filters.timescale.set(speed=1.2, pitch=1.2, rate=1)
        elif filter_type == "karaoke":
            filters.karaoke.set(level=2, mono_level=1, filter_band=220, filter_width=100)
        elif filter_type == "reset":
            filters.reset()
        else:
            await self.send_typing(ctx, 'ไม่มีฟิลเตอร์ที่คุณพิมพ์มา ฟิลเตอร์ทั้งหมด "nightcore" หรือ "karaoke" หรือ "reset".')
            return
        
        await player.set_filters(filters)
        await self.send_typing(ctx, f'ทำการตั้งค่าฟิลเตอร์เป็น **`{filter_type}`** แล้ว')

    @commands.command(name="autoplay", aliases=["enabled", "disabled"])
    async def autoplay_mode(self, ctx: commands.Context, mode: str) -> None:
        if not ctx.guild:
            return
        
        player: Optional[wavelink.Player] = ctx.voice_client
        if not player or not isinstance(player, wavelink.Player):
            await self.send_typing(ctx, 'หนูไม่ได้เชื่อมต่อกับช่องเสียงหรือไม่สามารถเข้าถึง Player ได้')
            return
        
        if player.channel != ctx.author.voice.channel:
            await self.send_typing(ctx, 'คุณต้องอยู่ในช่องเดียวกับหนูสิ ลองอีกครั้งนะ')
            return
        
        if mode == "enabled":
            player.autoplay = wavelink.AutoPlayMode.enabled
        elif mode == "disabled":
            player.autoplay = wavelink.AutoPlayMode.disabled
        else:
            await self.send_typing(ctx, 'ไม่มีโหมดที่คุณพิมพ์มา "enabled" หรือ "disabled')
            return
        
        await self.send_typing(ctx, f'เลือกโหมด **`{player.autoplay.name}**` แล้ว')

    @commands.command(name="volume", aliases=[
        "10",
        "20",
        "30",
        "40",
        "50",
        "60",
        "70",
        "80"
        "90",
        "100"
    ])
    async def volume_music(self, ctx: commands.Context, vol: str) -> None:
        if not ctx.guild:
            return
        
        player: Optional[wavelink.Player] = ctx.voice_client
        if not player or not isinstance(player, wavelink.Player):
            await self.send_typing(ctx, 'หนูไม่ได้เชื่อมต่อกับช่องเสียงหรือไม่สามารถเข้าถึง Player ได้')
            return
        
        if player.channel != ctx.author.voice.channel:
            await self.send_typing(ctx, 'คุณต้องอยู่ในช่องเดียวกับหนูสิ ลองอีกครั้งนะ')
            return
        
        try:
            volume = int(vol)
        except ValueError:
            await self.send_typing(ctx, f'ไม่มีค่าที่คุณระบุมา **`{vol}%`**')
            return
        
        if volume in {10, 20, 30, 40, 50, 60, 70, 80, 90, 100}:
            await player.set_volume(volume)
            await self.send_typing(ctx, f'ปรับระดับเสียงเป็น **`{volume}%`** แล้ว')
        else:
            await self.send_typing(ctx, f'ไม่มีค่าที่คุณระบุมา **`{vol}%`**')

async def setup(bot: commands.Bot):
    await bot.add_cog(Nekoriku_Music_Prefix(bot))