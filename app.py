import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import os

from llm import ask_llm
from pdf_report import generate_pdf

st.set_page_config("AI Data Analyst", layout="wide")
st.title("🤖 AI Data Analyst")

# --------- Chat history state ---------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- UTILS ----------------
def save_chart(fig, name):
    os.makedirs("charts", exist_ok=True)
    path = f"charts/{name}.png"
    fig.savefig(path, bbox_inches="tight")
    return path

def parse_sql_plan(text):
    plans = []
    blocks = text.split("QUERY")
    for b in blocks[1:]:
        try:
            sql = b.split("SQL:")[1].split("CHART:")[0].strip()
            chart = b.split("CHART:")[1].split("X:")[0].strip()
            x = b.split("X:")[1].split("Y:")[0].strip()
            y = b.split("Y:")[1].split("SECTION:")[0].strip()
            section = b.split("SECTION:")[1].strip()
            plans.append({"sql": sql, "chart": chart, "x": x, "y": y, "section": section})
        except:
            pass
    return plans

# ---------------- LOAD PROMPTS ----------------
with open("prompts/eda_prompt.txt") as f:
    EDA_PROMPT = f.read()
with open("prompts/sql_exec_prompt.txt") as f:
    SQL_PROMPT = f.read()
with open("prompts/chat_prompt.txt") as f:
    CHAT_PROMPT = f.read()

# ---------------- FILE UPLOAD ----------------
file = st.file_uploader("Upload CSV Dataset", type="csv")

if file:
    df = pd.read_csv(file)
    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head())

    conn = sqlite3.connect(":memory:")
    df.to_sql("data", conn, index=False, if_exists="replace")

    # ========== EDA ==========
    if st.button("Run AI End-to-End EDA"):
        schema = df.dtypes.astype(str).to_string()
        stats = df.describe(include="all").to_string()
        missing = df.isnull().sum().to_string()

        eda_input = f"""{EDA_PROMPT}

Schema:
{schema}

Missing:
{missing}

Stats:
{stats}
"""
        st.session_state.eda = ask_llm(eda_input)

    if "eda" in st.session_state:
        st.subheader("📊 AI EDA Report")
        st.write(st.session_state.eda)

    # ========== DASHBOARDS ==========
    
    if "eda" in st.session_state and st.button("Build AI Dashboards"):
        sql_input = f"""{SQL_PROMPT}

Table: data
Columns:
{df.dtypes.astype(str)}

EDA:
{st.session_state.eda}
"""
        sql_plan = ask_llm(sql_input)
        plans = parse_sql_plan(sql_plan)

        dashboards = {"Executive": [], "Performance": [], "Risk": []}
        sql_used = []
        def is_valid_dashboard(result_df, chart_type, x_col, y_col):
            # Must have data
            if result_df is None or result_df.empty:
                return False

            # Must have at least 2 columns
            if result_df.shape[1] < 2:
                return False

            # Must have more than 1 row for charts
            if chart_type != "table" and len(result_df) < 2:
                return False

            # X and Y must exist
            if chart_type != "table":
                if x_col not in result_df.columns or y_col not in result_df.columns:
                    return False

                # Y must be numeric
                if not pd.api.types.is_numeric_dtype(result_df[y_col]):
                    return False

                # Avoid flat / constant plots
                if result_df[y_col].nunique() <= 1:
                    return False

            return True
    
        for p in plans:
            if not p["sql"].lower().startswith("select"):
                continue

            try:
                result = pd.read_sql(p["sql"], conn)
            except Exception:
                continue  # skip invalid SQL

            chart = p["chart"]
            x_col = p["x"]
            y_col = p["y"]

            # Validate dashboard BEFORE plotting
            if not is_valid_dashboard(result, chart, x_col, y_col):
                continue

            sql_used.append(p["sql"])

            # Normalize section
            section = p["section"].lower()
            if "executive" in section:
                section_key = "Executive"
            elif "performance" in section:
                section_key = "Performance"
            elif "risk" in section:
                section_key = "Risk"
            else:
                section_key = "Executive"

            # Render
            fig, ax = plt.subplots()

            if chart == "table":
                st.subheader(f"{section_key} Dashboard")
                st.code(p["sql"], language="sql")
                st.dataframe(result)
            else:
                result.plot(kind=chart, x=x_col, y=y_col, ax=ax)
                img = save_chart(fig, f"{section_key}_{x_col}")

                dashboards[section_key].append({
                    "title": p["sql"],
                    "image": img
                })

                st.subheader(f"{section_key} Dashboard")
                st.code(p["sql"], language="sql")
                st.pyplot(fig)

# ========== CHAT ==========
st.divider()
st.subheader("💬 Chat With Your Data")

question = st.text_input("Ask a business question")

if question and "eda" in st.session_state:
    # Add user message to memory
    st.session_state.chat_history.append({
        "role": "user",
        "content": question
    })

    # Build conversation context
    conversation = f"{CHAT_PROMPT}\n\nEDA:\n{st.session_state.eda}\n\nConversation:\n"

    for msg in st.session_state.chat_history:
        conversation += f"{msg['role'].upper()}: {msg['content']}\n"

    answer = ask_llm(conversation)

    # Add AI reply to memory
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": answer
    })

# Display chat history
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"**🧑 You:** {msg['content']}")
    else:
        st.markdown(f"**🤖 AI:** {msg['content']}")

# Clear chat history
if st.button("🧹 Clear Chat History"):
    st.session_state.chat_history = []

    # ========== PDF EXPORT ==========
    if "dashboards" in st.session_state and st.button("📄 Export Full AI Report (PDF)"):
        generate_pdf(
            "AI_Analytics_Report.pdf",
            st.session_state.eda,
            st.session_state.dashboards,
            st.session_state.sql_used
        )

        with open("AI_Analytics_Report.pdf", "rb") as f:
            st.download_button(
                "⬇ Download PDF Report",
                f,
                file_name="AI_Analytics_Report.pdf"
            )
