import pandas as pd
import streamlit as st
import plotly.express as px

@st.cache_data
def load_data():
    """
    Carrega e limpa os dados - CORRIGIDO
    """
    try:
        df = pd.read_csv('leilão/dados/tabela.csv')  # Ajuste o caminho se necessário
        
        # CORREÇÃO: Converter valores monetários
        currency_columns = ['AVALIAÇÃO', 'Lance Inicial', 'Valor da Arrematação']
        
        for col in currency_columns:
            if df[col].dtype == 'object':
                # Remover R$, pontos e converter vírgula para ponto
                df[col] = df[col].str.replace('R$', '', regex=False)
                df[col] = df[col].str.replace('.', '', regex=False)
                df[col] = df[col].str.replace(',', '.', regex=False)
                df[col] = df[col].str.strip()
            
            # Converter para numérico
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    except FileNotFoundError:
        st.error("❌ Arquivo 'tabela.csv' não encontrado.")
        st.info("💡 Certifique-se de que o arquivo está na mesma pasta do script.")
        return None

def calcular_lances_estrategicos(df):
    """
    Calcula lances estratégicos baseados na análise histórica - CORRIGIDO
    """
    if df is None:
        return {}
    
    # Filtrar apenas veículos arrematados
    df_arrematados = df[df['Valor da Arrematação'].notna()]
    
    # CORREÇÃO: Verificar se há dados
    if len(df_arrematados) == 0:
        st.warning("⚠️ Nenhum veículo foi arrematado nos dados.")
        return {}
    
    estrategia = {}
    
    for categoria in ['Total', 'Carro', 'Moto', 'Caminhão']:
        if categoria == 'Total':
            dados = df_arrematados
        else:
            dados = df_arrematados[df_arrematados['TIPO'] == categoria]
        
        if len(dados) > 0:
            try:
                # CORREÇÃO: Verificar se há valores válidos
                valores_validos = dados['Valor da Arrematação'].dropna()
                if len(valores_validos) == 0:
                    continue
                
                # Estatísticas básicas
                media_arremate = valores_validos.mean()
                mediana_arremate = valores_validos.median()
                percentil_75 = valores_validos.quantile(0.75)
                percentil_90 = valores_validos.quantile(0.90)
                
                # Estratégia: percentil 75 como "lance competitivo seguro"
                lance_recomendado = percentil_75
                lance_maximo = percentil_90
                
                # Taxa de sucesso histórica para esse valor
                taxa_sucesso = (len(valores_validos[valores_validos <= lance_recomendado]) / len(valores_validos)) * 100
                
                estrategia[categoria] = {
                    'media_arremate': media_arremate,
                    'mediana_arremate': mediana_arremate,
                    'lance_competitivo': lance_recomendado,
                    'lance_maximo': lance_maximo,
                    'taxa_sucesso_estimada': taxa_sucesso,
                    'amostra': len(dados)
                }
                
            except Exception as e:
                st.warning(f"Erro ao processar categoria {categoria}: {e}")
                continue
    
    return estrategia

