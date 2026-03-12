# 📚 StudyOS Pro

StudyOS Pro is a **modern study productivity dashboard built with Streamlit**.
It helps track study sessions, measure focus, maintain consistency, and visualize progress using analytics and a GitHub-style heatmap.

The project combines **timer tracking, gamification, and analytics** to help students stay disciplined and motivated.

---

## ✨ Features

### ⏱ Study Timer

* Start, Pause, Resume, and End study sessions
* Pomodoro mode (25/5 focus cycles)
* Tracks session duration automatically

### 🎯 Goal Tracking

* Set a **daily study goal**
* Progress bar showing how close you are to the goal

### 🔥 Study Streak

* Tracks consecutive days of studying
* Encourages consistency

### 🧠 Focus Score

* Calculates a productivity score based on study time

### 🏆 Gamification

* XP system
* Level progression based on total study hours

### 📊 Analytics Dashboard

* Daily study trend charts
* Subject distribution visualization
* Session history table

### 📅 Study Heatmap

* GitHub-style study activity calendar
* Visualizes long-term study consistency

### 🔐 User Authentication

* Login / Register system
* Multiple users supported

### 💾 Local Database

* Uses SQLite to store all sessions locally

---

## 🖼 Dashboard Preview

The app provides a modern dashboard showing:

* Today's study time
* Study streak
* Focus score
* XP level
* Study progress
* Analytics charts
* Heatmap of study activity

---

## ⚙ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/studyos-pro.git
cd studyos-pro
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run study_os_pro.py
```

The app will open in your browser:

```
http://localhost:8501
```

---

## 📦 Project Structure

```
studyos-pro/
│
├── study_os_pro.py
├── requirements.txt
├── README.md
├── .gitignore
```

---

## 🧠 How It Works

### Focus Score

Focus score is calculated based on study hours:

```
Focus Score = min((study_hours × 20), 100)
```

Maximum score is capped at **100**.

---

### XP System

```
XP = total_study_hours × 10
Level = (XP // 100) + 1
```

Example:

| Study Hours | XP  | Level |
| ----------- | --- | ----- |
| 10          | 100 | 2     |
| 25          | 250 | 3     |
| 60          | 600 | 7     |

---

## 📊 Analytics Included

* Study time trend chart
* Subject study distribution
* GitHub-style study heatmap
* Session history table

---

## 🚀 Future Improvements

Possible future features:

* AI-powered study recommendations
* Calendar study planner
* Task + study session integration
* Smart break reminders
* Cloud database support
* Mobile responsive UI
* Leaderboard for group study

---

## 🛠 Built With

* **Streamlit** – Web app framework
* **Pandas** – Data analysis
* **Plotly** – Interactive charts
* **Calplot** – Calendar heatmap
* **SQLite** – Local database
* **Bcrypt** – Secure password hashing

---

## 📜 License

This project is open source and available under the **MIT License**.

---

## ⭐ Support

If you find this project useful, consider giving the repository a **star ⭐ on GitHub**.
