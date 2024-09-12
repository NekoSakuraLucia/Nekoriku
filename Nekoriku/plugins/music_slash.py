import discord
from discord import app_commands
from discord.ext import commands
from ..colored_logging import get_logger

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

async def setup(bot: commands.Bot):
    await bot.add_cog(Nekoriku_Music_Slash(bot))