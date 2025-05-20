class Options(dict[str, any]):
    default_options: dict[str, any] = {
        "port": 21,
        "host": "localhost",
        "username": None,
        "password": None,
        "debug": False,
    }

    def __init__(self, **kwargs: any) -> None:
        super().__init__(self.default_options)
        self.update(kwargs)
