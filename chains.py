import os

from langchain_core.exceptions import OutputParserException
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
load_dotenv()
os.getenv("GOOGLE_API_KEY")



class Chain:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the 
            following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):    
            """
        )

        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={'page_data': cleaned_text})

        try:
            json_parser = JsonOutputParser()
            json_res = json_parser.parse(res.content)
        except OutputParserException as e:
            raise OutputParserException(e)

        if isinstance(json_res, dict):
            return [json_res]  # single job
        elif isinstance(json_res, list):
            return json_res  # multiple jobs
        else:
            raise ValueError("Unexpected format returned from LLM.")

    def write_email(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB POSTING DETAILS:
            {job_posting}

            ### RELEVANT RESUME SECTIONS:
            {links}

            ### INSTRUCTION:
            You are Shravani Khopade, an undergraduate B.E. student.
            Your job is to write a cold email to the HR department of the company for this specific job posting.
            You are looking for an internship opportunity.
            Tailor the email to express your interest in this internship, highlighting how your skills and aspirations, as described in the relevant resume sections provided, align with the requirements of this job posting.
            Do not provide a preamble.

            ### EMAIL (NO PREAMBLE):
            """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({'job_posting': job, 'links': links})
        print("🔮 Gemini response:", res.content)
        return res.content
