import streamlit as st
from services.query_api import get_recommendations
import re

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
        precio = st.slider("Max Price ($)", 0, 100, 25)


        st.write("")
        search_clicked = st.button("Search Recommendations")

    # 5. Despliegue de Resultados (Sin porcentajes de Match)
    if search_clicked:
        if st.session_state.user_input:
            st.write("---")

            response = get_recommendations(st.session_state.user_input)

            if response.get("error"):
                st.error(response["error"])
                return

            if response.get("consulta_mejorada"):
                st.info(f"🔍 Búsqueda mejorada: {response['consulta_mejorada']}")

            st.subheader(f"🎮 Recommendations based on: '{st.session_state.user_input}'")

            games = response.get("recommendations", [])

            def parse_price(price):
                cleaned = re.sub(r'[^\d.]', '', str(price))
                parts = cleaned.split('.')
                if len(parts) > 2:
                    cleaned = parts[0] + '.' + ''.join(parts[1:])
                return float(cleaned or 0)

            games = [
                game for game in games
                if parse_price(game.get("original_price", 0)) <= precio
            ]

            st.write(f"Games after price filter: {len(games)}")

            if not games:
                st.warning("No recommendations found with the selected price filter.")
                return

            cols = st.columns(5)

            for i, game in enumerate(games[:5]):
                with cols[i]:

                    if game.get('trailer'):
                        st.markdown(f"""
                            <video width="100%" controls>
                                <source src="{game['trailer']}">
                            </video>
                        """, unsafe_allow_html=True)
                    st.markdown(f"**{game['name']}**")
                    st.caption(f"📊 Match: {game['match']:.2%}")
                    if game.get('descripcion'):
                        st.caption(game['descripcion'])
                    st.caption(f"Genre: {game['genre']}")
                    st.caption(f"{game['popular_tags']}")
                    if game.get('original_price') is None:
                        st.caption("💰 Free to play")
                    elif game.get('discount') and game['discount'] > 0:
                        st.caption(f"💰 {game['original_price']} 🏷️ -{game['discount']}% descuento")
                    else:
                        st.caption(f"💰 {game['original_price']}")
                    st.caption(f"⭐ {game['review_percentage']}")
                    st.write(f"🔗 [Link]({game['url']})")

        else:
            st.error("Please describe your ideal game first!")

    # 6. Pie de página
    st.markdown("<br><br><p style='text-align: center; color: #484f58;'>NLP Semantic Recommender | Le Wagon Final Project</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
