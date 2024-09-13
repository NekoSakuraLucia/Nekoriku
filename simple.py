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
Nekoriku.start('')
