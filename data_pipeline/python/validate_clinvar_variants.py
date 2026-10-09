from fetch_clinvar_variants import fetch_clinvar_variants
from normalize_clinvar_variants import (
    normalize_clinvar_variants,
)


def validate_clinvar_variant(
        variant: dict,
        expected_gene_symbol: str
) -> None:
    if variant["clinvar_variation_id"] <= 0:
        raise ValueError(
            "ClinVar Variation ID must be positive"
        )

    accession = variant.get(
        "clinvar_accession"
    )

    if (
        not accession
        or not accession.startswith("VCV")
    ):
        raise ValueError(
            "Invalid ClinVar VCV accession"
        )

    if variant.get(
        "reference_assembly"
    ) != "GRCh38":
        raise ValueError(
            "Variant is not mapped to GRCh38"
        )

    if not variant.get("chromosome"):
        raise ValueError(
            "Missing chromosome"
        )

    if variant["position"] <= 0:
        raise ValueError(
            "Variant position must be positive"
        )

    if not variant.get("variant_type"):
        raise ValueError(
            "Missing variant type"
        )

    if not variant.get(
        "clinical_significance"
    ):
        raise ValueError(
            "Missing clinical significance"
        )

    if (
        expected_gene_symbol
        not in variant["gene_symbols"]
    ):
        raise ValueError(
            f"Variant is not associated with "
            f"{expected_gene_symbol}"
        )


def validate_clinvar_variants(
        variants: list[dict],
        expected_gene_symbol: str
) -> None:
    variation_ids = set()

    for variant in variants:
        validate_clinvar_variant(
            variant,
            expected_gene_symbol,
        )

        variation_id = variant[
            "clinvar_variation_id"
        ]

        if variation_id in variation_ids:
            raise ValueError(
                f"Duplicate ClinVar Variation ID: "
                f"{variation_id}"
            )

        variation_ids.add(variation_id)


def main() -> None:
    gene_symbol = "TP53"

    summaries = fetch_clinvar_variants(
        gene_symbol,
        retmax=10,
    )

    variants, skipped = (
        normalize_clinvar_variants(summaries)
    )

    validate_clinvar_variants(
        variants,
        gene_symbol,
    )

    print("ClinVar records are valid.")
    print("Gene:", gene_symbol)
    print("Fetched:", len(summaries))
    print("Validated:", len(variants))
    print("Skipped:", len(skipped))


if __name__ == "__main__":
    main()