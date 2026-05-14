#API_BASE_URL = "https://game-on-frontend.run.app"
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
QUERY_API_ENDPOINT = f"{API_BASE_URL}/query"
