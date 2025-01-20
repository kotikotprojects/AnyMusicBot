from dataclasses import dataclass

from ..database import db


@dataclass
class Setting:
    name: str
    description: str
    choices: dict[str, str]
    value: str | None = None


settings_strings: dict[str, Setting] = {
    "search_preview": Setting(
        name="Search preview",
        description="Show only covers (better display), "
        "or add 30 seconds of track preview whenever possible?",
        choices={"cover": "Cover picture", "preview": "Audio preview"},
    ),
    "recode_youtube": Setting(
        name="Recode YouTube (and Spotify)",
        description="Recode when downloading from YouTube (and Spotify) to "
        "more compatible format (may take some time)",
        choices={"no": "Send original file", "yes": "Recode to libmp3lame"},
    ),
    "exact_spotify_search": Setting(
        name="Only exact Spotify matches",
        description="When searching on Youtube from Spotify, show only exact matches, "
        "may protect against inaccurate matches, but at the same time it "
        "can lose reuploaded tracks. Should be enabled always, except in "
        "situations where the track is not found on both YouTube and "
        "Deezer",
        choices={"yes": "Only exact matches", "no": "Fuzzy matches also"},
    ),
    "default_search_provider": Setting(
        name="Default search provider",
        description="Which service to use when searching without service filter",
        choices={"y": "YouTube", "d": "Deezer", "c": "SoundCloud", "s": "Spotify"},
    ),
}


@dataclass
class UserSettings:
    user_id: str | int

    def __post_init__(self):
        if type(self.user_id) is int:
            self.user_id = str(self.user_id)

        if db.settings.get(self.user_id) is None:
            db.settings[self.user_id] = dict(
                (setting, list(settings_strings[setting].choices)[0])
                for setting in settings_strings
            )

    def __getitem__(self, item):
        s = settings_strings.get(item)
        if s is None:
            return None
        try:
            s.value = db.settings[self.user_id][item]
        except KeyError:
            s.value = list(s.choices)[0]
            self[item] = s.value
        return s

    def __setitem__(self, key, value):
        h = db.settings[self.user_id]
        h[key] = value
        db.settings[self.user_id] = h
