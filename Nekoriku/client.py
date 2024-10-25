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
    **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**\n
    **As for other languages You can continue adding it yourself. If you are a translator**
    """
    def __init__(self, music_slash=False, command_prefix="!>") -> None:
        """
        EN:
        Initializes the bot with optional music slash command support and a command prefix.

        TH: 
        ฟังก์ชันนี้ใช้ในการเริ่มต้นบอท โดยสามารถกำหนดให้มีการใช้คำสั่งเพลงแบบ Slash และกำหนดคำสั่งเริ่มต้นได้

        :param music_slash: Indicates whether to enable music slash commands (default is False). / ระบุว่าจะเปิดใช้งานคำสั่งสแลชเพลงหรือไม่ (ค่าเริ่มต้นคือเท็จ)
        :param command_prefix: The prefix that will be used for bot commands (default is "!>"). / คำนำหน้าที่จะใช้สำหรับคำสั่งบอท (ค่าเริ่มต้นคือ "!>")

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**\n
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=command_prefix, intents=intents)
        self.music_slash = music_slash
    
    def setup_nodes(self, identifier: str | None, uri: str, password: str) -> None:
        """
        EN:
        Sets up the connection parameters for the music nodes.

        TH:
        ฟังก์ชันนี้ใช้ในการตั้งค่าพารามิเตอร์การเชื่อมต่อสำหรับโหนดเพลง

        :param identifier: Set the name of your Client Node. / ตั้งชื่อโหนดของคุณ
        :param uri: The URI for the node connection. / URI สำหรับการเชื่อมต่อโหนด
        :param password: The password for the node connection. / รหัสผ่านสำหรับการเชื่อมต่อโหนด

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**\n
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        self.node_identifier = identifier
        self.node_uri = uri
        self.node_password = password

    def setup_prefix(self, prefix: Optional[str] = None) -> None:
        """
        EN:
        Configures the command prefix for the bot.

        TH:
        ฟังก์ชันนี้ใช้ในการตั้งค่าคำสั่งเริ่มต้นสำหรับบอท

        :param prefix: The new command prefix to set. If None, the prefix remains unchanged. / คำนำหน้าคำสั่งใหม่ที่จะตั้งค่า หากไม่มี คำนำหน้าจะไปใช้ค่าเริ่มต้นก็คือ `"!"`

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**\n
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        if prefix is None:
            pass
        else:
            self.command_prefix = prefix

    async def on_ready(self):
        if hasattr(self, 'node_uri') and hasattr(self, 'node_password'):
            node_identifier = self.node_identifier if self.node_identifier else "Nekoriku/v0.2.4"
            node = wavelink.Node(identifier=node_identifier, uri=self.node_uri, password=self.node_password)
            await wavelink.Pool.connect(nodes=[node], client=self, cache_capacity=100)

        logger.info(f"[READY] -> Logged in as {self.user} | {self.user.id}")

        if self.music_slash:
            await self.tree.sync()
            logger.info("[READY] -> Slash Commands Synced.")

        activity = discord.Activity(type=discord.ActivityType.watching, name=f"{self.command_prefix}play | /play | Nekoriku v0.2.1")
        await self.change_presence(activity=activity)

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                description="ไม่มีคำสั่งนี้ / There is no this command.",
                color=0xFFC0CB
            )
            embed.set_author(name='There is no this command.', icon_url=f'{ctx.author.display_avatar}?size=512')
            embed.set_footer(text="ไม่มีคำสั่งนี้..", icon_url=f'{self.user.display_avatar.url}?size=256')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description="เกิดข้อผิดพลาดบางอย่าง / Something went wrong.",
                color=0xFFC0CB
            )
            embed.set_author(name='Something went wrong.', icon_url=f'{ctx.author.display_avatar}?size=512')
            embed.set_footer(text="เกิดข้อผิดพลาดบางอย่าง..", icon_url=f'{self.user.display_avatar.url}?size=256')
            await ctx.send(embed=embed)
    
    async def on_wavelink_node_ready(self, payload: wavelink.NodeReadyEventPayload) -> None:
        logger.info(f"[READY] -> Wavelink Node connected: {payload.node}")