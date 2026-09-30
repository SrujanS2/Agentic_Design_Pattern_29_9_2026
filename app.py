import sys
import os
import time
import streamlit as st
import streamlit.components.v1 as components

# Ensure the project root is on the Python path so internal imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from patterns.tool_using.graph import build_graph as build_tool_graph  # noqa: E402
from patterns.planner_executor.graph import build_graph as build_planner_graph  # noqa: E402

# ──────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Agentic AI – Patterns",
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
    .stTextArea [data-baseweb="textarea"],
    .stTextArea [data-baseweb="base-input"],
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
# Global Cursor Bubbles Animation
# ──────────────────────────────────────────────
components.html(
    """
    <script>
    const doc = window.parent.document;
    if (!doc.getElementById("cursor-bubble-script")) {
        const style = doc.createElement('style');
        style.innerHTML = `
            .cursor-bubble {
                position: fixed;
                width: 16px;
                height: 16px;
                background: radial-gradient(circle, rgba(165, 214, 167, 0.9) 0%, rgba(165, 214, 167, 0) 80%);
                border-radius: 50%;
                pointer-events: none;
                z-index: 99999;
                transform: translate(-50%, -50%);
                animation: bubble-fade 0.6s cubic-bezier(0.25, 1, 0.5, 1) forwards;
            }
            @keyframes bubble-fade {
                0% { transform: translate(-50%, -50%) scale(0.5); opacity: 1; }
                100% { transform: translate(-50%, -150%) scale(2.5); opacity: 0; }
            }
        `;
        doc.head.appendChild(style);

        doc.addEventListener('mousemove', function(e) {
            // throttle bubble creation slightly
            if (Math.random() > 0.4) {
                const bubble = doc.createElement('div');
                bubble.className = 'cursor-bubble';
                bubble.style.left = e.clientX + 'px';
                bubble.style.top = e.clientY + 'px';
                doc.body.appendChild(bubble);
                setTimeout(() => { bubble.remove(); }, 600);
            }
        });

        const marker = doc.createElement('div');
        marker.id = "cursor-bubble-script";
        doc.body.appendChild(marker);
    }
    </script>
    """,
    height=0,
)


# ──────────────────────────────────────────────
# Sidebar – Pattern Selection & Example Questions
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎛️ Select Pattern")
    pattern = st.radio("Choose the Agent Pattern:", ["Tool-Using Agent", "Planner-Executor Agent"])
    
    st.divider()

    st.markdown("### 📌 Example Questions")

    if pattern == "Tool-Using Agent":
        examples = [
            "What is the sum of 5 and 3?",
            "What is the square of the average of 10 and 5?",
            "What is 2 raised to the power of 10?",
            "What is 15% of 200?",
        ]
    else:
        examples = [
            "Create a simple 3-step plan for launching an AI chatbot product.",
            "Write a short guide on how to bake a chocolate cake.",
            "Explain how quantum computing works.",
        ]

    for ex in examples:
        if st.button(ex, key=f"ex_{ex}", use_container_width=True):
            st.session_state["prefill"] = ex

    st.divider()
    if pattern == "Tool-Using Agent":
        st.caption(
            "**How it works**\n\n"
            "1️⃣ Agent parses math question to expression\n\n"
            "2️⃣ Tool executes expression\n\n"
            "3️⃣ Returns precise result 🎯"
        )
    else:
        st.caption(
            "**How it works**\n\n"
            "1️⃣ Planner breaks task into steps\n\n"
            "2️⃣ Executor runs each step\n\n"
            "3️⃣ Combines results 🎯"
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
    st.markdown(f"## Agentic AI – {pattern}")

if pattern == "Tool-Using Agent":
    st.markdown("Ask a **math question** — the agent extracts the formula and calculates it.")
else:
    st.markdown("Give a **complex task** — the agent plans it out and executes each step.")

st.divider()

# ──────────────────────────────────────────────
# Input Area
# ──────────────────────────────────────────────
prefill = st.session_state.pop("prefill", "")
question = st.text_input(
    "Your question or task",
    value=prefill,
    placeholder="Enter your prompt here...",
    label_visibility="collapsed",
)

_, center_col, _ = st.columns([1, 1, 1])
with center_col:
    ask_clicked = st.button("🚀  Run Agent", use_container_width=True, type="primary")

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
        st.markdown('<div class="fade-in">', unsafe_allow_html=True)
        
        if pattern == "Tool-Using Agent":
            app_graph = build_tool_graph()
            result = app_graph.invoke({"question": question.strip()})
            thinking_placeholder.empty()

            st.success("🔢  **Mode: Tool-Using Agent**")
            
            if result.get("expression"):
                st.markdown("**📐 Extracted Expression**")
                st.code(result["expression"], language="python")
                
            st.markdown("**✅ Result**")
            result_text = str(result.get("result", ""))
            result_html = f'''<div style="height: 80px; overflow-y: auto; padding: 10px; background: transparent !important; color: #000000; border: 1px solid rgba(46,125,50,0.3); border-radius: 8px; white-space: pre-wrap; font-family: 'Inter', sans-serif;">{result_text}</div>'''
            st.markdown(result_html, unsafe_allow_html=True)
            
        else:
            app_graph = build_planner_graph()
            result = app_graph.invoke({"task": question.strip()})
            thinking_placeholder.empty()

            st.info("📝  **Mode: Planner-Executor Agent**")
            
            if result.get("plan"):
                st.markdown("**📋 Execution Plan**")
                plan_text = "\\n".join(result["plan"])
                st.code(plan_text, language="markdown")
                
            st.markdown("**✅ Final Output**")
            output_text = str(result.get("output", ""))
            output_html = f'''<div style="height: 300px; overflow-y: auto; padding: 10px; background: transparent !important; color: #000000; border: 1px solid rgba(46,125,50,0.3); border-radius: 8px; white-space: pre-wrap; font-family: 'Inter', sans-serif;">{output_text}</div>'''
            st.markdown(output_html, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        time.sleep(0.1)
        
        # Blaster animation instead of balloons
        components.html(
            """
            <script>
            const doc = window.parent.document;
            function blast() {
                for(let i=0; i<25; i++) {
                    setTimeout(() => {
                        const laser = doc.createElement('div');
                        laser.style.position = 'fixed';
                        laser.style.top = '-150px';
                        laser.style.left = Math.random() * 100 + 'vw';
                        laser.style.width = (Math.random() * 4 + 2) + 'px';
                        laser.style.height = (Math.random() * 120 + 60) + 'px';
                        laser.style.background = 'linear-gradient(to bottom, rgba(255,255,255,0), #66bb6a, #a5d6a7, #ffffff)';
                        laser.style.boxShadow = '0 0 15px #66bb6a, 0 0 30px #a5d6a7';
                        laser.style.borderRadius = '50px';
                        laser.style.zIndex = '999999';
                        laser.style.pointerEvents = 'none';
                        doc.body.appendChild(laser);
                        
                        laser.animate([
                            { top: '-150px' },
                            { top: '120vh' }
                        ], {
                            duration: Math.random() * 500 + 400,
                            easing: 'ease-in'
                        }).onfinish = () => laser.remove();
                    }, Math.random() * 1200);
                }
            }
            blast();
            </script>
            """,
            height=0,
        )

    except Exception as e:
        thinking_placeholder.empty()
        st.error(f"Something went wrong: {e}")

elif ask_clicked:
    st.warning("⚠️ Please enter a prompt first.")

# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.markdown("")
st.divider()
st.caption("Built with **LangGraph** · **LangChain** · **Streamlit**  |  Agentic Design Patterns")
