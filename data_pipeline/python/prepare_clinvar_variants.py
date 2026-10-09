from fetch_clinvar_release import (
    fetch_clinvar_last_update,
)
from fetch_clinvar_variants import (
    fetch_clinvar_variants,
)
from normalize_clinvar_variants import (
    normalize_clinvar_variants,
)
from validate_clinvar_variants import (
    validate_clinvar_variants,
)


CLINVAR_SOURCE_URL = (
    "https://www.ncbi.nlm.nih.gov/clinvar/"
)


def prepare_clinvar_records(
        gene_symbol: str,
        retmax: int = 20
) -> dict:
    summaries = fetch_clinvar_variants(
        gene_symbol,
        retmax,
    )

    variants, skipped = (
        normalize_clinvar_variants(summaries)
    )

    if not variants:
        raise ValueError(
            f"No usable ClinVar variants for "
            f"{gene_symbol}"
        )

    validate_clinvar_variants(
        variants,
        gene_symbol,
    )

    last_update = fetch_clinvar_last_update()

    source_release = {
        "source_name": "ClinVar",
        "source_version": last_update,
        "reference_assembly": "GRCh38",
        "source_url": CLINVAR_SOURCE_URL,
    }

    return {
        "gene_symbol": gene_symbol,
        "source_release": source_release,
        "variants": variants,
        "skipped": skipped,
    }


def main() -> None:
    prepared = prepare_clinvar_records(
        "TP53",
        retmax=10,
    )

    print(
        "Gene:",
        prepared["gene_symbol"],
    )
    print(
        "ClinVar version:",
        prepared["source_release"][
            "source_version"
        ],
    )
    print(
        "Assembly:",
        prepared["source_release"][
            "reference_assembly"
        ],
    )
    print(
        "Prepared variants:",
        len(prepared["variants"]),
    )
    print(
        "Skipped:",
        len(prepared["skipped"]),
    )


if __name__ == "__main__":
    main()