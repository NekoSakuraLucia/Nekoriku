import discord
from discord.ext import commands
from .colored_logging import get_logger
import wavelink
from typing import Optional

logger = get_logger('nekoriku_logger')

class BotClient(commands.Bot):
    """
    TH:
    `BotClient` Class หลักสำหรับเริ่มบอท

    EN:
    `BotClient` Main class for starting bots.

    TH / EN:
    **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
    **As for other languages You can continue adding it yourself. If you are a translator**
    """
    def __init__(self, music_slash=False, command_prefix="!>") -> None:
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=command_prefix, intents=intents)
        self.music_slash = music_slash
    
    def setup_nodes(self, uri: str, password: str) -> None:
        self.node_uri = uri
        self.node_password = password

    def setup_prefix(self, prefix: Optional[str] = None) -> None:
        if prefix is None:
            pass
        else:
            self.command_prefix = prefix

    async def on_ready(self):
        if hasattr(self, 'node_uri') and hasattr(self, 'node_password'):
            node = wavelink.Node(uri=self.node_uri, password=self.node_password)
            await wavelink.Pool.connect(nodes=[node], client=self, cache_capacity=100)

        logger.info(f"[READY] -> Logged in as {self.user} | {self.user.id}")

        if self.music_slash:
            await self.tree.sync()
            logger.info("[READY] -> Slash Commands Synced.")

        activity = discord.Activity(type=discord.ActivityType.watching, name="!>play | /play | Nekoriku v0.1")
        await self.change_presence(activity=activity)

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('ไม่มีคำสั่งนี้')
        else:
            await ctx.send('เกิดข้อผิดพลาดบางอย่าง')
    
    async def on_wavelink_node_ready(self, payload: wavelink.NodeReadyEventPayload) -> None:
        logger.info(f"[READY] -> Wavelink Node connected: {payload.node}")