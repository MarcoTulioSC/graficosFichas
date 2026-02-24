import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# CONFIG GOOGLE SHEETS
# ==============================

ID_PLANILHA = "1jXghWB8UgKcm6U72-doguM4auaDSQhvN7xt2QOTnc0w"
GID = "0"

URL = f"https://docs.google.com/spreadsheets/d/{ID_PLANILHA}/export?format=csv&gid={GID}"

st.set_page_config(layout="wide")
st.title("📊 Dashboard de Manutenção")

# ==============================
# CARREGAR DADOS
# ==============================

@st.cache_data
def carregar_dados():
    df = pd.read_csv(URL)
    
    # Ajuste os nomes das colunas exatamente como estão no seu Sheets
    df["Data"] = pd.to_datetime(df["Data"], dayfirst=True, errors="coerce")
    
    df = df.dropna(subset=["Data"])
    return df

df = carregar_dados()

# ==============================
# FILTROS DINÂMICOS
# ==============================

colFiltro1, colFiltro2 = st.columns(2)

# Anos disponíveis no banco
anos_disponiveis = sorted(df["Data"].dt.year.unique())

with colFiltro1:
    ano = st.selectbox("Ano", anos_disponiveis)

# Meses disponíveis dentro do ano escolhido
meses_disponiveis = sorted(
    df[df["Data"].dt.year == ano]["Data"].dt.month.unique()
)

with colFiltro2:
    mes = st.selectbox("Mês", meses_disponiveis)

# ==============================
# FILTRAR DADOS
# ==============================

df_filtrado = df[
    (df["Data"].dt.year == ano) &
    (df["Data"].dt.month == mes)
]

# ==============================
# AGRUPAMENTOS
# ==============================

defeitos = df_filtrado.groupby("Defeito").size().reset_index(name="Total")
carros = df_filtrado.groupby("Carro").size().reset_index(name="Total")
garagens = df_filtrado.groupby("Garagem").size().reset_index(name="Total")

# ==============================
# KPIs
# ==============================

total_registros = len(df_filtrado)

st.markdown("---")
st.metric("Total de Ocorrências no Período", total_registros)
st.markdown("---")

# ==============================
# GRÁFICOS
# ==============================

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("⚠️ Defeitos")
    if not defeitos.empty:
        fig1 = px.pie(defeitos, names="Defeito", values="Total")
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Sem dados nesse período")

with col2:
    st.subheader("🚗 Carros")
    if not carros.empty:
        fig2 = px.pie(carros, names="Carro", values="Total")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Sem dados nesse período")

with col3:
    st.subheader("🏢 Garagens")
    if not garagens.empty:
        fig3 = px.pie(garagens, names="Garagem", values="Total")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Sem dados nesse período")
