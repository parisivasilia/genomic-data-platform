from database import create_connection
from fetch_ensembl_gene import (
    ENSEMBL_BASE_URL,
    create_session,
)


def fetch_hgnc_synonyms(gene_id: str) -> list[str]:
    session = create_session()

    response = session.get(
        f"{ENSEMBL_BASE_URL}/xrefs/id/{gene_id}",
        params={
            "external_db": "HGNC",
            "object_type": "gene",
        },
        headers={"Accept": "application/json"},
        timeout=30,
    )

    response.raise_for_status()

    xrefs = response.json()
    synonyms = set()

    for xref in xrefs:
        for synonym in xref.get("synonyms", []):
            cleaned = synonym.strip()

            if cleaned:
                synonyms.add(cleaned)

    return sorted(synonyms)


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


def ingest_synonyms(
        gene_id: str,
        gene_symbol: str
) -> int:
    synonyms = fetch_hgnc_synonyms(gene_id)

    synonyms = [
        synonym
        for synonym in synonyms
        if synonym.upper() != gene_symbol.upper()
        and len(synonym) <= 128
    ]

    connection = create_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        inserted = 0

        for synonym in synonyms:
            cursor.execute(
                """
                INSERT IGNORE INTO gene_synonym (
                    gene_id,
                    synonym
                )
                VALUES (%s, %s)
                """,
                (gene_id, synonym),
            )

            inserted += cursor.rowcount

        connection.commit()

        return inserted

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


def main() -> None:
    genes = fetch_genes()

    total_inserted = 0
    failed = 0

    for gene_id, gene_symbol in genes:
        print(
            f"\n=== {gene_symbol} "
            f"({gene_id}) ==="
        )

        try:
            inserted = ingest_synonyms(
                gene_id,
                gene_symbol,
            )

            total_inserted += inserted
            print("New synonyms inserted:", inserted)

        except Exception as error:
            failed += 1
            print("Failed:", error)

    print("\n=== Synonym ingestion summary ===")
    print("Genes:", len(genes))
    print("New synonyms:", total_inserted)
    print("Failed:", failed)


if __name__ == "__main__":
    main()