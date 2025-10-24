import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from math import radians, sin, cos, sqrt, atan2


st.set_page_config(page_title="Análise Geográfica - Leilão de Veículos", layout="wide")


st.title("🌍 Análise Geográfica Estratégica - Mato Grosso")
st.markdown("""
**Ricardo Auto Leilões** - *Análise de Distribuição Territorial no Estado do Mato Grosso*
""")
st.markdown("---")

# Coordenadas dos municípios de Mato Grosso
COORDENADAS_MUNICIPIOS = {
    'Diamantino': {'lat': -14.4086, 'lon': -56.4464},
    'Cuiabá': {'lat': -15.6010, 'lon': -56.0974},
    'Rondonópolis': {'lat': -16.4673, 'lon': -54.6370},
    'Alto Garçal': {'lat': -11.8422, 'lon': -55.4808},
    'Cáceres': {'lat': -15.5366, 'lon': -57.4587},
    'Poconé': {'lat': -16.2560, 'lon': -56.6227},
    'Pontes e Licentia': {'lat': -15.2267, 'lon': -52.6711},
    'Comodoro': {'lat': -13.6631, 'lon': -59.7876},
    'Primavera do Leste': {'lat': -15.5238, 'lon': -54.3430},
    'Campo Verde': {'lat': -15.5450, 'lon': -55.1620},
    'Sorriso': {'lat': -12.5425, 'lon': -55.7211},
    'Nova Santa Helena': {'lat': -10.8167, 'lon': -55.8167},
    'Barra do Garças': {'lat': -15.8900, 'lon': -52.2567},
    'Água Boa': {'lat': -14.0500, 'lon': -52.1600}
}

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('leilão/dados/tabela.csv', encoding='utf-8')
        
        municipios_mt = list(COORDENADAS_MUNICIPIOS.keys())
        df = df[df['MUNICÍPIO'].isin(municipios_mt)]
        
        currency_columns = ['AVALIAÇÃO', 'Lance Inicial', 'Valor da Arrematação']
        
        for col in currency_columns:
            if df[col].dtype == 'object':
                df[col] = df[col].str.replace('R$', '').str.replace('.', '').str.replace(',', '.').str.strip()
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df['lat'] = df['MUNICÍPIO'].map(lambda x: COORDENADAS_MUNICIPIOS.get(x, {}).get('lat', np.nan))
        df['lon'] = df['MUNICÍPIO'].map(lambda x: COORDENADAS_MUNICIPIOS.get(x, {}).get('lon', np.nan))
        
        df['Categoria Valor'] = pd.cut(df['AVALIAÇÃO'], 
                                     bins=[0, 15000, 50000, 100000, float('inf')],
                                     labels=['Econômico', 'Médio', 'Alto', 'Premium'])
        

        df['Eficiência Arrematação'] = (df['Valor da Arrematação'] / df['AVALIAÇÃO']).fillna(0)
        
        return df
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("⚠️ Nenhum dado foi carregado. Verifique o arquivo CSV.")
    st.stop()

st.sidebar.header("🎯 Filtros Estratégicos")

municipios = st.sidebar.multiselect(
    "Município:",
    options=sorted(df['MUNICÍPIO'].unique()),
    default=sorted(df['MUNICÍPIO'].unique())
)

categorias = st.sidebar.multiselect(
    "Categoria de Valor:",
    options=df['Categoria Valor'].unique(),
    default=df['Categoria Valor'].unique()
)

tipos = st.sidebar.multiselect(
    "Tipo de Veículo:",
    options=df['TIPO'].unique(),
    default=df['TIPO'].unique()
)


df_filtered = df[
    (df['MUNICÍPIO'].isin(municipios)) & 
    (df['Categoria Valor'].isin(categorias)) &
    (df['TIPO'].isin(tipos))
]

if df_filtered.empty:
    st.warning("🚫 Nenhum dado encontrado com os filtros selecionados.")
    st.stop()

st.subheader("📊 Indicadores Estratégicos - Mato Grosso")

col1, col2, col3, col4 = st.columns(4)

with col1:
    valor_total = df_filtered['AVALIAÇÃO'].sum()
    st.metric("Valor Total em Leilão", f"R$ {valor_total:,.0f}")

with col2:
    taxa_arrematacao = (df_filtered['Valor da Arrematação'].notna().sum() / len(df_filtered)) * 100
    st.metric("Taxa de Arrematação", f"{taxa_arrematacao:.1f}%")

