import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
from ..colored_logging import get_logger
import wavelink
from ..embeds import NekorikuEmbeds
from ..utils import Nekoriku_Utils
import re
import random

logger = get_logger('nekoriku_logger')

class Nekoriku_Music_Slash(commands.Cog):
    """
    TH: คำสั่งเพลง Slash Commands คือคำสั่งที่เริ่มต้นด้วยสแลช (/) เช่น /play, /pause, /skip ซึ่งช่วยให้คุณควบคุมเพลงในเซิร์ฟเวอร์ดิสคอร์ดของคุณได้

    EN: Music Slash Commands start with a slash (/), like /play, /pause, /skip, allowing you to control music in a Discord server.

    TH / EN:
    **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
    **As for other languages You can continue adding it yourself. If you are a translator**
    """
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

    @app_commands.command(name="search", description="TH: ค้นหาเพลงด้วยชื่อ / EN: Search for songs by name")
    @app_commands.describe(search="TH: ป้อนชื่อเพลงเพื่อค้นหา / EN: Enter the name of the song to search.")
    async def search_song(self, interaction: discord.Interaction, search: str) -> None:
        await interaction.response.defer()

        if not interaction.guild:
            embed = NekorikuEmbeds.server_only(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        url_pattern = re.compile(r'https?://[^\s]+')
        if url_pattern.match(search):
            embed = NekorikuEmbeds.search_url_embed(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        if len(search) > 128:
            embed = NekorikuEmbeds.serach_limit_embed(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        player: Optional[wavelink.Player] = interaction.guild.voice_client
        if not player:
            try:
                player = await interaction.user.voice.channel.connect(cls=wavelink.Player, self_deaf=True)
            except Exception:
                embed = NekorikuEmbeds.join_voice_embed(interaction.user, self.bot)
                await interaction.followup.send(embed=embed)
                return
        
        if player.channel != interaction.user.voice.channel:
            embed = NekorikuEmbeds.player_voice_channel(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        embed = discord.Embed(title="ผลลัพธ์การค้นหา", description="นี้คือรายการเพลงที่ตรงกับที่คุณพิมพ์มา:", color=0xFFC0CB)
        
        search_tracks: list[wavelink.Playable] = await wavelink.Playable.search(search)
        if search_tracks:
            for index, track in enumerate(search_tracks):
                embed.add_field(name=f"{index + 1}. {track.title}", value=track.uri, inline=False)
        else:
            embed.add_field(name="ไม่พบเพลง", value="ไม่พบเพลงใด ๆ ที่ตรงกับคำค้นหานั้น โปรดลองอีกครั้ง.", inline=False)

        view = discord.ui.View()

        ramdom_button = discord.ui.Button(label="🎶 สุ่มเพลง", style=discord.ButtonStyle.green)

        async def random_song_callback(interaction: discord.Interaction):
            if search_tracks:
                index = random.randint(0, len(search_tracks) - 1)
                selected_track = search_tracks[index]
                player: Optional[wavelink.Player] = interaction.guild.voice_client

                if player:
                    await player.queue.put_wait(selected_track)
                    embed = NekorikuEmbeds.playing_music_embed(interaction.user, self.bot, selected_track, player.queue.count)
                    await interaction.response.send_message(embed=embed, ephemeral=True)

                    if not player.playing:
                        next_track = player.queue.get()
                        await player.play(next_track, volume=60)
                else:
                    embed = NekorikuEmbeds.no_player_found_in_voice(interaction.user, self.bot)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = NekorikuEmbeds.no_songs_found_list(interaction.user, self.bot)
                await interaction.response.send_message(embed=embed, ephemeral=True)

        ramdom_button.callback = random_song_callback
        view.add_item(ramdom_button)

        options = [discord.SelectOption(label=f"{index + 1}. {track.title}", value=str(index)) for index, track in enumerate(search_tracks)]
        select = discord.ui.Select(placeholder="เลือกเพลง...", options=options)

        async def select_callback(interaction: discord.Interaction):
            try:
                index = int(select.values[0])
                selected_track: wavelink.Playable = search_tracks[index]
                player: Optional[wavelink.Player] = interaction.guild.voice_client
                
                if player:
                    await player.queue.put_wait(selected_track)
                    embed = NekorikuEmbeds.playing_music_embed(interaction.user, self.bot, selected_track, player.queue.count)
                    await interaction.response.send_message(embed=embed, ephemeral=True) 
                    
                    if not player.playing:
                        next_track = player.queue.get()
                        await player.play(next_track, volume=60)
                else:
                    embed = NekorikuEmbeds.no_player_found_in_voice(interaction.user, self.bot)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f"เกิดข้อผิดพลาด: {str(e)}", ephemeral=True)
        
        select.callback = select_callback
        view.add_item(select)

        await interaction.followup.send(embed=embed, view=view)

    @app_commands.command(name="play", description="TH: ให้หนูเล่นเพลงให้คุณฟัง / EN: Let me play a song for you.")
    @app_commands.describe(song="TH: ป้อน URL ของเพลงเพื่อให้หนูเล่นเพลงให้คุณฟังได้ / EN: Enter the URL of the song so we can play it for you.")
    async def play_music(self, interaction: discord.Interaction, song: str) -> None:
        await interaction.response.defer()

        if not interaction.guild:
            embed = NekorikuEmbeds.server_only(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return

        player = interaction.guild.voice_client

        if not player:
            try:
                player = await interaction.user.voice.channel.connect(cls=wavelink.Player, self_deaf=True)
            except AttributeError:
                embed = NekorikuEmbeds.join_voice_embed(interaction.user, self.bot)
                await interaction.followup.send(embeds=embed)
                return
            except discord.ClientException:
                embed = NekorikuEmbeds.unable_join_voice_channel(interaction.user, self.bot)
                await interaction.followup.send(embed=embed)
                return
        
        if player.channel != interaction.user.voice.channel:
            embed = NekorikuEmbeds.player_voice_channel(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        tracks: wavelink.Player = await wavelink.Playable.search(song)
        if not tracks:
            embed = NekorikuEmbeds.no_songs_found_match(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        if isinstance(tracks, wavelink.Playlist):
            added: int = await player.queue.put_wait(tracks)
            embed = NekorikuEmbeds.song_playlist_added(interaction.user, self.bot, tracks.name, added)
            await interaction.followup.send(embed=embed)
        else:
            track: wavelink.Playable = tracks[0]
            await player.queue.put_wait(track)
            embed = NekorikuEmbeds.playing_music_embed(interaction.user, self.bot, track, player.queue.count)
            await interaction.followup.send(embed=embed)
        
        if not player.playing:
            next_track = player.queue.get()
            await player.play(next_track, volume=60)

    @app_commands.command(name="leave", description="TH: ทำลายเพลงและออกจากช่องเสียง / EN: Destroyed the song and left the sound room.")
    async def leave_music(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()

        if not interaction.guild:
            embed = NekorikuEmbeds.server_only(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        player: Optional[wavelink.Player] = interaction.guild.voice_client
        if not player or not isinstance(player, wavelink.Player):
            embed = NekorikuEmbeds.create_player_embed(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        if player.channel != interaction.user.voice.channel:
            embed = NekorikuEmbeds.player_voice_channel(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        await player.disconnect()
        embed = NekorikuEmbeds.leave_music_embed(interaction.user, self.bot)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="skip", description="TH: ข้ามไปยังเพลงถัดไป / EN: Skip to the next song.")
    async def skip_music(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()

        if not interaction.guild:
            embed = NekorikuEmbeds.server_only(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        player: Optional[wavelink.Player] = interaction.guild.voice_client
        if not player or not isinstance(player, wavelink.Player):
            embed = NekorikuEmbeds.create_player_embed(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        if player.channel != interaction.user.voice.channel:
            embed = NekorikuEmbeds.player_voice_channel(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        await player.stop()
        embed = NekorikuEmbeds.skip_music_embed(interaction.user, self.bot)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="toggle", description="TH: เลือกโหมดสำหรับการหยุดเพลงหรือคืนค่าเพลง / EN: Choose a mode for pause music or resume music.")
    @app_commands.describe(toggle_mode="TH: เลือกโหมด / EN: Select mode")
    @app_commands.choices(
        toggle_mode=[
            app_commands.Choice(name="Pause", value="pause"),
            app_commands.Choice(name="Resume", value="resume")
        ]
    )
    async def toggle_pause_resume(self, interaction: discord.Interaction, toggle_mode: str) -> None:
        await interaction.response.defer()

        if not interaction.guild:
            embed = NekorikuEmbeds.server_only(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        player: Optional[wavelink.Player] = interaction.guild.voice_client
        if not player or not isinstance(player, wavelink.Player):
            embed = NekorikuEmbeds.create_player_embed(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        if player.channel != interaction.user.voice.channel:
            embed = NekorikuEmbeds.player_voice_channel(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return

        await player.pause(toggle_mode == "pause")
        embed = NekorikuEmbeds.toggle_pause_resume_embed(interaction.user, self.bot, toggle_mode)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="volume", description="TH: ปรับระดับเสียงเพลง / EN: Adjust the music volume")
    @app_commands.describe(vol="TH: ค่าระดับเสียงที่คุณต้องการ / EN: Your desired volume level")
    async def volume_music(self, interaction: discord.Interaction, vol: str) -> None:
        await interaction.response.defer()

        if not interaction.guild:
            embed = NekorikuEmbeds.server_only(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
    
        player: Optional[wavelink.Player] = interaction.guild.voice_client
        if not player or not isinstance(player, wavelink.Player):
            embed = NekorikuEmbeds.create_player_embed(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        if player.channel != interaction.user.voice.channel:
            embed = NekorikuEmbeds.player_voice_channel(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        try:
            volume = int(vol)
            if 0 <= volume <= 100:
                await player.set_volume(volume)
                embed = NekorikuEmbeds.volume_music_embed(interaction.user, self.bot, volume)
                await interaction.followup.send(embed=embed)
            else:
                embed = NekorikuEmbeds.volume_music_embed_else(interaction.user, self.bot)
                await interaction.followup.send(embed=embed)
        except ValueError:
            embed = NekorikuEmbeds.volume_music_embed_error(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="loop", description="TH: วนเพลงซ้ำไปเรื่อยๆ / EN: Repeat the song continuously.")
    @app_commands.describe(repeat_mode="TH: เลือกโหมดที่ต้องการวนเพลง / EN: Select the mode in which you want to loop the song.")
    @app_commands.choices(
        repeat_mode=[
            app_commands.Choice(name="Repeat Track", value="track"),
            app_commands.Choice(name="Repeat Queue", value="queue"),
            app_commands.Choice(name="None", value="none")
        ]
    )
    async def repeat_song(self, interaction: discord.Interaction, repeat_mode: str) -> None:
        await interaction.response.defer()

        if not interaction.guild:
            embed = NekorikuEmbeds.server_only(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        player: Optional[wavelink.Player] = interaction.guild.voice_client
        if not player or not isinstance(player, wavelink.Player):
            embed = NekorikuEmbeds.create_player_embed(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        if player.channel != interaction.user.voice.channel:
            embed = NekorikuEmbeds.player_voice_channel(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        if player.autoplay != wavelink.AutoPlayMode.enabled:
            embed = NekorikuEmbeds.player_autoplay_embed_error(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return

        mode_mapping = {
            "track": wavelink.QueueMode.loop,
            "queue": wavelink.QueueMode.loop_all,
            "none": wavelink.QueueMode.normal
        }

        player.queue.mode = mode_mapping.get(repeat_mode, wavelink.QueueMode.normal)
        embed = NekorikuEmbeds.repeat_music_embed(interaction.user, self.bot, repeat_mode)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="seek", description="TH: กรอเวลาของเพลง / Fast forward the time of the song")
    @app_commands.describe(time="TH: เวลาที่ต้องการกรอเช่น 00:00 / EN: Time to fast forward the song, such as 00:00")
    async def forward_music(self, interaction: discord.Interaction, time: str) -> None:
        await interaction.response.defer()
        
        if not interaction.guild:
            embed = NekorikuEmbeds.server_only(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        player: Optional[wavelink.Player] = interaction.guild.voice_client
        if not player or not isinstance(player, wavelink.Player):
            embed = NekorikuEmbeds.create_player_embed(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        if player.channel != interaction.user.voice.channel:
            embed = NekorikuEmbeds.player_voice_channel(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        total_ms = Nekoriku_Utils.convert_time(time)
        if total_ms is None:
            embed = NekorikuEmbeds.forward_music_embed_error(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        await player.seek(total_ms)
        embed = NekorikuEmbeds.forward_music_embed(interaction.user, self.bot, time)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="autoplay", description="TH: ต่อคิวเพลงไปเรื่อยๆ / EN: Continue the song auto queue when the song ends.")
    @app_commands.describe(mode="TH: เลือกเปิดหรือปิด / EN: Select On or Off.")
    @app_commands.choices(
        mode=[
            app_commands.Choice(name="Autoplay (Enabled)", value="enabled"),
            app_commands.Choice(name="Autoplay (Diabled)", value="disabled")
        ]
    )
    async def autoplay_mode(self, interaction: discord.Interaction, mode: str) -> None:
        await interaction.response.defer()

        if not interaction.guild:
            embed = NekorikuEmbeds.server_only(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return

        player: Optional[wavelink.Player] = interaction.guild.voice_client
        if not player or not isinstance(player, wavelink.Player):
            embed = NekorikuEmbeds.create_player_embed(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        if player.channel != interaction.user.voice.channel:
            embed = NekorikuEmbeds.player_voice_channel(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return

        if mode == "enabled":
            player.autoplay = wavelink.AutoPlayMode.enabled
        elif mode == "disabled":
            player.autoplay = wavelink.AutoPlayMode.disabled

        embed = NekorikuEmbeds.player_autoplay_embed(interaction.user, self.bot, mode)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="filters", description="TH: เปิดการใช้งานฟิลเตอร์ / EN: Activate the Filters.")
    @app_commands.describe(filter="TH: เลือกรูปแบบฟิลเตอร์ที่ต้องการ / EN: Select the desired filter style.")
    @app_commands.choices(
        filter=[
            app_commands.Choice(name="Nightcore", value="nightcore"),
            app_commands.Choice(name="Karaoke", value="karaoke"),
            app_commands.Choice(name="LowPass", value="lowpass"),
            app_commands.Choice(name="None", value="none")
        ]
    )
    # TH: ตอนนี้เราจะทำฟิลเตอร์แค่สี่ตัวก่อน แล้วค่อยเพิ่มตัวอื่นๆ ทีหลัง
    # EN: Let's start with just four filters for now and add more later.

    # TH / EN:
    # **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
    # **As for other languages You can continue adding it yourself. If you are a translator**
    async def filter_mode(self, interaction: discord.Interaction, filter: str) -> None:
        await interaction.response.defer()

        if not interaction.guild:
            embed = NekorikuEmbeds.server_only(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        player: Optional[wavelink.Player] = interaction.guild.voice_client
        if not player or not isinstance(player, wavelink.Player):
            embed = NekorikuEmbeds.create_player_embed(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        if player.channel != interaction.user.voice.channel:
            embed = NekorikuEmbeds.player_voice_channel(interaction.user, self.bot)
            await interaction.followup.send(embed=embed)
            return
        
        filters: wavelink.Filters = player.filters
        filter_settings = {
            "nightcore": lambda: filters.timescale.set(speed=1.2, pitch=1.2, rate=1),
            "karaoke": lambda: filters.karaoke.set(level=2, mono_level=1, filter_band=220, filter_width=100),
            "lowpass": lambda: filters.low_pass.set(smoothing=20),
            "none": lambda: filters.reset()
        }

        if filter in filter_settings:
            filter_settings[filter]()
        else:
            pass

        await player.set_filters(filters)
        embed = NekorikuEmbeds.filters_music_embed(interaction.user, self.bot, filter)
        await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Nekoriku_Music_Slash(bot))