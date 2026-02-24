import aiohttp, asyncio, os

class TitanNetwork:
    def __init__(self, cache_dir):
        self.cache_dir = cache_dir

    async def fast_load(self, url, name):
        path = os.path.join(self.cache_dir, name)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    with open(path, 'wb') as f:
                        while chunk := await resp.content.read(65536):
                            f.write(chunk)
                    return True, path
        return False, "Error"
      
