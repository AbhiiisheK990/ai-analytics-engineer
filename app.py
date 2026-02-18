import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import os

from llm import ask_llm
from pdf_report import generate_pdf

st.set_page_config("Offline AI Analytics Engineer", layout="wide")
st.title("🤖 Offline AI Analytics Engineer")

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

        for p in plans:
            if not p["sql"].lower().startswith("select"):
                continue

            result = pd.read_sql(p["sql"], conn)
            sql_used.append(p["sql"])

            fig, ax = plt.subplots()
            if p["chart"] != "table":
                # Safe plotting: validate columns before plotting
                x_col = p["x"]
                y_col = p["y"]

                if x_col not in result.columns or y_col not in result.columns:
                    # Fallback to first two columns
                    cols = list(result.columns)

                    if len(cols) >= 2:
                        x_col = cols[0]
                        y_col = cols[1]
                    else:
                        st.warning("Not enough data to plot this chart.")
                        continue

                result.plot(kind=p["chart"], x=x_col, y=y_col, ax=ax)


            img = save_chart(fig, f"{p['section']}_{p['x']}")
            # Normalize section name to avoid KeyError
            section = p["section"].lower()

            if "executive" in section:
                section_key = "Executive"
            elif "performance" in section:
                section_key = "Performance"
            elif "risk" in section:
                section_key = "Risk"
            else:
                section_key = "Executive"  # fallback

            dashboards[section_key].append({
                "title": p["sql"],
                "image": img
            })


            st.subheader(f"{p['section']} Dashboard")
            st.code(p["sql"], language="sql")
            st.dataframe(result)
            st.pyplot(fig)

        st.session_state.dashboards = dashboards
        st.session_state.sql_used = sql_used

    # ========== CHAT ==========
    st.divider()
    question = st.text_input("Ask a business question")

    if question and "eda" in st.session_state:
        answer = ask_llm(f"""{CHAT_PROMPT}

EDA:
{st.session_state.eda}

Question:
{question}
""")
        st.subheader("🧠 AI Answer")
        st.write(answer)

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
