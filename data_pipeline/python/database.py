import os

import mysql.connector


def create_connection():
    password = os.getenv("INGEST_DB_PASSWORD")

    if not password:
        raise RuntimeError(
            "INGEST_DB_PASSWORD environment variable is not set"
        )

    return mysql.connector.connect(
        host=os.getenv("INGEST_DB_HOST", "localhost"),
        port=int(os.getenv("INGEST_DB_PORT", "3307")),
        user=os.getenv("INGEST_DB_USER", "genomic_ingest"),
        password=password,
        database=os.getenv("INGEST_DB_NAME", "genomic_platform"),
    )