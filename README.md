### 📊 Dashboard de Vendas (versão 2024.2)

Dashboard interativo desenvolvido com **Python**, **Pandas**, **Streamlit** e **Plotly**, pensado para quem precisa analisar rapidamente os resultados comerciais e gerar insights acionáveis.

#### Principais novidades (abril 2024)

| 🎯 O que mudou | 📌 Detalhes |
|----------------|------------|
| **Filtros avançados** | Agora é possível combinar filtros por **categoria**, **região**, **faixa de preço** e **período** ao mesmo tempo, usando sliders e menus suspensos. |
| **KPIs dinâmicos** | Além de **vendas** e **lucro**, adicionamos **ticket médio**, **taxa de conversão** e **crescimento YoY**. Cada KPI exibe um mini‑gráfico de tendência (sparkline). |
| **Visualizações interativas** | Gráficos de barra, linha e *heatmap* com **zoom**, **hover tooltips** customizáveis e escolha de **tema (claro/escuro)**. |
| **Exportação automática** | Botão “Gerar relatório” que baixa um **CSV** consolidado e um **PDF** (via `pdfkit`) contendo todos os gráficos selecionados. |
| **Insights por IA** (beta) | Integração leve com **OpenAI GPT‑4o** para gerar descrições automáticas de padrões detectados (ex.: “A região Sudeste apresentou queda de 12 % nas vendas do Q1”). |
| **Persistência de visualizações** | Usuário pode salvar a configuração atual (filtros + layout) em *localStorage* e restaurá‑la ao voltar ao dashboard. |
| **Performance otimizada** | Carregamento de dados em **chunks** (10 k rows) e cache de consultas frequentes usando `@st.cache_data`. |
| **Deploy simplificado** | Script `deploy.sh` que cria um ambiente no **Streamlit Cloud** com uma única linha: `streamlit run app.py`. |

> **Deploy ao vivo** https://dashboardsdadospy.streamlit.app/  
> **Repositório completo**: https://github.com/felipebarboza58/dashboard-vendas-python

---

#### Como usar

1. **Carregue** seu arquivo de vendas (`.csv` ou `.xlsx`).  
2. Selecione os filtros desejados no painel à esquerda.  
3. Observe os KPIs e gráficos atualizarem em tempo real.  
4. Clique em **“Gerar relatório”** para baixar CSV + PDF.  
5. (Opcional) Use o botão **“Gerar insights IA”** para receber sugestões automáticas.

---

#### Tecnologias empregadas

- **Python 3.11**  
- **Pandas** (manipulação de dados)  
- **Streamlit** (frontend web)  
- **Plotly** (visualizações interativas)  
- **OpenAI API** (geração de insights)  
- **pdfkit + wkhtmltopdf** (exportação PDF)  
- **GitHub Actions** (CI simples → lint + teste de sintaxe)


