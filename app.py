import streamlit as st
from datetime import datetime
import math
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

if "paused_time" not in st.session_state:
    st.session_state.paused_time = 0

if "running" not in st.session_state:
    st.session_state.running = False


# -------------------------
# Auto Refresh
# -------------------------

st_autorefresh(interval=1000, key="timer_refresh")


# -------------------------
# Time Formatter
# -------------------------

def format_time(seconds):

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


# -------------------------
# Timer Logic
# -------------------------

elapsed = st.session_state.paused_time

if st.session_state.running and st.session_state.start_time:

    elapsed = st.session_state.paused_time + int(
        (datetime.now() - st.session_state.start_time).total_seconds()
    )


# -------------------------
# Circular Progress
# -------------------------

radius = 110
circumference = 2 * math.pi * radius

# rotate every 60 minutes
progress = (elapsed % 3600) / 3600
stroke_offset = circumference * (1 - progress)

angle = progress * 360
dot_x = 150 + radius * math.cos(math.radians(angle - 90))
dot_y = 150 + radius * math.sin(math.radians(angle - 90))

time_display = format_time(elapsed)


# -------------------------
# Circular Timer UI
# -------------------------

st.markdown(
    f"""
    <div style="display:flex; justify-content:center; margin-top:30px; margin-bottom:30px;">
    <svg width="300" height="300">

        <circle
            cx="150"
            cy="150"
            r="{radius}"
            stroke="#2f3646"
            stroke-width="14"
            fill="none"
        />

        <circle
            cx="150"
            cy="150"
            r="{radius}"
            stroke="#6c8cff"
            stroke-width="14"
            fill="none"
            stroke-dasharray="{circumference}"
            stroke-dashoffset="{stroke_offset}"
            transform="rotate(-90 150 150)"
            stroke-linecap="round"
        />

        <circle
            cx="{dot_x}"
            cy="{dot_y}"
            r="6"
            fill="#6c8cff"
        />

        <text
            x="150"
            y="160"
            text-anchor="middle"
            font-size="34"
            fill="white"
            font-weight="bold"
        >
            {time_display}
        </text>

    </svg>
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

    if st.session_state.running:

        st.session_state.paused_time = elapsed
        st.session_state.running = False


if col3.button("🔄 Refresh"):

    st.session_state.start_time = None
    st.session_state.paused_time = 0
    st.session_state.running = False


if col4.button("✅ End Reading"):

    if elapsed > 0:

        end_time = datetime.now()

        save_session(
            end_time.strftime("%Y-%m-%d %H:%M:%S"),
            end_time.strftime("%Y-%m-%d %H:%M:%S"),
            elapsed
        )

        st.success("Session Saved!")

        st.session_state.start_time = None
        st.session_state.paused_time = 0
        st.session_state.running = False


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