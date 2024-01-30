import os

import dotenv


def load_environment():
    dotenv_file = os.path.join(os.path.dirname(__file__), ".env")

    if os.path.isfile(dotenv_file):
        dotenv.load_dotenv(dotenv_file)


if __name__ == "__main__":
    load_environment()
