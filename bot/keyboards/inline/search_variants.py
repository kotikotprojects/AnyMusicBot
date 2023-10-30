from aiogram.utils.keyboard import (InlineKeyboardMarkup, InlineKeyboardButton,
                                    InlineKeyboardBuilder)


deezer = {
    'd': '🎵 Search in Deezer'
}
soundcloud = {
    'c': '☁️ Search in SoundCloud'
}
youtube = {
    'y': '▶️ Search in YouTube'
}
spotify = {
    's': '🎧 Search in Spotify'
}


def get_search_variants_kb(
        query: str,
        services: dict[str, str],
) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=services[key],
                switch_inline_query_current_chat=f'{key}:{query}'
            )
        ] for key in services.keys()
    ]

    return InlineKeyboardBuilder(buttons).as_markup()
