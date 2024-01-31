import os

import dotenv

# fastapi imports
from fastapi.templating import Jinja2Templates

# langchain imports
from langchain.llms.ctransformers import CTransformers
from langchain_openai.llms import OpenAI

# for pdf generation
from xhtml2pdf import pisa


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


def render_to_pdf(
    template_engine: Jinja2Templates,
    template_src: str,
    context_dict: dict,
):
    """
    Shortcut function to render a template into a PDF.
    Returns PDF value.

    Args:
        template_engine (Jinja2Templates): Jinja2Templates instance.
        template_src (str): Template source.
        context_dict (dict): Context dictionary.

    """

    html = template_engine.get_template(template_src).render(context_dict)

    pdf_data = pisa.CreatePDF(
        html,
        encoding="utf-8",
        raise_exception=True,
    )

    return pdf_data.dest.getvalue()
