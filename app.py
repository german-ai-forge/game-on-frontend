import streamlit as st
from services.query_api import get_recommendations
import re
from utils.language_utils import is_english_query

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
        /* Importamos la tipografía Gamer */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

        .stApp { background-color: #0e1117; color: white; }

        .header-container {
            display: flex; flex-direction: column; align-items: center;
            justify-content: center; text-align: center; padding: 50px 0 30px 0;
        }

        .main-title {
            font-family: 'Orbitron', sans-serif !important;
            font-size: 110px !important;
            font-weight: 900 !important;
            margin: 0 !important;
            background: -webkit-linear-gradient(#ffffff, #4b6cb7) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            line-height: 1.1 !important;
            text-shadow: 0px 10px 20px rgba(75, 108, 183, 0.3) !important;
            letter-spacing: 5px !important;
            white-space: nowrap !important;
        }

        .main-subtitle {
            font-family: 'Orbitron', sans-serif !important;
            color: #8b949e !important;
            font-size: 28px !important;
            font-weight: 400 !important;
            letter-spacing: 2px !important;
            margin-top: 10px !important;
        }

        /* Inputs y Botón (igual que antes) */
        .stTextArea textarea {
            background-color: #161b22 !important; color: #ffffff !important;
            border: 1px solid #30363d !important; border-radius: 15px !important;
            font-size: 18px !important; font-weight: 500 !important;
        }
        .stTextArea textarea::placeholder { color: #e6edf3 !important; opacity: 0.8 !important; }

        div[data-testid="stWidgetLabel"] p, .stSlider label p {
            color: #ffffff !important; font-size: 16px !important; font-weight: 600 !important;
        }

        .stButton>button {
            background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%) !important;
            color: white !important; border-radius: 10px !important;
            font-weight: bold !important; height: 50px; border: none !important;
            transition: 0.3s;
        }
        .stButton>button:hover { border: 1px solid #ffffff !important; box-shadow: 0px 0px 15px rgba(75, 108, 183, 0.4); }

        /* --- MODIFICACIÓN: Estilos para la Lista Escalonada de Juegos --- */

        /* Contenedor de cada juego en la lista */
        .game-list-item {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 25px; /* Espacio entre juegos */
            transition: 0.3s;
            display: flex; /* Para asegurar alineación interna si hace falta */
            align-items: flex-start;
        }

        /* Efecto al pasar el mouse por encima de la tarjeta del juego */
        .game-list-item:hover {
            border: 1px solid #4b6cb7;
            box-shadow: 0px 0px 20px rgba(75, 108, 183, 0.2);
            transform: translateY(-2px); /* Pequeño levante */
        }

        /* Título del juego dentro de la lista */
        .game-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 28px !important;
            font-weight: 700;
            margin: 0 0 10px 0;
            color: #ffffff;
        }

        /* Video responsivo y redondeado */
        .stVideo video, .game-video video {
            border-radius: 15px !important;
            border: 1px solid #30363d;
        }

        /* Estilos para etiquetas de metadatos */
        .game-meta {
            color: #8b949e;
            font-size: 14px;
            margin-bottom: 5px;
        }

        .game-about {
            font-size: 16px;
            color: #e6edf3;
            line-height: 1.6;
            margin: 15px 0;
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

        # --- EL TRUCO INFALIBLE: SUB-COLUMNAS ---
        # Creamos 3 columnas pequeñas dentro de col2. La del medio es más ancha.
        sub_col1, sub_col2, sub_col3 = st.columns([1, 2, 1])
        with sub_col2:
            # use_container_width=True hace que el botón llene su sub-columna, quedando centrado
            search_clicked = st.button("Search Recommendations", use_container_width=True)

    # 5. Despliegue de Resultados (Sin porcentajes de Match)
    if search_clicked:

        if st.session_state.user_input:
            query = st.session_state.user_input.strip()

            if len(query.split()) < 3:
                st.warning("Please describe your ideal game in English using at least 3 words.")
                return

            if not is_english_query(query):
                st.warning("Please enter your game description in English.")
                return

            st.write("---")

            response = get_recommendations(query)

            if response.get("error"):
                st.error(response["error"])
                # Nota: Asegúrate de que este 'return' esté dentro de una función o cámbialo por un bloque condicional
            else:
                assistant_response = response.get("respuesta") or response.get("message")
                if assistant_response:
                    with st.chat_message("assistant"):
                        st.markdown(assistant_response)

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

            # Filtrado por precio
            green_dollar = '<span style="color: #2ecc71; font-weight: bold; margin-right: 5px;">&#36;</span>'
            games = [
                game for game in games
                if parse_price(game.get("original_price", 0)) <= precio
            ]

            st.write(f"Games after price filter: {len(games)}")

            if not games:
                st.warning("No recommendations found with the selected price filter.")
            else:
                # Iteración para mostrar cada juego en una fila vertical
                for game in games[:5]:
                    # Creamos una fila dividida en 2 columnas (proporción 2:3)
                    col_izq, col_der = st.columns([2, 3])

                    with col_izq:
                        # Obtenemos la imagen (usamos una por defecto si no existe)
                        #img_url = game.get('image_url') or game.get('header_image') or "https://via.placeholder.com/460x215?text=No+Image+Available"
                        img_url = game.get('image_url') or game.get('header_image')
                        if not img_url and game.get('app_id'):
                            img_url = f"https://cdn.akamai.steamstatic.com/steam/apps/{game['app_id']}/header.jpg"
                        if not img_url:
                            img_url = "https://via.placeholder.com/460x215?text=Preview+Not+Available"

                        if game.get('trailer'):
                            # Efecto "Slide": Pestañas para alternar entre Imagen y Video
                            tab_img, tab_video = st.tabs(["🖼️ Poster", "🎬 Trailer"])

                            with tab_img:
                                st.image(img_url, use_container_width=True)

                            with tab_video:
                                st.markdown(f'''
                                    <video width="100%" controls style="border-radius: 10px;">
                                        <source src="{game['trailer']}">
                                    </video>
                                ''', unsafe_allow_html=True)
                        else:
                            st.image(img_url, use_container_width=True)

                    with col_der:
                        # Columna Derecha: Información detallada
                        st.markdown(f"### **{game['name']}**")
                        st.caption(f"📊 Match: {game['match']:.2%}")

                        if game.get('descripcion'):
                            st.write(game['descripcion'])

                        st.write(f"**Genre:** {game['genre']}")
                        st.write(f"**Tags:** {game['popular_tags']}")

                        # Lógica de Precios/Descuentos
                        if game.get('original_price') is None:
                            st.markdown(f"{green_dollar} <span style='font-weight: bold;'>Free to play</span>", unsafe_allow_html=True)
                        elif game.get('discount') and game['discount'] > 0:
                            precio_html = f"""
                            {green_dollar} <span style='text-decoration: line-through; color: #8b949e;'>{game['original_price']}</span>
                            🏷️ <span style='color: #ff4b4b; font-weight: bold;'>-{game['discount']}% off</span>
                            """
                            st.markdown(precio_html, unsafe_allow_html=True)
                        else:
                            st.markdown(f"{green_dollar} {game['original_price']}", unsafe_allow_html=True)

                        st.write(f"⭐ {game['review_percentage']}")
                        st.markdown(f"🔗 [Ver en Steam]({game['url']})")

                    st.write("---") # Separador entre juegos

    else:
        st.error("Please describe your ideal game first!")

    # 6. Pie de página
    st.markdown("<br><br><p style='text-align: center; color: #484f58;'>NLP Semantic Recommender | Le Wagon Final Project</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
