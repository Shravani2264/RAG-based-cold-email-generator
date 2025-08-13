RAG-based Cold Email Generator
In today's competitive job market, personalized outreach is key to standing out. This project is a sophisticated and automated solution for generating highly personalized cold emails for job applications. By leveraging a powerful combination of web scraping, a Retrieval-Augmented Generation (RAG) system, and a Large Language Model (LLM), this tool efficiently tailors outreach to specific job descriptions, ensuring that your most relevant skills and experiences are highlighted. It effectively eliminates the manual, time-consuming process of drafting custom emails, allowing you to focus on your job search strategy.

✨ Features
Automated Personalization: Generates unique, personalized cold emails for each job application.

Job Site Scraping: Automatically scrapes job sites to extract key details like company name, job title, and required skills.

Resume-based Skill Matching: Uses your PDF resume and a RAG (Retrieval-Augmented Generation) system with ChromaDB to find relevant skills.

Advanced Generation: Leverages LangChain and Google Gemini to craft tailored emails that highlight your strengths for the specific role.

Efficient Workflow: Drastically reduces the time and effort required to send personalized job applications.

⚙️ Tech Stack
Python: The core programming language for the entire application.

LangChain: Framework used to orchestrate the RAG pipeline and interact with the LLM.

Google Gemini: The Large Language Model used for generating the personalized email content.

ChromaDB: A vector database for storing and retrieving vectorized data from your resume.

PDF Library: A Python library (e.g., PyMuPDF or PyPDF2) to parse and extract text from your resume PDF.

Web Scraping Libraries: Libraries (e.g., Beautiful Soup, Requests) to fetch and parse job listing data from websites.

🚀 Workflow
The application follows a simple yet powerful pipeline to generate the emails:

Data Ingestion: The script reads your resume in PDF format.

Vectorization: Using a tool like langchain-community and a vector embedding model, the text from your resume is converted into numerical vectors and stored in a ChromaDB vector store.

Web Scraping: The application scrapes a specified job site to collect job descriptions.

Skill Retrieval: For each job description, a query is sent to the ChromaDB vector store to retrieve the most relevant skills from your resume.

Email Generation: The job details, along with the retrieved skills from your resume, are provided to the Google Gemini LLM via a LangChain prompt.

Personalized Output: The LLM generates a personalized cold email draft, ready for you to review and send.
