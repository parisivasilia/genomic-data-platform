import time
from pathlib import Path

from database import create_connection
from ingest_clinvar_variants import ingest_clinvar_variants
from ingest_ensembl_gene import ingest_gene
from ingest_ensembl_synonyms import ingest_synonyms
from ingest_ensembl_transcripts import ingest_transcripts


def read_gene_symbols() -> list[str]:
    input_file = Path(__file__).with_name(
        "genes.txt"
    )

    with input_file.open(
        "r",
        encoding="utf-8",
    ) as file:
        return [
            line.strip()
            for line in file
            if line.strip()
        ]


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
    symbols = read_gene_symbols()

    print("=== Gene ingestion ===")

    for symbol in symbols:
        print(f"\nProcessing gene: {symbol}")

        ingest_gene(
            "homo_sapiens",
            symbol,
        )

    genes = fetch_genes()

    print(
        "\n=== Transcript / ClinVar / "
        "synonym ingestion ==="
    )

    successful = 0
    failed = 0

    for gene_id, gene_symbol in genes:
        print(
            f"\n=== {gene_symbol} "
            f"({gene_id}) ==="
        )

        try:
            ingest_transcripts(gene_id)

            ingest_clinvar_variants(
                gene_symbol,
                retmax=10,
            )

            synonym_count = ingest_synonyms(
                gene_id,
                gene_symbol,
            )

            print(
                "New synonyms:",
                synonym_count,
            )

            successful += 1

        except Exception as error:
            failed += 1

            print(
                f"Pipeline failed for "
                f"{gene_symbol}: {error}"
            )

        time.sleep(1)

    print("\n=== Full pipeline summary ===")
    print("Genes:", len(genes))
    print("Successful:", successful)
    print("Failed:", failed)


if __name__ == "__main__":
    main()