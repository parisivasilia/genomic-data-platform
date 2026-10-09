# Genomic Data Platform

A full-stack bioinformatics platform for ingesting, normalizing, storing, exploring, and serving genomic data from public biological data sources, with secure administrative support for human-curated annotations.

The project integrates gene and transcript information from **Ensembl** with clinically interpreted variants from **NCBI ClinVar**. Public-source data are processed through a Python ingestion pipeline, stored in a normalized MySQL database, exposed through a Spring Boot REST API, and explored through an Angular web application.

A separate authenticated administration workflow allows authorized users to create, edit, and delete **curated annotations** without modifying imported Ensembl or ClinVar records.

## Overview

The platform implements an end-to-end genomic data workflow:

```text
Ensembl + NCBI ClinVar
          |
          v
 Python Data Pipeline
          |
          v
Normalization + Validation
          |
          v
        MySQL
          |
          v
 Spring Boot REST API
      /           \
     v             v
Public Genomic   Secure Admin
   Explorer      Operations
```

The project emphasizes reproducibility, biological data provenance, genome assembly awareness, least-privilege access control, authentication and authorization, and separation between externally sourced genomic records and human-curated knowledge.

## Features

- Gene ingestion from Ensembl
- Transcript ingestion from Ensembl
- Gene synonym retrieval through Ensembl/HGNC cross-references
- ClinVar variant ingestion through NCBI E-utilities
- GRCh38-aware genomic records
- Source release and provenance tracking
- Data normalization and validation
- Idempotent ingestion workflows
- Relational MySQL genomic schema
- Flyway database migrations
- Least-privilege database roles
- Paginated and filterable REST API
- Gene search by symbol, chromosome, gene type, and keyword
- Synonym-aware gene search
- Gene detail pages
- Transcript exploration
- ClinVar variant exploration
- Clinical-significance visual indicators
- Public curated-annotation display
- Administrator login
- JWT-based stateless authentication
- Role-based authorization with `ROLE_ADMIN`
- Protected curated-annotation create, update, and delete operations
- Angular route protection for administrative views
- OpenAPI / Swagger documentation
- Dockerized backend, frontend, database, and ingestion pipeline
- Automated backend, pipeline, and frontend validation
- GitHub Actions continuous integration

## Technology Stack

### Data Pipeline

- Python 3.13
- Requests
- MySQL Connector/Python
- Ensembl REST API
- NCBI E-utilities
- ClinVar

### Backend

- Java 21
- Spring Boot
- Spring Data JPA
- Hibernate
- Spring Security
- OAuth2 Resource Server JWT support
- BCrypt password encoding
- Flyway
- Bean Validation
- springdoc OpenAPI

### Database

- MySQL 8
- Flyway-managed schema
- Separate migration, ingestion, and application database roles
- Table-scoped write permissions for curated annotations

### Frontend

- Angular
- TypeScript
- SCSS
- Angular route guards
- Session-scoped JWT storage
- Nginx

### Reproducibility

- Docker
- Docker Compose
- GitHub Actions

## Architecture

The platform separates imported biological source data from human-curated information.

```text
                     PUBLIC DATA SOURCES
                  Ensembl + NCBI ClinVar
                           |
                           v
                  Python Data Pipeline
                           |
                 Fetch / Normalize /
                 Validate / Ingest
                           |
                           v
                         MySQL
                    /             \
                   /               \
       Imported genomic data   Curated annotations
            read-only          controlled writes
                   \               /
                    \             /
                     Spring Boot API
                     /           \
                    /             \
          Public endpoints     JWT-protected
                              admin endpoints
                    \             /
                     \           /
                       Angular UI
```

### Python Data Pipeline

The ingestion workflow separates:

```text
Fetch
  |
Normalize
  |
Validate
  |
Ingest
```

Network requests include retry handling for transient API failures.

Ingestion is designed to be idempotent so repeated runs update existing source records instead of creating duplicate biological entities.

### MySQL Database

Core schema entities include:

```text
source_release
gene
gene_synonym
transcript
variant
gene_variant
curated_annotation
```

Source metadata are stored alongside biological records to preserve provenance.

The `curated_annotation` table is deliberately separate from imported genomic records. This allows authenticated users to maintain human-curated knowledge without altering Ensembl or ClinVar source data.

### Spring Boot REST API

The backend follows a layered architecture:

