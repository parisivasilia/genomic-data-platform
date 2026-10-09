import argparse

from database import create_connection
from ingest_ensembl_gene import get_or_create_source_release
from prepare_ensembl_transcripts import prepare_transcript_records


def ensure_gene_exists(cursor, gene_id: str) -> None:
    cursor.execute(
        "SELECT gene_id FROM gene WHERE gene_id = %s",
        (gene_id,),
    )

    if cursor.fetchone() is None:
        raise ValueError(
            f"Gene {gene_id} does not exist in the database. "
            "Ingest the gene before its transcripts."
        )


def upsert_transcript(
        cursor,
        transcript: dict,
        source_release_id: int
) -> str:
    cursor.execute(
        """
        SELECT transcript_id
        FROM transcript
        WHERE transcript_id = %s
        """,
        (transcript["transcript_id"],),
    )

    existing = cursor.fetchone()

    values = (
        transcript["transcript_name"],
        transcript["transcript_type"],
        transcript["chromosome"],
        transcript["start_position"],
        transcript["end_position"],
        transcript["strand"],
        transcript["gene_id"],
        source_release_id,
    )

    if existing:
        cursor.execute(
            """
            UPDATE transcript
            SET transcript_name = %s,
                transcript_type = %s,
                chromosome = %s,
                start_position = %s,
                end_position = %s,
                strand = %s,
                gene_id = %s,
                source_release_id = %s
            WHERE transcript_id = %s
            """,
            values + (transcript["transcript_id"],),
        )

        return "updated"

    cursor.execute(
        """
        INSERT INTO transcript (
            transcript_id,
            transcript_name,
            transcript_type,
            chromosome,
            start_position,
            end_position,
            strand,
            gene_id,
            source_release_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (transcript["transcript_id"],) + values,
    )

    return "inserted"


def ingest_transcripts(gene_id: str) -> None:
    prepared = prepare_transcript_records(gene_id)

    connection = create_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        ensure_gene_exists(cursor, gene_id)

        source_release_id = get_or_create_source_release(
            cursor,
            prepared["source_release"],
        )

        inserted = 0
        updated = 0

        for transcript in prepared["transcripts"]:
            action = upsert_transcript(
                cursor,
                transcript,
                source_release_id,
            )

            if action == "inserted":
                inserted += 1
            else:
                updated += 1

        connection.commit()

        print("Transcript ingestion successful.")
        print("Gene ID:", gene_id)
        print("Source release ID:", source_release_id)
        print("Inserted:", inserted)
        print("Updated:", updated)
        print("Total:", inserted + updated)

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest Ensembl transcripts for a gene."
    )

    parser.add_argument(
        "gene_id",
        help="Ensembl gene ID, for example ENSG00000139618",
    )

    args = parser.parse_args()

    ingest_transcripts(args.gene_id)


if __name__ == "__main__":
    main()