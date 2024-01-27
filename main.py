import os

import dotenv

# fastapi imports
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# langchain imports
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader
from langchain.prompts.prompt import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.llms import OpenAI

# pydantic
from pydantic import BaseModel


class Query(BaseModel):
    """
    Query model types for the chat endpoint.

    Args:
        about_company (str): About the company.
        about_job (str): About the job.
    """

    about_company: str
    about_job: str


dotenv_file = os.path.join(os.path.dirname(__file__), ".env")

if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


pdf = PyPDFLoader("docs/about_me.pdf")


if pdf is None:
    raise FileNotFoundError("PDF file not found")

pages = pdf.load_and_split()

text = ""
for page in pages:
    text += page.page_content

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, length_function=len
)

chunks = text_splitter.split_text(text)

pdf_name = pdf.file_path.split("/")[-1].split(".")[0]


if os.path.exists(os.path.join("outputs", pdf_name + ".pkl")):
    db = FAISS.load_local("outputs", OpenAIEmbeddings())
else:
    db = FAISS.from_texts(chunks, OpenAIEmbeddings())
    db.save_local("outputs")


template = """
You are expert at crafting cover letter for job applicant using the given context about the user. You don't assume anything about the user and 
you don't add fake experience in the cover letter. You are honest and you are trying to help the user to get the job.

About the job: {about_job}
About the company: {about_company}

Question: What is the best cover letter for this job?
"""


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Index endpoint; serves the index.html file with all the static files.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat(body: Query):
    """
    Chat endpoint; takes the user input and returns the answer/cover letter.
    """

    about_job, about_company = body.about_job, body.about_company

    chain = load_qa_chain(
        OpenAI(temperature=0),
        chain_type="stuff",
    )

    # check what the user have most similar to the job description
    docs = db.similarity_search(about_job)

    prompt = PromptTemplate(
        input_variables=["about_job", "about_company"],
        template=template,
    ).format(about_job=about_job, about_company=about_company)

    result = chain.invoke(
        {
            "input_documents": docs,
            "question": prompt,
        }
    )

    return {
        "answer": result["output_text"],
    }
