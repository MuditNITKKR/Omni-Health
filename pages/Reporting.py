import streamlit as st
import os
from src.nlp_engine import MedicalNLPEngine
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

st.set_page_config(page_title="Omni Health | Report Analyzer", layout="wide")

# Ensure API Key is available in environment or via sidebar fallback
if "GEMINI_API_KEY" not in os.environ and not st.sidebar.text_input("Enter Gemini API Key", type="password", key="temp_key"):
    st.warning("Please set the `GEMINI_API_KEY` environment variable or enter it in the sidebar to run this module.")
    st.stop()

if st.session_state.get("temp_key"):
    os.environ["GEMINI_API_KEY"] = st.session_state["temp_key"]

# Initialize the backend engine cleanly using cache
@st.cache_resource
def get_nlp_engine():
    return MedicalNLPEngine()

nlp_engine = get_nlp_engine()

st.title("✍️ Medical Report Analyzer & RAG Chat")
st.caption("Upload patient reports (PDF/TXT) for contextual summaries and instant clinical Q&A.")

# Check for transferred data from the Detection/Vision page
passed_findings = st.session_state.get('last_findings', None)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 Upload Document")
    uploaded_file = st.file_uploader("Choose medical report...", type=["pdf", "txt"])
    
    if passed_findings:
        st.info("💡 Received diagnostic findings from the Neural Imaging Suite!")
        if st.button("Clear Vision Suite Cache"):
            del st.session_state['last_findings']
            st.rerun()

with col2:
    st.subheader("📊 Automated Analysis")
    
    report_content = ""
    if uploaded_file:
        with st.spinner("Extracting and parsing medical document..."):
            report_content = nlp_engine.extract_text(uploaded_file)
    elif passed_findings:
        # Fallback text block using shared session data from vision suite
        report_content = "Vision Model Automated Findings:\n" + "\n".join([f"- {f['Condition']}: Confidence {f['Confidence']}" for f in passed_findings])

    if report_content:
        # Prevent continuous processing loops on UI re-renders
        if "current_summary" not in st.session_state or st.session_state.get("last_processed") != report_content:
            with st.spinner("Gemini Engine generating clinical summary..."):
                st.session_state["current_summary"] = nlp_engine.generate_summary(report_content)
                st.session_state["last_processed"] = report_content
        
        st.markdown(st.session_state["current_summary"])
    else:
        st.info("Awaiting medical document or cross-page clinical diagnostics input.")

# --- RAG INTERACTIVE CHAT SECTION ---
if report_content:
    st.divider()
    st.subheader("💬 Ask Questions About This Report")
    
    # Initialize UI state logs for chat tracking
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display prior conversational logging threads
    for role, text in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(text)

    # Chat Input handler
    if user_query := st.chat_input("e.g., What does the fasting glucose level imply?"):
        with st.chat_message("user"):
            st.write(user_query)
        st.session_state.chat_history.append(("user", user_query))

        with st.chat_message("assistant"):
            with st.spinner("Reviewing report context..."):
                # --- ULTIMATE FRONTEND FAILSAFE WRAPPER ---
                try:
                    answer = nlp_engine.answer_question(
                        report_content, 
                        user_query, 
                        st.session_state.chat_history[:-1]
                    )
                except Exception:
                    # Catches any untamed Tenacity/SDK errors escaping backend blocks
                    answer = "⚠️ The AI service is experiencing a temporary traffic spike. Please click send again to resubmit your question."
                # --- END WRAPPER ---
                
                st.write(answer)
        st.session_state.chat_history.append(("assistant", answer))