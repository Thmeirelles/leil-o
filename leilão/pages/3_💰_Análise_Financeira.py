import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy import stats


st.set_page_config(page_title="Análise Financeira - Leilão de Veículos", layout="wide")

st.title("💰 Análise Financeira - Leilão de Veículos")
st.markdown("---")

@st.cache_data
def load_data():
    df = pd.read_csv('leilão/dados/tabela.csv')
    currency_columns = ['AVALIAÇÃO', 'Lance Inicial', 'Valor da Arrematação']
    
    for col in currency_columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.replace('R$', '').str.replace('.', '').str.replace(',', '.').str.strip()
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['Diferença Percentual'] = ((df['Valor da Arrematação'] - df['AVALIAÇÃO']) / df['AVALIAÇÃO']) * 100

    df['Status Arrematação'] = df['Valor da Arrematação'].apply(lambda x: 'Arrematado' if pd.notna(x) else 'Não Arrematado')
    
    return df

try:
    df = load_data()
    
    st.sidebar.header("🔧 Filtros Financeiros")
    
    tipos = st.sidebar.multiselect(
        "Tipo de Veículo:",
        options=df['TIPO'].unique(),
        default=df['TIPO'].unique()
    )
    
    marcas = st.sidebar.multiselect(
        "Marca:",
        options=df['MARCA'].unique(),
        default=df['MARCA'].unique()
    )
    
    status_arrematacao = st.sidebar.multiselect(
        "Status de Arrematação:",
        options=df['Status Arrematação'].unique(),
        default=df['Status Arrematação'].unique()
    )
    
    min_avaliacao = float(df['AVALIAÇÃO'].min())
    max_avaliacao = float(df['AVALIAÇÃO'].max())
    
    faixa_avaliacao = st.sidebar.slider(
        "Faixa de Valor de Avaliação (R$):",
        min_value=min_avaliacao,
        max_value=max_avaliacao,
        value=(min_avaliacao, max_avaliacao)
    )
    
    df_filtered = df[
        (df['TIPO'].isin(tipos)) & 
        (df['MARCA'].isin(marcas)) &
        (df['Status Arrematação'].isin(status_arrematacao)) &
        (df['AVALIAÇÃO'] >= faixa_avaliacao[0]) &
        (df['AVALIAÇÃO'] <= faixa_avaliacao[1])
    ]
    
    st.subheader("📊 Métricas Financeiras Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_avaliacao = df_filtered['AVALIAÇÃO'].sum()
        st.metric("Valor Total em Avaliação", f"R$ {total_avaliacao:,.0f}")
    
    with col2:
        total_arrematado = df_filtered['Valor da Arrematação'].sum()
        st.metric("Valor Total Arrematado", f"R$ {total_arrematado:,.0f}")
    
    with col3:
        taxa_arrematacao = (df_filtered['Valor da Arrematação'].notna().sum() / len(df_filtered)) * 100
        st.metric("Taxa de Arrematação", f"{taxa_arrematacao:.1f}%")
    
    with col4:
        df_arrematados = df_filtered[df_filtered['Status Arrematação'] == 'Arrematado']
        if len(df_arrematados) > 0:
            desconto_medio = ((df_arrematados['AVALIAÇÃO'] - df_arrematados['Valor da Arrematação']).mean() / df_arrematados['AVALIAÇÃO'].mean()) * 100
            st.metric("Desconto Médio", f"{desconto_medio:.1f}%")
        else:
            st.metric("Desconto Médio", "N/A")
    
    st.subheader("📈 Gráfico de Dispersão: Avaliação vs Arrematação")
    
    df_dispersao = df_filtered[df_filtered['Status Arrematação'] == 'Arrematado']
    
    if not df_dispersao.empty:
       
        correlacao = df_dispersao['AVALIAÇÃO'].corr(df_dispersao['Valor da Arrematação'])
        
        x = df_dispersao['AVALIAÇÃO']
        y = df_dispersao['Valor da Arrematação']
        
        mask = ~np.isnan(x) & ~np.isnan(y)
        x_clean = x[mask]
        y_clean = y[mask]
        
        if len(x_clean) > 1:
            slope, intercept, r_value, p_value, std_err = stats.linregress(x_clean, y_clean)
            line = slope * x_clean + intercept
            
            equation = f"y = {slope:.4f}x + {intercept:.2f}"
            r_squared = r_value**2
            
            fig_dispersao = px.scatter(
                df_dispersao,
                x='AVALIAÇÃO',
                y='Valor da Arrematação',
                color='TIPO',
                size='AVALIAÇÃO',
                hover_data=['MARCA', 'NOME_POPULAR', 'MUNICÍPIO'],
                title=f'Relação entre Valor de Avaliação e Valor de Arrematação<br><sup>Correlação: {correlacao:.3f} | R²: {r_squared:.3f} | Equação: {equation}</sup>',
                labels={
                    'AVALIAÇÃO': 'Valor de Avaliação (R$)',
                    'Valor da Arrematação': 'Valor de Arrematação (R$)',
                    'TIPO': 'Tipo de Veículo'
                }
            )
            
            fig_dispersao.add_trace(
                go.Scatter(
                    x=x_clean,
                    y=line,
                    mode='lines',
                    line=dict(color='red', width=3, dash='dash'),
                    name=f'Linha de Tendência (R² = {r_squared:.3f})'
                )
            )
            
            max_val = max(df_dispersao['AVALIAÇÃO'].max(), df_dispersao['Valor da Arrematação'].max())
            fig_dispersao.add_trace(
                go.Scatter(
                    x=[0, max_val],
                    y=[0, max_val],
                    mode='lines',
                    line=dict(dash='dot', color='green', width=2),
                    name='Linha de Igualdade (Avaliação = Arrematação)'
                )
            )
            
        else:
            # Caso não haja dados suficientes para regressão
            fig_dispersao = px.scatter(
                df_dispersao,
                x='AVALIAÇÃO',
                y='Valor da Arrematação',
                color='TIPO',
                size='AVALIAÇÃO',
                hover_data=['MARCA', 'NOME_POPULAR', 'MUNICÍPIO'],
                title=f'Relação entre Valor de Avaliação e Valor de Arrematação<br><sup>Correlação: {correlacao:.3f}</sup>',
                labels={
                    'AVALIAÇÃO': 'Valor de Avaliação (R$)',
                    'Valor da Arrematação': 'Valor de Arrematação (R$)',
                    'TIPO': 'Tipo de Veículo'
                }
            )
        
        fig_dispersao.update_layout(height=600)
        st.plotly_chart(fig_dispersao, use_container_width=True)
        
        st.markdown("**📋 Análise da Correlação:**")
        
        if abs(correlacao) >= 0.9:
            forca = "muito forte"
        elif abs(correlacao) >= 0.7:
            forca = "forte"
        elif abs(correlacao) >= 0.5:
            forca = "moderada"
        elif abs(correlacao) >= 0.3:
            forca = "fraca"
        else:
            forca = "muito fraca"
        
        direcao = "positiva" if correlacao > 0 else "negativa"
        
        st.write(f"- **Coeficiente de correlação (r):** {correlacao:.3f}")
        if len(x_clean) > 1:
            st.write(f"- **Coeficiente de determinação (R²):** {r_squared:.3f}")
        st.write(f"- **Força da relação:** {forca}")
        st.write(f"- **Direção da relação:** {direcao}")
        
        st.markdown("**💡 Interpretação Prática:**")
        if correlacao > 0.7:
            st.write("✅ Há uma forte relação positiva: veículos com maior valor de avaliação tendem a ser arrematados por valores mais altos.")
        elif correlacao > 0.3:
            st.write("⚠️ Há uma relação moderada: o valor de avaliação influencia, mas não determina completamente o valor de arrematação.")
        else:
            st.write("🔍 A relação é fraca: outros fatores além do valor de avaliação podem estar influenciando mais os valores de arrematação.")

        st.markdown("**📊 Estatísticas Adicionais:**")
        acima_linha = len(df_dispersao[df_dispersao['Valor da Arrematação'] > df_dispersao['AVALIAÇÃO']])
        percentual_acima = (acima_linha / len(df_dispersao)) * 100
        
        st.write(f"- **Lotes arrematados acima do valor de avaliação:** {acima_linha} ({percentual_acima:.1f}%)")
        st.write(f"- **Lotes arrematados abaixo do valor de avaliação:** {len(df_dispersao) - acima_linha} ({(100 - percentual_acima):.1f}%)")
        
        if len(df_dispersao) > 0:
            desconto_medio_real = ((df_dispersao['AVALIAÇÃO'] - df_dispersao['Valor da Arrematação']).mean() / df_dispersao['AVALIAÇÃO'].mean()) * 100
            st.write(f"- **Desconto médio nos lotes arrematados:** {desconto_medio_real:.1f}%")
        
    else:
        st.warning("⚠️ Não há dados de lotes arrematados para exibir o gráfico de dispersão.")
    

    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📦 Distribuição de Valores por Tipo de Veículo")
        

        df_boxplot = df_filtered[df_filtered['Status Arrematação'] == 'Arrematado']
        
        if not df_boxplot.empty:
            fig_boxplot = px.box(
                df_boxplot,
                x='TIPO',
                y='Valor da Arrematação',
                color='TIPO',
                points="all",
                hover_data=['MARCA', 'NOME_POPULAR'],
                title='Distribuição dos Valores de Arrematação por Tipo de Veículo',
                labels={
                    'TIPO': 'Tipo de Veículo',
                    'Valor da Arrematação': 'Valor de Arrematação (R$)'
                }
            )
            
            fig_boxplot.update_layout(height=500)
            st.plotly_chart(fig_boxplot, use_container_width=True)
            

            st.markdown("**📊 Estatísticas por Tipo:**")
            stats_by_type = df_boxplot.groupby('TIPO')['Valor da Arrematação'].agg(['mean', 'median', 'min', 'max', 'count']).round(2)
            for tipo in stats_by_type.index:
                stats = stats_by_type.loc[tipo]
                st.write(f"**{tipo}:** {stats['count']} lotes, Média=R${stats['mean']:,.0f}, Mediana=R${stats['median']:,.0f}")
        else:
            st.warning("⚠️ Não há dados de lotes arrematados para exibir o boxplot.")
    
    with col_right:

        st.subheader("🏙️ Valores Médios por Município")
        

        municipio_stats = df_filtered.groupby('MUNICÍPIO').agg({
            'AVALIAÇÃO': 'mean',
            'Valor da Arrematação': 'mean',
            'LOTE': 'count'
        }).round(2).reset_index()
        
        municipio_stats.columns = ['Município', 'Avaliação Média', 'Arrematação Média', 'Quantidade de Lotes']
        
        municipio_stats = municipio_stats.sort_values('Quantidade de Lotes', ascending=False)
        
        fig_linhas = go.Figure()
        
        fig_linhas.add_trace(go.Scatter(
            x=municipio_stats['Município'],
            y=municipio_stats['Avaliação Média'],
            mode='lines+markers',
            name='Avaliação Média',
            line=dict(color='blue', width=3),
            marker=dict(size=8)
        ))
        
        municipios_com_arrematacao = municipio_stats[municipio_stats['Arrematação Média'].notna()]
        if not municipios_com_arrematacao.empty:
            fig_linhas.add_trace(go.Scatter(
                x=municipios_com_arrematacao['Município'],
                y=municipios_com_arrematacao['Arrematação Média'],
                mode='lines+markers',
                name='Arrematação Média',
                line=dict(color='green', width=3),
                marker=dict(size=8)
            ))
        
        fig_linhas.update_layout(
            title='Comparação entre Valor Médio de Avaliação e Arrematação por Município',
            xaxis_title='Município',
            yaxis_title='Valor (R$)',
            height=500,
            showlegend=True
        )
        
        fig_linhas.update_xaxes(tickangle=45)
        
        st.plotly_chart(fig_linhas, use_container_width=True)
        
        st.markdown("**📋 Resumo por Município:**")
        display_stats = municipio_stats.copy()
        display_stats['Avaliação Média'] = display_stats['Avaliação Média'].apply(lambda x: f"R$ {x:,.0f}" if pd.notna(x) else "N/A")
        display_stats['Arrematação Média'] = display_stats['Arrematação Média'].apply(lambda x: f"R$ {x:,.0f}" if pd.notna(x) else "N/A")
        st.dataframe(display_stats, use_container_width=True)
    
    st.subheader("📈 Análise de Desempenho Financeiro")
    
    if not df_dispersao.empty:
        col_perf1, col_perf2, col_perf3 = st.columns(3)
        
        with col_perf1:
            maior_desconto_idx = df_dispersao['Diferença Percentual'].idxmin()
            maior_desconto = df_dispersao.loc[maior_desconto_idx]
            st.metric("Maior Desconto", 
                     f"{(maior_desconto['Diferença Percentual']):.1f}%",
                     f"{maior_desconto['NOME_POPULAR']} - {maior_desconto['MUNICÍPIO']}")
        
        with col_perf2:
            menor_desconto_idx = df_dispersao['Diferença Percentual'].idxmax()
            menor_desconto = df_dispersao.loc[menor_desconto_idx]
            st.metric("Menor Desconto", 
                     f"{(menor_desconto['Diferença Percentual']):.1f}%",
                     f"{menor_desconto['NOME_POPULAR']} - {menor_desconto['MUNICÍPIO']}")
        
        with col_perf3:
            maior_valor_idx = df_dispersao['Valor da Arrematação'].idxmax()
            maior_valor = df_dispersao.loc[maior_valor_idx]
            st.metric("Maior Arrematação", 
                     f"R$ {maior_valor['Valor da Arrematação']:,.0f}",
                     f"{maior_valor['NOME_POPULAR']} - {maior_valor['MUNICÍPIO']}")
    
    st.subheader("🏆 Top 10 Maiores Arrematações")
    
    df_arrematados = df_filtered[df_filtered['Status Arrematação'] == 'Arrematado']
    if not df_arrematados.empty:
        top_arrematacoes = df_arrematados.nlargest(10, 'Valor da Arrematação')[
            ['MARCA', 'NOME_POPULAR', 'TIPO', 'MUNICÍPIO', 'AVALIAÇÃO', 'Valor da Arrematação', 'Diferença Percentual']
        ].copy()
        
        top_arrematacoes['Diferença Percentual'] = top_arrematacoes['Diferença Percentual'].round(2)
        top_arrematacoes['AVALIAÇÃO'] = top_arrematacoes['AVALIAÇÃO'].apply(lambda x: f"R$ {x:,.0f}")
        top_arrematacoes['Valor da Arrematação'] = top_arrematacoes['Valor da Arrematação'].apply(lambda x: f"R$ {x:,.0f}")
        top_arrematacoes['Diferença Percentual'] = top_arrematacoes['Diferença Percentual'].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(top_arrematacoes, use_container_width=True)
    else:
        st.info("ℹ️ Não há dados de arrematações para exibir o ranking.")

    st.subheader("📥 Download dos Dados Financeiros")
    
    csv = df_filtered.to_csv(index=False, sep=';', decimal=',')
    st.download_button(
        label="Baixar dados filtrados (CSV)",
        data=csv,
        file_name="dados_financeiros_filtrados.csv",
        mime="text/csv"
    )

except FileNotFoundError:
    st.error("❌ Arquivo 'tabela.csv' não encontrado. Certifique-se de que o arquivo está no diretório correto.")
    
except Exception as e:
    st.error(f"❌ Ocorreu um erro ao processar os dados: {str(e)}")
    st.info("💡 Dica: Verifique se o arquivo CSV está formatado corretamente.")

st.sidebar.markdown("---")
st.sidebar.header("ℹ️ Sobre a Análise Financeira")
st.sidebar.info(
     "Esta análise examina os aspectos financeiros do leilão, "
     "incluindo relações entre avaliação e arrematação, distribuição "
     "de valores por tipo de veículo e comparações entre municípios."
 )
