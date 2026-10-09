from fetch_ensembl_gene import create_session, ENSEMBL_BASE_URL


def fetch_ensembl_releases() -> list[int]:
    session = create_session()

    response = session.get(
        f"{ENSEMBL_BASE_URL}/info/data",
        headers={"Accept": "application/json"},
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()
    releases = data.get("releases", [])

    if not releases:
        raise ValueError("Ensembl did not return a data release")

    return releases


def main() -> None:
    releases = fetch_ensembl_releases()
    current_release = max(releases)

    print("Source: Ensembl")
    print("Available releases:", releases)
    print("Current release:", current_release)
    print("Source URL:", ENSEMBL_BASE_URL)


if __name__ == "__main__":
    main()