"""
TH:
`Nekoriku` เป็นแพ็คเกจสำหรับบอทดิสคอร์ดที่อำนวยความสะดวก สำหรับคนที่อยากได้บอทเพลง
แต่ไม่อยากทำเอง แต่อยากได้บอทเพลงแบบมีทั้ง prefix, slash แต่เนโกะริคุมีให้พร้อม ไม่ต้องเขียนโค้ดเอง
setup ง่ายมากแค่โค้ดไม่กี่บรรทัดคุณก็ได้บอทเพลงของคุณที่พร้อมทำงาน (ซึ่งสร้างโดยคนไทย ผมเองแหละ555 Neko Sakura Lucia ฝากด้วยครับ/ค่ะ)

EN:
`Nekoriku` is a package for convenient discord bots. For people who want a music bot
But I don't want to do it myself. But I want a music bot with prefix and slash, but Nekoriku has it ready. No need to write code yourself.
The setup is very easy, just a few lines of code and you have your music bot ready to work. (Which was created by a Thai person, myself, haha. Neko Sakura Lucia, please give it to me.)

TH / EN:
**ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
**As for other languages You can continue adding it yourself. If you are a translator**

&copy; 2024 • Nekoriku (Made by: NekoSakuraLucia)
"""
from .bot import start, setup_nodes, setup_prefix
from .plugins import create