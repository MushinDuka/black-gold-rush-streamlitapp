import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import matplotlib.pyplot as plt

df_dc_electr_90s = pd.read_csv('./data/discogs_electr_90s_clean.csv')


df_dc_electr_90s['styles'] = df_dc_electr_90s['styles'].str.split(',')
df_dc_electr_90s_exploded = df_dc_electr_90s.explode('styles')
df_dc_electr_90s_exploded['styles'] = df_dc_electr_90s_exploded['styles'].str.strip()


st.title('Development of Electronic Music Styles Over Time')


if st.checkbox('Show raw data'):
    st.write(df_dc_electr_90s_exploded)


st.header('Chronological Development of Styles')

# Group by year and style to count the number of releases per style each year
styles_by_year = df_dc_electr_90s_exploded.groupby(['release_year', 'styles']).size().reset_index(name='count')


#Display only the top N most common styles
top_styles = df_dc_electr_90s_exploded['styles'].value_counts().head(15).index.tolist()
styles_by_year_top = styles_by_year[styles_by_year['styles'].isin(top_styles)]

fig_top_styles_over_time = px.line(styles_by_year_top, x='release_year', y='count', color='styles',
                                   title='Development of Top 15 Styles Over Time',
                                   labels={'release_year': 'Release Year', 'count': 'Number of Releases'},
                                   markers=True)
st.plotly_chart(fig_top_styles_over_time)

st.header('Tree Map of Electronic Music Subgenres')

# Calculate style counts and filter to top 20
style_counts = df_dc_electr_90s_exploded['styles'].value_counts().reset_index()
style_counts.columns = ['styles', 'count']

# Filter to only include the top 20 styles
top_20_styles = style_counts.head(40)

# Create the tree map with the top 20 styles
fig_tree_map = px.treemap(top_20_styles, path=['styles'], values='count',
                          labels={'count': 'Number of Releases'})

st.plotly_chart(fig_tree_map)

# Section: Streamgraph of Top 15 Styles Over Time
st.title('Streamgraph of Top 15 Electronic Music Subgenres in the 90s')

# Identify the top 15 most common styles
top_15_styles = df_dc_electr_90s_exploded['styles'].value_counts().head(15).index.tolist()

# Filter the dataset for only the top 15 styles
filtered_styles = df_dc_electr_90s_exploded[df_dc_electr_90s_exploded['styles'].isin(top_15_styles)]

# Group by year and style to count the number of releases per style each year
styles_by_year = filtered_styles.groupby(['release_year', 'styles']).size().reset_index(name='count')

# Create a streamgraph using Plotly Express
fig_streamgraph = px.area(
    styles_by_year,
    x='release_year',
    y='count',
    color='styles',
    line_group='styles',
    labels={'release_year': 'Year', 'count': 'Number of Releases'},
    title='Development of Top 15 Electronic Music Subgenres in the 90s',
)

# Customize the layout for better readability
fig_streamgraph.update_layout(
    xaxis_title='Year',
    yaxis_title='Number of Releases',
    showlegend=True,
    legend_title_text='Styles',
    hovermode='x unified',
)

# Display the streamgraph
st.plotly_chart(fig_streamgraph)



# Section: Sunburst Chart of Top 10 Styles Over Time
st.title('Sunburst Chart of Top 10 Electronic Music Subgenres in the 90s')

# Identify the top 15 most common styles
top_10_styles = df_dc_electr_90s_exploded['styles'].value_counts().head(10).index.tolist()

# Filter the dataset for only the top 15 styles
filtered_styles = df_dc_electr_90s_exploded[df_dc_electr_90s_exploded['styles'].isin(top_10_styles)]

# Group by year and style to count the number of releases per style each year
styles_by_year = filtered_styles.groupby(['release_year', 'styles']).size().reset_index(name='count')

# Create a sunburst chart using Plotly Express
fig_sunburst = px.sunburst(
    styles_by_year,
    path=['release_year', 'styles'],
    values='count',
    color='styles',
    labels={'release_year': 'Year', 'styles': 'Style', 'count': 'Number of Releases'},
    title='Sunburst Chart of Top 15 Electronic Music Subgenres in the 90s',
)

# Customize the layout for better readability
fig_sunburst.update_layout(
    margin=dict(t=50, l=25, r=25, b=25)
)

# Display the sunburst chart
st.plotly_chart(fig_sunburst)








