import sys
import os
import time
import streamlit as st

# Ensure the project root is on the Python path so internal imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from patterns.tool_using.run import run_question  # noqa: E402

# ──────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Agentic AI – Tool-Using Pattern",
    page_icon="🤖",
    layout="centered",
)

# ──────────────────────────────────────────────
# Custom CSS – Rich light-green theme + animations
# ──────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* ══════════════════════════════════════════
       GLOBAL – Black text everywhere + animated green BG
       ══════════════════════════════════════════ */
    html, body, [class*="css"],
    .stApp,
    header[data-testid="stHeader"] {
        font-family: 'Inter', sans-serif !important;
        color: #000000 !important;
    }

    /* Animated shimmer gradient background */
    @keyframes shimmer-bg {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp {
        background: linear-gradient(
            -45deg, #e8f5e9, #c8e6c9, #a5d6a7, #81c784, #c8e6c9, #e8f5e9
        ) !important;
        background-size: 400% 400% !important;
        animation: shimmer-bg 12s ease infinite !important;
    }
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Force black on all Streamlit markdown / text elements */
    .stApp p, .stApp span, .stApp label, .stApp li,
    .stApp h1, .stApp h2, .stApp h3, .stApp h4,
    .stApp .stMarkdown, .stApp .stCaption,
    div[data-testid="stText"],
    div[data-testid="stCaptionContainer"] * {
        color: #000000 !important;
    }

    /* ══════════════════════════════════════════
       SIDEBAR
       ══════════════════════════════════════════ */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1b5e20 0%, #2e7d32 100%) !important;
    }
    section[data-testid="stSidebar"] * {
        color: #e8f5e9 !important;
    }
    section[data-testid="stSidebar"] button {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        color: #e8f5e9 !important;
    }
    section[data-testid="stSidebar"] button:hover {
        background: rgba(255,255,255,0.18) !important;
        border-color: rgba(255,255,255,0.35) !important;
        transform: translateX(6px) !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.15) !important;
    }

    /* ══════════════════════════════════════════
       PRIMARY BUTTON – breathing glow
       ══════════════════════════════════════════ */
    @keyframes btn-breathe {
        0%, 100% { box-shadow: 0 4px 15px rgba(46,125,50,0.30); }
        50%      { box-shadow: 0 6px 28px rgba(46,125,50,0.55); }
    }
    .stButton > button[kind="primary"],
    button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, #2e7d32, #43a047, #66bb6a) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0.6rem 2rem !important;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
        animation: btn-breathe 3s ease-in-out infinite !important;
    }
    .stButton > button[kind="primary"]:hover,
    button[data-testid="stBaseButton-primary"]:hover {
        transform: translateY(-3px) scale(1.04) !important;
        box-shadow: 0 10px 30px rgba(46,125,50,0.50) !important;
    }

    /* ══════════════════════════════════════════
       TEXT INPUT
       ══════════════════════════════════════════ */
    .stTextInput input {
        background: rgba(255,255,255,0.80) !important;
        border: 2px solid #a5d6a7 !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1.05rem !important;
        color: #000000 !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput input:focus {
        border-color: #2e7d32 !important;
        box-shadow: 0 0 0 3px rgba(46,125,50,0.18) !important;
    }
    .stTextInput input::placeholder {
        color: #558b2f !important;
    }

    /* ══════════════════════════════════════════
       TEXT AREA (output box) – transparent + black text
       ══════════════════════════════════════════ */
    .stTextArea textarea,
    .stTextArea textarea:disabled {
        background: transparent !important;
        background-color: transparent !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        border: none !important;
        border-radius: 0 !important;
        outline: none !important;
        box-shadow: none !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
        opacity: 1 !important;
        resize: none !important;
    }
    /* Remove container background/border too */
    .stTextArea > div,
    .stTextArea > div > div {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* ══════════════════════════════════════════
       CODE BLOCK – keep readable
       ══════════════════════════════════════════ */
    .stCodeBlock code {
        color: #1b5e20 !important;
    }

    /* ══════════════════════════════════════════
       ALERT BOXES – dark text inside
       ══════════════════════════════════════════ */
    div[data-testid="stAlert"] p,
    div[data-testid="stAlert"] span {
        color: #000000 !important;
    }

    /* ══════════════════════════════════════════
       GLOWING DIVIDERS
       ══════════════════════════════════════════ */
    @keyframes glow-line {
        0%, 100% { opacity: 0.4; box-shadow: none; }
        50%      { opacity: 1; box-shadow: 0 0 8px rgba(46,125,50,0.35); }
    }
    .stApp hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, #66bb6a, transparent) !important;
        animation: glow-line 4s ease-in-out infinite !important;
    }

    /* ══════════════════════════════════════════
       FLOATING PARTICLES
       ══════════════════════════════════════════ */
    @keyframes float-up {
        0%   { transform: translateY(100vh) scale(0) rotate(0deg); opacity: 0; }
        10%  { opacity: 0.55; }
        50%  { transform: translateY(50vh) scale(0.8) rotate(180deg); opacity: 0.55; }
        90%  { opacity: 0.55; }
        100% { transform: translateY(-10vh) scale(1) rotate(360deg); opacity: 0; }
    }
    .particles {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    .particle {
        position: absolute;
        bottom: -20px;
        border-radius: 50%;
        animation: float-up linear infinite;
    }

    /* ══════════════════════════════════════════
       SECTION ENTRANCE – staggered fade-slide
       ══════════════════════════════════════════ */
    @keyframes fadeSlideIn {
        from { opacity: 0; transform: translateY(22px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .stApp > div > div > div > section[data-testid="stMain"] > div {
        animation: fadeSlideIn 0.7s ease-out both;
    }
    .fade-in {
        animation: fadeSlideIn 0.6s ease-out forwards;
    }

    /* ══════════════════════════════════════════
       PULSE ICON
       ══════════════════════════════════════════ */
    @keyframes pulse-ring {
        0%   { box-shadow: 0 0 0 0 rgba(46,125,50,0.40); }
        70%  { box-shadow: 0 0 0 16px rgba(46,125,50,0); }
        100% { box-shadow: 0 0 0 0 rgba(46,125,50,0); }
    }
    .pulse-icon {
        display: inline-block;
        border-radius: 50%;
        animation: pulse-ring 2s ease-out infinite;
    }

    /* ══════════════════════════════════════════
       THINKING DOTS
       ══════════════════════════════════════════ */
    @keyframes blink {
        0%, 20% { opacity: 0.2; }
        50%     { opacity: 1; }
        100%    { opacity: 0.2; }
    }
    .dot { animation: blink 1.4s infinite both; display: inline-block; font-size: 1.4rem; }
    .dot:nth-child(2) { animation-delay: 0.2s; }
    .dot:nth-child(3) { animation-delay: 0.4s; }

    /* ══════════════════════════════════════════
       TYPEWRITER TITLE
       ══════════════════════════════════════════ */
    @keyframes typewriter {
        from { width: 0; }
        to   { width: 100%; }
    }
    @keyframes blink-caret {
        50% { border-color: transparent; }
    }
    .typewriter-wrap h2 {
        overflow: hidden;
        white-space: nowrap;
        border-right: 3px solid #2e7d32;
        animation:
            typewriter 2s steps(40,end) 0.5s 1 normal both,
            blink-caret 0.75s step-end infinite;
        color: #000000 !important;
    }
    </style>

    <!-- Floating particles -->
    <div class="particles">
        <div class="particle" style="left:3%;  width:8px;  height:8px;  background:#66bb6a; animation-duration:12s; animation-delay:0s;"></div>
        <div class="particle" style="left:12%; width:5px;  height:5px;  background:#a5d6a7; animation-duration:17s; animation-delay:2s;"></div>
        <div class="particle" style="left:24%; width:11px; height:11px; background:#81c784; animation-duration:14s; animation-delay:4s;"></div>
        <div class="particle" style="left:36%; width:6px;  height:6px;  background:#4caf50; animation-duration:19s; animation-delay:1s;"></div>
        <div class="particle" style="left:48%; width:7px;  height:7px;  background:#c8e6c9; animation-duration:11s; animation-delay:3s;"></div>
        <div class="particle" style="left:60%; width:9px;  height:9px;  background:#66bb6a; animation-duration:16s; animation-delay:5s;"></div>
        <div class="particle" style="left:72%; width:5px;  height:5px;  background:#a5d6a7; animation-duration:13s; animation-delay:0s;"></div>
        <div class="particle" style="left:84%; width:8px;  height:8px;  background:#81c784; animation-duration:18s; animation-delay:2s;"></div>
        <div class="particle" style="left:93%; width:6px;  height:6px;  background:#4caf50; animation-duration:15s; animation-delay:6s;"></div>
        <div class="particle" style="left:7%;  width:4px;  height:4px;  background:#c8e6c9; animation-duration:20s; animation-delay:7s;"></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
# Sidebar – Example Questions
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📌 Example Questions")

    st.markdown("**🔢 Math**")
    examples_math = [
        "What is the sum of 5 and 3?",
        "What is the square of the average of 10 and 5?",
        "What is 2 raised to the power of 10?",
        "What is 15% of 200?",
    ]
    for ex in examples_math:
        if st.button(ex, key=f"ex_{ex}", use_container_width=True):
            st.session_state["prefill"] = ex

    st.divider()

    st.markdown("**💡 General Knowledge**")
    examples_general = [
        "Define AI",
        "Who invented the telephone?",
        "What is photosynthesis?",
        "Explain the theory of relativity in simple terms",
    ]
    for ex in examples_general:
        if st.button(ex, key=f"ex_{ex}", use_container_width=True):
            st.session_state["prefill"] = ex

    st.divider()
    st.caption(
        "**How it works**\n\n"
        "1️⃣ Reasoning Agent classifies your question\n\n"
        "2️⃣ Math → Calculator tool | General → LLM fallback\n\n"
        "3️⃣ You get a precise answer either way 🎯"
    )

# ──────────────────────────────────────────────
# Hero Header (native Streamlit)
# ──────────────────────────────────────────────
st.markdown("")  # spacer
col_icon, col_title = st.columns([0.12, 0.88])
with col_icon:
    st.markdown(
        '<div class="pulse-icon" style="font-size:2.6rem; text-align:center;">🤖</div>',
        unsafe_allow_html=True,
    )
with col_title:
    st.markdown("## Agentic AI – Tool-Using Pattern")

st.markdown(
    "Ask a **math question** or a **general knowledge question** — "
    "the agent routes it automatically."
)

st.divider()

# ──────────────────────────────────────────────
# Input Area
# ──────────────────────────────────────────────
prefill = st.session_state.pop("prefill", "")
question = st.text_input(
    "Your question",
    value=prefill,
    placeholder="e.g.  What is the cube root of 27?   or   Define machine learning",
    label_visibility="collapsed",
)

_, center_col, _ = st.columns([1, 1, 1])
with center_col:
    ask_clicked = st.button("🚀  Ask the Agent", use_container_width=True, type="primary")

# ──────────────────────────────────────────────
# Run Agent & Display Results
# ──────────────────────────────────────────────
if ask_clicked and question.strip():
    # Animated "thinking" placeholder
    thinking_placeholder = st.empty()
    thinking_placeholder.markdown(
        '<div class="fade-in" style="text-align:center; padding:1.2rem; color:#2e7d32; font-weight:600;">'
        '🧠 Agent is thinking '
        '<span class="dot">.</span><span class="dot">.</span><span class="dot">.</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    try:
        result = run_question(question.strip())
        thinking_placeholder.empty()

        category = result.get("category", "GENERAL")
        is_math = category == "MATH"

        # Wrap output in a fade-in div
        st.markdown('<div class="fade-in">', unsafe_allow_html=True)

        # ── Category badge ──
        if is_math:
            st.success("🔢  **Category: Math**")
        else:
            st.info("💡  **Category: General Knowledge**")

        # ── Expression (math only) ──
        if is_math and result.get("expression"):
            st.markdown("**📐 Expression**")
            st.code(result["expression"], language="python")

        # ── Answer output box ──
        st.markdown("**✅ Answer**")
        st.text_area(
            "Answer output",
            value=result["result"],
            height=180 if not is_math else 80,
            disabled=True,
            label_visibility="collapsed",
        )

        st.markdown('</div>', unsafe_allow_html=True)

        # Fun confetti for math answers
        if is_math:
            time.sleep(0.3)
            st.balloons()

    except Exception as e:
        thinking_placeholder.empty()
        st.error(f"Something went wrong: {e}")

elif ask_clicked:
    st.warning("⚠️ Please enter a question first.")

# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.markdown("")
st.divider()
st.caption("Built with **LangGraph** · **LangChain** · **Streamlit**  |  Agentic Design Pattern")
