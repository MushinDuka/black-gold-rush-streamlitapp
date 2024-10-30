import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(layout="wide")



file_path = 'data/discogs_electr_90s_clean.csv'
df = pd.read_csv(file_path)

# Filter the data for only Vinyl format
vinyl_data = df[df['format'] == 'Vinyl']

# Prepare data for the stacked bar graphs
top_labels = df['label'].value_counts().head(15).index
label_format_data = df[df['label'].isin(top_labels)]
label_format_data = label_format_data.groupby(['label', 'format']).size().unstack(fill_value=0)

top_formats = df['format'].value_counts().head(3).index
label_format_data = label_format_data.loc[:, label_format_data.columns.isin(top_formats)]
label_format_data['Total'] = label_format_data.sum(axis=1)
label_format_data = label_format_data.sort_values(by='Total', ascending=False).drop(columns='Total')

top_countries = df['country'].value_counts().head(15).index
country_format_data = df[df['country'].isin(top_countries)]
country_format_data = country_format_data.groupby(['country', 'format']).size().unstack(fill_value=0)
country_format_data = country_format_data.loc[:, country_format_data.columns.isin(top_formats)]
country_format_data['Total'] = country_format_data.sum(axis=1)
country_format_data = country_format_data.sort_values(by='Total', ascending=False).drop(columns='Total')

exploded_styles = df.assign(styles=df['styles'].str.split(',')).explode('styles')
top_styles = exploded_styles['styles'].value_counts().head(20).index
style_format_data = exploded_styles[exploded_styles['styles'].isin(top_styles)]
style_format_data = style_format_data.groupby(['styles', 'format']).size().unstack(fill_value=0)
style_format_data = style_format_data.loc[:, style_format_data.columns.isin(top_formats)]
style_format_data['Total'] = style_format_data.sum(axis=1)
style_format_data = style_format_data.sort_values(by='Total', ascending=False).drop(columns='Total')

# Define custom colors
custom_colors = {
    'CD': '#A020F0',         # Purple
    'Vinyl': '#F769DC',      # Pink
    'Laserdisc': '#8B008B'   # Darker shade of purple
}


st.title("EDA for Discogs 90s Electronic Releases")

if st.checkbox('Show raw data'):
    st.write(df)

st.caption("""
**Source:** [kaggle](https://www.kaggle.com/datasets/thedevastator/music-sales-by-format-and-year/data)
  
**Data Curated by:** Charlie Hutcheson

""")




st.header("Some Basic Statistics")
tab1, tab2, tab3 = st.tabs(["Top 15 Labels", "Top 15 Countries", "Top 20 Styles"])

with tab1:
    fig1 = px.bar(label_format_data, x=label_format_data.index, y=label_format_data.columns,
                  title="Top 15 Labels with Top 3 Formats",
                  labels={"value": "Number of Releases", "label": "Label"},
                  barmode="stack", color_discrete_map=custom_colors)
    st.plotly_chart(fig1)

with tab2:
    fig2 = px.bar(country_format_data, x=country_format_data.index, y=country_format_data.columns,
                  title="Top 15 Countries with Top 3 Formats",
                  labels={"value": "Number of Releases", "country": "Country"},
                  barmode="stack", color_discrete_map=custom_colors)
    st.plotly_chart(fig2)

with tab3:
    fig3 = px.bar(style_format_data, x=style_format_data.index, y=style_format_data.columns,
                  title="Top 20 Styles with Top 3 Formats",
                  labels={"value": "Number of Releases", "styles": "Style"},
                  barmode="stack", color_discrete_map=custom_colors)
    st.plotly_chart(fig3)

# Distribution over the years
st.header("Distribution of Releases Over the Years")
year_format_data = df.groupby(['release_year', 'format']).size().unstack(fill_value=0)
year_format_data = year_format_data.loc[:, year_format_data.columns.isin(top_formats)]

fig4 = px.bar(year_format_data, x=year_format_data.index, y=year_format_data.columns,
              title="Distribution of Releases Over the Years with Top 3 Formats",
              labels={"value": "Number of Releases", "release_year": "Release Year"},
              barmode="stack", color_discrete_map=custom_colors)
st.plotly_chart(fig4)



