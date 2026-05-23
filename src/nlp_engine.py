import os
from google import genai
from google.genai import types
from google.genai.errors import ServerError, APIError
from pypdf import PdfReader

class MedicalNLPEngine:
    def __init__(self):
        # Initializes the client using the GEMINI_API_KEY environment variable
        self.client = genai.Client()
        # Using the current stable production model
        self.model_name = "gemini-2.5-flash"

    def extract_text(self, uploaded_file):
        """Extracts text content from PDF or TXT medical reports safely."""
        try:
            if uploaded_file.name.endswith('.pdf'):
                pdf_reader = PdfReader(uploaded_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
            else:
                return uploaded_file.read().decode("utf-8")
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def generate_summary(self, report_text):
        """Generates a structured clinical summary with built-in server error defense."""
        prompt = f"""
        You are an expert medical AI assistant attached to the 'Omni Health' diagnostic platform.
        Analyze the following medical report and provide a structured, highly accurate summary.
        Translate complex medical jargon into easy-to-understand terms for the patient, 
        but maintain absolute clinical accuracy for the physician.

        Medical Report Content:
        \"\"\"{report_text}\"\"\"

        Provide your analysis in the following Markdown format:
        ## 📋 Clinical Executive Summary
        [Provide a 2-3 sentence high-level overview]

        ### 🔍 Key Biomarkers & Findings
        * **[Finding/Metric Name]:** [Value/Status] -> [Simple Explanation]

        ### ⚠️ Areas of Concern / Abnormalities
        * [List any critical high/low values, fractures, or flags found. If none, state 'No major abnormalities detected']

        ### 💡 Recommended Next Steps
        1. [Actionable lifestyle advice or medical consultations based strictly on the report]
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            return response.text
        except ServerError:
            return (
                "⚠️ **Gemini Engine is currently experiencing heavy traffic.**\n\n"
                "Google's free-tier servers are temporarily overloaded. Please wait a few seconds and "
                "click the analyze/upload button again to retry."
            )
        except Exception as e:
            return f"❌ An unexpected error occurred: {str(e)}"

    def answer_question(self, report_text, question, conversation_history=[]):
        """Answers specific user chat questions based strictly on the provided report context."""
        history_context = ""
        for role, text in conversation_history:
            history_context += f"{role}: {text}\n"

        prompt = f"""
        You are a supportive, grounded medical AI assistant. Answer the user's question accurately 
        based ONLY on the provided medical report context. If the answer cannot be confidently 
        derived from the report, state gently that the report does not contain that information 
        and advise checking with a doctor.

        Medical Report Context:
        \"\"\"{report_text}\"\"\"

        Conversation History:
        {history_context}

        User Question: {question}
        
        Answer:
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            return response.text
        except ServerError:
            return "⚠️ Google servers are currently overloaded. Unable to fetch an answer right now. Please resubmit your question in a moment."
        except Exception as e:
            return f"❌ Error: {str(e)}"