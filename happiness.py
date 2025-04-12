import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv("/Users/rushabarram/Documents/happiness-cantril-ladder/happiness-cantril-ladder.csv")
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("Filter")
year_selected = st.sidebar.slider("Select Year", int(df["Year"].min()), int(df["Year"].max()), 2021)
df_year = df[df["Year"] == year_selected]

# Title
st.title("🌍 Global Happiness Dashboard")
st.markdown(f"## Happiness Scores in {year_selected}")

# Choropleth Map
fig_map = px.choropleth(
    df_year,
    locations="Code",
    color="Cantril ladder score",
    hover_name="Entity",
    color_continuous_scale="Viridis",
    labels={"Cantril ladder score": "Happiness Score"},
    title=f"Happiness Score by Country - {year_selected}"
)
st.plotly_chart(fig_map, use_container_width=True)

# Line chart
st.markdown("## 📈 Happiness Trend Over Time")
countries = st.multiselect("Select Countries", df["Entity"].unique(), default=["India", "United States", "Finland"])
trend_df = df[df["Entity"].isin(countries)]

fig_line = px.line(
    trend_df,
    x="Year",
    y="Cantril ladder score",
    color="Entity",
    markers=True,
    labels={"Cantril ladder score": "Happiness Score"}
)
st.plotly_chart(fig_line, use_container_width=True)

# Top 10 countries
st.markdown(f"## 😊 Top 10 Happiest Countries in {year_selected}")
top10 = df_year.sort_values(by="Cantril ladder score", ascending=False).head(10)
st.table(top10[["Entity", "Cantril ladder score"]].reset_index(drop=True))
