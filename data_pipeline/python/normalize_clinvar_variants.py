from datetime import datetime

from fetch_clinvar_variants import fetch_clinvar_variants


def find_grch38_location(
        summary: dict
) -> tuple[dict, dict]:
    variation_sets = summary.get(
        "variation_set", []
    )

    for variation in variation_sets:
        locations = variation.get(
            "variation_loc", []
        )

        for location in locations:
            if (
                location.get("assembly_name")
                == "GRCh38"
            ):
                return variation, location

    raise ValueError(
        "No GRCh38 location available"
    )


def extract_rs_id(variation: dict):
    for xref in variation.get(
        "variation_xrefs", []
    ):
        if (
            xref.get("db_source", "").lower()
            == "dbsnp"
        ):
            db_id = str(xref.get("db_id"))

            if db_id.startswith("rs"):
                return db_id

            return f"rs{db_id}"

    return None


def extract_alleles(
        variation: dict,
        location: dict
) -> tuple[str | None, str | None]:
    reference = location.get("ref") or None
    alternate = location.get("alt") or None

    if reference or alternate:
        return reference, alternate

    spdi = variation.get("canonical_spdi", "")

    parts = spdi.split(":", 3)

    if len(parts) == 4:
        return (
            parts[2] or None,
            parts[3] or None,
        )

    return None, None


def extract_classification(
        summary: dict
) -> tuple[
    str | None,
    str | None,
    str | None,
    object
]:
    classification_sources = [
        (
            "germline",
            "germline_classification",
        ),
        (
            "oncogenicity",
            "oncogenicity_classification",
        ),
        (
            "clinical_impact",
            "clinical_impact_classification",
        ),
    ]

    for (
        classification_type,
        field_name,
    ) in classification_sources:

        classification = (
            summary.get(field_name) or {}
        )

        description = (
            classification.get("description")
        )

        if not description:
            continue

        last_evaluated = classification.get(
            "last_evaluated"
        )

        parsed_date = None

        if (
            last_evaluated
            and not last_evaluated.startswith("1/")
        ):
            try:
                parsed_date = datetime.strptime(
                    last_evaluated,
                    "%Y/%m/%d %H:%M",
                ).date()
            except ValueError:
                parsed_date = None

        return (
            classification_type,
            description,
            classification.get(
                "review_status"
            ),
            parsed_date,
        )

    return None, None, None, None


def normalize_clinvar_variant(
        summary: dict
) -> dict:
    variation, location = (
        find_grch38_location(summary)
    )

    reference, alternate = extract_alleles(
        variation,
        location,
    )

    (
        classification_type,
        clinical_significance,
        review_status,
        last_evaluated,
    ) = extract_classification(summary)

    genes = [
        gene.get("symbol")
        for gene in summary.get("genes", [])
        if gene.get("symbol")
    ]

    return {
        "clinvar_variation_id": int(
            summary["uid"]
        ),
        "clinvar_accession": (
            summary.get("accession_version")
        ),
        "rs_id": extract_rs_id(variation),
        "chromosome": location.get("chr"),
        "position": int(location["start"]),
        "reference_allele": reference,
        "alternate_allele": alternate,
        "variant_type": (
            variation.get("variant_type")
            or summary.get("obj_type")
        ),
        "classification_type": (
            classification_type
        ),
        "clinical_significance": (
            clinical_significance
        ),
        "review_status": review_status,
        "last_evaluated": last_evaluated,
        "reference_assembly": "GRCh38",
        "gene_symbols": genes,
    }


def normalize_clinvar_variants(
        summaries: list[dict]
) -> tuple[list[dict], list[str]]:
    normalized = []
    skipped = []

    for summary in summaries:
        try:
            normalized.append(
                normalize_clinvar_variant(summary)
            )

        except (ValueError, KeyError) as error:
            skipped.append(
                f"{summary.get('uid')}: {error}"
            )

    return normalized, skipped


def main() -> None:
    summaries = fetch_clinvar_variants(
        "TP53",
        retmax=10,
    )

    variants, skipped = (
        normalize_clinvar_variants(summaries)
    )

    print("Fetched:", len(summaries))
    print("Normalized:", len(variants))
    print("Skipped:", len(skipped))
    print()

    for variant in variants[:3]:
        for field, value in variant.items():
            print(f"{field}: {value}")

        print("---")


if __name__ == "__main__":
    main()