```text
Controller
    |
Service
    |
Repository
    |
MySQL
```

DTOs define external API contracts rather than exposing persistence entities directly.

Public genomic endpoints are accessible without authentication.

Administrative write endpoints under:

```text
/api/v1/admin/**
```

require a valid JWT containing `ROLE_ADMIN`.

Authentication is stateless. Successful administrator login returns a signed JWT with a default lifetime of one hour.

### Angular Web Application

The frontend provides:

- Gene Explorer
- gene filtering and search
- gene detail pages
- synonym display
- Ensembl transcript tables
- ClinVar variant tables
- clinical-significance badges
- provenance information
- public curated-annotation display
- administrator login
- protected administration route
- curated annotation create, edit, and delete interface
- explicit sign-out

The administrator token is stored in browser `sessionStorage` and is removed on sign-out.

## Data Sources

### Ensembl

Ensembl provides:

- stable gene identifiers
- gene symbols
- gene descriptions
- genomic coordinates
- strand information
- gene biotypes
- transcript records
- HGNC-associated gene synonyms

The pipeline retrieves the Ensembl release dynamically and stores it as provenance.

### NCBI ClinVar

ClinVar provides clinically interpreted genomic variants.

For the demonstration dataset, the ingestion pipeline retrieves a controlled subset of **Pathogenic** and **Likely pathogenic** variants for each configured gene.

Normalized fields include:

- ClinVar Variation ID
- VCV accession
- dbSNP identifier when available
- GRCh38 genomic position
- reference and alternate alleles
- variant type
- classification type
- clinical significance
- review status
- provenance metadata

Imported Ensembl and ClinVar records are not manually editable through the web interface.

## Demonstration Dataset

The default gene set contains:

```text
BRCA1
BRCA2
TP53
EGFR
CFTR
APOE
```

A complete pipeline run processes all six genes together with their associated transcripts, synonyms, and ClinVar records.

For example, the current Ensembl dataset resolves **BRCA2 to 19 transcript records**.

## REST API

### Public genomic endpoints

```text
GET /api/v1/genes
GET /api/v1/genes/{geneId}

GET /api/v1/genes/{geneId}/transcripts
GET /api/v1/transcripts/{transcriptId}

GET /api/v1/genes/{geneId}/variants
GET /api/v1/variants/{clinvarVariationId}

GET /api/v1/genes/{geneId}/annotations
```

Gene searches support optional filters including:

```text
symbol
chromosome
geneType
keyword
```

Keyword search can also resolve gene synonyms.

### Authentication

```text
POST /api/v1/auth/login
```

A successful login returns a bearer JWT.

Administrator credentials and the JWT signing secret are supplied through environment variables and are not stored in source control.

### Protected administrative endpoints

```text
POST   /api/v1/admin/genes/{geneId}/annotations
PUT    /api/v1/admin/annotations/{annotationId}
DELETE /api/v1/admin/annotations/{annotationId}
```

These endpoints require `ROLE_ADMIN`.

The protected API modifies only human-curated annotations. Imported biological source records remain controlled by the ingestion and migration workflows.

### OpenAPI

When the backend is running:

```text
http://localhost:8080/swagger-ui.html
```

## Run with Docker

### Requirements

- Docker Desktop
- Docker Compose

Create a local `.env` file based on `.env.example`.

Required variables:

```text
MYSQL_ROOT_PASSWORD
API_PASSWORD
MIGRATOR_PASSWORD
INGEST_PASSWORD

ADMIN_USERNAME
ADMIN_PASSWORD
JWT_SECRET
JWT_TTL_SECONDS
```

`JWT_SECRET` should contain a strong random secret of at least 32 bytes.

`JWT_TTL_SECONDS` defaults to:

```text
3600
```

Start the database, backend, and frontend:

```bash
docker compose up -d db backend frontend
```

Services are then available at:

```text
Frontend:
http://localhost:4200

Backend:
http://localhost:8080

Swagger UI:
http://localhost:8080/swagger-ui.html
```

The application database is internal to the Docker Compose network and does not expose MySQL to the host.

## Run the Genomic Ingestion Pipeline

After the application stack is running:

```bash
docker compose --profile tools run --rm pipeline
```

The default pipeline performs:

```text
Gene ingestion
      |
Transcript ingestion
      |
ClinVar ingestion
      |
Gene synonym ingestion
```

A successful demonstration run reports:

