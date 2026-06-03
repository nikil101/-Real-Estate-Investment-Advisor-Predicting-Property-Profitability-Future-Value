import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("india_housing_prices original.csv")
    
    # Feature Engineering
    df['Price_per_SqFt'] = df['Price_in_Lakhs'] / df['Size_in_SqFt']
    df['Age_of_Property'] = 2025 - df['Year_Built']
    
    return df

df = load_data()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.title(" Filters")

city = st.sidebar.multiselect("City", df['City'].dropna().unique(), default=df['City'].dropna().unique())
ptype = st.sidebar.multiselect("Property Type", df['Property_Type'].dropna().unique(), default=df['Property_Type'].dropna().unique())
bhk = st.sidebar.multiselect("BHK", df['BHK'].dropna().unique(), default=df['BHK'].dropna().unique())

filtered_df = df[
    (df['City'].isin(city)) &
    (df['Property_Type'].isin(ptype)) &
    (df['BHK'].isin(bhk))
]

# ---------------- TITLE ----------------
st.title(" Real Estate Investment Dashboard")

# ---------------- KPIs ----------------
col1, col2, col3 = st.columns(3)

col1.metric("Avg Price (₹ Lakhs)", f"{filtered_df['Price_in_Lakhs'].mean():,.0f}")
col2.metric("Avg Size (SqFt)", f"{filtered_df['Size_in_SqFt'].mean():,.0f}")
col3.metric("Avg Price/SqFt", f"{filtered_df['Price_per_SqFt'].mean():,.2f}")

st.markdown("---")

# ---------------- USER INPUT ----------------
st.sidebar.markdown("##  Property Input")

size = st.sidebar.number_input("Size (SqFt)", 500, 5000, 1000)
bhk_input = st.sidebar.selectbox("BHK", [1,2,3,4,5])
amenities = st.sidebar.selectbox("Amenities", ["Low","Medium","High"])
transport = st.sidebar.selectbox("Transport Access", ["Low","Medium","High"])
schools = st.sidebar.slider("Nearby Schools", 0, 10, 3)

# ---------------- INVESTMENT LOGIC ----------------
median_price = df['Price_per_SqFt'].median()

user_price_per_sqft = filtered_df['Price_per_SqFt'].mean()

good_investment = (
    (user_price_per_sqft <= median_price) and
    (amenities == "High") and
    (transport == "High") and
    (schools >= 3)
)

st.subheader(" Investment Analysis")

if good_investment:
    st.success(" Good Investment")
else:
    st.error(" Not a Good Investment")

# ---------------- FUTURE PRICE ----------------
current_price = size * user_price_per_sqft

growth_rate = 0.08

future_price = current_price * (1 + growth_rate) ** 5

st.metric(" Estimated Price in 5 Years (₹)", f"{future_price:,.0f}")

st.markdown("---")

# ---------------- CHARTS ----------------

col1, col2 = st.columns(2)

with col1:
    st.subheader(" Price Distribution")
    fig1 = px.histogram(filtered_df, x='Price_in_Lakhs', nbins=30)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader(" Size Distribution")
    fig2 = px.histogram(filtered_df, x='Size_in_SqFt', nbins=30)
    st.plotly_chart(fig2, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader(" Size vs Price")
    fig3 = px.scatter(filtered_df, x='Size_in_SqFt', y='Price_in_Lakhs')
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader(" Price per SqFt by Property Type")
    p = filtered_df.groupby('Property_Type')['Price_per_SqFt'].mean().reset_index()
    fig4 = px.bar(p, x='Property_Type', y='Price_per_SqFt')
    st.plotly_chart(fig4, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader(" Avg Price by City")
    c = filtered_df.groupby('City')['Price_in_Lakhs'].mean().reset_index()
    fig5 = px.bar(c, x='City', y='Price_in_Lakhs')
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    st.subheader(" Amenities Impact")
    a = filtered_df.groupby('Amenities')['Price_in_Lakhs'].mean().reset_index()
    fig6 = px.bar(a, x='Amenities', y='Price_in_Lakhs')
    st.plotly_chart(fig6, use_container_width=True)

# ---------------- HEATMAP ----------------
st.subheader(" Correlation Heatmap")

fig, ax = plt.subplots()
sns.heatmap(df.corr(numeric_only=True), ax=ax)

st.pyplot(fig)

# ---------------- INSIGHTS ----------------
st.subheader(" Key Insights")

st.info("""
• Property prices increase with size  
• Metro cities show higher pricing  
• Amenities and transport improve value  
• Mid-range properties dominate market  
""")