import streamlit as st
from agent import build_agent

st.set_page_config(page_title="Research Agent — Manish Cheeti", layout="wide")

# ── Custom CSS ───────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400&display=swap');

    html, body, [class*="css"] {
    background-color: #f5f2ee !important;
    color: #1a1a1a !important;
    font-family: 'DM Mono', monospace !important;
}

p, span, div, label, input {
    color: #1a1a1a !important;
}

.ticket-title {
    color: #1a1a1a !important;
}

.ticket-label {
    color: #555 !important;
}
    .stApp { background-color: #f5f2ee; }
    h1, h2, h3 { font-family: 'DM Serif Display', serif; font-weight: 400; }
    .block-container { padding-top: 2rem; max-width: 900px; }

    .ticket-header {
        border: 1px solid #1a1a1a;
        padding: 2rem 2.5rem;
        margin-bottom: 2.5rem;
        background: #fff;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .ticket-label {
        font-size: 0.65rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #999;
        margin-bottom: 0.2rem;
    }
    .ticket-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.8rem;
        font-style: italic;
    }
    .ticket-tag {
        font-size: 0.65rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        border: 1px solid #1a1a1a;
        padding: 0.3rem 0.7rem;
        display: inline-block;
        margin-top: 0.5rem;
    }
    .section-label {
        font-size: 0.65rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #999;
        border-bottom: 1px solid #ddd;
        padding-bottom: 0.4rem;
        margin-bottom: 1rem;
    }
    .report-box {
        background: #fff;
        border: 1px solid #1a1a1a;
        padding: 2rem;
        margin-top: 1.5rem;
        line-height: 1.8;
    }
    .stTextInput input {
        background: #fff;
        border: 1px solid #1a1a1a;
        border-radius: 0;
        font-family: 'DM Mono', monospace;
        font-size: 0.9rem;
        padding: 0.7rem 1rem;
    }
    .stButton button {
        background: #1a1a1a;
        color: #f5f2ee;
        border: none;
        border-radius: 0;
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        padding: 0.6rem 2rem;
        width: 100%;
    }
    .stButton button:hover { background: #333; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────
st.markdown("""
<div class="ticket-header">
    <div>
        <div class="ticket-label">Tool</div>
        <div class="ticket-title">AI Research Agent</div>
        <span class="ticket-tag">Agentic · LangGraph · Claude</span>
    </div>
    <div style="text-align:right">
        <div class="ticket-label">Author</div>
        <div class="ticket-value" style="font-family:'DM Mono',monospace">Manish Cheeti</div>
        <div class="ticket-label" style="margin-top:0.8rem">Powered by</div>
        <div class="ticket-value" style="font-family:'DM Mono',monospace">Claude + Tavily</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Input ────────────────────────────────────────────────
st.markdown('<div class="section-label">— Enter Research Topic</div>', unsafe_allow_html=True)
topic = st.text_input("", placeholder="e.g. latest developments in reinforcement learning 2025")

if st.button("Run Research Agent"):
    if not topic.strip():
        st.warning("Please enter a research topic.")
    else:
        with st.spinner("Agent is searching and synthesizing... this takes ~30 seconds"):
            agent = build_agent()
            result = agent.invoke({
                "topic": topic,
                "search_results": [],
                "report": "",
                "messages": []
            })

        st.markdown('<div class="section-label" style="margin-top:2rem">— Research Report</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="report-box">{result["report"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)

        st.download_button(
            label="Download Report",
            data=result["report"],
            file_name=f"{topic[:30].replace(' ', '_')}_report.md",
            mime="text/markdown"
        )

# ── Footer ───────────────────────────────────────────────
st.markdown("""
<div style="border-top:1px solid #ddd; margin-top:3rem; padding-top:1rem; font-size:0.65rem; letter-spacing:0.15em; text-transform:uppercase; color:#999;">
    © 2025 Manish Cheeti · UMD MS Data Science · github.com/Man1shC
</div>
""", unsafe_allow_html=True)