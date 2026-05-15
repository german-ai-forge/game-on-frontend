# -*- coding: utf-8 -*-
import streamlit as st
from services.query_api import get_recommendations
import re


def main():

    # ---------------------------------------------------
    # PAGE CONFIG
    # ---------------------------------------------------
    st.set_page_config(
        page_title="GAME ON",
        page_icon="🎮",
        layout="wide"
    )

    # ---------------------------------------------------
    # SESSION STATE
    # ---------------------------------------------------
    if "search_done" not in st.session_state:
        st.session_state.search_done = False

    if "results" not in st.session_state:
        st.session_state.results = None

    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    if "last_input" not in st.session_state:
        st.session_state.last_input = ""

    if "active_trailer" not in st.session_state:
        st.session_state.active_trailer = None

    # ---------------------------------------------------
    # RESET STATE
    # ---------------------------------------------------
    def reset_state_if_needed():

        if st.session_state.user_input != st.session_state.last_input:

            st.session_state.search_done = False
            st.session_state.results = None
            st.session_state.active_trailer = None

    # ---------------------------------------------------
    # CSS
    # ---------------------------------------------------
    st.markdown("""
    <style>
    /* Ocultar progress bar de Streamlit */
    .stProgress {
        display: none !important;
    }

    div[data-testid="stStatusWidget"] {
        display: none !important;
    }

    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

    .stApp {
        background-color: #0e1117;
        color: white;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1rem;
        max-width: 1500px;
    }

    /* HEADER */

    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;

        text-align: center;

        padding-top: 25px;
        padding-bottom: 15px;
    }

    .main-title {

        font-family: 'Orbitron', sans-serif !important;

        font-size: 110px !important;

        font-weight: 900 !important;

        margin: 0 !important;

        background: linear-gradient(
            180deg,
            #ffffff 0%,
            #4b6cb7 100%
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        line-height: 1;

        letter-spacing: 4px;

        text-shadow:
            0px 10px 20px rgba(75,108,183,0.3);
    }

    .main-subtitle {

        color: #8b949e;

        font-size: 22px;

        margin-top: 10px;

        font-family: 'Orbitron', sans-serif;
    }

    /* INPUT */

    .stTextArea textarea {

        background-color: #161b22 !important;

        color: white !important;

        border-radius: 16px !important;

        border: 1px solid #30363d !important;

        font-size: 18px !important;

        padding: 14px !important;
    }

    .stTextArea textarea::placeholder {
        color: #8b949e !important;
    }

    /* BUTTON */

    .stButton > button {

        width: 100%;

        border-radius: 12px !important;

        border: none !important;

        background: linear-gradient(
            90deg,
            #4b6cb7 0%,
            #182848 100%
        ) !important;

        color: white !important;

        font-weight: 700 !important;

        height: 48px !important;

        transition: 0.25s;
    }

    .stButton > button:hover {

        border: 1px solid #4b6cb7 !important;

        box-shadow:
            0px 0px 18px rgba(75,108,183,0.35);
    }

    /* GAME CARD */

    .game-card {

        background-color: #161b22;

        border: 1px solid #30363d;

        border-radius: 18px;

        padding: 18px;

        margin-bottom: 18px;

        transition: 0.2s;
    }

    .game-card:hover {

        border: 1px solid #4b6cb7;

        box-shadow:
            0px 0px 18px rgba(75,108,183,0.18);
    }

    /* IMAGES */

    img {
        border-radius: 14px !important;
    }

    video {
        width: 100%;
        border-radius: 14px;
        border: 1px solid #30363d;
    }

    /* TEXT COMPACT */

    .compact-text {
        line-height: 1.15 !important;
    }

    /* SLIDER ESTÉTICO */

    div[data-testid="stSlider"] > div > div > div {
        height: 5px !important;
        background: #21262d !important;
        border-radius: 10px !important;
    }

    div[data-testid="stSlider"] div[role="slider"] {
        width: 22px !important;
        height: 22px !important;
        background: white !important;
        border: 3px solid #4b6cb7 !important;
        border-radius: 50% !important;
        box-shadow: 0 0 12px rgba(75,108,183,0.6) !important;
    }

    div[data-testid="stSlider"] div[role="slider"]:hover {
        box-shadow: 0 0 20px rgba(56,139,253,0.9) !important;
        border-color: #388bfd !important;
    }

    /* GAME DIVIDER */

    .game-divider {
        border: none;
        border-top: 1px solid #21262d;
        margin: 32px 0 32px 0;
    }

    /* LINK BUTTON */

    [data-testid="stLinkButton"] a {

        background: linear-gradient(
            90deg,
            #1f6feb 0%,
            #388bfd 100%
        ) !important;

        color: white !important;

        border-radius: 12px !important;

        border: none !important;

        font-weight: 700 !important;

        height: 46px !important;

        display: flex !important;

        align-items: center !important;

        justify-content: center !important;

        text-decoration: none !important;

        transition: 0.25s !important;
    }

    [data-testid="stLinkButton"] a:hover {

        border: 1px solid #4b6cb7 !important;

        box-shadow:
            0px 0px 18px rgba(75,108,183,0.35);
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------
    # HEADER
    # ---------------------------------------------------
    st.markdown(
        """
        <div class="header-container">
            <div class="main-title">GAME ON</div>
            <div class="main-subtitle">
                Find your next favorite game
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------------------------------------------
    # SEARCH SECTION
    # ---------------------------------------------------
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.text_area(
            label="",
            placeholder="Try: 'A relaxing adventure with a deep story and puzzles'...",
            height=120,
            key="user_input"
        )

        reset_state_if_needed()

        st.session_state.last_input = st.session_state.user_input

        st.markdown(
            """
            <div style="
                font-size:18px;
                font-weight:700;
                color:white;
                margin-bottom:4px;
                margin-top:8px;
                font-family:'Orbitron', sans-serif;
                letter-spacing:1px;
            ">
                💰 Precio Máximo
            </div>
            """,
            unsafe_allow_html=True
        )

        precio = st.slider(
            label="",
            min_value=0,
            max_value=300,
            value=100,
            format="S/.%d"
        )

        st.write("")
        sub_col1, sub_col2, sub_col3 = st.columns([1, 2, 1])

        with sub_col2:

            search_clicked = st.button(
                "Search Recommendations",
                use_container_width=True
                )
        if search_clicked:

            query = st.session_state.user_input.strip()

            st.session_state.search_done = True
            st.session_state.results = get_recommendations(query)

    # ---------------------------------------------------
    # RESULTS
    # ---------------------------------------------------
    if st.session_state.search_done and st.session_state.user_input:

        if st.session_state.results is None:

            st.session_state.results = get_recommendations(
                st.session_state.user_input
            )

        response = st.session_state.results

        if response.get("error"):

            st.error(response["error"])
            return

        assistant_response = (
            response.get("respuesta")
            or response.get("message")
        )

        if assistant_response:

            with st.chat_message("assistant"):
                st.markdown(assistant_response)

        if response.get("consulta_mejorada"):

            st.info(
                f"🔍 Improved query: "
                f"{response['consulta_mejorada']}"
            )

        st.subheader(
            f"🎮 Recommendations based on: "
            f"'{st.session_state.user_input}'"
        )

        games = response.get("recommendations", [])

        # ---------------------------------------------------
        # PRICE PARSER
        # ---------------------------------------------------
        def parse_price(price_str):

            if not price_str:
                return 0

            # Extraer solo el número con re, ignorando prefijos como S/.
            match = re.search(r'(\d+(?:\.\d+)?)', str(price_str).replace(',', '.'))
            if match:
                return float(match.group(1))

            return 0

        # ---------------------------------------------------
        # COMPARABLE PRICE (para el filtro)
        # El backend manda el precio FINAL en original_price
        # Si hay descuento, calculamos el precio original real
        # ---------------------------------------------------
        def get_comparable_price(g):

            price_str = (
                g.get("original_price", "")
                or g.get("price", "")
                or ""
            )
            discount = g.get("discount", 0)

            precio_original = parse_price(price_str)

            # Si hay descuento, comparar por el precio final que realmente pagas
            if discount and discount > 0:
                return precio_original * (1 - discount / 100)

            return precio_original

        # ---------------------------------------------------
        # FILTER
        # ---------------------------------------------------
        games = [
            g for g in games
            if get_comparable_price(g) <= precio
        ]

        if not games:

            st.warning(
                "No recommendations found."
            )

        else:

            for i, game in enumerate(games[:8]):

                game_id = game.get(
                    "name",
                    f"game_{i}"
                )

                best_match = i == 0

                # Separador entre juegos (no antes del primero)
                if i > 0:
                    st.markdown(
                        "<hr class='game-divider'>",
                        unsafe_allow_html=True
                    )

                col_left, col_right = st.columns([2, 3])

                # ---------------------------------------------------
                # LEFT
                # ---------------------------------------------------
                with col_left:

                    img_url = (
                        game.get("image_url")
                        or game.get("header_image")
                    )

                    if not img_url and game.get("app_id"):

                        img_url = (
                            "https://cdn.akamai.steamstatic.com/"
                            f"steam/apps/{game['app_id']}/header.jpg"
                        )

                    if not img_url:

                        img_url = (
                            "https://via.placeholder.com/"
                            "460x215?text=Preview+Not+Available"
                        )

                    trailer = game.get("trailer")

                    # ACTIVE TRAILER
                    if (
                        st.session_state.active_trailer
                        == game_id
                        and trailer
                    ):

                        st.markdown(
                            f"""
                            <video autoplay controls>
                                <source
                                    src="{trailer}"
                                    type="video/mp4">
                            </video>
                            """,
                            unsafe_allow_html=True
                        )

                    else:

                        st.image(
                            img_url,
                            use_container_width=True
                        )

                    # BUTTONS
                    btn1, btn2, btn3 = st.columns(3)

                    with btn1:

                        if trailer:

                            if st.button(
                                "🎬 Trailer",
                                key=f"trailer_{game_id}"
                            ):

                                st.session_state.active_trailer = game_id
                                st.rerun()

                    with btn2:

                        if st.button(
                            "◧ Cover",
                            key=f"poster_{game_id}"
                        ):

                            if (
                                st.session_state.active_trailer
                                == game_id
                            ):

                                st.session_state.active_trailer = None

                            st.rerun()

                    with btn3:

                        steam_url = game.get("url", "#")

                        st.link_button(
                            "🎮 View on Steam",
                            steam_url,
                            use_container_width=True
                        )

                # ---------------------------------------------------
                # RIGHT
                # ---------------------------------------------------
                with col_right:

                    # ---------------------------------------------------
                    # TITLE + BEST MATCH
                    # ---------------------------------------------------
                    title_cols = st.columns([5, 2])

                    with title_cols[0]:
                        st.markdown(
                            f"""
                            <div style="
                                font-size:30px;
                                font-weight:800;
                                color:white;
                                font-family:'Orbitron',sans-serif;
                                line-height:1.1;
                                margin-bottom:2px;
                            ">
                                {game['name']}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with title_cols[1]:

                        if best_match:

                            st.markdown(
                                """
                                <div style="
                                    background:#facc15;
                                    color:black;
                                    font-size:11px;
                                    font-weight:800;
                                    padding:6px 10px;
                                    border-radius:8px;
                                    text-align:center;
                                    margin-top:8px;
                                ">
                                    ⭐ BEST MATCH
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    # ---------------------------------------------------
                    # MATCH
                    # ---------------------------------------------------
                    match_pct = (game['match'] * 100)
                    match_color = (
                        "#2ecc71" if match_pct >= 70
                        else "#facc15" if match_pct >= 50
                        else "#8b949e"
                    )
                    st.markdown(
                        f"""
                        <div style="
                            display:inline-flex;
                            align-items:center;
                            gap:6px;
                            background:rgba(88,166,255,0.08);
                            border:1px solid rgba(88,166,255,0.2);
                            border-radius:20px;
                            padding:4px 12px;
                            margin-top:4px;
                            margin-bottom:10px;
                        ">
                            <span style="font-size:13px;">🎯</span>
                            <span style="
                                color:{match_color};
                                font-size:13px;
                                font-weight:800;
                                letter-spacing:0.5px;
                            ">{match_pct:.1f}% MATCH</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # ---------------------------------------------------
                    # DESCRIPTION
                    # ---------------------------------------------------
                    if game.get("descripcion"):

                        st.markdown(
                            f"""
                            <div style="
                                font-size:13.5px;
                                color:#c9d1d9;
                                line-height:1.55;
                                margin-bottom:12px;
                                padding:10px 14px;
                                background:rgba(255,255,255,0.03);
                                border-left:3px solid #4b6cb7;
                                border-radius:0 8px 8px 0;
                            ">
                                {game['descripcion']}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    # ---------------------------------------------------
                    # GENRE
                    # ---------------------------------------------------
                    st.markdown(
                        f"""
                        <div style="
                            color:#9ca3af;
                            font-size:13px;
                            line-height:1.1;
                            margin-bottom:4px;
                        ">
                            <span style="
                                color:white;
                                font-weight:700;
                            ">
                                Genre:
                            </span>
                            {game.get('genre', 'Unknown')}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # ---------------------------------------------------
                    # TAGS
                    # ---------------------------------------------------
                    st.markdown(
                        f"""
                        <div style="
                            color:#9ca3af;
                            font-size:13px;
                            line-height:1.1;
                            margin-bottom:8px;
                        ">
                            <span style="
                                color:white;
                                font-weight:700;
                            ">
                                Popular tags:
                            </span>
                            {game.get('popular_tags', 'N/A')}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # ---------------------------------------------------
                    # PRICE
                    # NOTA: el backend manda el precio FINAL en original_price
                    # Si hay descuento, calculamos el precio original real
                    # ---------------------------------------------------
                    discount = game.get("discount", 0)
                    price_str = (
                        game.get("original_price", "")
                        or game.get("price", "")
                        or ""
                    )

                    if not price_str:
                        # Free to play
                        st.markdown(
                            """
                            <div style="
                                display:inline-flex;
                                align-items:center;
                                gap:8px;
                                background:rgba(46,204,113,0.1);
                                border:1px solid rgba(46,204,113,0.35);
                                border-radius:10px;
                                padding:10px 18px;
                                margin-top:10px;
                                font-size:22px;
                                color:#2ecc71;
                                font-weight:800;
                                letter-spacing:0.5px;
                            ">
                                🎁 Free to Play
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    elif discount and discount > 0:
                        # original_price ES el precio original (sin descuento)
                        # El precio final se calcula: original * (1 - descuento/100)
                        valor_match = re.search(r'(\d+(?:[.,]\d+)?)', price_str)
                        precio_final_calculado = ""

                        if valor_match:
                            try:
                                valor_original = float(valor_match.group(1).replace(',', '.'))
                                valor_final = valor_original * (1 - discount / 100)
                                prefijo_match = re.search(r'^([^\d]+)', price_str.strip())
                                prefijo = prefijo_match.group(1) if prefijo_match else ""
                                precio_final_calculado = f"{prefijo}{valor_final:.2f}"
                            except (ValueError, ZeroDivisionError):
                                precio_final_calculado = ""

                        st.markdown(
                            f"""
                            <div style="
                                display:flex;
                                align-items:center;
                                gap:12px;
                                flex-wrap:wrap;
                                margin-top:10px;
                                padding:12px 16px;
                                background:rgba(46,204,113,0.06);
                                border:1px solid rgba(46,204,113,0.15);
                                border-radius:12px;
                            ">
                                <span style="
                                    text-decoration:line-through;
                                    color:#6e7681;
                                    font-size:18px;
                                    font-weight:500;
                                ">{price_str}</span>
                                <span style="
                                    background:linear-gradient(135deg, #c0392b, #e74c3c);
                                    color:white;
                                    font-size:15px;
                                    font-weight:900;
                                    padding:5px 12px;
                                    border-radius:8px;
                                    letter-spacing:1px;
                                    box-shadow:0 2px 8px rgba(192,57,43,0.4);
                                ">-{int(discount)}%</span>
                                <span style="
                                    color:#2ecc71;
                                    font-size:30px;
                                    font-weight:900;
                                    letter-spacing:0.5px;
                                    text-shadow:0 0 20px rgba(46,204,113,0.3);
                                ">{precio_final_calculado}</span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    else:
                        # Precio normal sin descuento
                        st.markdown(
                            f"""
                            <div style="
                                display:inline-flex;
                                align-items:center;
                                padding:10px 18px;
                                margin-top:10px;
                                background:rgba(46,204,113,0.06);
                                border:1px solid rgba(46,204,113,0.2);
                                border-radius:12px;
                                color:#2ecc71;
                                font-size:28px;
                                font-weight:900;
                                letter-spacing:0.5px;
                                text-shadow:0 0 20px rgba(46,204,113,0.3);
                            ">{price_str}</div>
                            """,
                            unsafe_allow_html=True
                        )

                    # ---------------------------------------------------
                    # REVIEWS
                    # ---------------------------------------------------
                    st.markdown(
                        f"""
                        <div style="
                            display:inline-flex;
                            align-items:center;
                            gap:5px;
                            margin-top:8px;
                            background:rgba(250,204,21,0.07);
                            border:1px solid rgba(250,204,21,0.2);
                            border-radius:20px;
                            padding:4px 12px;
                            font-size:12.5px;
                            color:#facc15;
                            font-weight:600;
                        ">
                            ⭐ {game.get('review_percentage', 'No reviews')}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
    else:

        st.info(
            "Describe your ideal game "
            "and click Search Recommendations"
        )

    # ---------------------------------------------------
    # FOOTER
    # ---------------------------------------------------
    st.markdown(
        """
        <br><br>

        <p style="
            text-align:center;
            color:#484f58;
        ">
            NLP Semantic Recommender |
            Le Wagon Final Project
        </p>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