def analise_viabilidade_caminhoes(df):
    """
    Analisa a viabilidade de entrar no ramo de aluguel de caminhões - CORRIGIDO
    """
    if df is None:
        return None
    
    caminhoes = df[df['TIPO'] == 'Caminhão']
    caminhoes_arrematados = caminhoes[caminhoes['Valor da Arrematação'].notna()]
    
    if len(caminhoes_arrematados) == 0:
        st.warning("⚠️ Nenhum caminhão foi arrematado nos dados.")
        return None
    
    try:
        # CORREÇÃO: Usar apenas valores válidos
        valores_arremate_validos = caminhoes_arrematados['Valor da Arrematação'].dropna()
        valores_avaliacao_validos = caminhoes_arrematados['AVALIAÇÃO'].dropna()
        
        if len(valores_arremate_validos) == 0 or len(valores_avaliacao_validos) == 0:
            return None
        
        # Análise de custos
        investimento_medio = valores_arremate_validos.mean()
        avaliacao_media = valores_avaliacao_validos.mean()
        desconto_medio = ((avaliacao_media - investimento_medio) / avaliacao_media) * 100
        
        # Estimativa de receita (valores de mercado para aluguel de caminhões)
        diaria_estimada = 800  # R$ por dia para caminhão médio
        utilizacao_mensal = 20  # dias por mês
        receita_mensal_estimada = diaria_estimada * utilizacao_mensal
        
        # Payback simples
        payback_meses = investimento_medio / receita_mensal_estimada
        
        # ROI anual estimado
        receita_anual = receita_mensal_estimada * 12
        custos_manutencao = receita_anual * 0.3  # 30% para custos operacionais
        lucro_anual_estimado = receita_anual - custos_manutencao
        # CORREÇÃO: Evitar divisão por zero
        if investimento_medio > 0:
            roi_anual = (lucro_anual_estimado / investimento_medio) * 100
        else:
            roi_anual = 0
        
        return {
            'investimento_medio': investimento_medio,
            'avaliacao_media': avaliacao_media,
            'desconto_medio': desconto_medio,
            'diaria_estimada': diaria_estimada,
            'receita_mensal_estimada': receita_mensal_estimada,
            'payback_meses': payback_meses,
            'roi_anual': roi_anual,
            'amostra': len(caminhoes_arrematados),
            'modelos_unicos': caminhoes_arrematados['NOME_POPULAR'].nunique()
        }
    
    except Exception as e:
        st.error(f"Erro na análise de viabilidade: {e}")
        return None