with col3:
    eficiencia_media = df_filtered[df_filtered['Valor da Arrematação'].notna()]['Eficiência Arrematação'].mean() * 100
    if not np.isnan(eficiencia_media):
        st.metric(
            "Eficiência Média", 
            f"{eficiencia_media:.1f}%",
            help="Performance média do mercado local - percentual do valor de avaliação que está sendo realizado nas arrematações"
        )
    else:
        st.metric("Eficiência Média", "N/A")

with col4:
    municipios_ativos = df_filtered['MUNICÍPIO'].nunique()
    st.metric("Municípios Ativos", municipios_ativos)

st.markdown("---")
st.subheader("🗺️ Mapa de Oportunidades - Mato Grosso")

municipio_stats = df_filtered.groupby('MUNICÍPIO').agg({
    'AVALIAÇÃO': ['count', 'sum', 'mean'],
    'Valor da Arrematação': ['sum', lambda x: x.notna().sum()],
    'Eficiência Arrematação': 'mean',
    'lat': 'first',
    'lon': 'first'
}).round(2)

municipio_stats.columns = ['Qtd Lotes', 'Valor Total', 'Valor Médio', 
                           'Valor Arrematado', 'Lotes Arrematados', 
                           'Eficiência Média', 'lat', 'lon']

municipio_stats = municipio_stats.reset_index()

fig_oportunidades = px.scatter_mapbox(
    municipio_stats,
    lat="lat",
    lon="lon",
    size="Valor Total",
    color="Eficiência Média",
    size_max=40,
    zoom=5.5,
    height=500,
    hover_name="MUNICÍPIO",
    hover_data={
        'Qtd Lotes': True,
        'Valor Total': ':.0f',
        'Eficiência Média': ':.1%',
        'Valor Médio': ':.0f',
        'lat': False,
        'lon': False
    },
    title="Mapa de Oportunidades por Município - Mato Grosso (Cor: Eficiência Média = Performance do mercado local)",
    color_continuous_scale=px.colors.sequential.Viridis
)

fig_oportunidades.update_layout(
    mapbox_style="open-street-map",
    margin={"r":0,"t":40,"l":0,"b":0}
)

st.plotly_chart(fig_oportunidades, use_container_width=True)

st.markdown("---")
st.subheader("📈 Análise Comparativa por Município")

col_analise1, col_analise2 = st.columns(2)

with col_analise1:
    fig_valor_municipio = px.bar(
        municipio_stats.nlargest(10, 'Valor Total'),
        x='MUNICÍPIO',
        y='Valor Total',
        title='Top 10 Municípios por Valor Total',
        color='Valor Total',
        color_continuous_scale='viridis'
    )
    fig_valor_municipio.update_layout(height=400, xaxis_tickangle=45)
    st.plotly_chart(fig_valor_municipio, use_container_width=True)

with col_analise2:
    fig_eficiencia = px.bar(
        municipio_stats.nlargest(10, 'Eficiência Média'),
        x='MUNICÍPIO',
        y='Eficiência Média',
        title='Eficiência de Arrematação por Município (Performance do mercado local)',
        color='Eficiência Média',
        color_continuous_scale='blues'
    )
    fig_eficiencia.update_layout(height=400, xaxis_tickangle=45)
    fig_eficiencia.update_yaxes(tickformat=".1%")
    st.plotly_chart(fig_eficiencia, use_container_width=True)

st.markdown("---")
st.subheader("🔥 Heatmap de Concentração de Valor")

df_heatmap = df_filtered[df_filtered['lat'].notna()].copy()

if not df_heatmap.empty:
    fig_heatmap = px.density_mapbox(
        df_heatmap,
        lat='lat',
        lon='lon',
        z='AVALIAÇÃO',
        radius=25,
        zoom=5.5,
        height=500,
        title="Concentração de Valor por Localização - Mato Grosso",
        hover_data=['MARCA', 'NOME_POPULAR', 'AVALIAÇÃO', 'MUNICÍPIO'],
        color_continuous_scale=px.colors.sequential.Hot
    )
    
    fig_heatmap.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":40,"l":0,"b":0}
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)

st.markdown("---")
st.subheader("🏙️ Segmentação por Município")

municipio_opp = df_filtered.groupby('MUNICÍPIO').agg({
    'AVALIAÇÃO': ['count', 'sum'],
    'Valor da Arrematação': lambda x: x.notna().sum(),
    'Eficiência Arrematação': 'mean'
}).round(2)

municipio_opp.columns = ['Qtd Lotes', 'Valor Total', 'Lotes Arrematados', 'Eficiência Média']
municipio_opp = municipio_opp.reset_index()

