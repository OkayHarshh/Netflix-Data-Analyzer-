import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("🎬 Netflix Data Analyzer")

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    return df

df = load_data()


# Show raw data
if st.checkbox("Show Raw Data"):
    st.write(df)

# Show basic stats
st.subheader("Dataset Overview")
st.write(f"Total Titles: {df.shape[0]}")
st.write(f"Date Range: {df['release_year'].min()} - {df['release_year'].max()}")

# Filter by type
st.sidebar.header("🔍 Filter Options")
selected_type = st.sidebar.multiselect("Select Type", options=df['type'].unique(), default=df['type'].unique())
filtered_df = df[df['type'].isin(selected_type)]

# Country filter
countries = df['country'].dropna().unique()
selected_country = st.sidebar.selectbox("Filter by Country", options=['All'] + sorted(countries.tolist()))
if selected_country != 'All':
    filtered_df = filtered_df[filtered_df['country'] == selected_country]

# Year slider
min_year = int(df['release_year'].min())
max_year = int(df['release_year'].max())
year_range = st.sidebar.slider("Select Release Year Range", min_year, max_year, (min_year, max_year))
filtered_df = filtered_df[(filtered_df['release_year'] >= year_range[0]) & (filtered_df['release_year'] <= year_range[1])]

# Show filtered results
st.subheader("🎥 Filtered Titles")
st.write(filtered_df[['title', 'type', 'release_year', 'country']])

# Plot: Number of releases by year
st.subheader("📊 Number of Releases per Year")
year_counts = filtered_df['release_year'].value_counts().sort_index()
fig, ax = plt.subplots()
year_counts.plot(kind='bar', ax=ax)
plt.xlabel("Year")
plt.ylabel("Number of Titles")
st.pyplot(fig)

# Plot: Top 10 countries
st.subheader("🌍 Top Countries by Number of Titles")
top_countries = df['country'].value_counts().head(10)
st.bar_chart(top_countries)


