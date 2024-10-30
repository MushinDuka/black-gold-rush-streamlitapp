import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(layout="wide")



st.markdown("<h1 style='font-size: 90px; text-align: center; color: purple;'>Black Gold Rush</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: black;'>Short Exploratory Data Analysis of the Vinyl Records Market with focus on Electronic Genre Music Sold on Discogs</h2>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

st.image("finalProjTitelBild.png")
st.caption("""
**Source:** [luminate-2022-u-s-year-end-report](https://luminatedata.com/reports/luminate-2022-u-s-year-end-report/)
 **Luminate U.S. Year-End Music Report for 2022**
            """)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

st.image("Discogs_logo.png")
st.header('What is Discogs?')
st.markdown("""
Discogs is an online music database and marketplace that serves music collectors and enthusiasts. It was founded by Kevin Lewandowski in 2000. It initially started as a tool for tracking record collections and gradually grew into a worldwide music database and sales platform.

The primary purpose of Discogs is to allow users to track their own music collections and share them with other music enthusiasts. Users can catalog albums, singles, LPs, and other music recordings. Each record has a detailed page containing artist information, track listings, release details, and more.

One of the significant features of Discogs is its wiki-style database that enables users to add, edit, and correct information about music recordings. This allows users to correct missing or erroneous information and keeps the music database continuously updated.

Additionally, music recordings can be bought and sold on Discogs. Users can list their collections for sale or purchase music recordings from other users. This provides music collectors with the opportunity to find rare or special editions from a wide range of sources.

Discogs has become a crucial resource for music enthusiasts and collectors, hosting a vast database with millions of music recordings from around the world. Despite changes in the music industry, Discogs continues to assist in preserving and sharing music.""")