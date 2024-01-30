# fastapi imports
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# langchain imports
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts.prompt import PromptTemplate
from langchain_openai.llms import OpenAI

# local imports
from data_model.query import Query
from helper import load_environment
from ingest import get_vector_database

# loading environment
load_environment()

# settings FastAPI app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


prompt_template = """
You are expert at crafting cover letter for job applicant using the given context about the user. You don't assume anything about the user and 
you don't add fake experience in the cover letter. You are honest and you are trying to help the user to get the job.

Job description: {job_description}
Company Description: {company_description}

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

    job_description, company_description = (
        body.job_description,
        body.company_description,
    )

    chain = load_qa_chain(
        OpenAI(temperature=0),
        chain_type="stuff",
    )

    db = get_vector_database()

    # check what the user have most similar to the job description
    docs = db.similarity_search(job_description)

    prompt = PromptTemplate(
        input_variables=["job_description", "company_description"],
        template=prompt_template,
    ).format(job_description=job_description, company_description=company_description)

    result = chain.invoke(
        {
            "input_documents": docs,
            "question": prompt,
        }
    )

    return {
        "answer": result["output_text"],
    }
