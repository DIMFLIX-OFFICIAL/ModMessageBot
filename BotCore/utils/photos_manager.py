import aiofiles
from aiogram.types import BufferedInputFile


class Photo:
    @classmethod
    async def file(cls, filename: str = "main.jpg"):
        async with aiofiles.open("General/assets/" + filename, 'rb') as f:
            photo = await f.read()

        return BufferedInputFile(photo, "photo")
