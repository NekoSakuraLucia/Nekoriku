from .client import BotClient
from typing import Optional

bot = BotClient()

def start(token: str) -> None:
    """
    TH:
    เริ่มต้นการทำงานของบอท Discord ด้วยโทเคนที่คุณกำหนด

    EN:
    Starts the Discord bot using the token you provide

    TH / EN:
    **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
    **As for other languages You can continue adding it yourself. If you are a translator**
    """
    bot.run(token)

def setup_nodes(uri: str, password: str) -> None:
    """
    TH:
    เริ่มต้นการสร้างโหนดลาวาลิงค์เพื่อให้บอทสามารถเล่นเพลงให้คุณฟังได้

    EN:
    Start creating a Lavalink node so that the bot can play music for you.

    TH / EN:
    **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
    **As for other languages You can continue adding it yourself. If you are a translator**
    """
    bot.setup_nodes(uri, password)

def setup_prefix(prefix: Optional[str] = None) -> None:
    """
    TH:
    ตั้งค่า prefix สำหรับบอท Discord

    EN:
    Sets the prefix for the Discord bot

    TH / EN:
    **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
    **As for other languages You can continue adding it yourself. If you are a translator**
    """
    bot.setup_prefix(prefix)