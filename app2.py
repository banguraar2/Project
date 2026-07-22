import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv("cps_project_data.csv")
# Page configurations
st.set_page_config(
    page_title="Weekly Earnings Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFD1DF;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Widgets
# Widget 1
st.sidebar.header("Filters")
edu = [
    "All Education Groups"
] + sorted(df["EDUC_GROUP"].dropna().unique().tolist())
select_edu = st.sidebar.selectbox(
    "Select Education Group:",
    options=edu
)
# Widget 2
select_sex = st.sidebar.radio(
    "Select Gender:",
    options=["All", "Male", "Female"],
    horizontal=True
)
# Dataframe Filters
# filtering education groups
df_filter = df.copy() # saves a complete copy 
if select_edu != "All Education Groups":
  df_filter = df_filter[
      df_filter["EDUC_GROUP"] == select_edu
  ]
# filtering by gender
if select_sex != "All":
  df_filter = df_filter[
      df_filter["SEX_LABEL"] == select_sex
  ]
# 1 Chart
# Histogram
st.subheader("Weekly Earnings Distribution")
earnings = df_filter["EARNWEEK2"].dropna()
fig, ax = plt.subplots(figsize=(8,6))
ax.hist(earnings, bins=30, color="hotpink", edgecolor="white")
ax.set_title(" Weekly Earnings Distributiion")
ax.set_xlabel(" Weekly Earnings")
ax.set_ylabel("Number of Workers")
ax.grid(axis="y", alpha=0.25)
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)
# 1 Statistics Table
st.subheader("Summary Statistics Table")
summary = (
    df_filter["EARNWEEK2"]
    .describe()
    .rename(
        {
            "count": "# of Workers",
            "mean": "Mean",
            "std": "Standard Deviation",
            "min": "Minimum",
            "25%": "Quartile 1",
            "50%": "Median",
            "75%": "Quartile 3",
            "max": "Maximum"

        }
    )
    .to_frame(name="Weekly Earnings")
)
summary["Weekly Earnings"] = (
    summary["Weekly Earnings"].round(2)
)
st.dataframe(
    summary,
    use_container_width=True
)
