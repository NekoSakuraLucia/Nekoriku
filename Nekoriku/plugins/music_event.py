import discord
from discord.ext import commands
from ..colored_logging import get_logger
import wavelink

logger = get_logger('nekoriku_logger')

class Nekoriku_Music_Event(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

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
        
        track: wavelink.Playable = payload.track
        logger.info(f'[MUSIC] -> Now playing: {track.title} | Author: {track.author}')

async def setup(bot: commands.Bot):
    await bot.add_cog(Nekoriku_Music_Event(bot))