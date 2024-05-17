from aiogram.filters import Filter
from aiogram.types import Message

class NumberFilter(Filter):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    async def __call__(self, message: Message) -> bool:
        try:
            num = int(message.text)
            return self.min_value <= num <= self.max_value
        except ValueError:
            return False