municipio_opp['Taxa Arrematação'] = (municipio_opp['Lotes Arrematados'] / municipio_opp['Qtd Lotes'] * 100).round(1)

def classificar_oportunidade(row):
    if row['Taxa Arrematação'] < 50 and row['Valor Total'] > 100000:
        return 'Alta Oportunidade'
    elif row['Taxa Arrematação'] < 70 and row['Valor Total'] > 50000:
        return 'Média Oportunidade'
    else:
        return 'Baixa Oportunidade'

municipio_opp['Classificação'] = municipio_opp.apply(classificar_oportunidade, axis=1)

fig_oportunidades_municipio = px.scatter(
    municipio_opp,
    x='Taxa Arrematação',
    y='Valor Total',
    size='Qtd Lotes',
    color='Classificação',
    hover_name='MUNICÍPIO',
    title='Análise de Oportunidades por Município - Mato Grosso (Eixo Y: Valor Total, Eixo X: Performance do mercado)',
    labels={
        'Taxa Arrematação': 'Taxa de Arrematação (%)',
        'Valor Total': 'Valor Total (R$)'
    },
    size_max=30
)

st.plotly_chart(fig_oportunidades_municipio, use_container_width=True)

st.markdown("---")
st.subheader("💡 Recomendações Estratégicas")

recomendacoes = []

alta_oportunidade = municipio_opp[municipio_opp['Classificação'] == 'Alta Oportunidade']
if not alta_oportunidade.empty:
    for _, municipio in alta_oportunidade.nlargest(3, 'Valor Total').iterrows():
        recomendacoes.append(f"**{municipio['MUNICÍPIO']}**: Potencial não explorado - {municipio['Qtd Lotes']} lotes disponíveis com apenas {municipio['Taxa Arrematação']}% de arrematação.")

top_valor_disponivel = municipio_opp.nlargest(3, 'Valor Total')
for _, municipio in top_valor_disponivel.iterrows():
    if municipio['MUNICÍPIO'] not in [r.split('**')[1].split('**')[0] for r in recomendacoes if '**' in r]:
        recomendacoes.append(f"**{municipio['MUNICÍPIO']}**: Maior valor total em leilão - R$ {municipio['Valor Total']:,.0f}")

if recomendacoes:
    for rec in recomendacoes:
        st.info(rec)
else:
    st.success("✅ Todas as regiões estão com boa performance!")


st.markdown("---")
st.subheader("📊 Dashboard de Performance Municipal")

metrica = st.selectbox(
    "Selecione a Métrica para Análise:",
    ['Valor Total', 'Qtd Lotes', 'Eficiência Média', 'Taxa Arrematação']
)

if metrica in ['Valor Total', 'Qtd Lotes']:
    fig_performance = px.bar(
        municipio_stats.nlargest(15, metrica),
        x='MUNICÍPIO',
        y=metrica,
        title=f'{metrica} por Município',
        color=metrica,
        color_continuous_scale='teal'
    )
else:
    fig_performance = px.bar(
        municipio_opp.nlargest(15, metrica),
        x='MUNICÍPIO',
        y=metrica,
        title=f'{metrica} por Município' + (' (Performance do mercado local)' if metrica == 'Eficiência Média' else ''),
        color=metrica,
        color_continuous_scale='purples'
    )
    if metrica in ['Eficiência Média']:
        fig_performance.update_yaxes(tickformat=".1%")

fig_performance.update_layout(height=400, xaxis_tickangle=45)
st.plotly_chart(fig_performance, use_container_width=True)

st.markdown("---")
with st.expander("📋 Tabela Detalhada por Município"):
    st.subheader("📋 Tabela Detalhada por Município")
    tabela_display = municipio_opp.copy()
    tabela_display['Valor Total'] = tabela_display['Valor Total'].apply(lambda x: f"R$ {x:,.0f}")
    tabela_display['Eficiência Média'] = tabela_display['Eficiência Média'].apply(lambda x: f"{x:.1%}")
    tabela_display['Taxa Arrematação'] = tabela_display['Taxa Arrematação'].apply(lambda x: f"{x}%")
    st.dataframe(tabela_display, use_container_width=True)


st.sidebar.markdown("---")
st.sidebar.header("📖 Sobre a Eficiência")

st.sidebar.info("""
**Eficiência Média = Performance do mercado local**

- **🟢 Alta (80-100%)**: Mercado aquecido, bom interesse
- **🟡 Média (60-80%)**: Mercado estável, performance normal  
- **🔴 Baixa (0-60%)**: Mercado fraco, necessita ações

""")
