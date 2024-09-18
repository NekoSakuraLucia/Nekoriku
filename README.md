# Nekoriku

<p align="center">
    <img src="/images/image.jpg" alt="Nekoriku" />
</p>

<p align="center">
    <a href="https://pypi.org/project/nekoriku/" target="_blank">
        <img src="https://badge.fury.io/py/nekoriku.svg" alt="Nekoriku" />
    </a>
</p>

### TH:
แพ็คเกจของเราใช้ discord.py และ wavelink เป็นฐานในการทำบอท

### EN:
Our package uses discord.py and wavelink as the base for bots.

## Installation
```
python3 -m pip install nekoriku
```

## Example:
```py
# Default Prefix: !>

import Nekoriku
from Nekoriku.plugins import create

create(
    module={
        "music_prefix": True,
        "music_slash": True
    },
    event={
        "music_event": True
    }
)

Nekoriku.setup_nodes(
    uri="",
    password=""
)
Nekoriku.start('โทเค้นบอทของคุณ / YOUR_BOT_TOKEN')
```


### TH:
`Nekoriku` เป็นแพ็คเกจสำหรับบอทดิสคอร์ดที่อำนวยความสะดวก สำหรับคนที่อยากได้บอทเพลง
แต่ไม่อยากทำเอง แต่อยากได้บอทเพลงแบบมีทั้ง prefix, slash แต่เนโกะริคุมีให้พร้อม ไม่ต้องเขียนโค้ดเอง
setup ง่ายมากแค่โค้ดไม่กี่บรรทัดคุณก็ได้บอทเพลงของคุณที่พร้อมทำงาน

### EN:
`Nekoriku` is a package for convenient discord bots. For people who want a music bot
But I don't want to do it myself. But I want a music bot with prefix and slash, but Nekoriku has it ready. No need to write code yourself.
The setup is very easy, just a few lines of code and you have your music bot ready to work.

# WARNING ❗
TH: ไม่แนะนำให้เอาไปใช้งานจริง เพราะอาจซ้ำกับบอทตัวอื่นได้..

EN: It is not recommended to use it for real use. Because it may be duplicated with other bots..








###### &copy; 2024 - Nekoriku