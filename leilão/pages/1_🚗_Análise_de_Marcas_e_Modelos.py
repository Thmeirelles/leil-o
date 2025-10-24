import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re
st.set_page_config(page_title="Análise de Leilão - Marcas e Modelos", layout="wide")
st.markdown("# 🚗 Análise de Marcas e Modelos - Leilão de Veículos")
st.sidebar.markdown("# 🚗 Análise de Marcas e Modelos - Leilão de Veículos")

st.markdown("---")

@st.cache_data
def load_data():
  
    df = pd.read_csv('leilão/dados/tabela.csv')
    
    currency_columns = ['AVALIAÇÃO', 'Lance Inicial', 'Valor da Arrematação']
    
    for col in currency_columns:
        df[col] = df[col].str.replace('R$', '').str.replace('.', '').str.replace(',', '.').str.strip()
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

try:
    df = load_data()
    
    st.sidebar.header("🔧 Filtros")
    
    tipos = st.sidebar.multiselect(
        "Tipo de Veículo:",
        options=df['TIPO'].unique(),
        default=df['TIPO'].unique()
    )
    
    municipios = st.sidebar.multiselect(
        "Município:",
        options=df['MUNICÍPIO'].unique(),
        default=df['MUNICÍPIO'].unique()
    )
    
    df_filtered = df[
        (df['TIPO'].isin(tipos)) & 
        (df['MUNICÍPIO'].isin(municipios))
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top 10 Marcas com Mais Lotes")
        
        marcas_count = df_filtered['MARCA'].value_counts().head(10)
        
        fig_marcas = px.bar(
            x=marcas_count.values,
            y=marcas_count.index,
            orientation='h',
            color=marcas_count.values,
            color_continuous_scale='blues',
            text=marcas_count.values
        )
        
        fig_marcas.update_layout(
            xaxis_title="Quantidade de Lotes",
            yaxis_title="Marca",
            showlegend=False,
            height=500
        )
        
        st.plotly_chart(fig_marcas, use_container_width=True)
        
        st.markdown("**📊 Estatísticas das Marcas:**")
        total_marcas = df_filtered['MARCA'].nunique()
        st.write(f"- **Total de marcas diferentes:** {total_marcas}")
        st.write(f"- **Marca mais frequente:** {marcas_count.index[0]} ({marcas_count.values[0]} lotes)")
        st.write(f"- **Participação do top 5:** {marcas_count.head(5).sum() / len(df_filtered) * 100:.1f}% do total")
    
    with col2:
        st.subheader("📈 Modelos Mais Frequentes")
        
        modelos_count = df_filtered['NOME_POPULAR'].value_counts().head(10)
        
        fig_modelos = px.bar(
            x=modelos_count.values,
            y=modelos_count.index,
            orientation='h',
            color=modelos_count.values,
            color_continuous_scale='greens',
            text=modelos_count.values
        )
        
        fig_modelos.update_layout(
            xaxis_title="Quantidade de Lotes",
            yaxis_title="Modelo",
            showlegend=False,
            height=500
        )
        
        st.plotly_chart(fig_modelos, use_container_width=True)
        
        st.markdown("**📈 Estatísticas dos Modelos:**")
        total_modelos = df_filtered['NOME_POPULAR'].nunique()
        st.write(f"- **Total de modelos diferentes:** {total_modelos}")
        st.write(f"- **Modelo mais frequente:** {modelos_count.index[0]} ({modelos_count.values[0]} lotes)")
    st.markdown("---")

    st.subheader("Distribuição de Veículos por Marca e Modelo")
    
    treemap_data = df_filtered.groupby(['MARCA', 'NOME_POPULAR']).size().reset_index(name='QUANTIDADE')
    
    fig_treemap = px.treemap(
        treemap_data,
        path=['MARCA', 'NOME_POPULAR'],
        values='QUANTIDADE',
        color='QUANTIDADE',
        color_continuous_scale='viridis',
        title='🌳 Hierarquia Marca → Modelo'
    )
    
    fig_treemap.update_layout(height=600)
    
    st.plotly_chart(fig_treemap, use_container_width=True)
    st.markdown("---")
    
    st.subheader("📋 Detalhamento por Marca e Modelo")
    with st.expander("🔍 Clique para ver a tabela detalhada"):

        resumo_table = df_filtered.groupby(['MARCA', 'NOME_POPULAR', 'TIPO']).agg({
            'LOTE': 'count',
            'AVALIAÇÃO': 'mean',
            'Valor da Arrematação': 'mean'
        }).round(2).reset_index()
        
        resumo_table.columns = ['Marca', 'Modelo', 'Tipo', 'Quantidade', 'Valor Médio Avaliação', 'Valor Médio Arrematação']
        
  
        resumo_table = resumo_table.sort_values('Quantidade', ascending=False)
        
        st.dataframe(resumo_table, use_container_width=True)
    
 
    
    with st.expander("📊 Métricas Gerais",expanded=True):
        col_met1, col_met2, col_met3, col_met4 = st.columns(4)
        
        with col_met1:
            st.metric("Total de Lotes", len(df_filtered))
        
        with col_met2:
            st.metric("Marcas Únicas", df_filtered['MARCA'].nunique())
        
        with col_met3:
            st.metric("Modelos Únicos", df_filtered['NOME_POPULAR'].nunique())
        
        with col_met4:
            taxa_arrematacao = (df_filtered['Valor da Arrematação'].notna().sum() / len(df_filtered)) * 100
            st.metric("Taxa de Arrematação", f"{taxa_arrematacao:.1f}%")
        

    st.subheader("📥 Download dos Dados Processados")
    
    csv = resumo_table.to_csv(index=False)
    st.download_button(
        label="Baixar tabela resumo (CSV)",
        data=csv,
        file_name="resumo_marcas_modelos.csv",
        mime="text/csv"
    )

except FileNotFoundError:
    st.error("❌ Arquivo 'tabela.csv' não encontrado. Certifique-se de que o arquivo está no diretório correto.")
    
except Exception as e:
    st.error(f"❌ Ocorreu um erro ao processar os dados: {str(e)}")

# Informações sobre o aplicativo
# st.sidebar.markdown("---")
# st.sidebar.header("ℹ️ Sobre o App")
# st.sidebar.info(

# )
