import os
import uuid
import PyPDF2
import chromadb

class Portfolio:
    def __init__(self, file_path=r"C:\Users\Admin\Desktop\langchain\cold-email-generator\resource\newResume.pdf"):
        self.file_path = file_path
        self.resume_text = self.extract_text_from_pdf(file_path)

        if not self.resume_text.strip():
            raise ValueError("Resume PDF seems to be empty or unreadable.")

        self.chroma_client = chromadb.PersistentClient(path="vectorstore")
        try:
            self.chroma_client.delete_collection(name="portfolio")
        except:
            pass
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def extract_text_from_pdf(self, file_path):
        text = ""
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text.strip() + "\n"
        return text

    def load_portfolio(self):
        if self.collection.count() == 0:
            self.collection.add(
                documents=[self.resume_text],
                ids=[str(uuid.uuid4())]
            )
            print("Resume loaded and added to ChromaDB collection.")

    def query_links(self, skills_list):
        relevant_resume_sections = []
        for skills in skills_list:
            results = self.collection.query(query_texts=[skills], n_results=1).get('documents', [])
            if results and results[0]:
                relevant_resume_sections.append(results[0][0])
            else:
                relevant_resume_sections.append("")
        return relevant_resume_sections
