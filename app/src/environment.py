import os


class Environment:
    database_driver = os.getenv("DATABASE_DRIVER")
    database_host = os.getenv("DATABASE_HOST")
    database_name = os.getenv("DATABASE_NAME")
