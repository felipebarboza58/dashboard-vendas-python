import os
import pandas as pd
import streamlit as st
import plotly.express as px

# ===================== CONFIG =====================
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

# Tema DARK premium
st.markdown("""
<style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .stMetric {
        background-color: #1c1f26;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.5);
    }
</style>
""", unsafe_allow_html=True)

st.title("🌙 Dashboard de Vendas")

# ===================== DESCRIÇÃO =====================
st.info("""
Dashboard interativo para análise de vendas com filtros dinâmicos e geração de insights.

Tecnologias:
- Python
- Pandas
- Streamlit
- Plotly
""")

# ===================== UPLOAD =====================
uploaded_file = st.sidebar.file_uploader("📂 Enviar arquivo Excel", type=["xlsx"])

# ===================== LOAD DATA =====================
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
    else:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "dados_dashboard_python.xlsx")
        df = pd.read_excel(file_path)

    df["Mes"] = df["Data"].dt.to_period("M").astype(str)
    return df

df = load_data(uploaded_file)

# ===================== FILTROS =====================
st.sidebar.header("Filtros")

categoria = st.sidebar.multiselect(
    "Categoria",
    df["Categoria"].unique(),
    default=df["Categoria"].unique()
)

regiao = st.sidebar.multiselect(
    "Região",
    df["Região"].unique(),
    default=df["Região"].unique()
)

data_range = st.sidebar.date_input(
    "Período",
    [df["Data"].min(), df["Data"].max()]
)

# ===================== FILTRAR =====================
filtered_df = df[
    (df["Categoria"].isin(categoria)) &
    (df["Região"].isin(regiao)) &
    (df["Data"] >= pd.to_datetime(data_range[0])) &
    (df["Data"] <= pd.to_datetime(data_range[1]))
]

# ===================== KPIs =====================
total_vendas = filtered_df["Vendas"].sum()
total_lucro = filtered_df["Lucro"].sum()

col1, col2 = st.columns(2)

col1.metric("💰 Vendas", f"R$ {total_vendas:,.2f}")
col2.metric("📈 Lucro", f"R$ {total_lucro:,.2f}")

# ===================== INSIGHTS =====================
st.subheader("📊 Insights")

df_cat = filtered_df.groupby("Categoria")["Vendas"].sum().reset_index()

if not df_cat.empty:
    df_cat = df_cat.sort_values(by="Vendas", ascending=False)
    top_categoria = df_cat.iloc[0]["Categoria"]
    top_regiao = filtered_df.groupby("Região")["Vendas"].sum().idxmax()

    st.success(f"""
    🔎 Categoria líder: **{top_categoria}**  
    🌍 Região líder: **{top_regiao}**
    """)

# ===================== GRÁFICOS =====================
st.subheader("📈 Vendas no Tempo")
fig_time = px.line(filtered_df, x="Data", y="Vendas")
st.plotly_chart(fig_time, use_container_width=True)

st.subheader("📊 Categoria")
fig_cat = px.bar(df_cat, x="Categoria", y="Vendas")
st.plotly_chart(fig_cat, use_container_width=True)

st.subheader("🌎 Região")
fig_reg = px.pie(filtered_df, names="Região", values="Vendas")
st.plotly_chart(fig_reg, use_container_width=True)

st.subheader("📅 Mensal")
df_mes = filtered_df.groupby("Mes")["Vendas"].sum().reset_index()
fig_mes = px.bar(df_mes, x="Mes", y="Vendas")
st.plotly_chart(fig_mes, use_container_width=True)