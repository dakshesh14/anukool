from pydantic import BaseModel


class Query(BaseModel):
    """
    Query model types for the chat endpoint.

    Args:
        about_company (str): About the company.
        about_job (str): About the job.
    """

    company_description: str
    job_description: str


class PDFQuery(BaseModel):
    """
    PDF Query model types for the cover letter pdf generation endpoint.

    Args:
        full_name (str): Full name of the candidate.
        job_title (str): Job title of the candidate.
        content (str): Cover letter content.
    """

    full_name: str
    job_title: str
    content: str
