from aiogram.filters import BaseFilter
from aiogram.types import InlineQuery


class ServiceSearchFilter(BaseFilter):
    def __init__(self, service_letter: str):
        self.service_letter = f'{service_letter}:'

    async def __call__(self, inline_query: InlineQuery):
        return (
                inline_query.query.startswith(self.service_letter) and
                inline_query.query != self.service_letter
        )
