import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
st.set_page_config(layout="wide")
st.image("https://github.com/Thmeirelles/leil-o/blob/main/leil%C3%A3o/Imagens/ricardoauto.png")
@st.cache_data
def load_data():
    return pd.read_csv("leilão/dados/tabela.csv")

df = load_data()
# Análise por Tipo de Veículo
st.title("📊 Análise geral do leilão")

total_veiculos = len(df)
carros = len(df[df["TIPO"] == "Carro"])
motos = len(df[df["TIPO"] == "Moto"])
caminhoes = len(df[df["TIPO"] == "Caminhão"])

percentual_carros = (carros / total_veiculos) * 100
percentual_motos = (motos / total_veiculos) * 100
percentual_caminhoes = (caminhoes / total_veiculos) * 100

total_cores = len(df)
preta = len(df[df["COR"] == "PRETA"])
vermelha = len(df[df["COR"] == "VERMELHA"])
branca = len(df[df["COR"] == "BRANCA"])

percentual_preta = (preta / total_cores) * 100
percentual_vermelha = (vermelha / total_cores) * 100
percentual_branca = (branca / total_cores) * 100

# Métricas da distribuição
st.subheader("📈 Distribuição por Tipo de Veículo")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Geral", total_veiculos)
with col2:
    st.metric("Carros", f"{carros} ({percentual_carros:.1f}%)")
with col3:
    st.metric("Motos", f"{motos} ({percentual_motos:.1f}%)")
with col4:
    st.metric("Caminhões", f"{caminhoes} ({percentual_caminhoes:.1f}%)")
st.markdown("---")

left_spacer, center_col, right_spacer = st.columns([1, 2, 1])
with center_col:
    st.markdown('<div class="centered-section">', unsafe_allow_html=True)
    with st.expander("🎯 Gráfico - Distribuição por Tipo", expanded=True):
        labels = ['Carros', 'Motos', 'Caminhões']
        sizes = [carros, motos, caminhoes]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        
        fig = go.Figure()
        
        for i, (label, size, color) in enumerate(zip(labels, sizes, colors)):
            fig.add_trace(go.Bar(
                x=[label],
                y=[size],
                name=label,
                marker_color=color,
                text=[f"{size}"],
                textposition='auto',
                showlegend=False
            ))
        
        fig.update_layout(
            title='Distribuição por Tipo de Veículo',
            xaxis_title='Tipo de Veículo',
            yaxis_title='Quantidade',
            title_font_size=20,
            title_font_family='Arial',
            title_font_color='#2C3E50',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            xaxis=dict(
                type='category',
                tickangle=0
            )
        )
        
        fig.update_xaxes(title_font=dict(size=14))
        fig.update_yaxes(title_font=dict(size=14))
        
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
#--------------------------------------------------------------------------
st.markdown("---")
st.subheader("📊 Análise de Arrematações")
# Criar abas para cada tipo
tab1, tab2, tab3, tab4 = st.tabs(["Total", "🚗 Carros", "🏍️ Motos", "🚛 Caminhões"])

with tab1:
    total_veiculos = len(df)
    arrematados = df["Valor da Arrematação"].notna().sum()
    nao_arrematados = df["Valor da Arrematação"].isna().sum()

    percentual_arrematados = (arrematados / total_veiculos) * 100
    percentual_nao_arrematados = (nao_arrematados / total_veiculos) * 100

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Veículos", total_veiculos)
    with col2:
        st.metric("Arrematados", f"{arrematados} ({percentual_arrematados:.1f}%)")
    with col3:
        st.metric("Não Arrematados", f"{nao_arrematados} ({percentual_nao_arrematados:.1f}%)")
    st.markdown("---")    
    left_spacer, center_col, right_spacer = st.columns([1, 2, 1])
    with center_col:
        with st.expander("📊 Gráfico - Total",expanded=True):
            fig, ax = plt.subplots()
            labels = ['Arrematados', 'Não Arrematados']
            sizes = [arrematados, nao_arrematados]
            colors = ['#4CAF50', '#F44336']
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            plt.title('Distribuição Geral de Veículos Arrematados', fontsize=14, fontweight='bold', pad=20)
            st.pyplot(fig)
    st.markdown("---")
