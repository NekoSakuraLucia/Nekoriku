import Nekoriku
from Nekoriku.plugins import create

create(
    module={
        "music_prefix": True
    },
    event={
        "music_event": True
    }
)

Nekoriku.setup_nodes(
    uri="http://node.lewdhutao.my.eu.org:80",
    password="youshallnotpass"
)
Nekoriku.start('MTI4MTkyMzA1NzUxODI1MjA1NQ.Gix63f.05DqAQKxhd6-y4N8BTswxL_KyNRkmCKnx-oqbg')