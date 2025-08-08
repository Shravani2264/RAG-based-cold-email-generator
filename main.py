import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
import os
from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(chain, portfolio):
    st.title("📧 Cold Email Generator")

    url_input = st.text_input("Enter Career Page URL :", value="https://southasiacareers.deloitte.com/go/Deloitte-India/718244/")
    USER_AGENT = os.getenv("USER_AGENT", "LangChainBot/1.0")
    submit_button = st.button("Generate Emails")


    if submit_button:
        try:
            with st.spinner("Loading and processing data..."):
                loader = WebBaseLoader(url_input, header_template={"User-Agent": USER_AGENT})
                raw_data = loader.load().pop().page_content
                cleaned_data = clean_text(raw_data)

                portfolio.load_portfolio()

                jobs = chain.extract_jobs(cleaned_data)

                print("DEBUG - Jobs extracted:", jobs)
                print("DEBUG - Type of first item:", type(jobs[0]))

                if isinstance(jobs, list) and len(jobs) == 1 and isinstance(jobs[0], list):
                    jobs = jobs[0]

                if isinstance(jobs, dict):
                    jobs = [jobs]

                st.success(f"{len(jobs)} job(s) found. Generating emails...")

                for i, job in enumerate(jobs, start=1):
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = chain.write_email(job, links)

                    with st.expander(f"✉️ Email for Job #{i}"):
                        st.code(email, language='markdown')

        except Exception as e:
            st.error(f"🚨 An Error Occurred: {e}")


if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio)
