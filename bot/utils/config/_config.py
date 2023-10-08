import tomllib


class Config(dict):
    def __init__(self, _config: dict = None):
        try:
            if _config is None:
                config = tomllib.load(open('config.toml', 'rb'))

                super().__init__(**config)
            else:
                super().__init__(**_config)

        except FileNotFoundError:
            super().__init__()

    def __getattr__(self, item):
        return (
            self.get(item)
            if type(self.get(item)) is not dict
            else Config(self.get(item))
        )
