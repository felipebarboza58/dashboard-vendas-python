import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(
    page_title="Crie seu Dashboard Interativo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para deixar mais bonito
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.3rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho principal
st.markdown('<p class="main-header">📊 Crie seu Dashboard Interativo</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Transforme seus dados em visualizações profissionais em segundos!</p>',
            unsafe_allow_html=True)

# Introdução
with st.container():
    st.markdown("""
    <div class="info-box">
        <h3>🎯 Como funciona?</h3>
        <ol>
            <li><strong>Faça upload</strong> do seu arquivo Excel (.xlsx)</li>
            <li><strong>Selecione</strong> as colunas que deseja analisar</li>
            <li><strong>Visualize</strong> gráficos automáticos e interativos</li>
            <li><strong>Apresente</strong> seus dados de forma profissional!</li>
        </ol>
        <p>💡 <strong>Dica:</strong> Funciona para vendas, finanças, estatísticas, dados escolares e muito mais!</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar para upload
with st.sidebar:
    st.header("📁 Upload de Dados")
    uploaded_file = st.file_uploader(
        "Escolha seu arquivo Excel",
        type=['xlsx'],
        help="Faça upload de um arquivo .xlsx com seus dados"
    )

    st.markdown("---")
    st.markdown("""
    ### 📋 Requisitos do arquivo:
    - Formato: `.xlsx`
    - Primeira linha: cabeçalhos
    - Dados organizados em colunas

    ### 🎨 Recursos disponíveis:
    - ✅ Gráficos interativos
    - ✅ Análise automática
    - ✅ Múltiplas visualizações
    - ✅ Filtros dinâmicos
    """)

# Processamento do arquivo
if uploaded_file is not None:
    try:
        # Leitura do arquivo
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)

        st.success(f"✅ Arquivo carregado com sucesso! {len(df)} linhas encontradas.")

        # Abas de navegação
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Dados", "📈 Gráficos", "🔍 Análise", "⚙️ Personalizar"])

        # TAB 1: Visualização dos dados
        with tab1:
            st.subheader("📋 Visualização dos Dados")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Linhas", len(df))
            with col2:
                st.metric("Total de Colunas", len(df.columns))
            with col3:
                st.metric("Colunas Numéricas", len(df.select_dtypes(include=['number']).columns))

            st.dataframe(df, use_container_width=True, height=400)

            # Download dos dados
            st.download_button(
                label="📥 Baixar dados filtrados",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name='dados_dashboard.csv',
                mime='text/csv'
            )

        # TAB 2: Gráficos automáticos
        with tab2:
            st.subheader("📈 Visualizações Interativas")

            # Detectar colunas numéricas e categóricas
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

            if len(numeric_cols) > 0:
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### Selecione os dados para o gráfico:")

                    # Seleção de eixo X
                    x_column = st.selectbox(
                        "Eixo X (Categoria/Data)",
                        options=categorical_cols + numeric_cols if categorical_cols else numeric_cols,
                        key="x_axis"
                    )

                    # Seleção de eixo Y
                    y_column = st.selectbox(
                        "Eixo Y (Valores)",
                        options=numeric_cols,
                        key="y_axis"
                    )

                with col2:
                    st.markdown("#### Opções de visualização:")

                    chart_type = st.selectbox(
                        "Tipo de Gráfico",
                        ["Barras", "Linha", "Pizza", "Área", "Dispersão"]
                    )

                    color_theme = st.selectbox(
                        "Tema de Cores",
                        ["Padrão", "Viridis", "Plasma", "Turbo", "Sunset"]
                    )

                # Mapear temas de cores
                color_map = {
                    "Padrão": None,
                    "Viridis": "viridis",
                    "Plasma": "plasma",
                    "Turbo": "turbo",
                    "Sunset": "sunset"
                }

                # Gerar gráfico baseado na seleção
                st.markdown("---")

                if chart_type == "Barras":
                    fig = px.bar(df, x=x_column, y=y_column,
                                 color=x_column if x_column in categorical_cols else None,
                                 color_discrete_sequence=px.colors.qualitative.Set3,
                                 title=f"{y_column} por {x_column}")

                elif chart_type == "Linha":
                    fig = px.line(df, x=x_column, y=y_column,
                                  title=f"Evolução de {y_column}")
                    fig.update_traces(line_color="#667eea", line_width=3)

                elif chart_type == "Pizza":
                    if x_column in categorical_cols:
                        df_grouped = df.groupby(x_column)[y_column].sum().reset_index()
                        fig = px.pie(df_grouped, values=y_column, names=x_column,
                                     title=f"Distribuição de {y_column}")
                    else:
                        st.warning("⚠️ Para gráfico de pizza, escolha uma coluna categórica no eixo X")
                        fig = None

                elif chart_type == "Área":
                    fig = px.area(df, x=x_column, y=y_column,
                                  title=f"Área de {y_column}")
                    fig.update_traces(line_color="#667eea", fillcolor="rgba(102, 126, 234, 0.3)")

                else:  # Dispersão
                    fig = px.scatter(df, x=x_column, y=y_column,
                                     title=f"Dispersão: {x_column} vs {y_column}",
                                     trendline="ols")

                if fig:
                    fig.update_layout(height=500, showlegend=True)
                    st.plotly_chart(fig, use_container_width=True)

                # Gráficos adicionais automáticos
                st.markdown("---")
                st.subheader("📊 Visualizações Adicionais")

                col1, col2 = st.columns(2)

                with col1:
                    # Top 10 valores
                    if x_column in categorical_cols:
                        st.markdown("#### 🏆 Top 10")
                        top_10 = df.groupby(x_column)[y_column].sum().nlargest(10).reset_index()
                        fig_top = px.bar(top_10, x=x_column, y=y_column,
                                         color=y_column,
                                         color_continuous_scale="Blues")
                        fig_top.update_layout(height=400)
                        st.plotly_chart(fig_top, use_container_width=True)

                with col2:
                    # Estatísticas básicas
                    st.markdown("#### 📈 Estatísticas")
                    stats_df = df[numeric_cols].describe().round(2)
                    st.dataframe(stats_df, use_container_width=True)

            else:
                st.warning("⚠️ Nenhuma coluna numérica encontrada no arquivo. Verifique seus dados.")

        # TAB 3: Análise detalhada
        with tab3:
            st.subheader("🔍 Análise Detalhada")

            if len(numeric_cols) > 0:
                # Seleção de coluna para análise
                analysis_col = st.selectbox("Selecione a coluna para análise:", numeric_cols)

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Média", f"{df[analysis_col].mean():.2f}")
                with col2:
                    st.metric("Mediana", f"{df[analysis_col].median():.2f}")
                with col3:
                    st.metric("Máximo", f"{df[analysis_col].max():.2f}")
                with col4:
                    st.metric("Mínimo", f"{df[analysis_col].min():.2f}")

                # Histograma
                st.markdown("#### 📊 Distribuição dos Dados")
                fig_hist = px.histogram(df, x=analysis_col, nbins=30,
                                        title=f"Distribuição de {analysis_col}")
                fig_hist.update_traces(marker_color="#667eea")
                st.plotly_chart(fig_hist, use_container_width=True)

                # Box plot
                fig_box = px.box(df, y=analysis_col,
                                 title=f"Box Plot de {analysis_col}")
                fig_box.update_traces(marker_color="#764ba2")
                st.plotly_chart(fig_box, use_container_width=True)

        # TAB 4: Personalização
        with tab4:
            st.subheader("⚙️ Personalize seu Dashboard")

            st.markdown("""
            ### 🎨 Recursos de Personalização:

            - **Gráficos Interativos:** Passe o mouse sobre os gráficos para ver detalhes
            - **Zoom:** Clique e arraste para dar zoom em áreas específicas
            - **Download:** Clique no ícone da câmera para salvar gráficos como imagem
            - **Filtros:** Use os controles acima para filtrar dados

            ### 💡 Dicas de Uso:

            1. **Para apresentações:** Use o modo tela cheia (F11)
            2. **Para relatórios:** Faça capturas de tela dos gráficos
            3. **Para análise:** Explore diferentes combinações de colunas
            4. **Para compartilhar:** Envie o link do dashboard

            ### 🚀 Próximos passos:

            - Teste diferentes tipos de gráficos
            - Explore as estatísticas detalhadas
            - Baixe seus dados processados
            - Compartilhe insights com sua equipe!
            """)

    except Exception as e:
        st.error(f"❌ Erro ao processar o arquivo: {str(e)}")
        st.info("💡 Verifique se o arquivo está no formato correto e tente novamente.")

else:
    # Tela inicial quando não há arquivo
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### 📊 Múltiplos Gráficos
        Visualize seus dados em barras, linhas, pizza e muito mais!
        """)

    with col2:
        st.markdown("""
        ### ⚡ Análise Rápida
        Estatísticas automáticas e insights em segundos!
        """)

    with col3:
        st.markdown("""
        ### 🎯 Fácil de Usar
        Sem código, sem complicação. Só fazer upload!
        """)

    st.markdown("---")
    st.info("👈 **Comece agora!** Faça upload do seu arquivo Excel na barra lateral")

