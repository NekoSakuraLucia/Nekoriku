import discord
from discord.ext import commands
from ..colored_logging import get_logger
import wavelink
import asyncio

logger = get_logger('nekoriku_logger')

class Nekoriku_Music_Event(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.timeout_task = None

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        if logger:
            logger.info('[READY] -> Music_Event is ready.')
        else:
            raise RuntimeError("TH: Logger ไม่ได้ถูกติดตั้งอย่างถูกต้อง / EN: Logger is not initialized.")

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload) -> None:
        player: wavelink.Player | None = payload.player
        if not player:
            return
        
        if self.timeout_task:
            self.timeout_task.cancel()
            
        track: wavelink.Playable = payload.track
        logger.info(f'[MUSIC] -> Now playing: {track.title} | Author: {track.author}')

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEndEventPayload) -> None:
        player = payload.player
        if not player:
            return
        
        if player.queue.is_empty:
            if self.timeout_task:
                self.timeout_task.cancel()
            
            async def wait_and_disconnect():
                try:
                    await asyncio.sleep(30)
                    if player.queue.is_empty:
                        await player.disconnect()
                        logger.info("[MUSIC] -> Queue is empty. Player disconnected.")
                except asyncio.CancelledError:
                    pass

            self.timeout_task = self.bot.loop.create_task(wait_and_disconnect())
        else:
            if self.timeout_task:
                self.timeout_task.cancel()
            
            next_track = player.queue.get()
            await player.play(next_track)
            logger.info(f"[MUSIC] -> Queue is not empty. Playing next track: {next_track.title}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Nekoriku_Music_Event(bot))