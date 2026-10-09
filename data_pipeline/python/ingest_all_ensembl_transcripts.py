from database import create_connection
from ingest_ensembl_transcripts import ingest_transcripts


def fetch_genes() -> list[tuple[str, str]]:
    connection = create_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT gene_id, gene_symbol
            FROM gene
            ORDER BY gene_symbol
            """
        )

        return cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


def main() -> None:
    genes = fetch_genes()

    if not genes:
        raise ValueError("No genes found in the database")

    successful = 0
    failed = 0

    for gene_id, gene_symbol in genes:
        print(
            f"\n=== Processing {gene_symbol} "
            f"({gene_id}) ==="
        )

        try:
            ingest_transcripts(gene_id)
            successful += 1

        except Exception as error:
            failed += 1
            print(
                f"Failed: {gene_symbol} ({gene_id})"
            )
            print(f"Reason: {error}")

    print("\n=== Transcript batch summary ===")
    print("Genes:", len(genes))
    print("Successful:", successful)
    print("Failed:", failed)


if __name__ == "__main__":
    main()