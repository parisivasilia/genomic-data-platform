import json

from fetch_ensembl_gene import ENSEMBL_BASE_URL, fetch_gene_by_symbol
from fetch_ensembl_release import fetch_ensembl_releases
from normalize_ensembl_gene import normalize_gene
from validate_gene import validate_gene


def prepare_gene_record(species: str, symbol: str) -> dict:
    raw_gene = fetch_gene_by_symbol(species, symbol)
    gene = normalize_gene(raw_gene)

    validate_gene(gene)

    releases = fetch_ensembl_releases()
    current_release = max(releases)

    source_release = {
        "source_name": "Ensembl",
        "source_version": str(current_release),
        "reference_assembly": gene["reference_assembly"],
        "source_url": ENSEMBL_BASE_URL,
    }

    gene_record = {
        "gene_id": gene["gene_id"],
        "gene_symbol": gene["gene_symbol"],
        "description": gene["description"],
        "gene_type": gene["gene_type"],
        "chromosome": gene["chromosome"],
        "start_position": gene["start_position"],
        "end_position": gene["end_position"],
        "strand": gene["strand"],
        "gc_content": gene["gc_content"],
    }

    return {
        "source_release": source_release,
        "gene": gene_record,
    }


def main() -> None:
    record = prepare_gene_record("homo_sapiens", "BRCA2")

    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()