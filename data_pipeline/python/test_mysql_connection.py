import os

import mysql.connector


def create_connection():
    password = os.getenv("INGEST_DB_PASSWORD")

    if not password:
        raise RuntimeError(
            "INGEST_DB_PASSWORD environment variable is not set"
        )

    return mysql.connector.connect(
        host="localhost",
        port=3307,
        user="genomic_ingest",
        password=password,
        database="genomic_platform",
    )


def main() -> None:
    connection = create_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT DATABASE(), CURRENT_USER(), COUNT(*) FROM gene"
        )

        database, user, gene_count = cursor.fetchone()

        print("Database:", database)
        print("Connected as:", user)
        print("Gene records:", gene_count)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()