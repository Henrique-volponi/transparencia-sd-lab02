
import asyncio
from typing import Optional

async def fetch_user_remote(
    user_id: int,
    timeout: float = 2.0
) -> Optional[dict]:
    await asyncio.sleep(0.5)
    if user_id == 42:
        return {"id": 42, "name": "Usuario Teste"}
    return None

async def main():
    user = await fetch_user_remote(42)
    print(user)

asyncio.run(main())
