import os

import dotenv
from langchain.llms.ctransformers import CTransformers
from langchain_openai.llms import OpenAI


def load_environment():
    """
    Load environment variables from the .env file.
    """
    dotenv_file = os.path.join(os.path.dirname(__file__), ".env")

    if os.path.isfile(dotenv_file):
        dotenv.load_dotenv(dotenv_file)


def load_model(
    temperature=0,
):
    """
    Load the model from the environment variables.
    """

    load_environment()

    MODEL_NAME = os.environ.get("MODEL_NAME", "openai-gpt")

    if MODEL_NAME == "openai-gpt":
        return OpenAI(
            temperature=temperature,
        )

    return CTransformers(
        model=f"models/{MODEL_NAME}",
        model_type="llama",
        max_new_tokens=1024,
        temperature=temperature,
        config={
            "context_length": 2048,
        },
    )
