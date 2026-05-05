import streamlit as st

# 1. Configuración de la página
st.set_page_config(page_title="GAME ON", page_icon="🎮", layout="wide")

# 2. CSS: Letras blancas en prompt + Header Centrado
st.markdown("""
    <style>
    /* Fondo de la aplicación */
    .stApp {
        background-color: #0e1117;
        color: white;
    }

    /* Contenedor del Título Centrado */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 60px 0 30px 0;
        width: 100%;
    }

    .main-title {
        font-size: 85px;
        font-weight: 800;
        margin: 0;
        background: -webkit-linear-gradient(#ffffff, #4b6cb7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
    }

    .sub-title {
        color: #8b949e;
        font-size: 22px;
        margin-top: 10px;
    }

    /* Configuración del área de texto (Prompt con letras blancas) */
    .stTextArea textarea {
        background-color: #161b22 !important;
        color: #ffffff !important; /* Letras blancas al escribir */
        border: 1px solid #30363d !important;
        border-radius: 15px !important;
        font-size: 18px !important;
        caret-color: white !important;
    }

    .stTextArea textarea::placeholder {
        color: #8b949e !important;
        opacity: 1;
    }

    /* Botón personalizado */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%) !important;
        color: white !important;
        border: none !important;
        padding: 15px !important;
        border-radius: 10px !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Renderizado del Header Centrado
# Usamos un div con la clase header-container definida arriba
st.markdown("""
    <div class="header-container">
        <h1 class="main-title">GAME ON</h1>
        <p class="sub-title">Find your next favorite game</p>
    </div>
    """, unsafe_allow_html=True)

# 4. Layout del buscador (Centrado usando columnas)
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # El área de descripción (NLP Input)
    user_description = st.text_area(
        label="",
        placeholder="Try: 'A relaxing adventure with a deep story and puzzles'...",
        height=150
    )

    st.write("") # Espacio

    # Botón de búsqueda
    if st.button("Search Recommendations"):
        if user_description:
            st.write("---")
            st.success(f"Analizando tu búsqueda: {user_description}")
        else:
            st.error("Please describe what you're looking for first!")

# 5. Footer
st.markdown("<br><br><p style='text-align: center; color: #484f58;'>NLP Semantic Recommender | Le Wagon Final Project</p>", unsafe_allow_html=True)
