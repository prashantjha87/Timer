import streamlit as st
import time
from datetime import datetime
from database import init_db, save_session
from analytics import plot_daily_hours

init_db()

st.title("📚 Study Time Tracker")

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "elapsed" not in st.session_state:
    st.session_state.elapsed = 0

if "running" not in st.session_state:
    st.session_state.running = False


col1, col2, col3, col4 = st.columns(4)

if col1.button("▶ Start Reading"):

    if not st.session_state.running:
        st.session_state.start_time = datetime.now()
        st.session_state.running = True


if col2.button("⏸ Pause"):

    st.session_state.running = False


if col3.button("🔄 Refresh"):

    st.session_state.elapsed = 0
    st.session_state.start_time = None
    st.session_state.running = False


if col4.button("✅ End Reading"):

    if st.session_state.start_time:

        end_time = datetime.now()

        duration = st.session_state.elapsed

        save_session(
            st.session_state.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            end_time.strftime("%Y-%m-%d %H:%M:%S"),
            duration
        )

        st.success("Session Saved!")

        st.session_state.elapsed = 0
        st.session_state.running = False
        st.session_state.start_time = None


placeholder = st.empty()

while st.session_state.running:

    time.sleep(1)

    st.session_state.elapsed += 1

    mins = st.session_state.elapsed // 60
    secs = st.session_state.elapsed % 60

    placeholder.metric("Study Timer", f"{mins}:{secs:02d}")

    st.rerun()


mins = st.session_state.elapsed // 60
secs = st.session_state.elapsed % 60

placeholder.metric("Study Timer", f"{mins}:{secs:02d}")


st.divider()

st.subheader("📊 Study Analytics")

fig = plot_daily_hours()

if fig:
    st.plotly_chart(fig)
else:

    st.info("No study sessions yet.")
