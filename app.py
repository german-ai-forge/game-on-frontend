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

        precio = st.slider(
            "Max Price ($)",
            0,
            100,
            25
        )

        st.write("")

        sub1, sub2, sub3 = st.columns([1, 2, 1])

        with sub2:

            if st.button(
                "Search Recommendations",
                use_container_width=True
            ):

                st.session_state.search_done = True
                st.session_state.results = None

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
        def parse_price(price):

            if price is None:
                return 0

            cleaned = re.sub(
                r"[^\d.]",
                "",
                str(price)
            )

            parts = cleaned.split(".")

            if len(parts) > 2:
                cleaned = (
                    parts[0]
                    + "."
                    + "".join(parts[1:])
                )

            return float(cleaned or 0)

        # ---------------------------------------------------
        # FILTER
        # ---------------------------------------------------
        games = [
            g for g in games
            if parse_price(
                g.get("original_price", 0)
            ) <= precio
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

                st.markdown(
                    '<div class="game-card">',
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
                    st.markdown(
                        f"""
                        <div style="
                            color:#58a6ff;
                            font-size:14px;
                            font-weight:700;
                            margin-top:2px;
                            margin-bottom:8px;
                        ">
                            🎯 {(game['match'] * 100):.1f}% MATCH
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
                                font-size:14px;
                                color:#d1d5db;
                                line-height:1.2;
                                margin-bottom:8px;
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
                    # ---------------------------------------------------

                    def normalize_price(price):

                        if price is None:
                            return None

                        try:

                            # extrae únicamente números
                            cleaned = re.sub(
                                r"[^\d.]",
                                "",
                                str(price)
                            )

                            parts = cleaned.split(".")

                            if len(parts) > 2:
                                cleaned = (
                                    parts[0]
                                    + "."
                                    + "".join(parts[1:])
                                )

                            value = float(cleaned or 0)

                            # ---------------------------------------------------
                            # APROX USD NORMALIZATION
                            # ---------------------------------------------------
                            # Steam suele devolver MXN para LATAM
                            # Conversión aproximada MXN -> USD
                            # Ajusta si deseas otro rate
                            # ---------------------------------------------------

                            usd_value = value / 20

                            return f"USD ${usd_value:.2f}"

                        except:
                            return str(price)


                    # FREE
                    if game.get("original_price") is None:

                        st.markdown(
                            """
                            <div style="
                                font-size:20px;
                                color:#2ecc71;
                                font-weight:800;
                                margin-bottom:8px;
                            ">
                                Free to play
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    # DISCOUNT
                    elif (
                        game.get("discount")
                        and game["discount"] > 0
                    ):

                        # ---------------- ORIGINAL PRICE ----------------
                        raw_price = game.get("original_price")

                        cleaned = re.sub(
                            r"[^\d.]",
                            "",
                            str(raw_price)
                        )

                        original_value = float(cleaned or 0)

                        # MXN -> USD aprox
                        original_usd = original_value / 20

                        # ---------------- DISCOUNT ----------------
                        discount = float(game.get("discount", 0))

                        final_price = (
                            original_usd
                            * (1 - discount / 100)
                        )

                        original_price = f"USD ${original_usd:.2f}"

                        discounted_price = f"USD ${final_price:.2f}"

                        # ---------------- UI ----------------
                        price_col1, price_col2, price_col3 = st.columns([2, 1, 2])

                        with price_col1:

                            st.markdown(
                                f"""
                                <div style="
                                    text-decoration:line-through;
                                    color:#8b949e;
                                    font-size:16px;
                                    font-weight:600;
                                    margin-top:6px;
                                ">
                                    {original_price}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        with price_col2:

                            st.markdown(
                                f"""
                                <div style="
                                    color:#ff4b4b;
                                    font-size:15px;
                                    font-weight:800;
                                    margin-top:7px;
                                    text-align:center;
                                ">
                                    -{int(discount)}%
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        with price_col3:

                            st.markdown(
                                f"""
                                <div style="
                                    color:#2ecc71;
                                    font-size:20px;
                                    font-weight:800;
                                    text-align:left;
                                ">
                                    {discounted_price}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    # NORMAL PRICE
                    else:

                        normal_price = normalize_price(
                            game.get("original_price")
                        )

                        st.markdown(
                            f"""
                            <div style="
                                font-size:22px;
                                color:#2ecc71;
                                font-weight:800;
                                margin-bottom:8px;
                            ">
                                {normal_price}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    # ---------------------------------------------------
                    # REVIEWS
                    # ---------------------------------------------------
                    st.markdown(
                        f"""
                        <div style="
                            font-size:13px;
                            color:#facc15;
                            line-height:1;
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
