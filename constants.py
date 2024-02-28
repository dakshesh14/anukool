"""
Constants values for the app. Also loads the environment variables from the .env file.
"""

import os

# env
from envparse import env

dotenv_file = os.path.join(os.path.dirname(__file__), ".env")

if os.path.isfile(dotenv_file):
    env.read_envfile(dotenv_file)


MODEL_PATH = env.str("MODEL_PATH", default=None)
HUGGINGFACEHUB_API_TOKEN = env.str("HUGGINGFACEHUB_API_TOKEN", default=None)
USE_OPENAI = MODEL_PATH is None
OPENAI_API_KEY = env.str("OPENAI_API_KEY", default=None)

if MODEL_PATH and not HUGGINGFACEHUB_API_TOKEN:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN is required when using a custom model.")


if USE_OPENAI and not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is required when using OpenAI.")
