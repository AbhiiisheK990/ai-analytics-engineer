![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)
![AI Powered](https://img.shields.io/badge/AI-Powered-purple.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![Deployment](https://img.shields.io/badge/Deployment-Streamlit%20Cloud-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

# 🤖 AI Analytics Engineer – End-to-End Analytics Platform

An AI-powered analytics application that transforms raw datasets into **insights, dashboards, SQL queries, and executive reports** with minimal human intervention.

The system is designed to simulate the workflow of a **Senior Data Analyst / Analytics Engineer**, combining automated EDA, SQL generation, visualization, conversational BI, and report export.

---

## 🚀 Key Features

- 🔍 **Automated Exploratory Data Analysis (EDA)**
  - Dataset understanding
  - Data quality checks
  - Statistical summaries
  - Pattern, trend, risk, and opportunity detection

- 🧮 **AI-Generated SQL**
  - Automatic SQL query creation
  - Aggregations, grouping, and analytical queries
  - Safe execution against in-memory databases

- 📊 **Dynamic Dashboards**
  - Executive, Performance, and Risk dashboards
  - Auto-selected chart types
  - Robust handling of AI-generated edge cases

- 💬 **Conversational Business Intelligence**
  - Chat with your data in natural language
  - Context-aware responses using EDA insights
  - Follow-up questions supported

- 📄 **PDF Report Export**
  - One-click generation of executive-ready analytics reports
  - Includes insights, dashboards, and SQL appendix

- 🌐 **Online & Offline Support**
  - Offline version using a local LLM (privacy-focused)
  - Online version deployed on Streamlit Cloud (always running)

---

## 🏗️ Architecture Overview

Dataset Upload
↓
AI-Driven EDA
↓
AI SQL Generation
↓
SQL Execution
↓
Dashboards & Visualizations
↓
Conversational BI
↓
PDF Report Export


---

## 🛠️ Tech Stack

- **Frontend / App Framework**: Streamlit  
- **Data Processing**: Pandas, NumPy  
- **Visualization**: Matplotlib  
- **Database**: SQLite (in-memory)  
- **AI / LLM**:
  - Offline: Local LLM (Ollama)
  - Online: Cloud LLM (Groq / OpenAI)
- **Reporting**: ReportLab (PDF generation)
- **Version Control & Deployment**: GitHub + Streamlit Cloud  

---

## 📂 Project Structure

ai-analytics-engineer/
│
├── app.py
├── llm.py
├── pdf_report.py
├── requirements.txt
├── prompts/
│ ├── eda_prompt.txt
│ ├── sql_prompt.txt
│ └── chat_prompt.txt
└── README.md


---

## ▶️ How to Run (Online – Always Running)

1. Push the code to GitHub  
2. Deploy using **Streamlit Cloud**
3. Add API key in Streamlit **Secrets**
4. Access the permanent public URL  

No local setup required.

---

## ▶️ How to Run (Offline – Local)

1. Install Python 3.10+
2. Install dependencies
3. Run a local LLM (Ollama)
4. Start the app with:
   ```bash
   streamlit run app.py
📊 Typical User Workflow
Upload a CSV dataset

Run automated EDA

Generate AI dashboards

Ask business questions in chat

Export a PDF analytics report

🎯 Use Cases
Data Analyst / Analytics Engineer portfolios

Executive analytics demos

Business intelligence automation

Learning applied AI in analytics

Secure, offline data analysis environments

🧠 Why This Project Is Different
No hardcoded KPIs or dashboards

AI drives analysis logic end-to-end

Handles AI uncertainty with production-safe checks

Demonstrates real-world analytics engineering practices

📌 Future Enhancements
Role-based dashboards (CXO vs Analyst)

Authentication and access control

Multi-dataset joins

Alerting and KPI monitoring

Containerized deployment

📄 License
This project is intended for educational and portfolio use.