# Tabbed interface for Vinyl-specific analysis
st.header("Vinyl-Specific Analysis")
tab4, tab5, tab6 = st.tabs(["Average 'Have'", "Average 'Want'", "Average 'Median Price'"])

avg_have_per_year = vinyl_data.groupby('release_year')['have'].mean()
avg_want_per_year = vinyl_data.groupby('release_year')['want'].mean()
avg_median_price_per_year = vinyl_data.groupby('release_year')['median price_(USD)'].mean()

line_color = '#800080'  # Purple

with tab4:
    fig5 = px.line(avg_have_per_year, x=avg_have_per_year.index, y=avg_have_per_year.values,
                   title='Average "Have" for Each Release Year (Vinyl Format)',
                   labels={"x": "Release Year", "y": "Average 'Have'"}, line_shape="linear")
    fig5.update_traces(line=dict(color=line_color))
    st.plotly_chart(fig5)

with tab5:
    fig6 = px.line(avg_want_per_year, x=avg_want_per_year.index, y=avg_want_per_year.values,
                   title='Average "Want" for Each Release Year (Vinyl Format)',
                   labels={"x": "Release Year", "y": "Average 'Want'"}, line_shape="linear")
    fig6.update_traces(line=dict(color=line_color))
    st.plotly_chart(fig6)

with tab6:
    fig7 = px.line(avg_median_price_per_year, x=avg_median_price_per_year.index, y=avg_median_price_per_year.values,
                   title='Average "Median Price (USD)" for Each Release Year (Vinyl Format)',
                   labels={"x": "Release Year", "y": "Average Median Price (USD)"}, line_shape="linear")
    fig7.update_traces(line=dict(color=line_color))
    st.plotly_chart(fig7)
st.image("discogs_statistics_screenshot.png")
st.markdown("""
### Analysis of Vinyl-Specific Metrics Over the Years

- **Average "Have" Over the Years**:
    - The trend in the average "have" metric shows how the popularity and collectibility of vinyl releases have evolved over time.
    - An increasing trend suggests that certain years' releases are becoming more widely collected, possibly due to their rarity, cultural significance, or resurgence in popularity.
    - Periods with spikes may indicate the release of iconic albums or the influence of reissues that have boosted ownership.

- **Average "Want" Over the Years**:
    - The average "want" metric provides insights into the desirability of vinyl releases from different years.
    - A rising trend indicates growing demand, suggesting that collectors and enthusiasts are increasingly seeking out releases from specific periods.
    - Peaks in the "want" trend could be linked to particular genres, artists, or albums gaining renewed interest or achieving cult status.

- **Average "Median Price (USD)" Over the Years**:
    - The average median price trend reflects the market value of vinyl releases over time.
    - An upward trend suggests that records from certain years are appreciating in value, possibly due to increased demand or their growing status as collector's items.
    - Significant fluctuations in median price may be influenced by the rarity of records, the condition in which they are available, or market dynamics such as supply and demand.
""")
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)



# Tabbed interface for distribution plots
st.header("Distributions of key metrics for Vinyl Format")
distribution_columns = ['have', 'want', 'lowest_price_(USD)', 'median price_(USD)', 'highest_price_(USD)', 'mean_rating']
distribution_titles = ["Distribution of 'Have'", "Distribution of 'Want'", "Distribution of 'Lowest Price (USD)'",
                       "Distribution of 'Median Price (USD)'", "Distribution of 'Highest Price (USD)'",
                       "Distribution of 'Mean Rating'"]

tab7, tab8, tab9, tab10, tab11, tab12 = st.tabs(distribution_titles)

tabs = [tab7, tab8, tab9, tab10, tab11, tab12]

for i, column in enumerate(distribution_columns):
    with tabs[i]:
        fig = px.histogram(vinyl_data, x=column, nbins=30, marginal="box", title=distribution_titles[i],
                           labels={column: column.replace("_", " ").capitalize()}, color_discrete_sequence=['#F769DC'])
        st.plotly_chart(fig)
