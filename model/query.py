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
