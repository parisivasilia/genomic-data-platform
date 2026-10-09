import argparse
import os

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


NCBI_EUTILS_BASE_URL = (
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
)


def create_ncbi_session() -> requests.Session:
    retry_strategy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session = requests.Session()
    session.mount("https://", adapter)

    return session


def common_params() -> dict:
    params = {
        "tool": "genomic_data_platform",
    }

    api_key = os.getenv("NCBI_API_KEY")

    if api_key:
        params["api_key"] = api_key

    return params


def search_clinvar_ids(
        gene_symbol: str,
        retmax: int = 20
) -> list[str]:
    session = create_ncbi_session()

    query = (
        f'{gene_symbol}[gene] '
        'AND single_gene[prop] '
        'AND ('
        '"clinsig pathogenic"[Properties] '
        'OR '
        '"clinsig likely pathogenic"[Properties]'
        ')'
    )

    params = common_params()
    params.update(
        {
            "db": "clinvar",
            "term": query,
            "retmode": "json",
            "retmax": retmax,
        }
    )

    response = session.get(
        f"{NCBI_EUTILS_BASE_URL}/esearch.fcgi",
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    return data.get(
        "esearchresult", {}
    ).get(
        "idlist", []
    )


def fetch_clinvar_summaries(
        clinvar_ids: list[str]
) -> list[dict]:
    if not clinvar_ids:
        return []

    session = create_ncbi_session()

    params = common_params()
    params.update(
        {
            "db": "clinvar",
            "id": ",".join(clinvar_ids),
            "retmode": "json",
        }
    )

    response = session.get(
        f"{NCBI_EUTILS_BASE_URL}/esummary.fcgi",
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()
    result = data.get("result", {})
    uids = result.get("uids", [])

    return [
        result[uid]
        for uid in uids
        if uid in result
    ]


def fetch_clinvar_variants(
        gene_symbol: str,
        retmax: int = 20
) -> list[dict]:
    clinvar_ids = search_clinvar_ids(
        gene_symbol,
        retmax,
    )

    return fetch_clinvar_summaries(
        clinvar_ids
    )


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("gene_symbol")

    parser.add_argument(
        "--retmax",
        type=int,
        default=20,
    )

    args = parser.parse_args()

    variants = fetch_clinvar_variants(
        args.gene_symbol,
        args.retmax,
    )

    print("Gene:", args.gene_symbol)
    print("ClinVar records:", len(variants))

    if variants:
        first = variants[0]

        print("First Variation ID:", first.get("uid"))
        print(
            "First accession:",
            first.get("accession_version"),
        )
        print(
            "First variant type:",
            first.get("obj_type"),
        )


if __name__ == "__main__":
    main()