from fetch_ensembl_gene import ENSEMBL_BASE_URL
from fetch_ensembl_release import fetch_ensembl_releases
from fetch_ensembl_transcripts import fetch_gene_with_transcripts
from normalize_ensembl_transcripts import normalize_transcripts
from validate_transcripts import validate_transcripts


def prepare_transcript_records(gene_id: str) -> dict:
    raw_gene = fetch_gene_with_transcripts(gene_id)

    raw_transcripts = raw_gene.get("Transcript", [])

    if not raw_transcripts:
        raise ValueError(
            f"No transcripts returned for gene {gene_id}"
        )

    transcripts = normalize_transcripts(
        raw_transcripts,
        gene_id,
    )

    validate_transcripts(transcripts)

    releases = fetch_ensembl_releases()
    current_release = max(releases)

    source_release = {
        "source_name": "Ensembl",
        "source_version": str(current_release),
        "reference_assembly": raw_gene.get("assembly_name"),
        "source_url": ENSEMBL_BASE_URL,
    }

    return {
        "gene_id": gene_id,
        "source_release": source_release,
        "transcripts": transcripts,
    }


def main() -> None:
    prepared = prepare_transcript_records(
        "ENSG00000139618"
    )

    print("Gene ID:", prepared["gene_id"])
    print(
        "Source:",
        prepared["source_release"]["source_name"]
    )
    print(
        "Release:",
        prepared["source_release"]["source_version"]
    )
    print(
        "Assembly:",
        prepared["source_release"]["reference_assembly"]
    )
    print(
        "Prepared transcripts:",
        len(prepared["transcripts"])
    )


if __name__ == "__main__":
    main()