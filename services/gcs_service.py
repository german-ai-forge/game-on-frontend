from google.cloud import storage
import os

BUCKET_NAME = os.getenv(
    "GCS_BUCKET_NAME"
)

def download_cache():

    storage_client = storage.Client()

    bucket = storage_client.bucket(
        BUCKET_NAME
    )

    files = [
        "cleaned_games.parquet",
        "embeddings.pt"
    ]

    os.makedirs(
        "data/cache",
        exist_ok=True
    )

    for file_name in files:

        blob = bucket.blob(file_name)

        blob.download_to_filename(
            f"data/cache/{file_name}"
        )
