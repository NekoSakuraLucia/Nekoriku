import discord
from discord.ext import commands
from ..colored_logging import get_logger
import wavelink
from typing import Optional, Callable
from ..embeds import NekorikuEmbeds
from ..utils import Nekoriku_Utils
from ..ControlsView import NekorikuControls
import asyncio
import re
import random

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

    async def send_typing(self, ctx: commands.Context, message: str = None, embed=None, view=None) -> None:
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
                await ctx.send(embed=embed, view=view)
            elif message:
                await ctx.send(message)
            else:
                await ctx.send('กำลังพิมพ์...')

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        if logger:
          logger.info("Music_prefix plugins is ready")
        else:
            raise RuntimeError('TH: Logger ไม่ได้ถูกติดตั้งอย่างถูกต้อง / EN: Logger is not initialized.')
        
    @commands.command(name="search")
    async def search_song(self, ctx: commands.Context, *, search_name: str) -> None:
        if not ctx.guild:
            embed = NekorikuEmbeds.server_only(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        url_pattern = re.compile(r'https?://[^\s]+')
        if url_pattern.match(search_name):
            embed = NekorikuEmbeds.search_url_embed(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return

        if len(search_name) > 128:
            embed = NekorikuEmbeds.serach_limit_embed(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        player: Optional[wavelink.Player] = ctx.voice_client
        if not player:
            try:
                player = await ctx.author.voice.channel.connect(cls=wavelink.Player, self_deaf=True)
            except Exception:
                embed = NekorikuEmbeds.join_voice_embed(ctx.author, self.bot)
                await self.send_typing(ctx, embed=embed)
                return
        
        if player.channel != ctx.author.voice.channel:
            embed = NekorikuEmbeds.player_voice_channel(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        embed = discord.Embed(title="ผลลัพธ์การค้นหา", description="นี้คือรายการเพลงที่ตรงกับที่คุณพิมพ์มา:", color=0xFFC0CB)
        
        search_tracks: list[wavelink.Playable] = await wavelink.Playable.search(search_name)
        if search_tracks:
            for index, track in enumerate(search_tracks):
                embed.add_field(name=f"{index + 1}. {track.title}", value=track.uri, inline=False)
        else:
            embed.add_field(name="ไม่พบเพลง", value="ไม่พบเพลงใด ๆ ที่ตรงกับคำค้นหานั้น โปรดลองอีกครั้ง.", inline=False)

        msg = await ctx.send(embed=embed)
        view = discord.ui.View()

        ramdom_button = discord.ui.Button(label="🎶 สุ่มเพลง", style=discord.ButtonStyle.green)

        async def random_song_callback(interaction: discord.Interaction):
            if search_tracks:
                index = random.randint(0, len(search_tracks) - 1)
                selected_track = search_tracks[index]
                player: Optional[wavelink.Player] = interaction.guild.voice_client

                if player:
                    await player.queue.put_wait(selected_track)
                    embed = NekorikuEmbeds.playing_music_embed(interaction.user, self.bot, selected_track, player.queue.count, player.node.identifier)
                    await interaction.response.send_message(embed=embed, ephemeral=True)

                    if not player.playing:
                        next_track = player.queue.get()
                        await player.play(next_track, volume=60)
                else:
                    embed = NekorikuEmbeds.no_player_found_in_voice(ctx.author, self.bot)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = NekorikuEmbeds.no_songs_found_list(ctx.author, self.bot)
                await interaction.response.send_message(embed=embed, ephemeral=True)

        ramdom_button.callback = random_song_callback
        view.add_item(ramdom_button)

        options = [discord.SelectOption(label=f"{index + 1}. {track.title}", value=str(index)) for index, track in enumerate(search_tracks)]
        select = discord.ui.Select(placeholder="เลือกเพลง...", options=options)

        async def select_callback(interaction: discord.Interaction):
            try:
                index = int(select.values[0])
                selected_track: wavelink.Playable = search_tracks[index]
                player: Optional[wavelink.Player] = ctx.voice_client
                
                if player:
                    await player.queue.put_wait(selected_track)
                    embed = NekorikuEmbeds.playing_music_embed(ctx.author, self.bot, selected_track, player.queue.count, player.node.identifier)
                    await interaction.response.send_message(embed=embed, ephemeral=True) 

                    if not player.playing:
                        next_track = player.queue.get()
                        await player.play(next_track, volume=60)
                        
                    await asyncio.sleep(3)
                    await msg.delete()
                else:
                    embed = NekorikuEmbeds.no_player_found_in_voice(ctx.author, self.bot)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f"เกิดข้อผิดพลาด: {str(e)}", ephemeral=True)
        
        select.callback = select_callback

        view.add_item(select)

        await msg.edit(view=view)

        try:
            await asyncio.sleep(5)
            await ctx.message.delete()
        except discord.HTTPException:
            pass


    @commands.command(name="play")
    async def play(self, ctx: commands.Context, *, url: str) -> None:
        if not ctx.guild:
            embed = NekorikuEmbeds.server_only(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return

        player: Optional[wavelink.Player] = ctx.voice_client
        if not player:
            try:
                player = await ctx.author.voice.channel.connect(cls=wavelink.Player, self_deaf=True)
            except AttributeError:
                embed = NekorikuEmbeds.join_voice_embed(ctx.author, self.bot)
                await self.send_typing(ctx, embed=embed)
                return
            except discord.ClientException:
                embed = NekorikuEmbeds.unable_join_voice_channel(ctx.author, self.bot)
                await self.send_typing(ctx, embed=embed)
                return
        
        if player.channel != ctx.author.voice.channel:
            embed = NekorikuEmbeds.player_voice_channel(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        controls_view = NekorikuControls(bot=self.bot, player=player)
        
        tracks: wavelink.Playable = await wavelink.Playable.search(url)
        if not tracks:
            embed = NekorikuEmbeds.no_songs_found_match(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        if isinstance(tracks, wavelink.Playlist):
            added: int = await player.queue.put_wait(tracks)
            embed = NekorikuEmbeds.song_playlist_added(ctx.author, self.bot, tracks, added, player.node.identifier)
            await self.send_typing(ctx, embed=embed, view=controls_view)
        else:
            track: wavelink.Playable = tracks[0]
            await player.queue.put_wait(track)
            embed = NekorikuEmbeds.playing_music_embed(ctx.author, self.bot, track, player.queue.count, player.node.identifier)
            await self.send_typing(ctx, embed=embed, view=controls_view)

        if not player.playing:
            next_track = player.queue.get()
            await player.play(next_track, volume=60)
        
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

    @commands.command(name="leave")
    async def leave_voice(self, ctx: commands.Context) -> None:
        if not ctx.guild:
            embed = NekorikuEmbeds.server_only(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
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
            embed = NekorikuEmbeds.server_only(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
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
            embed = NekorikuEmbeds.server_only(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
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
        
        filters: wavelink.Filters = player.filters
        valid_filters: dict[str, Callable[[wavelink.Filters], None]] = {
            "nightcore": lambda filters: filters.timescale.set(speed=1.2, pitch=1.2, rate=1),
            "karaoke": lambda filters: filters.karaoke.set(level=2, mono_level=1, filter_band=220, filter_width=100),
            "lowpass": lambda filters: filters.low_pass.set(smoothing=20),
            "slow": lambda filters: filters.timescale.set(speed=0.8, pitch=0.9, rate=1),
            "reset": lambda filters: filters.reset()
        }

        if filter_type in valid_filters:
            valid_filters[filter_type](filters)
        else:
            valid_filters_list = ', '.join(valid_filters.keys())
            embed = discord.Embed(
                description=f"ไม่มีฟิลเตอร์ที่คุณพิมพ์มา ฟิลเตอร์ทั้งหมด: {valid_filters_list}.",
                color=0xFFC0CB
            )
            embed.set_author(name='The filter you typed does not exist.', icon_url=f'{ctx.author.display_avatar}?size=512')
            embed.set_footer(text='ไม่มีฟิลเตอร์ที่คุณพิมพ์มา', icon_url=f'{self.bot.user.display_avatar.url}?size=256')
            await self.send_typing(ctx, embed=embed)
            return
        
        await player.set_filters(filters)
        embed = NekorikuEmbeds.filters_music_embed(ctx.author, self.bot, filter_type)
        await self.send_typing(ctx, embed=embed)

    @commands.command(name="autoplay")
    async def autoplay_mode(self, ctx: commands.Context, *, mode: str = "enabled") -> None:
        if not ctx.guild:
            embed = NekorikuEmbeds.server_only(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
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
            embed = discord.Embed(
                description='ไม่มีโหมดที่คุณพิมพ์มา "enabled" หรือ "disabled',
                color=0xFFC0CB
            )
            embed.set_author(name='Autoplay Mode', icon_url=f'{ctx.author.display_avatar}?size=512')
            embed.set_footer(text="โหมดเล่นเพลงอัตโนมัติ", icon_url=f'{self.bot.user.display_avatar.url}?size=256')
            await self.send_typing(ctx, embed=embed)
            return
        
        embed = NekorikuEmbeds.player_autoplay_embed(ctx.author, self.bot, mode)
        await self.send_typing(ctx, embed=embed)

    @commands.command(name="toggle")
    async def pause_and_resume(self, ctx: commands.Context, *, toggle_mode: str) -> None:
        if not ctx.guild:
            embed = NekorikuEmbeds.server_only(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
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
            embed = NekorikuEmbeds.server_only(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
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

        repeat_modes = {
            "track": wavelink.QueueMode.loop,
            "queue": wavelink.QueueMode.loop_all,
            "none": wavelink.QueueMode.normal
        }

        if repeat_mode in repeat_modes:
            player.queue.mode = repeat_modes[repeat_mode]
        else:
            embed = discord.Embed(
                description='ไม่มีโหมดที่คุณพิมพ์มา "track" หรือ "queue" และ "none"',
                color=0xFFC0CB
            )
            embed.set_author(name='the mode you typed is not available.', icon_url=f'{ctx.author.display_avatar}?size=512')
            embed.set_footer(text="ไม่มีโหมดที่คุณพิมพ์มา", icon_url=f'{self.bot.user.display_avatar.url}?size=256')
            await self.send_typing(ctx, embed=embed)
            return

        embed = NekorikuEmbeds.repeat_music_embed(ctx.author, self.bot, repeat_mode)
        await self.send_typing(ctx, embed=embed)

    @commands.command(name="seek")
    async def seek_music(self, ctx: commands.Context, *, time_str: str) -> None:
        if not ctx.guild:
            embed = NekorikuEmbeds.server_only(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
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
            embed = NekorikuEmbeds.server_only(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
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

    # คำสั่งดูข้อมูลคิวทั้งหมดของเพลง
    @commands.command(name="queue")
    async def queue_length(self, ctx: commands.Context) -> None:
        player: Optional[wavelink.Player] = ctx.voice_client
        if not player or not isinstance(player, wavelink.Player):
            embed = NekorikuEmbeds.create_player_embed(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        if player.channel != ctx.author.voice.channel:
            embed = NekorikuEmbeds.player_voice_channel(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        if player.queue.is_empty:
            embed = NekorikuEmbeds.queue_empty_embed(ctx.author, self.bot)
            await self.send_typing(ctx, embed=embed)
            return
        
        embed = discord.Embed(title="รายการคิวเพลง", color=0xFFC0CB)
        for index, track in enumerate(player.queue):
            embed.add_field(name=f"{index + 1}. {track.title}", value=f"โดย: {track.author}", inline=False)
        await self.send_typing(ctx, embed=embed)
        

async def setup(bot: commands.Bot):
    await bot.add_cog(Nekoriku_Music_Prefix(bot))