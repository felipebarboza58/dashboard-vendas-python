import os
import pandas as pd
import streamlit as st
import plotly.express as px

# ===================== CONFIG =====================
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

# 🎨 DARK THEME PROFISSIONAL
st.markdown("""
<style>
    body {
        background-color: #0e1117;
        color: #FAFAFA;
    }

    .main {
        background-color: #0e1117;
    }

    .stMetric {
        background-color: #1c1f26;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #2a2f3a;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.4);
    }

    h1, h2, h3 {
        color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Sales Performance Dashboard")
st.markdown("---")

# ===================== DESCRIÇÃO =====================
st.markdown("""
Análise interativa de vendas com foco em performance por região, categoria e período.
""")

# ===================== LOAD DATA =====================
@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "dados_dashboard_python.xlsx")
    df = pd.read_excel(file_path)
    df["Mes"] = df["Data"].dt.to_period("M").astype(str)
    return df

df = load_data()

# ===================== SIDEBAR =====================
st.sidebar.header("⚙️ Filters")

categoria = st.sidebar.multiselect(
    "Category",
    df["Categoria"].unique(),
    default=df["Categoria"].unique()
)

regiao = st.sidebar.multiselect(
    "Region",
    df["Região"].unique(),
    default=df["Região"].unique()
)

data_range = st.sidebar.date_input(
    "Date Range",
    [df["Data"].min(), df["Data"].max()]
)

# ===================== FILTRO =====================
filtered_df = df[
    (df["Categoria"].isin(categoria)) &
    (df["Região"].isin(regiao)) &
    (df["Data"] >= pd.to_datetime(data_range[0])) &
    (df["Data"] <= pd.to_datetime(data_range[1]))
]

# ===================== KPIs =====================
total_vendas = filtered_df["Vendas"].sum()
total_lucro = filtered_df["Lucro"].sum()
media_vendas = filtered_df["Vendas"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Revenue", f"${total_vendas:,.0f}")
col2.metric("📈 Profit", f"${total_lucro:,.0f}")
col3.metric("📊 Avg Ticket", f"${media_vendas:,.0f}")

st.markdown("---")

# ===================== INSIGHTS =====================
st.subheader("📌 Key Insights")

df_cat = filtered_df.groupby("Categoria")["Vendas"].sum().reset_index()

if not df_cat.empty:
    df_cat = df_cat.sort_values(by="Vendas", ascending=False)
    top_categoria = df_cat.iloc[0]["Categoria"]
    top_regiao = filtered_df.groupby("Região")["Vendas"].sum().idxmax()

    st.markdown(f"""
    <div style='background-color:#1c1f26;padding:15px;border-radius:10px;border:1px solid #2a2f3a'>
    🔎 <b>Top Category:</b> {top_categoria} <br>
    🌍 <b>Top Region:</b> {top_regiao} <br>
    💰 <b>Total Revenue:</b> ${total_vendas:,.0f}
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ===================== GRÁFICOS =====================

# Linha
st.subheader("📈 Sales Trend")

df_time = filtered_df.groupby("Data")["Vendas"].sum().reset_index()
fig_time = px.line(df_time, x="Data", y="Vendas", template="plotly_dark")
st.plotly_chart(fig_time, use_container_width=True)

# Categoria + Região
st.subheader("📊 Sales Distribution")

col4, col5 = st.columns(2)

with col4:
    df_cat = filtered_df.groupby("Categoria")["Vendas"].sum().reset_index()
    df_cat = df_cat.sort_values(by="Vendas", ascending=False)
    fig_cat = px.bar(df_cat, x="Categoria", y="Vendas", template="plotly_dark", text_auto=True)
    st.plotly_chart(fig_cat, use_container_width=True)

with col5:
    fig_reg = px.pie(filtered_df, names="Região", values="Vendas", template="plotly_dark")
    st.plotly_chart(fig_reg, use_container_width=True)

# Mensal
st.subheader("📅 Monthly Analysis")

df_mes = filtered_df.groupby("Mes")["Vendas"].sum().reset_index()
fig_mes = px.bar(df_mes, x="Mes", y="Vendas", template="plotly_dark")
st.plotly_chart(fig_mes, use_container_width=True)

st.markdown("---")

# ===================== TABELA =====================
st.subheader("📋 Detailed Data")
st.dataframe(filtered_df)