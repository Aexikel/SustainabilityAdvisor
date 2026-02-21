import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from PIL import Image
from ultralytics import YOLO
from supabase import create_client, Client
import google.generativeai as genai
import requests
from streamlit_lottie import st_lottie
from advisor import sustainability_db

# --- 1. CONFIGURATION & SECRETS ---
# Make sure your .streamlit/secrets.toml is set up!
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
llm_model = genai.GenerativeModel('gemini-2.5-flash')

st.set_page_config(page_title="EcoSort Advisor", page_icon="♻️", layout="wide")

# --- 2. ASSETS & ROBUST LOADERS ---
@st.cache_data
def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

# Attempt to load the animation
lottie_eco = load_lottieurl("https://lottie.host/8e202534-7221-432a-9811-04930d674174/Hn9mAn6XmB.json")

# --- 3. SESSION STATE INITIALIZATION ---
if "theme" not in st.session_state: st.session_state.theme = "dark"
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "auth_mode" not in st.session_state: st.session_state.auth_mode = "landing"
if "detected_items" not in st.session_state: st.session_state.detected_items = []
if "user" not in st.session_state: st.session_state.user = None

# --- 4. DYNAMIC UI ENGINE (CSS) ---
common_styles = """
<style>
    .stApp { transition: all 0.5s ease; }
    /* Animated Gradient Background */
    .animated-bg {
        background: linear-gradient(-45deg, #0d1b15, #1a2e26, #07120e);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    /* Card Polish & Hover */
    .custom-card {
        padding: 24px; border-radius: 15px; margin-bottom: 20px;
        transition: all 0.3s ease; border: 1px solid transparent;
    }
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(76, 175, 80, 0.15);
    }
</style>
"""
dark_theme = common_styles + """<style>
    .stApp { background-color: #0d1b15; color: #e0e0e0; }
    .custom-card { background-color: #1a2e26; border-color: #2e4d3e; }
    .metric-value { color: #4caf50; font-size: 2.2rem; font-weight: bold; }
</style>"""
light_theme = common_styles + """<style>
    .stApp { background-color: #f0f4f2; color: #1a2e26; }
    .custom-card { background-color: #ffffff; border-color: #e0e0e0; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .metric-value { color: #2e7d32; font-size: 2.2rem; font-weight: bold; }
</style>"""

st.markdown(dark_theme if st.session_state.theme == "dark" else light_theme, unsafe_allow_html=True)

# --- 5. COMPONENT & UTILITY FUNCTIONS ---
def render_top_right_toggle():
    t_col1, t_col2 = st.columns([15, 1])
    with t_col2:
        icon = "☀️" if st.session_state.theme == "dark" else "🌙"
        if st.button(icon):
            st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
            st.rerun()

