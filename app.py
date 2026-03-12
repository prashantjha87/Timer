import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import bcrypt
import time
import calplot
import matplotlib.pyplot as plt
from datetime import date, timedelta

st.set_page_config(page_title="StudyOS Pro", page_icon="📚", layout="wide")

# -------------------------
# CUSTOM STYLE
# -------------------------

st.markdown("""
<style>

.main-title{
font-size:40px;
font-weight:700;
text-align:center;
margin-bottom:20px;
}

.metric-card{
background:#1c1f26;
padding:20px;
border-radius:15px;
text-align:center;
box-shadow:0 4px 20px rgba(0,0,0,0.3);
}

.timer-card{
background:#11151c;
padding:40px;
border-radius:20px;
text-align:center;
font-size:42px;
font-weight:700;
margin-top:20px;
}

.stButton>button{
width:100%;
height:50px;
border-radius:12px;
font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# DATABASE
# -------------------------

conn = sqlite3.connect("studyos_pro.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sessions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
date TEXT,
subject TEXT,
seconds INTEGER
)
""")

conn.commit()

# -------------------------
# HELPERS
# -------------------------

def format_time(sec):
    h=int(sec//3600)
    m=int((sec%3600)//60)
    s=int(sec%60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def save_session(user,subject,seconds):

    cursor.execute(
    "INSERT INTO sessions(username,date,subject,seconds) VALUES(?,?,?,?)",
    (user,str(date.today()),subject,int(seconds))
    )

    conn.commit()

def load_data(user):

    return pd.read_sql(
    "SELECT * FROM sessions WHERE username=?",
    conn,
    params=(user,)
    )

def get_streak(df):

    if df.empty:
        return 0

    dates=sorted(df["date"].unique(),reverse=True)

    streak=0
    today=date.today()

    for i,d in enumerate(dates):

        if str(today - timedelta(days=i))==d:
            streak+=1
        else:
            break

    return streak

def get_xp(total_seconds):

    hours = total_seconds/3600
    xp = int(hours*10)
    level = xp//100 + 1

    return xp,level

# -------------------------
# SESSION STATE
# -------------------------

if "user" not in st.session_state:
    st.session_state.user=None

if "running" not in st.session_state:
    st.session_state.running=False

if "elapsed" not in st.session_state:
    st.session_state.elapsed=0

if "start_time" not in st.session_state:
    st.session_state.start_time=None

# -------------------------
# LOGIN
# -------------------------

if st.session_state.user is None:

    st.title("📚 StudyOS Pro")

    tab1,tab2=st.tabs(["Login","Register"])

    with tab1:

        u=st.text_input("Username")
        p=st.text_input("Password",type="password")

        if st.button("Login"):

            res=cursor.execute(
            "SELECT password FROM users WHERE username=?",
            (u,)
            ).fetchone()

            if res and bcrypt.checkpw(p.encode(),res[0].encode()):

                st.session_state.user=u
                st.rerun()

            else:

                st.error("Invalid credentials")

    with tab2:

        u=st.text_input("New Username")
        p=st.text_input("New Password",type="password")

        if st.button("Register"):

            hash_pw=bcrypt.hashpw(p.encode(),bcrypt.gensalt())

            try:

                cursor.execute(
                "INSERT INTO users(username,password) VALUES(?,?)",
                (u,hash_pw.decode())
                )

                conn.commit()

                st.success("Account created")

            except:

                st.error("Username exists")

    st.stop()

# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.title("Study Settings")

subject=st.sidebar.selectbox(
"Subject",
["0 Revision","Anatomy","Physiology","Biochemistry","Pathology","Pharmacology","Microbiology","FMT","PSM","Medicine","Surgery","OBG","Pediatrics","Orthopedics","Ophthalmology","ENT","Dermatology","Psychiatry","Anesthesiology","Radiology"]
)

mode=st.sidebar.selectbox(
"Mode",
["Normal","Pomodoro 25/5"]
)

goal=st.sidebar.slider("Daily Goal (hours)",1,10,4)

if st.sidebar.button("Logout"):

    st.session_state.user=None
    st.rerun()

# -------------------------
# DASHBOARD
# -------------------------

st.markdown('<div class="main-title">📚 StudyOS Pro Dashboard</div>',unsafe_allow_html=True)

df=load_data(st.session_state.user)

today=str(date.today())

today_sec=df[df["date"]==today]["seconds"].sum() if not df.empty else 0

streak=get_streak(df)

total_seconds=df["seconds"].sum() if not df.empty else 0

xp,level=get_xp(total_seconds)

focus_score = min(int((today_sec/3600)*20),100)

col1,col2,col3,col4=st.columns(4)

with col1:
    st.metric("Today's Study",format_time(today_sec))

with col2:
    st.metric("Study Streak 🔥",f"{streak} days")

with col3:
    st.metric("Level 🏆",level)

with col4:
    st.metric("Focus Score 🧠",f"{focus_score}/100")

st.progress(min(today_sec/(goal*3600),1))

# -------------------------
# TIMER
# -------------------------

def start():

    st.session_state.running=True
    st.session_state.start_time=time.time()

def pause():

    if st.session_state.running:

        st.session_state.elapsed+=time.time()-st.session_state.start_time
        st.session_state.running=False

def resume():

    st.session_state.running=True
    st.session_state.start_time=time.time()

def end():

    if st.session_state.running:

        st.session_state.elapsed+=time.time()-st.session_state.start_time

    save_session(
    st.session_state.user,
    subject,
    st.session_state.elapsed
    )

    st.session_state.running=False
    st.session_state.elapsed=0

    st.success("Session saved")

timer=st.empty()

timer.markdown(
f"<div class='timer-card'>{format_time(st.session_state.elapsed)}</div>",
unsafe_allow_html=True
)

col1,col2,col3,col4=st.columns(4)

with col1:
    st.button("Start",on_click=start)

with col2:
    st.button("Pause",on_click=pause)

with col3:
    st.button("Resume",on_click=resume)

with col4:
    st.button("End",on_click=end)

while st.session_state.running:

    current=st.session_state.elapsed+(time.time()-st.session_state.start_time)

    timer.markdown(
    f"<div class='timer-card'>{format_time(current)}</div>",
    unsafe_allow_html=True
    )

    if mode=="Pomodoro 25/5" and current>=1500:

        st.warning("Pomodoro completed 🍅")

        end()

        break

    time.sleep(1)

    st.rerun()

# -------------------------
# ANALYTICS
# -------------------------

st.divider()
st.subheader("Study Analytics")

if not df.empty:

    df["hours"]=df["seconds"]/3600

    col1,col2=st.columns(2)

    with col1:

        daily=df.groupby("date")["hours"].sum().reset_index()

        fig=px.line(daily,x="date",y="hours",title="Daily Study Trend")

        st.plotly_chart(fig,use_container_width=True)

    with col2:

        subject_chart=df.groupby("subject")["hours"].sum().reset_index()

        fig=px.pie(subject_chart,names="subject",values="hours",title="Subject Distribution")

        st.plotly_chart(fig,use_container_width=True)

# -------------------------
# HEATMAP
# -------------------------

st.subheader("📅 Study Consistency Heatmap (Last 90 Days)")

if not df.empty:

    heat = df.groupby("date")["seconds"].sum()

    heat.index = pd.to_datetime(heat.index)

    # convert to minutes instead of hours
    heat = heat / 60


    start = pd.to_datetime(date.today() - timedelta(days=90))
    end = pd.to_datetime(date.today())

    all_days = pd.date_range(start, end)

    heat = heat.reindex(all_days, fill_value=0)


    fig, ax = calplot.calplot(
        heat,
        cmap="Greens",
        figsize=(14,4),
        edgecolor="#222",
        linewidth=0.5,
        vmin=0,
        vmax=120,  # assume max 2 hours/day for scaling
        suptitle="Study Minutes per Day"
    )

    st.pyplot(fig)

# -------------------------
# HISTORY
# -------------------------

st.subheader("Session History")

if not df.empty:

    df["duration"]=df["seconds"].apply(format_time)

    st.dataframe(
    df[["date","subject","duration"]],
    use_container_width=True
    )

else:

    st.info("No study sessions yet")