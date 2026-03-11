import pandas as pd
import plotly.express as px
from database import get_sessions


def load_dataframe():

    data = get_sessions()

    df = pd.DataFrame(data, columns=[
        "id",
        "start_time",
        "end_time",
        "duration"
    ])

    if df.empty:
        return df

    df["start_time"] = pd.to_datetime(df["start_time"])
    df["date"] = df["start_time"].dt.date
    df["duration_min"] = df["duration"] / 60

    return df


def plot_daily_hours():

    df = load_dataframe()

    if df.empty:
        return None

    daily = df.groupby("date")["duration_min"].sum().reset_index()

    fig = px.bar(
        daily,
        x="date",
        y="duration_min",
        title="Daily Study Time (minutes)"
    )

    return fig