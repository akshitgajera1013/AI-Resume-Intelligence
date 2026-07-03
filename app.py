# =========================================================================================
# 🧠 TALENT-NEXUS: EXECUTIVE ATS SCORING ENGINE (ENTERPRISE BUILD)
# Version: 3.1.0 | Build: Production/Max-Scale
# Description: Advanced AI Resume Analyzer with Real-Time Web Intelligence
# Theme: Corporate Cyber (Deep Slate + Azure/Emerald Accents)
# =========================================================================================

import streamlit as st
import os
import tempfile
import time
import base64
import uuid
from datetime import datetime
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from tavily import TavilyClient

# =========================================================================================
# 1. PAGE CONFIGURATION & INITIALIZATION
# =========================================================================================
load_dotenv()

st.set_page_config(
    page_title="TALENT-NEXUS | ATS Intelligence",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())[:8].upper()
if "analysis_complete" not in st.session_state:
    st.session_state["analysis_complete"] = False
if "report_content" not in st.session_state:
    st.session_state["report_content"] = None
if "execution_time" not in st.session_state:
    st.session_state["execution_time"] = 0.0

# =========================================================================================
# 2. ENTERPRISE CSS INJECTION (MASSIVE STYLESHEET)
# =========================================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&family=Inter:wght@300;400;500;600&family=Fira+Code:wght@400;600&display=swap');

    :root {
        --azure: #3b82f6;
        --azure-light: #60a5fa;
        --azure-dark: #1d4ed8;
        --emerald: #10b981;
        --emerald-dark: #059669;
        --slate-bg: #020617;
        --slate-surface: #0f172a;
        --glass-bg: rgba(59, 130, 246, 0.04);
        --glass-border: rgba(59, 130, 246, 0.15);
        --glow-primary: 0 0 35px rgba(59, 130, 246, 0.2);
        --text-main: #f8fafc;
        --text-muted: rgba(248, 250, 252, 0.6);
    }

    /* ── BASE TYPOGRAPHY & APP STYLE ── */
    .stApp { background: var(--slate-bg); font-family: 'Inter', sans-serif; color: var(--text-main); }
    h1, h2, h3, h4, h5, h6 { font-family: 'Space Grotesk', sans-serif; color: var(--text-main); }
    
    /* ── DYNAMIC BACKGROUND ANIMATIONS ── */
    .stApp::before {
        content: ''; position: fixed; inset: 0;
        background: 
            radial-gradient(circle at 15% 0%, rgba(59, 130, 246, 0.08) 0%, transparent 45%),
            radial-gradient(circle at 85% 100%, rgba(16, 185, 129, 0.05) 0%, transparent 45%);
        pointer-events: none; z-index: 0;
        animation: pulseBg 12s ease-in-out infinite alternate;
    }
    @keyframes pulseBg {
        0% { opacity: 0.6; transform: scale(1); }
        100% { opacity: 1; transform: scale(1.05); }
    }

    /* ── HERO SECTION ── */
    .hero { text-align: center; padding: 60px 20px 40px; position: relative; z-index: 1; animation: slideDown 0.8s both; }
    @keyframes slideDown { from { opacity: 0; transform: translateY(-30px); } to { opacity: 1; transform: translateY(0); } }
    
    .hero-badge {
        display: inline-flex; align-items: center; gap: 12px;
        background: rgba(59, 130, 246, 0.08); border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 50px; padding: 8px 24px; font-family: 'Fira Code', monospace; font-size: 11px;
        color: var(--azure-light); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 20px;
        box-shadow: var(--glow-primary);
    }
    .hero-badge-dot {
        width: 8px; height: 8px; border-radius: 50%; background: var(--azure);
        box-shadow: 0 0 12px var(--azure); animation: pulseDot 1.5s infinite;
    }
    @keyframes pulseDot { 50% { transform: scale(1.5); box-shadow: 0 0 20px var(--azure); } }

    .hero-title { font-size: clamp(35px, 5vw, 65px); font-weight: 700; line-height: 1.1; margin-bottom: 12px; letter-spacing:-1px; }
    .hero-title em { font-style: normal; background: linear-gradient(135deg, var(--azure-light), var(--emerald)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .hero-sub { font-size: 16px; font-weight: 300; color: var(--text-muted); letter-spacing: 1px; }

    /* ── GLASS PANELS ── */
    .glass-panel {
        background: var(--glass-bg); border: 1px solid var(--glass-border);
        border-radius: 20px; padding: 35px; margin-bottom: 25px; position: relative; z-index: 1;
        transition: all 0.4s ease; backdrop-filter: blur(10px);
    }
    .glass-panel:hover { border-color: rgba(59, 130, 246, 0.3); box-shadow: var(--glow-primary); transform: translateY(-2px); }
    .panel-heading { font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 700; color: var(--azure-light); letter-spacing: 1.5px; margin-bottom: 25px; border-bottom: 1px solid rgba(59, 130, 246, 0.2); padding-bottom: 15px; }

    /* ── CUSTOM BUTTON ── */
    div.stButton > button {
        width: 100% !important; background: linear-gradient(135deg, var(--azure-dark) 0%, var(--azure) 100%) !important;
        color: #ffffff !important; font-family: 'Space Grotesk', sans-serif !important; font-size: 20px !important;
        font-weight: 700 !important; letter-spacing: 3px !important; text-transform: uppercase !important;
        border: 1px solid rgba(96, 165, 250, 0.5) !important; border-radius: 16px !important; padding: 24px !important;
        transition: all 0.3s ease !important; box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3) !important; margin-top: 20px !important;
    }
    div.stButton > button:hover { transform: translateY(-3px) !important; box-shadow: 0 15px 40px rgba(59, 130, 246, 0.5) !important; border-color:#fff !important; }

    /* ── RESULT BOX ── */
    .result-box {
        background: rgba(15, 23, 42, 0.8); border: 1px solid var(--emerald);
        border-radius: 24px; padding: 50px; margin-top: 40px; position: relative;
        box-shadow: 0 0 50px rgba(16, 185, 129, 0.15); animation: popIn 0.8s cubic-bezier(0.175,0.885,0.32,1.275) both;
    }
    @keyframes popIn { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
    
    .result-header { font-family: 'Fira Code', monospace; color: var(--emerald); font-size: 14px; letter-spacing: 4px; margin-bottom: 20px; text-transform: uppercase; }

    /* ── SIDEBAR STYLING ── */
    section[data-testid="stSidebar"] { background: linear-gradient(180deg, #020617 0%, #0f172a 100%) !important; border-right: 1px solid rgba(59, 130, 246, 0.15) !important; }
    .sb-logo-text { font-family: 'Space Grotesk', sans-serif; font-size: 32px; font-weight: 800; background: linear-gradient(135deg, var(--azure-light), var(--emerald)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 2px; text-align:center; }
    .sb-title { font-family: 'Space Grotesk', sans-serif; font-size: 15px; font-weight: 700; color: var(--azure); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 16px; border-bottom: 1px solid rgba(59, 130, 246, 0.2); padding-bottom: 10px; margin-top: 30px; }

    /* ── DATANODES ANIMATION ── */
    .particles { position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden; }
    .node { position: absolute; border-radius: 50%; background: radial-gradient(circle, var(--azure-light) 0%, transparent 60%); opacity: 0.1; animation: floatNodes linear infinite; }
    .node:nth-child(1) { width: 90px; height: 90px; left: 10%; animation-duration: 25s; }
    .node:nth-child(2) { width: 50px; height: 50px; left: 30%; animation-duration: 18s; animation-delay: 5s; }
    .node:nth-child(3) { width: 120px; height: 120px; left: 80%; animation-duration: 35s; animation-delay: 2s; }
    @keyframes floatNodes { 0% { transform: translateY(110vh) scale(0.8); opacity: 0; } 20% { opacity: 0.15; } 80% { opacity: 0.15; } 100% { transform: translateY(-10vh) scale(1.2); opacity: 0; } }
</style>

<div class="particles">
    <div class="node"></div><div class="node"></div><div class="node"></div>
</div>
""", unsafe_allow_html=True)

# =========================================================================================
# 3. AI AGENT & TOOL ARCHITECTURE (VERSION-PROOF FIX)
# =========================================================================================
@st.cache_resource
def initialize_ats_engine():
    """
    Initializes the LLM and creates a ReAct Agent graph.
    Uses @st.cache_resource so we do not re-initialize the Tavily Client 
    and Mistral model on every single Streamlit re-render.
    """
    try:
        model = ChatMistralAI(model='mistral-small-latest', api_key=os.getenv("MISTRAL_API_KEY"))
        tavily_client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))
    except Exception as e:
        return None, None, f"Initialization Error: Ensure MISTRAL_API_KEY and TAVILY_API_KEY are set in .env. ({str(e)})"

    @tool
    def surfInternet(query: str) -> str:
        """
        Search the web for the candidate's GitHub profile,
        LinkedIn profile, portfolio, or any public information
        when it helps evaluate the resume against the JD.
        """
        try:
            result = tavily_client.search(query=query)
            return str(result['results'])
        except Exception as e:
            return f"Web search failed: {str(e)}"

    system_modifier = """
    You are an elite, highly experienced technical hiring manager and ATS (Applicant Tracking System) specialist. 
    Your task is to analyze a candidate's Resume against a provided Job Description (JD).
    
    If the resume contains GitHub, LinkedIn, or portfolio URLs, you MUST use the `surfInternet` tool to inspect their public footprint before generating the report. If no links exist, proceed normally.
    
    Your final output MUST be structured using professional Markdown. Include:
    1. **Estimated ATS Match Score**: Give a realistic percentage match.
    2. **Key Strengths**: Bullet points where the candidate perfectly matches the JD.
    3. **Key Weaknesses / Gaps**: Bullet points where the candidate falls short.
    4. **Web Intelligence Insights**: A brief summary of what you found on their GitHub/LinkedIn (if applicable).
    
    Maintain a highly professional, clinical, and objective tone.
    """
    
    try:
        # Create the agent without the state_modifier to avoid version conflicts
        agent = create_react_agent(
            model=model,
            tools=[surfInternet]
        )
        return agent, system_modifier, "Success"
    except Exception as e:
        return None, None, f"Agent Creation Error: {str(e)}"

# Boot the engine and unpack all 3 variables
ats_agent, system_modifier, engine_status = initialize_ats_engine()

# =========================================================================================
# 4. SIDEBAR TELEMETRY
# =========================================================================================
with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding:10px 0 20px;'>
            <div class="sb-logo-text">TALENT-NEXUS</div>
            <div style="font-family:'Fira Code'; font-size:10px; color:var(--text-muted); letter-spacing:2px; margin-top:5px;">INTELLIGENT RECRUITMENT TERMINAL</div>
            <div style="font-family:'Fira Code'; font-size:9px; color:rgba(255,255,255,0.3); margin-top:5px;">SESSION ID: {}</div>
        </div>
    """.format(st.session_state["session_id"]), unsafe_allow_html=True)
    
    st.markdown('<div class="sb-title">📡 System Diagnostics</div>', unsafe_allow_html=True)
    
    if ats_agent:
        st.markdown('<div style="background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3); padding:15px; border-radius:10px; text-align:center;"><span style="color:#10b981; font-weight:bold; font-family:\'Space Grotesk\';">🟢 NEURAL ENGINE ONLINE</span></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background:rgba(15,23,42,0.6); padding:15px; border-radius:10px; border:1px solid rgba(59,130,246,0.2); font-size:12px; color:rgba(248,250,252,0.7); line-height:1.6; margin-top:15px;">
            <b>LLM Core:</b> Mistral-Small-Latest<br>
            <b>Agent Type:</b> ReAct (Reason + Act)<br>
            <b>Search API:</b> Tavily Intelligence<br>
            <b>Parser:</b> PyPDF Document Loader<br>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error(f"🔴 Offline: {engine_status}")

# =========================================================================================
# 5. HERO HEADER & MAIN INTERFACE
# =========================================================================================
st.markdown("""
    <div class="hero">
        <div class="hero-badge"><div class="hero-badge-dot"></div>Autonomous Tool-Calling Agent</div>
        <div class="hero-title">Executive <em>ATS Scoring</em> Engine</div>
        <div class="hero-sub">Upload candidate artifacts to automatically cross-reference against job requirements with live web intelligence.</div>
    </div>
""", unsafe_allow_html=True)

# Layout for Inputs
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="glass-panel"><div class="panel-heading">📄 1. Candidate Artifact (PDF)</div>', unsafe_allow_html=True)
    uploaded_pdf = st.file_uploader("Upload Resume", type=['pdf'], label_visibility="collapsed")
    if uploaded_pdf:
        st.success(f"Loaded: {uploaded_pdf.name}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-panel"><div class="panel-heading">🎯 2. Requisition Profile (JD)</div>', unsafe_allow_html=True)
    job_description = st.text_area("Job Description", height=150, placeholder="Paste the complete Job Description, technical requirements, and responsibilities here...", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================================================
# 6. EXECUTION LOGIC & FILE HANDLING
# =========================================================================================
_, btn_col, _ = st.columns([1, 2, 1])

with btn_col:
    analyze_btn = st.button("🧬 SYNTHESIZE ATS EVALUATION")

if analyze_btn:
    if not ats_agent:
        st.error("Cannot proceed: The AI Engine is offline. Check your API keys.")
    elif not uploaded_pdf:
        st.warning("⚠️ Critical: Missing Applicant Resume. Please upload a PDF.")
    elif not job_description.strip():
        st.warning("⚠️ Critical: Missing Job Description. Provide text for evaluation.")
    else:
        # Reset state for fresh run
        st.session_state["analysis_complete"] = False
        st.session_state["report_content"] = None
        
        with st.status("Initializing Talent-Nexus protocol...", expanded=True) as status:
            try:
                start_time = time.time()
                
                # Step 1: Safely write the uploaded PDF to a temporary file
                status.update(label="Extracting vectorized text from PDF artifact...")
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_pdf.getvalue())
                    tmp_file_path = tmp_file.name
                
                # Step 2: Use PyPDFLoader to parse the document
                loader = PyPDFLoader(tmp_file_path)
                docs = loader.load()
                resume_text = " ".join([doc.page_content for doc in docs])
                
                # Cleanup the temporary file immediately after reading
                os.unlink(tmp_file_path)
                
                # Step 3: Construct the final payload for the Agent
                prompt_payload = f"Candidate Resume:\n<resume>\n{resume_text}\n</resume>\n\nTarget Job Description:\n<jd>\n{job_description}\n</jd>"
                
                # Step 4: Invoke the LangGraph ReAct Agent (Passing SystemMessage dynamically)
                status.update(label="Agent reasoning and executing web searches via Tavily...")
                response = ats_agent.invoke({
                    "messages": [
                        SystemMessage(content=system_modifier),
                        HumanMessage(content=prompt_payload)
                    ]
                })
                
                end_time = time.time()
                
                # Save to session state
                st.session_state["report_content"] = response["messages"][-1].content
                st.session_state["execution_time"] = round(end_time - start_time, 2)
                st.session_state["analysis_complete"] = True
                
                status.update(label="Analysis Successfully Synthesized!", state="complete", expanded=False)
                
            except Exception as e:
                status.update(label="Critical Error Encountered", state="error", expanded=False)
                st.error(f"Inference Pipeline Error: {str(e)}")

# =========================================================================================
# 7. OUTPUT RENDERING & EXPORT
# =========================================================================================
if st.session_state["analysis_complete"] and st.session_state["report_content"]:
    report_md = st.session_state["report_content"]
    
    st.markdown(f"""
        <div class="result-box">
            <div class="result-header">✅ INTELLIGENCE REPORT GENERATED | LATENCY: {st.session_state["execution_time"]}s</div>
    """, unsafe_allow_html=True)
    
    # Render the markdown generated by Mistral
    st.markdown(report_md)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Download Button Logic
    st.markdown("<br>", unsafe_allow_html=True)
    col_dl1, col_dl2, col_dl3 = st.columns([1,2,1])
    with col_dl2:
        b64_md = base64.b64encode(report_md.encode()).decode()
        dl_link = f'<a href="data:text/markdown;base64,{b64_md}" download="ATS_Report_{st.session_state["session_id"]}.md" style="display:block; text-align:center; padding:15px; background:linear-gradient(135deg, var(--emerald-dark), var(--emerald)); color:white; text-decoration:none; font-family:\'Space Grotesk\'; font-weight:700; font-size:16px; border-radius:12px; letter-spacing:2px; box-shadow:0 10px 25px rgba(16,185,129,0.3);">⬇️ DOWNLOAD REPORT (MARKDOWN)</a>'
        st.markdown(dl_link, unsafe_allow_html=True)

# =========================================================================================
# 8. GLOBAL FOOTER
# =========================================================================================
st.markdown(
    """
    <div style="text-align:center; padding:60px; margin-top:80px; border-top:1px solid rgba(59,130,246,0.15); font-family:'Fira Code'; font-size:12px; color:rgba(248,250,252,0.3); letter-spacing:3px; text-transform:uppercase;">
        &copy; 2026 | Developed by Akshit Gajera | ATS Intelligence Terminal v3.1<br>
        <span style="color:rgba(59,130,246,0.5); font-size:10px; display:block; margin-top:10px;">Powered by Mistral AI, LangGraph, & Tavily Intelligence</span>
    </div>
    """,
    unsafe_allow_html=True,
)