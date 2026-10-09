from fetch_ensembl_transcripts import fetch_transcripts_by_gene_id


def normalize_transcript(
        raw_transcript: dict,
        gene_id: str
) -> dict:
    return {
        "transcript_id": raw_transcript.get("id"),
        "transcript_name": raw_transcript.get("display_name"),
        "transcript_type": raw_transcript.get("biotype"),
        "chromosome": raw_transcript.get("seq_region_name"),
        "start_position": raw_transcript.get("start"),
        "end_position": raw_transcript.get("end"),
        "strand": raw_transcript.get("strand"),
        "gene_id": gene_id,
    }


def normalize_transcripts(
        raw_transcripts: list[dict],
        gene_id: str
) -> list[dict]:
    return [
        normalize_transcript(transcript, gene_id)
        for transcript in raw_transcripts
    ]


def main() -> None:
    gene_id = "ENSG00000139618"

    raw_transcripts = fetch_transcripts_by_gene_id(gene_id)

    transcripts = normalize_transcripts(
        raw_transcripts,
        gene_id,
    )

    print("Normalized transcript count:", len(transcripts))
    print()

    for transcript in transcripts[:5]:
        for field, value in transcript.items():
            print(f"{field}: {value}")

        print("---")


if __name__ == "__main__":
    main()