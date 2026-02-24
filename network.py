import aiohttp, asyncio

class TitanNet:
    async def fetch_lib(self, url, dest):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    with open(dest, 'wb') as f:
                        f.write(data)
                    return True
        return False
      
