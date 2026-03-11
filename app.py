import streamlit as st
import time
from datetime import datetime
from database import init_db, save_session
from analytics import plot_daily_hours
from streamlit_autorefresh import st_autorefresh

init_db()

st.set_page_config(page_title="Study Timer", layout="centered")

st.title("📚 Study Time Tracker")


# -------------------------
# Session State
# -------------------------

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "elapsed" not in st.session_state:
    st.session_state.elapsed = 0

if "running" not in st.session_state:
    st.session_state.running = False


# -------------------------
# Auto Refresh Every Second
# -------------------------

if st.session_state.running:
    st_autorefresh(interval=1000, key="timer_refresh")


# -------------------------
# Time Format
# -------------------------

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


# -------------------------
# Timer Logic
# -------------------------

if st.session_state.running and st.session_state.start_time:

    now = datetime.now()
    elapsed = int((now - st.session_state.start_time).total_seconds())
    st.session_state.elapsed = elapsed


# -------------------------
# Circular Timer UI
# -------------------------

time_display = format_time(st.session_state.elapsed)

st.markdown(
    f"""
    <div style="
        display:flex;
        justify-content:center;
        align-items:center;
        margin-top:40px;
        margin-bottom:40px;
    ">
        <div style="
            width:260px;
            height:260px;
            border-radius:50%;
            border:10px solid #3e4557;
            display:flex;
            justify-content:center;
            align-items:center;
            font-size:42px;
            color:white;
            background:#2f3646;
            font-weight:bold;
        ">
            {time_display}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# -------------------------
# Controls
# -------------------------

col1, col2, col3, col4 = st.columns(4)

if col1.button("▶ Start Reading"):

    if not st.session_state.running:
        st.session_state.start_time = datetime.now()
        st.session_state.running = True


if col2.button("⏸ Pause"):
    st.session_state.running = False


if col3.button("🔄 Refresh"):
    st.session_state.elapsed = 0
    st.session_state.running = False
    st.session_state.start_time = None


if col4.button("✅ End Reading"):

    if st.session_state.start_time:

        end_time = datetime.now()

        save_session(
            st.session_state.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            end_time.strftime("%Y-%m-%d %H:%M:%S"),
            st.session_state.elapsed
        )

        st.success("Session Saved!")

        st.session_state.elapsed = 0
        st.session_state.running = False
        st.session_state.start_time = None


# -------------------------
# Analytics
# -------------------------

st.divider()

st.subheader("📊 Study Analytics")

fig = plot_daily_hours()

if fig:
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No study sessions yet.")