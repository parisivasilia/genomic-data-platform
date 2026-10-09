from fetch_ensembl_gene import ENSEMBL_BASE_URL, create_session


def fetch_gene_with_transcripts(gene_id: str) -> dict:
    session = create_session()

    response = session.get(
        f"{ENSEMBL_BASE_URL}/lookup/id/{gene_id}",
        params={"expand": 1},
        headers={"Accept": "application/json"},
        timeout=30,
    )

    response.raise_for_status()
    return response.json()


def fetch_transcripts_by_gene_id(gene_id: str) -> list[dict]:
    gene = fetch_gene_with_transcripts(gene_id)

    transcripts = gene.get("Transcript", [])

    if not transcripts:
        raise ValueError(
            f"No transcripts returned for gene {gene_id}"
        )

    return transcripts


def main() -> None:
    gene = fetch_gene_with_transcripts(
        "ENSG00000139618"
    )

    transcripts = gene.get("Transcript", [])

    print("Gene ID:", gene.get("id"))
    print("Assembly:", gene.get("assembly_name"))
    print("Transcript count:", len(transcripts))
    print()

    for transcript in transcripts[:5]:
        print("Transcript ID:", transcript.get("id"))
        print("Name:", transcript.get("display_name"))
        print("Biotype:", transcript.get("biotype"))
        print("Chromosome:", transcript.get("seq_region_name"))
        print("Start:", transcript.get("start"))
        print("End:", transcript.get("end"))
        print("Strand:", transcript.get("strand"))
        print("---")


if __name__ == "__main__":
    main()