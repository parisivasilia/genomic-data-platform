import argparse

from database import create_connection
from ingest_ensembl_gene import (
    get_or_create_source_release,
)
from prepare_clinvar_variants import (
    prepare_clinvar_records,
)


def find_gene_id(
        cursor,
        gene_symbol: str
) -> str:
    cursor.execute(
        """
        SELECT gene_id
        FROM gene
        WHERE UPPER(gene_symbol) = UPPER(%s)
        """,
        (gene_symbol,),
    )

    row = cursor.fetchone()

    if row is None:
        raise ValueError(
            f"Gene {gene_symbol} does not exist "
            "in the database"
        )

    return row[0]


def upsert_variant(
        cursor,
        variant: dict,
        source_release_id: int
) -> tuple[int, str]:
    cursor.execute(
        """
        SELECT variant_id
        FROM variant
        WHERE clinvar_variation_id = %s
        """,
        (
            variant["clinvar_variation_id"],
        ),
    )

    existing = cursor.fetchone()

    values = (
        variant["clinvar_accession"],
        variant["rs_id"],
        variant["chromosome"],
        variant["position"],
        variant["reference_allele"],
        variant["alternate_allele"],
        variant["variant_type"],
        variant["classification_type"],
        variant["clinical_significance"],
        variant["review_status"],
        variant["last_evaluated"],
        source_release_id,
    )

    if existing:
        variant_id = existing[0]

        cursor.execute(
            """
            UPDATE variant
            SET clinvar_accession = %s,
                rs_id = %s,
                chromosome = %s,
                position = %s,
                reference_allele = %s,
                alternate_allele = %s,
                variant_type = %s,
                classification_type = %s,
                clinical_significance = %s,
                review_status = %s,
                last_evaluated = %s,
                source_release_id = %s
            WHERE variant_id = %s
            """,
            values + (variant_id,),
        )

        return variant_id, "updated"

    cursor.execute(
        """
        INSERT INTO variant (
            clinvar_variation_id,
            clinvar_accession,
            rs_id,
            chromosome,
            position,
            reference_allele,
            alternate_allele,
            variant_type,
            classification_type,
            clinical_significance,
            review_status,
            last_evaluated,
            source_release_id
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s
        )
        """,
        (
            variant["clinvar_variation_id"],
        ) + values,
    )

    return cursor.lastrowid, "inserted"


def ensure_gene_variant_link(
        cursor,
        gene_id: str,
        variant_id: int
) -> bool:
    cursor.execute(
        """
        SELECT 1
        FROM gene_variant
        WHERE gene_id = %s
          AND variant_id = %s
        """,
        (gene_id, variant_id),
    )

    if cursor.fetchone():
        return False

    cursor.execute(
        """
        INSERT INTO gene_variant (
            gene_id,
            variant_id
        )
        VALUES (%s, %s)
        """,
        (gene_id, variant_id),
    )

    return True


def ingest_clinvar_variants(
        gene_symbol: str,
        retmax: int = 20
) -> None:
    prepared = prepare_clinvar_records(
        gene_symbol,
        retmax,
    )

    connection = create_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        gene_id = find_gene_id(
            cursor,
            gene_symbol,
        )

        source_release_id = (
            get_or_create_source_release(
                cursor,
                prepared["source_release"],
            )
        )

        inserted = 0
        updated = 0
        links_created = 0

        for variant in prepared["variants"]:
            variant_id, action = upsert_variant(
                cursor,
                variant,
                source_release_id,
            )

            if action == "inserted":
                inserted += 1
            else:
                updated += 1

            if ensure_gene_variant_link(
                cursor,
                gene_id,
                variant_id,
            ):
                links_created += 1

        connection.commit()

        print("ClinVar ingestion successful.")
        print("Gene:", gene_symbol)
        print("Gene ID:", gene_id)
        print(
            "Source release ID:",
            source_release_id,
        )
        print("Inserted:", inserted)
        print("Updated:", updated)
        print(
            "Gene-variant links created:",
            links_created,
        )
        print(
            "Skipped during normalization:",
            len(prepared["skipped"]),
        )
        print(
            "Total processed:",
            inserted + updated,
        )

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Ingest ClinVar variants for a gene."
        )
    )

    parser.add_argument("gene_symbol")

    parser.add_argument(
        "--retmax",
        type=int,
        default=20,
    )

    args = parser.parse_args()

    ingest_clinvar_variants(
        args.gene_symbol,
        args.retmax,
    )


if __name__ == "__main__":
    main()