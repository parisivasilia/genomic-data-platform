from fetch_ensembl_gene import fetch_gene_by_symbol


def normalize_gene(raw_gene: dict) -> dict:
    return {
        "gene_id": raw_gene.get("id"),
        "gene_symbol": raw_gene.get("display_name"),
        "description": raw_gene.get("description"),
        "gene_type": raw_gene.get("biotype"),
        "chromosome": raw_gene.get("seq_region_name"),
        "start_position": raw_gene.get("start"),
        "end_position": raw_gene.get("end"),
        "strand": raw_gene.get("strand"),
        "gc_content": None,
        "reference_assembly": raw_gene.get("assembly_name"),
    }


def main() -> None:
    raw_gene = fetch_gene_by_symbol("homo_sapiens", "BRCA2")
    normalized_gene = normalize_gene(raw_gene)

    for field, value in normalized_gene.items():
        print(f"{field}: {value}")


if __name__ == "__main__":
    main()