#--------------------------------------------------------------------------   
with tab2:
    df_carros = df[df["TIPO"] == "Carro"]
    total_carros = len(df_carros)
    arrematados_carros = df_carros["Valor da Arrematação"].notna().sum()
    nao_arrematados_carros = df_carros["Valor da Arrematação"].isna().sum()
    
    percentual_arrematados_carros = (arrematados_carros / total_carros) * 100
    percentual_nao_arrematados_carros = (nao_arrematados_carros / total_carros) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Carros", total_carros, f"{percentual_carros:.1f}%")
    with col2:
        st.metric("Arrematados", f"{arrematados_carros} ({percentual_arrematados_carros:.1f}%)")
    with col3:
        st.metric("Não Arrematados", f"{nao_arrematados_carros} ({percentual_nao_arrematados_carros:.1f}%)")
    st.markdown("---")
    left_spacer, center_col, right_spacer = st.columns([1, 2, 1])
    with center_col:
        with st.expander("📊 Gráfico - Carros",expanded=True):
            fig, ax = plt.subplots()
            labels = ['Arrematados', 'Não Arrematados']
            sizes = [arrematados_carros, nao_arrematados_carros]
            colors = ['#4CAF50', '#F44336']
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            plt.title('Distribuição de Carros Arrematados', fontsize=14, fontweight='bold', pad=20)
            st.pyplot(fig)

with tab3:
    df_motos = df[df["TIPO"] == "Moto"]
    total_motos = len(df_motos)
    arrematados_motos = df_motos["Valor da Arrematação"].notna().sum()
    nao_arrematados_motos = df_motos["Valor da Arrematação"].isna().sum()
    
    percentual_arrematados_motos = (arrematados_motos / total_motos) * 100
    percentual_nao_arrematados_motos = (nao_arrematados_motos / total_motos) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Motos", total_motos, f"{percentual_motos:.1f}%")
    with col2:
        st.metric("Arrematados", f"{arrematados_motos} ({percentual_arrematados_motos:.1f}%)")
    with col3:
        st.metric("Não Arrematados", f"{nao_arrematados_motos} ({percentual_nao_arrematados_motos:.1f}%)")
    left_spacer, center_col, right_spacer = st.columns([1, 2, 1])
    with center_col:
        with st.expander("📊 Gráfico - Motos",expanded=True):
            fig, ax = plt.subplots()
            labels = ['Arrematados', 'Não Arrematados']
            sizes = [arrematados_motos, nao_arrematados_motos]
            colors = ['#4CAF50', '#F44336']
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            plt.title('Distribuição de Motos Arrematadas', fontsize=14, fontweight='bold', pad=20)
            st.pyplot(fig)

with tab4:
    df_caminhoes = df[df["TIPO"] == "Caminhão"]
    total_caminhoes = len(df_caminhoes)
    arrematados_caminhoes = df_caminhoes["Valor da Arrematação"].notna().sum()
    nao_arrematados_caminhoes = df_caminhoes["Valor da Arrematação"].isna().sum()
    
    percentual_arrematados_caminhoes = (arrematados_caminhoes / total_caminhoes) * 100
    percentual_nao_arrematados_caminhoes = (nao_arrematados_caminhoes / total_caminhoes) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Caminhões", total_caminhoes, f"{percentual_caminhoes:.1f}%")
    with col2:
        st.metric("Arrematados", f"{arrematados_caminhoes} ({percentual_arrematados_caminhoes:.1f}%)")
    with col3:
        st.metric("Não Arrematados", f"{nao_arrematados_caminhoes} ({percentual_nao_arrematados_caminhoes:.1f}%)")
    left_spacer, center_col, right_spacer = st.columns([1, 2, 1])
    with center_col:
        with st.expander("📊 Gráfico - Caminhões",expanded=True):
            st.write('Todos foram arrematados')
