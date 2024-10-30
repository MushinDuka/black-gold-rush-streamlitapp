import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(layout="wide")

@st.cache_data
def load_data(file_path):
    df_discogs = pd.read_csv(file_path)
    return df_discogs

file_path = 'data/discogs_clean.csv'
df_discogs = load_data(file_path)


st.image("Discogs_logo.png")

st.title('Some General Insights into Discogs Catalogue')


if st.checkbox('Show raw data'):
    st.write(df_discogs)

st.caption("""
**Source:** [kaggle](https://www.kaggle.com/datasets/ofurkancoban/discogs-releases-dataset/data)
  
**Data Curated by:** Furkan Çoban

""")


#for column in ['country', 'format', 'genre']:

    #from plotly.express import bar

   # bar(data_frame=df_discogs['country'].value_counts().to_frame().reset_index().head(n=10), x=column, y='count').show()


   
def plot_top_genres(df):
    genre_counts = df['genre'].value_counts().head(10)
    fig = px.bar(
        genre_counts, 
        x=genre_counts.index, 
        y=genre_counts.values,
        labels={"x": "", "y": "Count"},
        color_discrete_sequence=['#A020F0']
    )
    fig.update_layout(xaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)

def plot_top_formats(df):
    format_counts = df['format'].value_counts().head(5)
    fig = px.bar(
        format_counts, 
        x=format_counts.index, 
        y=format_counts.values,
        labels={"x": "", "y": "Count"},
        color_discrete_sequence=['#A020F0']
    )
    fig.update_layout(xaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)

def plot_top_countries_with_electronic(df):
    # Exclude 'Europe' and count total entries per country
    total_counts = df_discogs[df_discogs['country'] != 'Europe']['country'].value_counts().reset_index().head(10)
    total_counts.columns = ['Country', 'Total Count']

    # Count 'Electronic' genre entries per country
    electronic_counts = (
        df_discogs[df_discogs['genre'] == 'Electronic']
        .groupby('country')
        .size()
        .reset_index(name='Electronic Count')
    )

    # Merge the two counts
    merged_counts = pd.merge(total_counts, electronic_counts, how='left', left_on='Country', right_on='country')
    merged_counts['Electronic Count'] = merged_counts['Electronic Count'].fillna(0)
    merged_counts = merged_counts.drop(columns=['country'])  # Drop redundant column

    # Melt the data for Plotly Express to create grouped bars
    melted_counts = merged_counts.melt(id_vars='Country', value_vars=['Total Count', 'Electronic Count'])

    # Create the bar chart
    fig = px.bar(
        data_frame=melted_counts,
        x='Country',
        y='value',
        color='variable',
        barmode='group',
        labels={'value': 'Count', 'variable': ''},
        template='plotly_dark',
        color_discrete_map={"Total Count": "#A020F0", "Electronic Count": "#F769DC"}
    )
    fig.update_layout(xaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)


def plot_releases_by_genre_and_year(df):
    # Filter for top 10 genres based on overall count
    top_genres = df['genre'].value_counts().head(10).index
    
    # Filter the DataFrame for these top genres and only up to the year 2020
    filtered_df = df[(df['genre'].isin(top_genres)) & (df['release_year'] <= 2020)]
    
    # Group by year and genre
    genre_year_grouped = filtered_df.groupby(['release_year', 'genre']).size().unstack(fill_value=0)
    
    # Plot the line chart
    fig = px.line(
        genre_year_grouped,
        x=genre_year_grouped.index,
        y=[genre_year_grouped[col] for col in genre_year_grouped.columns],
        labels={"value": "Number of Releases", "variable": "Genre", "index": ""},
        height=800  # Adjusted height for better visibility 
    )
    fig.update_layout(xaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)

    
def plot_labels_releasing_top_genres_over_time(df):
    # Identify the top 5 genres based on the overall number of releases
    top_genres = df['genre'].value_counts().head(5).index.tolist()

    # Filter the DataFrame to include only the top 5 genres and years up to 2020
    top_genre_df = df[(df['genre'].isin(top_genres)) & (df['release_year'] <= 2020)]

    # Group by year and genre, and count unique labels for each genre per year
    labels_per_year_genre = top_genre_df.groupby(['release_year', 'genre'])['label'].nunique().reset_index()

    # Plot the line graph using Plotly Express
    fig = px.line(
        labels_per_year_genre,
        x='release_year',
        y='label',
        color='genre',
        labels={'label': 'Number of Unique Labels', 'release_year': 'Year', 'genre': 'Genre'},
        height=800  # Adjusted for better visibility
    )
    fig.update_layout(xaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)



def plot_unique_styles_over_time(df):
    # Filter for electronic genre and year <= 2020
    electronic_df = df[(df['genre'] == 'Electronic') & (df['release_year'] <= 2020)]
    
    # Explode the 'styles' column which contains comma-separated values
    electronic_df['styles'] = electronic_df['styles'].str.split(',').explode()
    
    # Drop any NA values that might result from empty styles fields
    electronic_df = electronic_df.dropna(subset=['styles'])
    
    # Group by year and count unique styles
    styles_per_year = electronic_df.groupby('release_year')['styles'].nunique().reset_index()
    
    # Plot the line graph
    fig = px.line(
        styles_per_year, 
        x='release_year', 
        y='styles',
        labels={'styles': 'Unique Styles', 'release_year': 'Year'},
        height=800 
    )
    fig.update_layout(xaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)




def main():
    st.subheader("Top 10 Genres")
    plot_top_genres(df_discogs)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("Top 5 Formats")
    plot_top_formats(df_discogs)
    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("Top 10 Countries in Terms of Total Music Releases compared to Electronic Music Genre")
    plot_top_countries_with_electronic(df_discogs)
    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("Trends of Music Releases by Genre Over Years")
    plot_releases_by_genre_and_year(df_discogs)
    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("Number of Labels Issuing Releases by Genre and Year")
    plot_labels_releasing_top_genres_over_time(df_discogs)
    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("Analysis of Electronic Music Subgenres Over Time")
    plot_unique_styles_over_time(df_discogs)

if __name__ == "__main__":
    main()