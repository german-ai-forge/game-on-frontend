API_BASE_URL = "https://gameon-api-790173096042.southamerica-west1.run.app"

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
QUERY_API_ENDPOINT = f"{API_BASE_URL}/query"
