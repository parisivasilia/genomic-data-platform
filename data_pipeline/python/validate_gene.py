from normalize_ensembl_gene import normalize_gene
from fetch_ensembl_gene import fetch_gene_by_symbol


def validate_gene(gene: dict) -> None:
    required_fields = [
        "gene_id",
        "gene_symbol",
        "gene_type",
        "chromosome",
        "start_position",
        "end_position",
        "strand",
        "reference_assembly",
    ]

    for field in required_fields:
        if gene.get(field) is None:
            raise ValueError(f"Missing required field: {field}")

    if not gene["gene_id"].startswith("ENSG"):
        raise ValueError("gene_id is not a valid Ensembl gene identifier")

    if gene["start_position"] <= 0:
        raise ValueError("start_position must be positive")

    if gene["end_position"] <= 0:
        raise ValueError("end_position must be positive")

    if gene["start_position"] > gene["end_position"]:
        raise ValueError("start_position cannot be greater than end_position")

    if gene["strand"] not in (-1, 1):
        raise ValueError("strand must be -1 or 1")

    gc_content = gene.get("gc_content")

    if gc_content is not None and not 0 <= gc_content <= 100:
        raise ValueError("gc_content must be between 0 and 100")


def main() -> None:
    raw_gene = fetch_gene_by_symbol("homo_sapiens", "BRCA2")
    gene = normalize_gene(raw_gene)

    validate_gene(gene)

    print("Gene record is valid.")
    print("Gene ID:", gene["gene_id"])
    print("Symbol:", gene["gene_symbol"])
    print("Assembly:", gene["reference_assembly"])


if __name__ == "__main__":
    main()