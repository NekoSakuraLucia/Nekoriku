from typing import Dict
from ..bot import bot
import asyncio

def create(module: Dict[str, bool], event: Dict[str, bool]):
    """
    TH:
    `Nekoriku_create` เป็นฟังก์ชันการสร้างโมดูล หรือ อีเว้นท์ ของการโหลดคำสั่งหรือเหตุการณ์ของบอท 
    เช่นหากคุณต้องการ prefix คุณก็สามารถกำหนดด้วยตัวเองได้ หรือใช้ค่าเริ่มต้นคือ prefix, slash จะเป็น True ทั้งสองบอทก็จะสามารถใช้ได้ทั้ง prefix และ slash

    EN:
    The `Nekoriku_create` function is used for creating modules or events related to loading commands or bot events. 
    For example, if you want to set a prefix, you can specify it yourself or use the default value. Both bots can use both prefix and slash commands 
    if the slash option is set to True.

    TH / EN:
    **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
    **As for other languages You can continue adding it yourself. If you are a translator**
    """
    loop = asyncio.get_event_loop()
    if module.get("music_prefix"):
        loop.run_until_complete(load_cog('Nekoriku.plugins.music_prefix'))
    if module.get("music_slash"):
        bot.music_slash = True
        loop.run_until_complete(load_cog('Nekoriku.plugins.music_slash'))
    
    if event.get("music_event"):
        loop.run_until_complete(load_cog('Nekoriku.plugins.music_event'))

async def load_cog(cog_path: str):
    """
    TH:
    `Load_Cog` โหลดคำสั่งทั้งหมด

    EN:
    `Load_Cog` loads all commands.

    TH / EN:
    **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
    **As for other languages You can continue adding it yourself. If you are a translator**
    """
    try:
        await bot.load_extension(cog_path)
    except Exception as e:
        print(f"Failed to load extension {cog_path}: {e}")