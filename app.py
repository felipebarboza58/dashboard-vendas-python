import os
import pandas as pd
import streamlit as st
import plotly.express as px

# CONFIG
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# HEADER
st.title("📊 Sales Analytics Dashboard")
st.caption("Real-time performance insights")

st.markdown("---")

# LOAD DATA
@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "dados_dashboard_python.xlsx")
    df = pd.read_excel(file_path)
    df["Mes"] = df["Data"].dt.to_period("M").astype(str)
    return df

df = load_data()

# SIDEBAR
with st.sidebar:
    st.header("🔎 Filters")

    categoria = st.multiselect(
        "Category",
        df["Categoria"].unique(),
        default=df["Categoria"].unique()
    )

    regiao = st.multiselect(
        "Region",
        df["Região"].unique(),
        default=df["Região"].unique()
    )

    data_range = st.date_input(
        "Date Range",
        [df["Data"].min(), df["Data"].max()]
    )

# FILTER
filtered_df = df[
    (df["Categoria"].isin(categoria)) &
    (df["Região"].isin(regiao)) &
    (df["Data"] >= pd.to_datetime(data_range[0])) &
    (df["Data"] <= pd.to_datetime(data_range[1]))
]

# KPIs
total_vendas = filtered_df["Vendas"].sum()
total_lucro = filtered_df["Lucro"].sum()
media_vendas = filtered_df["Vendas"].mean()

k1, k2, k3 = st.columns(3)

k1.metric("💰 Revenue", f"${total_vendas:,.0f}")
k2.metric("📈 Profit", f"${total_lucro:,.0f}")
k3.metric("📊 Avg Ticket", f"${media_vendas:,.0f}")

st.markdown("---")

# GRÁFICOS
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Sales Trend")
    df_time = filtered_df.groupby("Data")["Vendas"].sum().reset_index()
    fig = px.line(df_time, x="Data", y="Vendas", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🏆 Top Categories")
    df_cat = filtered_df.groupby("Categoria")["Vendas"].sum().reset_index()
    df_cat = df_cat.sort_values(by="Vendas", ascending=False)
    fig = px.bar(df_cat, x="Categoria", y="Vendas", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# FULL WIDTH
st.subheader("🌍 Regional Distribution")
fig = px.pie(filtered_df, names="Região", values="Vendas", template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# INSIGHTS
st.markdown("---")
st.subheader("📌 Insights")

if not filtered_df.empty:
    top_categoria = filtered_df.groupby("Categoria")["Vendas"].sum().idxmax()
    top_regiao = filtered_df.groupby("Região")["Vendas"].sum().idxmax()

    st.success(f"""
Top Category: {top_categoria}  
Top Region: {top_regiao}  
Total Revenue: ${total_vendas:,.0f}
""")

# TABLE
st.markdown("---")
st.subheader("📋 Data")
st.dataframe(filtered_df)