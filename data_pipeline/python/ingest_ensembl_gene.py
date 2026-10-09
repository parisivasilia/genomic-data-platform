import argparse

from database import create_connection
from prepare_ensembl_gene import prepare_gene_record


def get_or_create_source_release(cursor, source_release: dict) -> int:
    cursor.execute(
        """
        SELECT source_release_id
        FROM source_release
        WHERE source_name = %s
          AND source_version = %s
          AND reference_assembly = %s
        """,
        (
            source_release["source_name"],
            source_release["source_version"],
            source_release["reference_assembly"],
        ),
    )

    row = cursor.fetchone()

    if row:
        return row[0]

    cursor.execute(
        """
        INSERT INTO source_release (
            source_name,
            source_version,
            reference_assembly,
            source_url
        )
        VALUES (%s, %s, %s, %s)
        """,
        (
            source_release["source_name"],
            source_release["source_version"],
            source_release["reference_assembly"],
            source_release["source_url"],
        ),
    )

    return cursor.lastrowid


def upsert_gene(cursor, gene: dict, source_release_id: int) -> str:
    cursor.execute(
        "SELECT gene_id FROM gene WHERE gene_id = %s",
        (gene["gene_id"],),
    )

    existing_gene = cursor.fetchone()

    values = (
        gene["gene_symbol"],
        gene["description"],
        gene["gene_type"],
        gene["chromosome"],
        gene["start_position"],
        gene["end_position"],
        gene["strand"],
        gene["gc_content"],
        source_release_id,
    )

    if existing_gene:
        cursor.execute(
            """
            UPDATE gene
            SET gene_symbol = %s,
                description = %s,
                gene_type = %s,
                chromosome = %s,
                start_position = %s,
                end_position = %s,
                strand = %s,
                gc_content = %s,
                source_release_id = %s
            WHERE gene_id = %s
            """,
            values + (gene["gene_id"],),
        )

        return "updated"

    cursor.execute(
        """
        INSERT INTO gene (
            gene_id,
            gene_symbol,
            description,
            gene_type,
            chromosome,
            start_position,
            end_position,
            strand,
            gc_content,
            source_release_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (gene["gene_id"],) + values,
    )

    return "inserted"


def ingest_gene(species: str, symbol: str) -> None:
    record = prepare_gene_record(species, symbol)

    connection = create_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        source_release_id = get_or_create_source_release(
            cursor,
            record["source_release"],
        )

        action = upsert_gene(
            cursor,
            record["gene"],
            source_release_id,
        )

        connection.commit()

        print("Ingestion successful.")
        print("Gene:", record["gene"]["gene_id"])
        print("Symbol:", record["gene"]["gene_symbol"])
        print("Source release ID:", source_release_id)
        print("Action:", action)

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest a gene from Ensembl into genomic_platform."
    )

    parser.add_argument(
        "symbol",
        help="Gene symbol, for example BRCA2 or TP53",
    )

    parser.add_argument(
        "--species",
        default="homo_sapiens",
        help="Ensembl species name (default: homo_sapiens)",
    )

    args = parser.parse_args()

    ingest_gene(args.species, args.symbol)


if __name__ == "__main__":
    main()