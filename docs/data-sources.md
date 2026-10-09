# Data Sources and Methodology



## Reference Assembly



The current platform stores genomic coordinates using the **GRCh38** reference assembly.



Reference-assembly information is stored together with source provenance so that genomic records can be interpreted in the correct coordinate context.



## Ensembl



Ensembl is used as the primary source for gene and transcript information.



The ingestion pipeline retrieves gene records through the Ensembl REST API and normalizes fields including:



- Ensembl gene ID

- gene symbol

- gene description

- gene biotype

- chromosome

- start position

- end position

- strand



Transcript records include:



- Ensembl transcript ID

- transcript name

- transcript biotype

- chromosome

- genomic coordinates

- strand

- parent gene



The pipeline also uses Ensembl HGNC cross-reference data to retrieve known gene synonyms.



The Ensembl release number is retrieved dynamically and stored in the `source_release` table.



## NCBI ClinVar



NCBI ClinVar is used as the source of clinically interpreted genomic variants.



The pipeline uses NCBI E-utilities to search for and retrieve ClinVar records.



For the portfolio demonstration dataset, ClinVar retrieval is intentionally restricted to a controlled subset of **Pathogenic** and **Likely pathogenic** variants for each configured gene.



This keeps the demonstration dataset lightweight while preserving realistic clinical-variant integration.



Normalized ClinVar fields include:



- ClinVar Variation ID

- VCV accession

- dbSNP identifier when available

- chromosome

- GRCh38 genomic position

- reference allele

- alternate allele

- variant type

- classification type

- clinical significance

- review status

- evaluation date where available

- source provenance



ClinVar source update metadata are stored in the `source_release` table.



## Demonstration Gene Set



The default `genes.txt` file currently contains:



```text

BRCA1

BRCA2

TP53

EGFR

CFTR

APOE

```



These genes provide a compact demonstration dataset containing biologically and clinically well-characterized genomic records.



A full pipeline run processes all six genes together with their associated transcripts, synonyms, and ClinVar variants.



## Data Normalization



External API responses are converted into application-specific normalized structures before database persistence.



Normalization includes:



- stable biological identifiers

- genomic coordinates

- chromosome values

- strand values

- biological entity types

- variant identifiers

- clinical interpretation fields

- source metadata



This prevents source-specific response structures from being coupled directly to the database schema.



## Validation



Normalized records are validated before persistence.



Validation checks include examples such as:



- required stable identifiers

- required chromosome information

- valid genomic coordinates

- start position not exceeding end position

- required ClinVar identifiers

- expected normalized field structures



Records that fail validation are rejected before database insertion.



## Idempotent Ingestion



The ingestion process supports repeated execution.



Existing biological records are updated when appropriate rather than duplicated.



Uniqueness constraints are also used for relationships such as:



- gene synonyms

- gene–variant associations

- ClinVar Variation IDs



This allows the pipeline to be rerun safely against the same database.



## Provenance



The platform records source provenance through the `source_release` table.



Stored provenance includes:



- source name

- source version

- reference assembly

- source URL

- ingestion timestamp



Genes, transcripts, and variants reference their originating source-release records.



This makes the data traceable to the public biological source from which they were retrieved.



## External API Reliability



The ingestion layer includes retry handling for transient HTTP failures.



Retry logic is used for temporary conditions such as:



- HTTP 429 rate limiting

- HTTP 500 errors

- HTTP 502 errors

- HTTP 503 errors

- HTTP 504 errors



This reduces the chance that temporary public-API failures interrupt a complete ingestion run.



## Scope and Limitations



The platform is intentionally portfolio-scale.



The demonstration dataset is not intended to represent the complete contents of Ensembl or ClinVar.



The ClinVar subset is deliberately limited per gene to keep ingestion reproducible and manageable.



Clinical interpretation should always be considered together with:



- source release

- review status

- evaluation date

- interpretation criteria

- reference assembly



The application is not intended for clinical diagnosis or medical decision-making.


