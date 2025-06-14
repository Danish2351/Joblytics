import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px


# ---------- Page Configuration ----------
st.set_page_config(layout="wide")


# ---------- Database Connection ----------
def mySQL_to_df(role):
    host = st.secrets["db_credentials"]["host"]
    port = st.secrets["db_credentials"]["port"]
    database = st.secrets["db_credentials"]["database"]
    user = st.secrets["db_credentials"]["user"]
    password = st.secrets["db_credentials"]["password"]

    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
    query = f"SELECT * FROM job_data WHERE job_title = '{role}'"
    return pd.read_sql(query, engine)


# ---------- Role Selection Mapping ----------
role_to_table = [
    "Data Scientist",
    "Data Analyst",
    "AI Engineer"
]

# ---------- Centered Title and Subtitle ----------
st.markdown("<h1 style='text-align: center;'>Your Career, Backed by Data</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Discover top skills, tools, and education trends for your dream job role.</p>", unsafe_allow_html=True)

# ---------- Centered Role Selection ----------
col1, col2, col3 = st.columns([2, 4, 2])
with col2:
    selected_role = st.selectbox("Select Job Role:", role_to_table)

# ---------- Load Data ----------
role = selected_role
df = mySQL_to_df(role)

# ---------- Right-aligned Job Count ----------
_, right_col = st.columns([6, 1])
with right_col:
    st.markdown(f"<p style='text-align:right; font-weight:500;'>According to <b>{len(df)}</b> job posts.</p>", unsafe_allow_html=True)

# ---------- Normalization Map ----------
normalization_map = {
    'bachelors': 'Bachelors', 'bachelor': 'Bachelors', 'bs': 'Bachelors', 'ba': 'Bachelors', 'b.sc': 'Bachelors', 'bsc': 'Bachelors',
    'masters': 'Masters', 'master': 'Masters', 'ms': 'Masters', 'msc': 'Masters', 'm.sc': 'Masters', 'ma': 'Masters',
    'phd': 'Phd', 'doctorate': 'Phd',
}

# ---------- Frequency Counting ----------
def get_value_counts(column, normalization_map=None):
    all_values = df[column].dropna().str.lower().str.split(",")
    flat_list = []
    for sublist in all_values:
        for item in sublist:
            word = item.strip()
            if not word:
                continue
            word = normalization_map.get(word, word) if normalization_map else word
            flat_list.append(word)
    return pd.Series(flat_list).value_counts()

# ---------- Top-N Setup ----------
top_n_per_column = {
    'Languages': 6,
    'Technologies': 8,
    'Skills': 6,
    'Education': 3
}

# ---------- Visualization Grid ----------
col1, col2 = st.columns(2)

# --- Education Pie ---
with col1:
    st.subheader("Education")
    edu_counts = get_value_counts("Education", normalization_map=normalization_map).head(top_n_per_column["Education"])
    fig_edu = px.pie(
        names=edu_counts.index,
        values=edu_counts.values,
        hole=0.4
    )
    st.plotly_chart(fig_edu, use_container_width=True, config={'displayModeBar': False})

# --- Languages Bar ---
with col2:
    st.subheader("Languages")
    lang_counts = get_value_counts("Languages").head(top_n_per_column["Languages"]).sort_values(ascending=False)
    fig_lang = px.bar(
        x=lang_counts.index,
        y=lang_counts.values,
        labels={'x': '', 'y': ''},
        height=400
    )
    fig_lang.update_layout(xaxis=dict(tickangle=45))
    st.plotly_chart(fig_lang, use_container_width=True, config={'displayModeBar': False})

# ---------- Bottom Row ----------
col3, col4 = st.columns(2)

# --- Technologies Bar ---
with col3:
    st.subheader("Technologies")
    tech_counts = get_value_counts("Technologies").head(top_n_per_column["Technologies"]).sort_values(ascending=False)
    fig_tech = px.bar(
        x=tech_counts.index,
        y=tech_counts.values,
        labels={'x': '', 'y': ''},
        height=400
    )
    fig_tech.update_layout(xaxis=dict(tickangle=45))
    st.plotly_chart(fig_tech, use_container_width=True, config={'displayModeBar': False})

# --- Skills Bar ---
with col4:
    st.subheader("Skills")
    skill_counts = get_value_counts("Skills").head(top_n_per_column["Skills"]).sort_values(ascending=False)
    fig_skill = px.bar(
        x=skill_counts.index,
        y=skill_counts.values,
        labels={'x': '', 'y': ''},
        height=400
    )
    fig_skill.update_layout(xaxis=dict(tickangle=45))
    st.plotly_chart(fig_skill, use_container_width=True, config={'displayModeBar': False})
 