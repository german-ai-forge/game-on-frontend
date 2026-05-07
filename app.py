from urllib import response

import streamlit as st
from services.query_api import get_recommendations

def main():
    """
    Función principal de GAME ON.
    Muestra una interfaz limpia con resultados de búsqueda, manteniendo el input
    del usuario mediante session_state y eliminando métricas de match.
    """

    # 1. Configuración de la página
    st.set_page_config(page_title="GAME ON", page_icon="🎮", layout="wide")

    # Inicializamos el estado de la sesión para el prompt si no existe
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""

    # 2. Estilos Personalizados (CSS)
    st.markdown("""
        <style>
        .stApp { background-color: #0e1117; color: white; }
        .header-container {
            display: flex; flex-direction: column; align-items: center;
            justify-content: center; text-align: center; padding: 40px 0 20px 0;
        }
        .main-title {
            font-size: 85px; font-weight: 800; margin: 0;
            background: -webkit-linear-gradient(#ffffff, #4b6cb7);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            line-height: 1.1;
        }
        .stTextArea textarea {
            background-color: #161b22 !important; color: #ffffff !important;
            border: 1px solid #30363d !important; border-radius: 15px !important;
            font-size: 18px !important;
        }
        .stButton>button {
            width: 100%; background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%) !important;
            color: white !important; border-radius: 10px !important;
            font-weight: bold !important; height: 50px;
        }
        </style>
        """, unsafe_allow_html=True)

    # 3. Encabezado centrado
    st.markdown("""
        <div class="header-container">
            <h1 class="main-title">GAME ON</h1>
            <p style="color: #8b949e; font-size: 22px;">Find your next favorite game</p>
        </div>
        """, unsafe_allow_html=True)

    # 4. Sección de Buscador y Filtros
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Input vinculado a session_state para persistencia
        user_description = st.text_area(
            label="",
            placeholder="Try: 'A relaxing adventure with a deep story and puzzles'...",
            height=120,
            key="user_input"
        )

        # Filtros técnicos debajo del prompt
        f1, f2, f3 = st.columns(3)
        with f1:
            precio = st.slider("Max Price ($)", 0, 100, 25)
        with f2:
            modo = st.selectbox("Mode", ["Any", "Single-player", "Online Co-op", "Multiplayer"])
        with f3:
            mando = st.selectbox("Controller", ["Any", "Full Support", "Partial"])

        st.write("")
        search_clicked = st.button("Search Recommendations")

    # 5. Despliegue de Resultados (Sin porcentajes de Match)
    if search_clicked:
        if st.session_state.user_input:
            st.write("---")
            st.subheader(f"🎮 Recommendations based on: '{st.session_state.user_input}'")

            # Llamada a la API para obtener recomendaciones
            response = get_recommendations(
                 st.session_state.user_input
                )

            if response.get("error"):
                st.error(response["error"])
            return

            games = response.get("recommendations", [])
            # Renderizado de tarjetas en 5 columnas
            cols = st.columns(5)
            for i, game in enumerate(games):
                with cols[i]:
                    st.image(game["img"], use_container_width=True)
                    st.markdown(f"**{game['title']}**")
                    st.caption(f"Genre: {game['genre']}")
                    # Aquí ya no están los st.progress ni los textos de match
        else:
            st.error("Please describe your ideal game first!")

    # 6. Pie de página
    st.markdown("<br><br><p style='text-align: center; color: #484f58;'>NLP Semantic Recommender | Le Wagon Final Project</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