st.markdown("""
### Analysis of Vinyl-Specific Distributions

- **Distribution of 'Have'**:
    - The distribution of the "have" metric indicates the number of users who own each vinyl release.
    - A right-skewed distribution suggests that most vinyl releases are owned by a moderate number of users, with a few highly popular releases being widely collected.
    - This pattern highlights the niche nature of many vinyl releases, with certain records achieving significant popularity.

- **Distribution of 'Want'**:
    - The "want" distribution reflects how many users desire each vinyl release.
    - A skew towards lower values with some high outliers suggests that while most releases have limited demand, a few are highly sought after.
    - The peaks in this distribution likely represent iconic or rare records that are particularly desirable to collectors.

- **Distribution of 'Lowest Price (USD)'**:
    - This distribution shows the lowest price at which each vinyl release is available.
    - A left-skewed distribution indicates that many vinyl records are accessible at lower price points, though some records have a relatively higher minimum price.
    - The presence of higher prices could reflect factors like rarity, condition, or demand for certain releases.

- **Distribution of 'Median Price (USD)'**:
    - The median price distribution provides a better sense of the typical pricing for vinyl releases.
    - A central peak in this distribution suggests that most vinyl records fall within a common price range, with fewer records being significantly more expensive.
    - This distribution can help identify the market value for the majority of vinyl releases, while highlighting outliers that command higher prices.

- **Distribution of 'Highest Price (USD)'**:
    - The "highest price" distribution captures the maximum price that collectors have paid for each vinyl release.
    - A right-skewed distribution indicates that while many records do not reach high prices, some have been sold at premium levels, possibly due to their rarity or collector status.
    - This distribution is useful for understanding the upper end of the market and identifying particularly valuable records.

- **Distribution of 'Mean Rating'**:
    - The distribution of "mean rating" reflects the average rating users have given to each vinyl release.
    - If the distribution is skewed towards higher values, it indicates that the majority of vinyl records are well-regarded by collectors and listeners.
    - This can suggest that the dataset primarily includes high-quality or culturally significant records that have been positively received.
""")
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


# Correlation matrix
st.header("Correlation Matrix for Vinyl Releases")
correlation_columns = ['have', 'want', 'lowest_price_(USD)', 'median price_(USD)', 'highest_price_(USD)', 'mean_rating', 'num_ratings', 'release_year']
correlation_data = vinyl_data[correlation_columns]
correlation_matrix = correlation_data.corr()

# Use a suitable purple color scale
fig_corr = px.imshow(correlation_matrix, text_auto=True, aspect="auto", title="Correlation Matrix for Vinyl Releases",
                     color_continuous_scale=px.colors.sequential.Purples)
st.plotly_chart(fig_corr)

# Analysis
st.subheader("Correlation Matrix Analysis")
st.write("""
The correlation matrix reveals several interesting insights:

1. **Have and Want**: There is a strong positive correlation between 'have' and 'want' values, indicating that releases that are widely owned are also highly desired.

2. **Prices**: The correlation between the different price points (lowest, median, highest) is strong, which is expected. However, 'median price' correlates slightly more with 'want' than 'lowest price', suggesting that more desirable releases tend to be priced higher.

3. **Mean Rating**: 'Mean rating' shows a moderate positive correlation with 'have' and 'want', implying that better-rated releases are both more owned and desired.

4. **Num Ratings**: The 'num_ratings' is highly correlated with both 'have' and 'want', as expected. Popular releases tend to attract more ratings.

5. **Release Year**: The 'release_year' shows a weak correlation with most variables, except for a slight negative correlation with prices, suggesting that older releases may be slightly more expensive.
""")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

st.header("The Cheapest and the Most Expensive Records:")
st.markdown("<br>", unsafe_allow_html=True)
# Display the images side by side
col1, col2 = st.columns(2)

with col1:
    st.image("cheapest_release.jpg", caption="Cheapest Record")
    st.markdown("""
    **Artist**: Pick-4  
    **Title**: Think (Just A Little Bit)  
    **Label**: Global Village, UK              
    **lowest_price_(USD)**: 0.0$
    """)

with col2:
    st.image("mostExpensive.jpg", caption="Most Expensive Record")
    st.markdown("""
    **Artist**: Jaco  
    **Title**: Show Some Love  
    **Label**: Warp Records, UK            
    **Highest_price_(USD)**: 550.0$            
    """)