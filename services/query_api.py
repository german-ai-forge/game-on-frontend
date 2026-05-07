import logging
import requests

from config.settings import QUERY_API_ENDPOINT


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def get_recommendations(query: str) -> dict:
    payload = {"query": query}

    try:
        logger.info("Calling recommendation API with query: %s", query)

        response = requests.post(
            QUERY_API_ENDPOINT,
            json=payload,
            timeout=30
        )

        logger.info(
            "Backend response status code: %s",
            response.status_code
        )

        if response.status_code == 200:
            return response.json()

        elif response.status_code == 500:
            logger.error(
                "Backend internal server error: %s",
                response.text
            )

            return {
                "error": (
                    "Internal server error from "
                    "recommendation engine."
                )
            }

        else:
            logger.warning(
                "Unexpected backend response: %s - %s",
                response.status_code,
                response.text
            )

            return {
                "error": (
                    f"Unexpected backend response: "
                    f"{response.status_code}"
                )
            }

    except requests.exceptions.Timeout:
        logger.exception("Recommendation API timeout")

        return {
            "error": "The recommendation service timed out."
        }

    except requests.exceptions.ConnectionError:
        logger.exception("Could not connect to backend API")

        return {
            "error": "Could not connect to the backend API."
        }

    except requests.exceptions.RequestException:
        logger.exception("Unexpected request error")

        return {
            "error": "Unexpected request error."
        }
