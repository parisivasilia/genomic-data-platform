from fetch_clinvar_variants import (
    NCBI_EUTILS_BASE_URL,
    common_params,
    create_ncbi_session,
)


def fetch_clinvar_last_update() -> str:
    session = create_ncbi_session()

    params = common_params()
    params.update(
        {
            "db": "clinvar",
            "retmode": "json",
        }
    )

    response = session.get(
        f"{NCBI_EUTILS_BASE_URL}/einfo.fcgi",
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    dbinfo = (
        data.get("einforesult", {})
        .get("dbinfo", [])
    )

    if not dbinfo:
        raise ValueError(
            "NCBI EInfo returned no ClinVar metadata"
        )

    last_update = dbinfo[0].get("lastupdate")

    if not last_update:
        raise ValueError(
            "ClinVar LastUpdate metadata is missing"
        )

    return last_update


def main() -> None:
    print(
        "ClinVar LastUpdate:",
        fetch_clinvar_last_update(),
    )


if __name__ == "__main__":
    main()