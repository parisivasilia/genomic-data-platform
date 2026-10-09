import argparse
from pathlib import Path

from ingest_ensembl_gene import ingest_gene


def read_gene_symbols(file_path: Path) -> list[str]:
    symbols = []

    with file_path.open("r", encoding="utf-8") as file:
        for line in file:
            symbol = line.strip()

            if symbol:
                symbols.append(symbol)

    return symbols


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Batch ingest gene symbols from Ensembl."
    )

    parser.add_argument(
        "input_file",
        help="Text file containing one gene symbol per line.",
    )

    parser.add_argument(
        "--species",
        default="homo_sapiens",
        help="Ensembl species name (default: homo_sapiens)",
    )

    args = parser.parse_args()

    input_path = Path(args.input_file)

    if not input_path.is_file():
        raise FileNotFoundError(
            f"Input file does not exist: {input_path}"
        )

    symbols = read_gene_symbols(input_path)

    if not symbols:
        raise ValueError("Input file contains no gene symbols")

    successful = 0
    failed = 0

    for symbol in symbols:
        print(f"\n--- Processing {symbol} ---")

        try:
            ingest_gene(args.species, symbol)
            successful += 1

        except Exception as error:
            failed += 1
            print(f"Failed: {symbol}")
            print(f"Reason: {error}")

    print("\n=== Batch summary ===")
    print("Total:", len(symbols))
    print("Successful:", successful)
    print("Failed:", failed)


if __name__ == "__main__":
    main()