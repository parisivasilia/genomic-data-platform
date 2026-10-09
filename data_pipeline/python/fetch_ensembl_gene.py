import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


ENSEMBL_BASE_URL = "https://rest.ensembl.org"


def create_session() -> requests.Session:
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


def fetch_gene_by_symbol(species: str, symbol: str) -> dict:
    url = f"{ENSEMBL_BASE_URL}/lookup/symbol/{species}/{symbol}"

    session = create_session()

    response = session.get(
        url,
        headers={"Accept": "application/json"},
        timeout=30,
    )

    response.raise_for_status()
    return response.json()


def main() -> None:
    gene = fetch_gene_by_symbol("homo_sapiens", "BRCA2")

    print("Ensembl ID:", gene.get("id"))
    print("Symbol:", gene.get("display_name"))
    print("Biotype:", gene.get("biotype"))
    print("Chromosome:", gene.get("seq_region_name"))
    print("Start:", gene.get("start"))
    print("End:", gene.get("end"))
    print("Strand:", gene.get("strand"))
    print("Assembly:", gene.get("assembly_name"))
    print("Description:", gene.get("description"))


if __name__ == "__main__":
    main()