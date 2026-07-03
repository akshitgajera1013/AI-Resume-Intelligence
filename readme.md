# 🧠 AI-Resume-Intelligence

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/Agent-LangGraph-green.svg)](https://python.langchain.com/)
[![Mistral](https://img.shields.io/badge/LLM-Mistral_AI-orange.svg)](https://mistral.ai/)
[![Tavily](https://img.shields.io/badge/Search-Tavily_API-blueviolet.svg)](https://tavily.com/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)

An enterprise-grade, autonomous AI recruitment tool designed to critically evaluate candidate resumes against complex Job Descriptions (JDs). 

Built using a modern **LangGraph ReAct (Reason + Act)** agent framework, this engine does not just analyze the provided text. It actively utilizes the **Tavily Search API** as an integrated tool to dynamically search the web, verifying the candidate's GitHub, LinkedIn, and public portfolio projects in real-time before synthesizing its final evaluation.

## ✨ Core Architecture & Features

* 🧠 **Autonomous Web Verification:** If a resume contains links or references to external projects, the agent automatically triggers internet searches via Tavily to validate the candidate's real-world footprint and open-source contributions.
* 📊 **ATS Match Scoring:** Provides a structured, clinical report detailing a predicted ATS percentage match, core strengths, and critical gaps.
* 📄 **Native PDF Processing:** Seamlessly ingests uploaded resume PDFs via `PyPDFLoader`, utilizing secure OS-level temporary file streaming to prevent local memory leaks.
* 🛡️ **Version-Proof Agent Routing:** Utilizes robust state modifiers and dynamic `SystemMessage` injection to ensure stability across different LangGraph library versions.
* 🎨 **Immersive Cyber UI:** Features a custom "Corporate Cyber" CSS architecture utilizing glassmorphism, responsive grid layouts, and dynamic loading states.

## 🏗️ Repository Structure

📦 ai-resume-intelligence

    ┣ 📜 app.py                  # Streamlit UI & LangGraph Agent Logic
    ┣ 📜 requirements.txt        # Project Dependencies
    ┣ 📜 .env                    # Hidden API Keys (Mistral & Tavily)
    ┣ 📜 .gitignore              # Git Ignore Directives
    ┗ 📜 README.md               # Project Documentation


🚀 Local Installation & Setup

1. Clone the repository

        git clone [https://github.com/akshitgajera1013/ai-resume-intelligence.git](https://github.com/akshitgajera1013/AI-Resume-Intelligence.git)

    cd AI-Resume-Intelligence

2. Configure Environment Variables
Create a .env file in the root directory. You must supply your own API keys for the LLM and the Search engine.

MISTRAL_API_KEY="your_mistral_api_key_here"
TAVILY_API_KEY="your_tavily_api_key_here"

3. Create a Virtual Environment & Install Dependencies

        python -m venv venv

# Windows Activation:

    venv\Scripts\activate

# Mac/Linux Activation:

    source venv/bin/activate

    pip install -r requirements.txt


4. Launch the Intelligence Terminal

Start the local Streamlit application server:

    streamlit run app.py

The ATS terminal will automatically open in your default web browser at http://localhost:8501.

Disclaimer: This software is an educational portfolio project simulating autonomous machine learning architectures. It should be used to augment human resource pipelines, not replace human hiring decisions.