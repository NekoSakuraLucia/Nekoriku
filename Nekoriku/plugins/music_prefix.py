import discord
from discord.ext import commands
from ..colored_logging import get_logger
import wavelink
from typing import Optional
from ..embeds import NekorikuEmbeds
from ..utils import Nekoriku_Utils

logger = get_logger('nekoriku_logger')

class Nekoriku_Music_Prefix(commands.Cog):
    """
    TH: คำสั่ง Music Prefix ในบอทเพลงดิสคอร์ดคือชุดคำสั่งที่เริ่มด้วยคำสั่งหลัก เช่น !play, !pause, !skip, และอื่นๆ เพื่อควบคุมเพลงในเซิร์ฟเวอร์ดิสคอร์ด
    
    EN: Music Prefix Commands are a set of commands starting with a prefix like !play, !pause, !skip, and others to control music in a Discord server.

    TH / EN:
    **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
    **As for other languages You can continue adding it yourself. If you are a translator**
    """
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def send_typing(self, ctx: commands.Context, message: str = None, embed=None) -> None:
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
            if embed:
                await ctx.send(embed=embed)
            elif message:
                await ctx.send(message)
            else:
                await ctx.send('กำลังพิมพ์...')

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        if logger:
          logger.info("[READY] -> Music_prefix plugins is ready")
        else:
            raise RuntimeError('TH: Logger ไม่ได้ถูกติดตั้งอย่างถูกต้อง / EN: Logger is not initialized.')

    @commands.command(name="join")
    async def connect_voice(self, member: discord.Member, ctx: commands.Context) -> None:
        if not ctx.guild:
            await self.send_typing(ctx, message='TH: คำสั่งนี้สามารถใช้ได้เฉพาะในเซิร์ฟเวอร์เท่านั้น\nEN: This command can only be used on the server.')
            return
        
        player: Optional[discord.VoiceClient] = ctx.voice_client
        if not player:
            try:
                player = await ctx.author.voice.channel.connect(cls=wavelink.Player, self_deaf=True)
                embed = discord.Embed(
                    description=f"เข้าร่วมช่องเสียง: **{ctx.voice_client.channel}** แล้ว",
                    color=0xFFC0CB
                )
                embed.set_author(name='Player Voice Channel', icon_url=f'{member.display_avatar}?size=512')
                embed.set_footer(text="คุณต้องอยู่ห้องเดียวกับหนู..", icon_url=f'{self.bot.user.display_avatar.url}?size=256')
                await self.send_typing(ctx, embed=embed)
                return
            except AttributeError:
                embed = NekorikuEmbeds.join_voice_embed(ctx.author, self.bot)
                await self.send_typing(ctx, embed=embed)
                return
            except discord.ClientException:
                await self.send_typing(ctx, message="ขออภัยหนูไม่สามารถเข้าร่วมช่องเสียงของคุณได้ ลองใหม่อีกครั้งสิ")
                return
            
        if ctx.voice_client:
            await self.send_typing(ctx, message=f"บอทเชื่อมต่ออยู่แล้ว: **{ctx.voice_client.channel}**")
            return

    @commands.command(name="play")
    async def play(self, ctx: commands.Context, *, url: str) -> None:
        if not ctx.guild:
            await self.send_typing(ctx, message='TH: คำสั่งนี้สามารถใช้ได้เฉพาะในเซิร์ฟเวอร์เท่านั้น\nEN: This command can only be used on the server.')
            return

        player: Optional[wavelink.Player] = ctx.voice_client
        if not player:
            try:
                player = await ctx.author.voice.channel.connect(cls=wavelink.Player, self_deaf=True)
            except AttributeError:
                await self.send_typing(ctx, message="กรุณาเข้าร่วมช่องเสียงก่อนใช้คำสั่งนี้")
                return
            except discord.ClientException:
                await self.send_typing(ctx, message="ขออภัยหนูไม่สามารถเข้าร่วมช่องเสียงของคุณได้ ลองใหม่อีกครั้งสิ")
                return
        
        if player.channel != ctx.author.voice.channel:
            await self.send_typing(ctx, message="คุณต้องอยู่ในช่องเดียวกับหนูสิ ลองอีกครั้งนะ")
            return
        
        tracks: wavelink.Playable = await wavelink.Playable.search(url)
        if not tracks:
            await self.send_typing(ctx, message=f'{ctx.author.mention} - ไม่พบเพลงใด ๆ ที่ตรงกับคำค้นหานั้น โปรดลองอีกครั้ง')
            return
        
        if isinstance(tracks, wavelink.Playlist):
            added: int = await player.queue.put_wait(tracks)
            await self.send_typing(ctx, message=f"เพิ่มเพลลิสต์เพลงแล้ว **`{tracks.name}`** | ({added} เพลงทั้งหมด) เข้าคิวแล้ว")
        else:
            track: wavelink.Playable = tracks[0]
            await player.queue.put_wait(track)
            embed = NekorikuEmbeds.playing_music_embed(ctx.author, self.bot, track)
            await self.send_typing(ctx, embed=embed)

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
            await self.send_typing(ctx, message='TH: คำสั่งนี้สามารถใช้ได้เฉพาะในเซิร์ฟเวอร์เท่านั้น\nEN: This command can only be used on the server.')
            return
        
        player: Optional[wavelink.Player] = ctx.voice_client
        if not player or not isinstance(player, wavelink.Player):
            embed = NekorikuEmbeds.create_player_embed(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        if player.channel != ctx.author.voice.channel:
            embed = NekorikuEmbeds.player_voice_channel(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        await player.disconnect()
        embed = NekorikuEmbeds.leave_music_embed(ctx.author, self.bot)
        await self.send_typing(ctx, embed=embed)
    
    @commands.command(name="skip")
    async def skip_voice(self, ctx: commands.Context) -> None:
        if not ctx.guild:
            await self.send_typing(ctx, message='TH: คำสั่งนี้สามารถใช้ได้เฉพาะในเซิร์ฟเวอร์เท่านั้น\nEN: This command can only be used on the server.')
            return
        
        player: Optional[wavelink.Player] = ctx.voice_client
        if not player or not isinstance(player, wavelink.Player):
            embed = NekorikuEmbeds.create_player_embed(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        if player.channel != ctx.author.voice.channel:
            embed = NekorikuEmbeds.player_voice_channel(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        await player.stop()
        embed = NekorikuEmbeds.skip_music_embed(ctx.author, self.bot)
        await self.send_typing(ctx, embed=embed)

    @commands.command(name="filters")
    async def filter_mode(self, ctx: commands.Context, *, filter_type: str) -> None:
        if not ctx.guild:
            await self.send_typing(ctx, message='TH: คำสั่งนี้สามารถใช้ได้เฉพาะในเซิร์ฟเวอร์เท่านั้น\nEN: This command can only be used on the server.')
            return

        player: Optional[wavelink.Player] = ctx.voice_client
        if not player or not isinstance(player, wavelink.Player):
            embed = NekorikuEmbeds.create_player_embed(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        if player.channel != ctx.author.voice.channel:
            embed = NekorikuEmbeds.player_voice_channel(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        valid_filters = ["nightcore", "karaoke", "reset"]
        
        filters: wavelink.Filters = player.filters
        if filter_type == "nightcore":
            filters.timescale.set(speed=1.2, pitch=1.2, rate=1)
        elif filter_type == "karaoke":
            filters.karaoke.set(level=2, mono_level=1, filter_band=220, filter_width=100)
        elif filter_type == "reset":
            filters.reset()
        else:
            valid_filters_list = ', '.join(valid_filters)
            all_options = f'{valid_filters_list}'
            await self.send_typing(ctx, message=f'ไม่มีฟิลเตอร์ที่คุณพิมพ์มา ฟิลเตอร์ทั้งหมด: {all_options}.')
            return
        
        await player.set_filters(filters)
        embed = NekorikuEmbeds.filters_music_embed(ctx.author, self.bot, filter_type)
        await self.send_typing(ctx, embed=embed)

    @commands.command(name="autoplay")
    async def autoplay_mode(self, ctx: commands.Context, *, mode: str) -> None:
        if not ctx.guild:
            await self.send_typing(ctx, message='TH: คำสั่งนี้สามารถใช้ได้เฉพาะในเซิร์ฟเวอร์เท่านั้น\nEN: This command can only be used on the server.')
            return
        
        player: Optional[wavelink.Player] = ctx.voice_client
        if not player or not isinstance(player, wavelink.Player):
            embed = NekorikuEmbeds.create_player_embed(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        if player.channel != ctx.author.voice.channel:
            embed = NekorikuEmbeds.player_voice_channel(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        if mode == "enabled":
            player.autoplay = wavelink.AutoPlayMode.enabled
        elif mode == "disabled":
            player.autoplay = wavelink.AutoPlayMode.disabled
        else:
            await self.send_typing(ctx, message='ไม่มีโหมดที่คุณพิมพ์มา "enabled" หรือ "disabled')
            return
        
        embed = NekorikuEmbeds.player_autoplay_embed(ctx.author, self.bot, mode)
        await self.send_typing(ctx, embed=embed)

    @commands.command(name="toggle")
    async def pause_and_resume(self, ctx: commands.Context, *, toggle_mode: str) -> None:
        if not ctx.guild:
            await self.send_typing(ctx, message='TH: คำสั่งนี้สามารถใช้ได้เฉพาะในเซิร์ฟเวอร์เท่านั้น\nEN: This command can only be used on the server.')
            return
        
        player: Optional[wavelink.Player] = ctx.voice_client
        if not player or not isinstance(player, wavelink.Player):
            embed = NekorikuEmbeds.create_player_embed(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        if player.channel != ctx.author.voice.channel:
            embed = NekorikuEmbeds.player_voice_channel(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return

        if toggle_mode not in ["pause", "resume"]:
            embed = NekorikuEmbeds.toggle_pause_resume_embed_error(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        await player.pause(toggle_mode == "pause")
        embed = NekorikuEmbeds.toggle_pause_resume_embed(ctx.author, self.bot, toggle_mode)
        await self.send_typing(ctx, embed=embed)

    @commands.command(name="loop")
    async def repeat_song(self, ctx: commands.Context, *, repeat_mode: str) -> None:
        if not ctx.guild:
            await self.send_typing(ctx, message='TH: คำสั่งนี้สามารถใช้ได้เฉพาะในเซิร์ฟเวอร์เท่านั้น\nEN: This command can only be used on the server.')
            return
        
        player: Optional[wavelink.Player] = ctx.voice_client
        if not player or not isinstance(player, wavelink.Player):
            embed = NekorikuEmbeds.create_player_embed(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        if player.channel != ctx.author.voice.channel:
            embed = NekorikuEmbeds.player_voice_channel(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        if player.autoplay != wavelink.AutoPlayMode.enabled:
            embed = NekorikuEmbeds.player_autoplay_embed_error(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        if repeat_mode == "track":
            player.queue.mode = wavelink.QueueMode.loop
        elif repeat_mode == "queue":
            player.queue.mode = wavelink.QueueMode.loop_all
        elif repeat_mode == "none":
            player.queue.mode = wavelink.QueueMode.normal
        else:
            await self.send_typing(ctx, message='ไม่มีโหมดที่คุณพิมพ์มา "track" หรือ "queue" และ "none"')
            return

        embed = NekorikuEmbeds.repeat_music_embed(ctx.author, self.bot, repeat_mode)
        await self.send_typing(ctx, embed=embed)

    # @commands.command(name="pause")
    # async def pause_music(self, ctx: commands.Context) -> None:
    #     if not ctx.guild:
    #         return
        
    #     player: Optional[wavelink.Player] = ctx.voice_client
    #     if not player or not isinstance(player, wavelink.Player):
    #         embed = NekorikuEmbeds.create_player_embed(ctx.author, self.bot)
    #         await self.send_typing(ctx, embed=embed)
    #         return
        
    #     if player.channel != ctx.author.voice.channel:
    #         embed = NekorikuEmbeds.player_voice_channel(ctx.author, self.bot)
    #         await self.send_typing(ctx, embed=embed)
    #         return
        
    #     await player.pause(True)
    #     await self.send_typing(ctx, message="หยุดเล่นเพลงชั่วคราวแล้ว")
    
    # @commands.command(name="resume")
    # async def resume_music(self, ctx: commands.Context) -> None:
    #     if not ctx.guild:
    #         return
        
    #     player: Optional[wavelink.Player] = ctx.voice_client
    #     if not player or not isinstance(player, wavelink.Player):
    #         embed = NekorikuEmbeds.create_player_embed(ctx.author, self.bot)
    #         await self.send_typing(ctx, embed=embed)
    #         return
        
    #     if player.channel != ctx.author.voice.channel:
    #         embed = NekorikuEmbeds.player_voice_channel(ctx.author, self.bot)
    #         await self.send_typing(ctx, embed=embed)
    #         return
        
    #     await player.pause(False)
    #     await self.send_typing(ctx, message="ทำการเล่นเพลงต่อหลังจากหยุดชั่วคราว")

    @commands.command(name="seek")
    async def seek_music(self, ctx: commands.Context, *, time_str: str) -> None:
        if not ctx.guild:
            await self.send_typing(ctx, message='TH: คำสั่งนี้สามารถใช้ได้เฉพาะในเซิร์ฟเวอร์เท่านั้น\nEN: This command can only be used on the server.')
            return
        
        player: Optional[wavelink.Player] = ctx.voice_client
        if not player or not isinstance(player, wavelink.Player):
            embed = NekorikuEmbeds.create_player_embed(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        if player.channel != ctx.author.voice.channel:
            embed = NekorikuEmbeds.player_voice_channel(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        total_ms = Nekoriku_Utils.convert_time(time_str)
        if total_ms is None:
            embed = NekorikuEmbeds.forward_music_embed_error(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        await player.seek(total_ms)
        embed = NekorikuEmbeds.forward_music_embed(ctx.author, self.bot, time_str)
        await self.send_typing(ctx, embed=embed)

    @commands.command(name="volume")
    async def volume_music(self, ctx: commands.Context, *, vol: str) -> None:
        if not ctx.guild:
            await self.send_typing(ctx, message='TH: คำสั่งนี้สามารถใช้ได้เฉพาะในเซิร์ฟเวอร์เท่านั้น\nEN: This command can only be used on the server.')
            return
        
        player: Optional[wavelink.Player] = ctx.voice_client
        if not player or not isinstance(player, wavelink.Player):
            embed = NekorikuEmbeds.create_player_embed(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        if player.channel != ctx.author.voice.channel:
            embed = NekorikuEmbeds.player_voice_channel(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        try:
            volume = int(vol)
        except ValueError:
            embed = NekorikuEmbeds.volume_music_embed_else(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        if volume in {10, 20, 30, 40, 50, 60, 70, 80, 90, 100}:
            await player.set_volume(volume)
            embed = NekorikuEmbeds.volume_music_embed(ctx.author, self.bot, volume)
            await self.send_typing(ctx, embed=embed)
        else:
            embed = NekorikuEmbeds.volume_music_embed_else(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Nekoriku_Music_Prefix(bot))