#--------------------------------------------------------------------------           
# ANALISE CORES
#--------------------------------------------------------------------------
st.subheader("📊 Análise de Cores")
cores_p = ["PRETA", "VERMELHA", "BRANCA", "PRATA", "AZUL", "CINZA"]
df["COR_AJUSTADA"] = df["COR"].apply(lambda cor: cor if cor in cores_p else "OUTRAS")

st.write("**Selecione as cores para visualizar:**")
with st.container():
    cols = st.columns(7)
    opcoes_cores = ["PRETA", "VERMELHA", "BRANCA", "PRATA", "AZUL", "CINZA", "OUTRAS"]
    cores_selecionadas = []  
    for i, cor in enumerate(opcoes_cores):
        with cols[i]:
            if st.checkbox(cor, value=True, key=f"check_{cor}"):
                cores_selecionadas.append(cor)
mapeamento_cores = {
    "PRETA": "black",
    "VERMELHA": "red",
    "BRANCA": "white",
    "PRATA": "silver",
    "AZUL": "blue",
    "CINZA": "gray",
    "OUTRAS": "darkgreen"
}
if not cores_selecionadas:
    st.warning("⚠️ Selecione pelo menos uma cor para visualizar o gráfico!")
else:
    df_filtrado = df[df["COR_AJUSTADA"].isin(cores_selecionadas)]
    contagem_filtrada = df_filtrado["COR_AJUSTADA"].value_counts()
    
    contagem_filtrada = contagem_filtrada.reindex(cores_selecionadas).fillna(0)
    
    cores_barras = [mapeamento_cores[cor] for cor in contagem_filtrada.index]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=contagem_filtrada.index,
        y=contagem_filtrada.values,
        marker_color=cores_barras,
        marker_line=dict(color='black', width=1),
        text=contagem_filtrada.values,
        textposition='auto',
        hovertemplate='<b>Cor:</b> %{x}<br><b>Quantidade:</b> %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="<b>Contagem de Cores dos Veículos</b>",
            x=0.5,
            xanchor='center',
            font=dict(size=20)
        ),
        xaxis=dict(
            title="<b>Cor</b>",
            title_font=dict(size=14)
        ),
        yaxis=dict(
            title="<b>Quantidade</b>",
            title_font=dict(size=14)
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="**Total de Veículos**",
            value=f"{contagem_filtrada.sum():,}"
        )
    
    with col2:
        st.metric(
            label="**Cores Selecionadas**",
            value=len(cores_selecionadas)
        )
    
    with col3:
        if not contagem_filtrada.empty:
            cor_mais_comum = contagem_filtrada.idxmax()
            count_mais_comum = contagem_filtrada.max()
            total_veiculos = contagem_filtrada.sum()
            porcentagem_mais_comum = (count_mais_comum / total_veiculos) * 100
            
            st.metric(
                label="**Cor Mais Frequente**",
                value=cor_mais_comum,
                delta=f"{porcentagem_mais_comum:.1f}% do total"
            )
        else:
            st.metric(
                label="**Cor Mais Frequente**",
                value="N/A"
            )
#--------------------------------------------------------------------------
# Seleção de dados brutos
#--------------------------------------------------------------------------
with st.expander("📋 Visualizar Dados Brutos"):
    st.dataframe(df[["COR", "COR_AJUSTADA"]].head(100))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Distribuição Original de Cores:**")
        st.write(df["COR"].value_counts())
    
    with col2:
        st.write("**Distribuição Ajustada de Cores:**")
        st.write(df["COR_AJUSTADA"].value_counts())
st.markdown("---")
#--------------------------------------------------------------------------