```text
Genes: 6
Successful: 6
Failed: 0
```

## Database Roles

The project separates database responsibilities using least-privilege accounts.

### `genomic_migrator`

Used by Flyway for schema creation and migrations.

It has the schema privileges required to apply versioned database changes.

### `genomic_ingest`

Used by the Python pipeline.

It can read, insert, and update imported genomic data.

### `genomic_api`

Used by the Spring Boot application.

It has:

```text
SELECT
```

access across the application schema, plus narrowly scoped:

```text
INSERT
UPDATE
DELETE
```

permissions on:

```text
curated_annotation
```

This allows authenticated administrative curation while preventing the API layer from manually modifying imported Ensembl or ClinVar records.

## Security Model

The platform intentionally distinguishes between **source genomic data** and **curated application data**.

```text
Ensembl / ClinVar records
        |
        | modified only by
        v
 ingestion / migration workflows


Curated annotations
        |
        | modified only by
        v
 authenticated ROLE_ADMIN endpoints
```

Administrator authentication uses a single portfolio-scale administrative account configured through environment variables.

Passwords are verified through BCrypt.

JWTs are signed with an environment-provided HMAC secret and are validated by Spring Security.

The backend is stateless and does not maintain server-side login sessions.

## Testing and Validation

The project has been validated through:

- Spring Boot automated tests
- Spring Security-enabled application tests
- Python validation tests
- Angular production builds
- independent Docker image builds
- clean Docker Compose deployment
- Flyway migrations against MySQL
- full Ensembl and ClinVar ingestion
- REST API verification
- administrator login verification
- JWT-protected create, update, and delete verification
- public curated-annotation retrieval
- Angular administrator workflow verification
- frontend verification against the Dockerized backend

### Backend Tests

From `backend`:

```bash
./mvnw test
```

On Windows:

```powershell
.\mvnw.cmd test
```

### Python Pipeline Tests

From `data_pipeline/python`:

```bash
python -m unittest discover -s tests -v
```

### Frontend Build

From `frontend`:

```bash
npm ci
npm run build
```

On Windows PowerShell environments that restrict `npm.ps1`:

```powershell
npm.cmd run build
```

## Project Structure

```text
genomic-data-platform/
|
|-- backend/
|   |-- src/
|   |   |-- main/
|   |   |   |-- java/
|   |   |   `-- resources/db/migration/
|   |   `-- test/
|   |-- Dockerfile
|   `-- pom.xml
|
|-- frontend/
|   |-- src/app/
|   |   |-- core/
|   |   |   |-- auth/
|   |   |   |-- models/
|   |   |   `-- services/
|   |   `-- features/
|   |       |-- gene-explorer/
|   |       |-- gene-detail/
|   |       |-- admin-login/
|   |       `-- admin-annotations/
|   |-- public/
|   |-- Dockerfile
|   `-- nginx.conf
|
|-- data_pipeline/
|   `-- python/
|       |-- tests/
|       |-- genes.txt
|       |-- run_full_pipeline.py
|       `-- Dockerfile
|
|-- docker/
|   `-- mysql/
|       `-- init/
|
|-- docs/
|
|-- .github/
|   `-- workflows/
|       `-- ci.yml
|
|-- docker-compose.yml
|-- .env.example
|-- .gitignore
`-- README.md
```

## Design Principles

The project emphasizes:

- biological data provenance
- reproducibility
- genome assembly awareness
- idempotent ingestion
- validation before persistence
- least-privilege database access
- separation of imported and curated data
- authentication and role-based authorization
- stateless API security
- separation of concerns
- transparent REST interfaces
- reproducible containerized deployment
- independently testable components

## Scope

This project is a portfolio-scale genomic data platform designed to demonstrate bioinformatics data engineering, backend architecture, database design, full-stack development, security, and reproducible software delivery.

The project originated from a university team-project concept. The current repository is an independent redesign and reimplementation, including a new genomic data-ingestion pipeline, revised database architecture, layered REST API, secure administration workflow, new Angular frontend, containerization, automated testing, and CI workflow.

The application is intended for educational and portfolio demonstration purposes.

It is **not intended for clinical diagnosis or medical decision-making**.

## Author

**Vasiliki Parisi**

MSc Bioinformatics – Computational Biology

GitHub: `parisivasilia`

LinkedIn:  
https://www.linkedin.com/in/vasilia-parisi-416333226/