def render_footer():
    st.markdown("<br><br><hr>", unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align: center; opacity: 0.7; font-size: 0.9rem;">
            <p>POWERED BY THE SUSTAINABILITY STACK</p>
            <div style="font-size: 1.5rem; letter-spacing: 15px; margin: 15px 0;">
                🐍 ⚡ 🐙 🔥 🎨 ♊ 💻 🚀 📸
            </div>
            <p style="font-size: 0.7rem;">Python • Supabase • GitHub • Firebase • Figma • Gemini • VS Code • NVIDIA • ImageAI</p>
            <p>EcoSort Advisor © 2026 | Circular Economy Initiative</p>
        </div>
    """, unsafe_allow_html=True)

@st.dialog("Eco-Alternative Advisor")
def chat_dialog(items):
    st.write(f"Analyzing alternatives for: {', '.join(items)}")
    if prompt := st.chat_input("How can I reduce this waste?"):
        with st.spinner("Consulting Eco-Expert..."):
            response = llm_model.generate_content(f"User has detected {items}. Suggest zero-waste swaps for: {prompt}")
            st.markdown(response.text)

@st.cache_resource
def load_yolo():
    return YOLO("best.pt")

# --- 6. PAGE ROUTING & LOGIC ---
render_top_right_toggle()

if not st.session_state.logged_in:
    if st.session_state.auth_mode == "landing":
        # HERO SECTION
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        
        # Safe Lottie Render
        if lottie_eco:
            st_lottie(lottie_eco, height=220, key="main_eco")
        else:
            st.markdown("<div style='font-size: 6rem;'>🌍</div>", unsafe_allow_html=True)
            
        st.markdown("""
            <h1 style='font-size: 3.5rem; margin-bottom: 0;'>EcoSort <span style='color: #4caf50;'>Advisor</span></h1>
            <p style='font-size: 1.3rem; opacity: 0.8;'>The Professional Resource Recovery Dashboard</p>
            <p style='font-style: italic; color: #88a096; max-width: 700px; margin: auto;'>
                "Every item sorted is a step toward a circular future, turning the waste of today into the resources of tomorrow."
            </p>
        </div>""", unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # 3-STEP GUIDE
        s1, s2, s3 = st.columns(3)
        steps = [
            ("📸 Capture", "Snap a photo of waste using AI-powered vision."),
            ("⚙️ Process", "Identify materials and calculate RRI impact."),
            ("🌿 Recover", "Discover sustainable swaps and track progress.")
        ]
        for i, col in enumerate([s1, s2, s3]):
            with col:
                st.markdown(f'<div class="custom-card" style="text-align:center;"><h3>{steps[i][0]}</h3><p>{steps[i][1]}</p></div>', unsafe_allow_html=True)

        # ACCESS MODES
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="custom-card" style="text-align:center;">', unsafe_allow_html=True)
        st.write("#### Secure Access Portal")
        a1, a2, a3 = st.columns(3)
        if a1.button("🚀 Test Mode", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.auth_mode = "guest"
            st.rerun()
        if a2.button("🔑 Login", use_container_width=True):
            st.session_state.auth_mode = "login"
            st.rerun()
        if a3.button("📝 Sign Up", use_container_width=True):
            st.session_state.auth_mode = "signup"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        render_footer()

    else:
        # AUTH FORMS (Login/Signup)
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("Member Access" if st.session_state.auth_mode == "login" else "New Registration")
        email = st.text_input("Email")
        pw = st.text_input("Password", type="password")
        if st.button("Continue"):
            try:
                if st.session_state.auth_mode == "login":
                    res = supabase.auth.sign_in_with_password({"email": email, "password": pw})
                    st.session_state.user = res.user
                else:
                    supabase.auth.sign_up({"email": email, "password": pw})
                    st.success("Registration successful! You can now log in.")
                st.session_state.logged_in = True
                st.rerun()
            except Exception as e: 
                st.error(f"Authentication Error: {e}")
        if st.button("Back"):
            st.session_state.auth_mode = "landing"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- MAIN DASHBOARD ---
    with st.sidebar:
        st.title("EcoSort Settings")
        st.write(f"Logged as: {st.session_state.user.email if st.session_state.user else 'Guest'}")
        if st.button("Sign Out"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.auth_mode = "landing"
            st.rerun()

    st.title("Resource Recovery Dashboard")
    
    # 1. Fetch History for Chart
    user_id = st.session_state.user.id if st.session_state.user else None
    history_df = pd.DataFrame()
    if user_id:
        try:
            res = supabase.table("user_history").select("rri_score, created_at").eq("user_id", user_id).execute()
            history_df = pd.DataFrame(res.data)
        except Exception as e:
            st.warning("Could not load user history.")

    # 2. Stats Row
    c1, c2, c3 = st.columns(3)
    total_rri = int(history_df["rri_score"].sum()) if not history_df.empty else 0
    with c1: st.markdown(f'<div class="custom-card"><p class="metric-label">LIFETIME RRI</p><p class="metric-value">{total_rri}</p></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="custom-card"><p class="metric-label">EFFICIENCY</p><p class="metric-value">88%</p></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="custom-card"><p class="metric-label">SENSORS</p><p class="metric-value">Active</p></div>', unsafe_allow_html=True)

    # 3. Main Body
    left, right = st.columns([2, 1])
    with left:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("📸 AI Waste Scanner")
        model = load_yolo()
        files = st.file_uploader("Upload images", accept_multiple_files=True)
        
        if files and st.button("⚡ Start Analysis"):
            session_rri = 0
            detected = set()
            for f in files[:5]:
                img = Image.open(f)
                results = model(np.array(img))
                st.image(results[0].plot()[:,:,::-1], use_container_width=True)
                for r in results:
                    for c in r.boxes.cls:
                        name = model.names[int(c)]
                        detected.add(name)
                        session_rri += sustainability_db.get(name, {}).get('rri_score', 0)
            
            st.session_state.detected_items = list(detected)
            
            if user_id and session_rri > 0:
                supabase.table("user_history").insert({"user_id": user_id, "rri_score": session_rri}).execute()
                st.success(f"Added {session_rri} RRI points to your profile!")
                st.rerun()
            elif not user_id:
                st.success(f"Test Score: +{session_rri} RRI points")
                
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        # TREND CHART
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("RRI Trends")
        if not history_df.empty:
            history_df['created_at'] = pd.to_datetime(history_df['created_at'])
            # Sort chronologically so the line draws correctly
            history_df = history_df.sort_values(by="created_at") 
            chart_theme = "plotly_dark" if st.session_state.theme == "dark" else "plotly_white"
            line_color = "#4caf50" if st.session_state.theme == "dark" else "#2e7d32"
            
            fig = px.line(history_df, x="created_at", y="rri_score", template=chart_theme)
            fig.update_traces(line_color=line_color, line_width=3, mode='lines+markers')
            fig.update_layout(margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_title=None, yaxis_title="RRI")
            st.plotly_chart(fig, use_container_width=True)
        else: 
            st.info("Log in and scan items to see your trends.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chatbot Trigger
        if st.session_state.detected_items:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.subheader("💡 Expert Guidance")
            if st.button("Find Sustainable Alternatives?"): 
                chat_dialog(st.session_state.detected_items)
            st.markdown('</div>', unsafe_allow_html=True)

    render_footer()