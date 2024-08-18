import os


class Environment:
    database_driver = os.getenv("DATABASE_DRIVER")
    database_host = os.getenv("DATABASE_HOST")
    database_name = os.getenv("DATABASE_NAME")
    secrets_config_filepath = os.getenv("SECRETS_CONFIG_FILEPATH")

    def __str__(self):
        attrs = [d for d in dir(self) if "__" not in d]
        values = [getattr(self, attr) for attr in attrs]
        zipped = zip(attrs, values)
        return str({z[0]: z[1] for z in zipped})
