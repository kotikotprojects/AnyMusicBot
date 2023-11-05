from dataclasses import dataclass
from ..database import db


@dataclass
class Setting:
    name: str
    description: str
    choices: dict[str, str]
    value: str | None = None


settings_strings: dict[str, Setting] = {
    'search_preview': Setting(
        name='Search preview',
        description='Show only covers (better display), '
                    'or add 30 seconds of track preview whenever possible?',
        choices={
            'cover': 'Cover picture',
            'preview': 'Audio preview'
        },
    ),
    'recode_youtube': Setting(
        name='Recode YouTube (and Spotify)',
        description='Recode when downloading from YouTube (and Spotify) to '
                    'more compatible format (may take some time)',
        choices={
            'no': 'Send original file',
            'yes': 'Recode to libmp3lame'
        },
    )
}


@dataclass
class UserSettings:
    user_id: str

    def __post_init__(self):
        if db.settings.get(self.user_id) is None:
            db.settings[self.user_id] = dict(
                (setting, list(settings_strings[setting].choices)[0]) for setting in
                settings_strings
            )

    def __getitem__(self, item):
        s = settings_strings.get(item)
        if s is None:
            return None
        s.value = db.settings[self.user_id][item]
        return s

    def __setitem__(self, key, value):
        db.settings[self.user_id][key] = value