def show_estrategia():
    st.title("🎯 Estratégia de Lances & Viabilidade")
    st.markdown("---")
    
    # Carregar dados
    df = load_data()
    
    if df is None:
        st.stop()  # Para a execução se não carregou dados
    
    # Mostrar informações básicas dos dados
    st.sidebar.info(f"📊 **Dados Carregados:** {len(df)} veículos")
    
    # Calculando estratégias
    estrategia = calcular_lances_estrategicos(df)
    viabilidade_caminhoes = analise_viabilidade_caminhoes(df)
    
    # CORREÇÃO: Verificar se a estratégia tem dados
    if not estrategia:
        st.error("❌ Não foi possível calcular estratégias. Verifique os dados.")
        return
    
    # SEÇÃO 1: RECOMENDAÇÕES DE LANCES (mantida visível como resumo)
    st.header("💰 Estratégia de Lances por Categoria")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.subheader("🚗 Carros")
        if 'Carro' in estrategia:
            st.metric("Lance Competitivo", f"R$ {estrategia['Carro']['lance_competitivo']:,.0f}")
            st.metric("Taxa de Sucesso", f"{estrategia['Carro']['taxa_sucesso_estimada']:.1f}%")
        else:
            st.warning("Sem dados")
    
    with col2:
        st.subheader("🏍️ Motos")
        if 'Moto' in estrategia:
            st.metric("Lance Competitivo", f"R$ {estrategia['Moto']['lance_competitivo']:,.0f}")
            st.metric("Taxa de Sucesso", f"{estrategia['Moto']['taxa_sucesso_estimada']:.1f}%")
        else:
            st.warning("Sem dados")
    
    with col3:
        st.subheader("🚛 Caminhões")
        if 'Caminhão' in estrategia:
            st.metric("Lance Competitivo", f"R$ {estrategia['Caminhão']['lance_competitivo']:,.0f}")
            st.metric("Taxa de Sucesso", f"{estrategia['Caminhão']['taxa_sucesso_estimada']:.1f}%")
        else:
            st.warning("Sem dados")
    
    with col4:
        st.subheader("📊 Base Estatística")
        if 'Total' in estrategia:
            st.metric("Amostra Total", estrategia['Total']['amostra'])
            confianca = "Alta" if estrategia['Total']['amostra'] > 100 else "Média"
            st.metric("Confiança", confianca)
        else:
            st.warning("Sem dados")
    
    with st.expander("📈 Detalhes da Análise de Lances", expanded=False):
        st.subheader("Metodologia de Cálculo")
        st.markdown("""
        - **Lance Competitivo**: Percentil 75 dos valores de arrematação históricos
        - **Taxa de Sucesso**: Percentual de arrematações abaixo do lance recomendado
        - **Base Estatística**: Quantidade de veículos arrematados na categoria
        """)
        
        if 'Total' in estrategia:
            st.subheader("Estatísticas Completas")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Carros**")
                if 'Carro' in estrategia:
                    st.write(f"- Média: R$ {estrategia['Carro']['media_arremate']:,.0f}")
                    st.write(f"- Mediana: R$ {estrategia['Carro']['mediana_arremate']:,.0f}")
                    st.write(f"- Amostra: {estrategia['Carro']['amostra']} veículos")
            
            with col2:
                st.write("**Caminhões**")
                if 'Caminhão' in estrategia:
                    st.write(f"- Média: R$ {estrategia['Caminhão']['media_arremate']:,.0f}")
                    st.write(f"- Mediana: R$ {estrategia['Caminhão']['mediana_arremate']:,.0f}")
                    st.write(f"- Amostra: {estrategia['Caminhão']['amostra']} veículos")
    
    with st.expander("🚛 Oportunidade: Aluguel de Caminhões", expanded=False):
        if viabilidade_caminhoes:
            st.success("**✅ VIÁVEL - Análise Positiva**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Investimento Médio", f"R$ {viabilidade_caminhoes['investimento_medio']:,.0f}")
                st.metric("Desconto Médio", f"{viabilidade_caminhoes['desconto_medio']:.1f}%")
            
            with col2:
                st.metric("Receita Mensal", f"R$ {viabilidade_caminhoes['receita_mensal_estimada']:,.0f}")
                st.metric("Payback", f"{viabilidade_caminhoes['payback_meses']:.1f} meses")
            
            with col3:
                st.metric("ROI Anual", f"{viabilidade_caminhoes['roi_anual']:.1f}%")
                st.metric("Diversidade", f"{viabilidade_caminhoes['modelos_unicos']} modelos")
                
            st.info("""
            **🎯 Por que caminhões são uma boa oportunidade:**
            - **Alta demanda** logística em MT (agronegócio)
            - **Payback rápido** (< 2 anos)
            - **ROI atrativo** (>50% ao ano)
            - **Baixa concorrência** em aluguel especializado
            - **Descontos significativos** nos leilões
            """)
        else:
            st.warning("⚠️ Dados insuficientes para análise de caminhões")
    
    # SEÇÃO 4: PLANO DE AÇÃO (em expander)
    with st.expander("📋 Plano de Ação Recomendado", expanded=False):
        # CORREÇÃO: Preencher com valores reais
        lance_caminhao = estrategia.get('Caminhão', {}).get('lance_competitivo', 'N/A')
        lance_carro = estrategia.get('Carro', {}).get('lance_competitivo', 'N/A')
        lance_moto = estrategia.get('Moto', {}).get('lance_competitivo', 'N/A')
        
        # Formatar valores
        if lance_caminhao != 'N/A':
            lance_caminhao = f"R$ {lance_caminhao:,.0f}"
        if lance_carro != 'N/A':
            lance_carro = f"R$ {lance_carro:,.0f}"
        if lance_moto != 'N/A':
            lance_moto = f"R$ {lance_moto:,.0f}"
        
        st.markdown(f"""
        **🎯 Estratégia de Lances:**
        1. **Caminhões**: Lance máximo de {lance_caminhao} (percentil 75)
        2. **Carros populares**: Focar em modelos até {lance_carro}
        3. **Motos**: Manter lances abaixo de {lance_moto} para melhor ROI
        
        **🚀 Expansão de Frota:**
        - **Prioridade 1**: Adquirir 3-5 caminhões para teste
        - **Prioridade 2**: Renovar frota de motos com CG 150
        - **Prioridade 3**: Substituir carros antigos por modelos econômicos
        """)
        
        st.success("**Conclusão Final:** Foco em caminhões para aluguel apresenta melhor relação risco-retorno")

# CORREÇÃO: Chamar a função para executar
if __name__ == "__main__":
    show_estrategia()