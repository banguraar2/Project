# Packages
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
# Improves readability for streamlit
@st.cache_data
def load_data():
    return = pd.read_csv("filter_cps_project_data.csv")
df = load_data()
# Page Configurations
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
df_filter = df.copy() 
if select_edu != "All Education Groups":
  df_filter = df_filter[
      df_filter["EDUC_GROUP"] == select_edu
  ]
if select_sex != "All":
  df_filter = df_filter[
      df_filter["SEX_LABEL"] == select_sex
  ]
# 1 Chart
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
# Summary Statistics
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
# Customizing my summary table
customize = (
    summary.style
    .set_table_styles([
        {
            "selector": "th",
            "props":[
                ("background-color", "#FF69B4") # making the table header hot pink
                ("color", "white"),
                ("font-weight", "bold"),
                ("text-align", "center")
            ]
        }
    ])
    .set_properties(**{
        "background-color": "#FFE4EC", # making the table light pink
        "color": "white"
    })
)
st.dataframe(
    customize,
    use_container_width=True
)
#st.dataframe(
    #summary,
    #use_container_width=True
#)
