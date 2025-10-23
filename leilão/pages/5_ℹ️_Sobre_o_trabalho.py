import streamlit as st
from PIL import Image

def sobre_page():
    st.title("👨‍💻 Sobre o Projeto")
    st.markdown("---")
    
    # Seção de Desenvolvedores - Destaque maior para o desenvolvedor
    st.header("👥 Desenvolvimento")
    
    st.markdown("""
    **Este sistema de análise de leilões foi desenvolvido por Thales Meirelles**  
    *Como trabalho acadêmico para a disciplina de Análise Exploratória de Dados*
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Thales Meirelles")
        st.markdown("""
        🎓 Bacharelado em Estatística - UFBA  
        📧 thalesmeirelles17@gmail.com  
        🐙 [GitHub](https://github.com/Thmeirelles)
        
        **Desenvolvedor principal**  
        *Análise, programação e implementação*
        """)
    
    with col2:
        st.subheader("Pedro Vasconcelos")
        st.markdown("""
        🎓 Bacharelado em Estatística - UFBA  
        📊 Cientista de Dados
        
        **Colaborador**  
        *Desenvolvimento do trabalho*
        """)
    
    # Seção do Projeto
    st.markdown("---")
    st.header("📚 Contexto Acadêmico")
    
    st.markdown("""
    **Trabalho desenvolvido para a disciplina de Análise Exploratória de Dados**  
    *Bacharelado em Estatística - Universidade Federal da Bahia (UFBA)*
    
    Projeto acadêmico que aplica técnicas de análise exploratória de dados 
    em um contexto de negócios, simulando a operação de uma empresa de leilões.
    """)
    
    # Repositórios
    st.markdown("---")
    st.header("📂 Repositórios")
    
    repo_cols = st.columns(2)
    with repo_cols[0]:
        st.markdown("""
        **👨‍💻 GitHub Pessoal (Thales)**  
        [github.com/Thmeirelles](https://github.com/Thmeirelles)
        """)
    
    with repo_cols[1]:
        st.markdown("""
        **💻 Código do Trabalho**  
        [github.com/Thmeirelles/leil-](https://github.com/Thmeirelles/leil-)
        """)
    
    # Stack Tecnológica
    st.markdown("---")
    st.header("🛠️ Stack Tecnológica")
    
    st.markdown("""
    ### 📊 **Análise Exploratória & Estatística**
    - **Pandas**: Manipulação e limpeza de dados
    - **NumPy**: Cálculos numéricos e estatísticos
    - **SciPy**: Testes estatísticos avançados
    - **Statistics**: Estatísticas descritivas básicas
    
    ### 📈 **Visualização de Dados**
    - **Plotly**: Gráficos interativos e dinâmicos
    - **Streamlit**: Interface web e dashboard
    - **Matplotlib**: Visualizações estáticas personalizadas
    
    ### ⚙️ **Desenvolvimento & Deployment**
    - **Python 3.x**: Linguagem principal
    - **Streamlit Components**: UI/UX responsiva
    - **PIL/Pillow**: Processamento de imagens
    
    ### 🔍 **Métodos Estatísticos Aplicados**
    - Análise descritiva univariada e multivariada
    - Análise de distribuições e outliers
    - Correlações e associações
    - Agrupamento e segmentação
    - Análise de tendências e padrões
    """)
    
    # Agradecimentos
    st.markdown("---")
    st.header("🙏 Agradecimentos")
    
    st.markdown("""
    ### 🎓 **Professor Orientador**
    **Ricardo Rocha**  
    *Professor da disciplina de Análise Exploratória de Dados - UFBA*
    
    ### 👥 **Colegas**
    Agradecemos aos colegas da turma de Estatística da UFBA 
    por assistirem e ouvirem a apresentação deste trabalho.
    
    ### 🎭 **Contextualização**
    **Ricardo Auto** é uma empresa fictícia criada para contextualizar 
    a apresentação deste trabalho acadêmico.
    """)
    
    # Objetivos Acadêmicos
    st.markdown("---")
    st.header("🎯 Objetivos Acadêmicos")
    
    st.markdown("""
    Este trabalho buscou demonstrar a aplicação prática dos conceitos 
    aprendidos na disciplina de Análise Exploratória de Dados:
    
    - Coleta e limpeza de dados reais
    - Análise descritiva completa dos dados
    - Visualização eficaz de informações estatísticas
    - Identificação de padrões e insights relevantes
    - Comunicação clara dos resultados obtidos
    - Contextualização em um problema de negócios real
    """)
    
    # Informações da Instituição
    st.markdown("---")
    st.header("🏫 Instituição de Ensino")
    
    # Logo da UFBA
    
    
    st.markdown("""
    **Universidade Federal da Bahia (UFBA)**  
    *Instituto de Matemática e Estatística*  
    *Bacharelado em Estatística*
    
    *virtute spiritus*
    """)
    try:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            ufba_logo = Image.open('leilão/imagens/logo_ufba.jpg')  # Ajuste o caminho
            st.image(ufba_logo, width=200)
    except:
        st.info("Logo da UFBA")
# Chamada da função
sobre_page()