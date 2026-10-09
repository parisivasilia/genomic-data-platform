import argparse
import time

from database import create_connection
from ingest_clinvar_variants import ingest_clinvar_variants


def fetch_genes() -> list[tuple[str, str]]:
    connection = create_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT gene_id, gene_symbol
            FROM gene
            WHERE gene_symbol IS NOT NULL
            ORDER BY gene_symbol
            """
        )

        return cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest ClinVar variants for all genes."
    )

    parser.add_argument(
        "--retmax",
        type=int,
        default=10,
    )

    args = parser.parse_args()

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
            ingest_clinvar_variants(
                gene_symbol,
                args.retmax,
            )
            successful += 1

        except Exception as error:
            failed += 1
            print(
                f"Failed: {gene_symbol} ({gene_id})"
            )
            print(f"Reason: {error}")

        time.sleep(1)

    print("\n=== ClinVar batch summary ===")
    print("Genes:", len(genes))
    print("Successful:", successful)
    print("Failed:", failed)


if __name__ == "__main__":
    main()