from fetch_ensembl_transcripts import fetch_transcripts_by_gene_id
from normalize_ensembl_transcripts import normalize_transcripts


def validate_transcript(transcript: dict) -> None:
    required_fields = [
        "transcript_id",
        "transcript_type",
        "chromosome",
        "start_position",
        "end_position",
        "strand",
        "gene_id",
    ]

    for field in required_fields:
        if transcript.get(field) is None:
            raise ValueError(
                f"Missing required field: {field}"
            )

    if not transcript["transcript_id"].startswith("ENST"):
        raise ValueError(
            f"Invalid Ensembl transcript ID: "
            f"{transcript['transcript_id']}"
        )

    if not transcript["gene_id"].startswith("ENSG"):
        raise ValueError(
            f"Invalid Ensembl gene ID: "
            f"{transcript['gene_id']}"
        )

    if transcript["start_position"] <= 0:
        raise ValueError(
            "start_position must be positive"
        )

    if transcript["end_position"] <= 0:
        raise ValueError(
            "end_position must be positive"
        )

    if (
        transcript["start_position"]
        > transcript["end_position"]
    ):
        raise ValueError(
            "start_position cannot be greater than end_position"
        )

    if transcript["strand"] not in (-1, 1):
        raise ValueError(
            "strand must be -1 or 1"
        )


def validate_transcripts(
        transcripts: list[dict]
) -> None:
    transcript_ids = set()

    for transcript in transcripts:
        validate_transcript(transcript)

        transcript_id = transcript["transcript_id"]

        if transcript_id in transcript_ids:
            raise ValueError(
                f"Duplicate transcript ID: {transcript_id}"
            )

        transcript_ids.add(transcript_id)


def main() -> None:
    gene_id = "ENSG00000139618"

    raw_transcripts = fetch_transcripts_by_gene_id(
        gene_id
    )

    transcripts = normalize_transcripts(
        raw_transcripts,
        gene_id,
    )

    validate_transcripts(transcripts)

    print("Transcript records are valid.")
    print("Gene ID:", gene_id)
    print("Validated transcripts:", len(transcripts))


if __name__ == "__main__":
    main()