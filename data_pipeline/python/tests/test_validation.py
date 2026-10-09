import unittest

from validate_gene import validate_gene
from validate_transcripts import validate_transcript
from validate_clinvar_variants import (
    validate_clinvar_variant,
)


class ValidationTests(unittest.TestCase):

    def test_valid_gene(self):
        gene = {
            "gene_id": "ENSG00000139618",
            "gene_symbol": "BRCA2",
            "gene_type": "protein_coding",
            "chromosome": "13",
            "start_position": 32315086,
            "end_position": 32400268,
            "strand": 1,
            "gc_content": None,
            "reference_assembly": "GRCh38",
        }

        validate_gene(gene)

    def test_gene_rejects_invalid_coordinates(self):
        gene = {
            "gene_id": "ENSG00000139618",
            "gene_symbol": "BRCA2",
            "gene_type": "protein_coding",
            "chromosome": "13",
            "start_position": 500,
            "end_position": 100,
            "strand": 1,
            "gc_content": None,
            "reference_assembly": "GRCh38",
        }

        with self.assertRaises(ValueError):
            validate_gene(gene)

    def test_valid_transcript(self):
        transcript = {
            "transcript_id": "ENST00000544455",
            "transcript_name": "BRCA2-206",
            "transcript_type": "protein_coding",
            "chromosome": "13",
            "start_position": 32315086,
            "end_position": 32400268,
            "strand": 1,
            "gene_id": "ENSG00000139618",
        }

        validate_transcript(transcript)

    def test_valid_clinvar_variant(self):
        variant = {
            "clinvar_variation_id": 12345,
            "clinvar_accession": "VCV000012345.1",
            "chromosome": "17",
            "position": 1000,
            "variant_type": "single nucleotide variant",
            "clinical_significance": "Pathogenic",
            "reference_assembly": "GRCh38",
            "gene_symbols": ["TP53"],
        }

        validate_clinvar_variant(
            variant,
            "TP53",
        )


if __name__ == "__main__":
    unittest.main()