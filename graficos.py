import streamlit as st
import pandas as pd
import plotly.express as px

ID_PLANILHA = "COLE_AQUI_SEU_ID"
GID = "0"

URL = "1jXghWB8UgKcm6U72-doguM4auaDSQhvN7xt2QOTnc0w"

st.set_page_config(layout="wide")
st.title("📊 Dashboard de Análise")

df = pd.read_csv(URL)

# Ajuste os índices conforme sua planilha
df_defeitos = df.iloc[23:30, 9:12]
df_defeitos.columns = ["Defeito","Total","Percentual"]
df_defeitos = df_defeitos.dropna()

df_carros = df.iloc[23:30, 13:16]
df_carros.columns = ["Carro","Total","Percentual"]
df_carros = df_carros.dropna()

df_garagens = df.iloc[34:37, 13:16]
df_garagens.columns = ["Garagem","Total","Percentual"]
df_garagens = df_garagens.dropna()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Defeitos")
    st.plotly_chart(px.pie(df_defeitos, names="Defeito", values="Total"), use_container_width=True)

with col2:
    st.subheader("Carros")
    st.plotly_chart(px.pie(df_carros, names="Carro", values="Total"), use_container_width=True)

with col3:
    st.subheader("Garagens")
    st.plotly_chart(px.pie(df_garagens, names="Garagem", values="Total"), use_container_width=True)
