import asyncio
from enum import Enum

class ConnectionState(Enum):
    CONNECTED    = "connected"
    MIGRATING    = "migrating"
    RECONNECTING = "reconnecting"

class TransparentWSClient:
     def __init__(self, url):
        self.url = url
        self.state = ConnectionState.CONNECTED
        self._message_buffer = []
