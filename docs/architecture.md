# Architecture

## System Overview

The Genomic Data Platform combines reproducible public-data ingestion with a secure human-curation layer.

```text
                  PUBLIC DATA SOURCES
             +---------------------------+
             | Ensembl | NCBI ClinVar   |
             +------------+--------------+
                          |
                          v
             +---------------------------+
             | Python Data Pipeline      |
             |                           |
             | Fetch                     |
             | Normalize                 |
             | Validate                  |
             | Ingest                    |
             +------------+--------------+
                          |
                          v
             +---------------------------+
             | MySQL                     |
             |                           |
             | Source genomic data       |
             | Curated annotations       |
             | Provenance                |
             +------------+--------------+
                          |
                          v
             +---------------------------+
             | Spring Boot REST API      |
             |                           |
             | Public genomic API        |
             | JWT authentication        |
             | ROLE_ADMIN authorization  |
             +------------+--------------+
                          |
                          v
             +---------------------------+
             | Angular Frontend          |
             |                           |
             | Gene Explorer             |
             | Gene Detail               |
             | Admin Login               |
             | Curated Annotation Admin  |
             +---------------------------+
```

The central architectural rule is that imported biological records and human-curated application records are treated differently.

Imported Ensembl and ClinVar data are controlled by ingestion and migration workflows.

Curated annotations are application-owned records that may be created, updated, and deleted through authenticated administrative endpoints.

## Data Pipeline

The Python ingestion layer communicates with external biological data services and separates the workflow into four stages:

```text
Retrieval
   |
   v
Normalization
   |
   v
Validation
   |
   v
Persistence
```

This keeps source-specific API logic separate from database, backend, and presentation logic.

Network requests include retry handling for transient HTTP failures.

Database ingestion is designed to be idempotent, allowing the same source records to be processed repeatedly without creating duplicate biological entities.

## Provenance

The `source_release` table stores source metadata including:

- source name
- source version
- reference assembly
- source URL
- ingestion timestamp

Genes, transcripts, and variants reference source-release records.

This allows biological records to be interpreted together with the source and release from which they originated.

Human-curated annotations are intentionally separated from source provenance so that application-level curation cannot be confused with Ensembl or ClinVar content.

## Database Model

Core entities include:

```text
source_release
      |
      +---- gene
      |      |
      |      +---- gene_synonym
      |      |
      |      +---- transcript
      |      |
      |      +---- gene_variant ---- variant
      |
      +---- transcript
      |
      +---- variant


gene
 |
 +---- curated_annotation
```

Ensembl stable identifiers are used for gene and transcript identifiers.

ClinVar Variation IDs are preserved as unique identifiers for ClinVar records.

`curated_annotation` stores human-authored information associated with a gene.

The table contains:

```text
id
gene_id
title
annotation_text
category
created_by
created_at
updated_at
```

The schema is version-controlled through Flyway.

The curated annotation table is introduced through:

```text
V3__create_curated_annotations.sql
```

## Database Access Separation

Three database roles separate application responsibilities.

### `genomic_migrator`

Used by Flyway for schema creation and migration.

It receives the schema privileges required to apply versioned migrations.

### `genomic_ingest`

Used by the Python ingestion pipeline.

It has:

```text
SELECT
INSERT
UPDATE
```

permissions across the genomic application schema.

This account is responsible for imported source data.

### `genomic_api`

Used by the Spring Boot application.

It has schema-wide:

```text
SELECT
```

access.

It additionally receives:

```text
INSERT
UPDATE
DELETE
```

only on:

```text
genomic_platform.curated_annotation
```

This is a deliberate least-privilege boundary.

The API may maintain application-owned curated records while remaining unable to manually alter imported gene, transcript, synonym, variant, or source-release records.

## Backend Architecture

The Spring Boot backend follows a layered architecture:

```text
HTTP Request
     |
     v
Controller
     |
     v
Service
     |
     v
Repository
     |
     v
MySQL
```

Controllers expose versioned REST endpoints under:

```text
/api/v1
```

Services contain application-level logic.

Repositories encapsulate persistence operations.

DTOs define external API representations and prevent persistence entities from being exposed directly.

## Public API

Public endpoints provide read access to genomic information.

Examples include:

```text
GET /api/v1/genes
GET /api/v1/genes/{geneId}
GET /api/v1/genes/{geneId}/transcripts
GET /api/v1/genes/{geneId}/variants
GET /api/v1/genes/{geneId}/annotations
```

Curated annotations are publicly readable because they form part of the displayed gene knowledge layer.

Public clients cannot create, edit, or delete them.

## Authentication

Administrator authentication is exposed through:

```text
POST /api/v1/auth/login
```

The administrative account is configured through environment variables:

```text
ADMIN_USERNAME
ADMIN_PASSWORD
```

The configured password is encoded with BCrypt during backend initialization and is verified using Spring Security's password encoder.

No real administrator credentials are stored in the repository.

## JWT Security

Successful authentication returns a signed JSON Web Token.

JWT configuration is supplied through:

```text
JWT_SECRET
JWT_TTL_SECONDS
```

The default token lifetime is:

```text
3600 seconds
```

JWTs contain the administrator identity and an `ADMIN` role claim.

Spring Security converts this claim into:

```text
ROLE_ADMIN
```

The API is stateless.

```text
Login
  |
  v
Credential verification
  |
  v
Signed JWT
  |
  v
Authorization: Bearer <token>
  |
  v
Spring Security validation
  |
  v
ROLE_ADMIN
```

## Protected Administrative API

Administrative write operations are grouped under:

```text
/api/v1/admin/**
```

Spring Security requires:

```text
ROLE_ADMIN
```

for these endpoints.

The protected annotation API includes:

```text
POST   /api/v1/admin/genes/{geneId}/annotations
PUT    /api/v1/admin/annotations/{annotationId}
DELETE /api/v1/admin/annotations/{annotationId}
```

These operations affect only `curated_annotation`.

Imported Ensembl and ClinVar data remain outside the administrative CRUD workflow.

## Security Boundary

The architecture intentionally creates two data-management paths.

```text
             IMPORTED SOURCE DATA

Ensembl / ClinVar
       |
       v
Python ingestion
       |
       v
validation
       |
       v
MySQL genomic tables

No manual web CRUD


             CURATED APPLICATION DATA

Administrator
       |
       v
JWT authentication
       |
       v
ROLE_ADMIN
       |
       v
Protected REST API
       |
       v
curated_annotation
```

This prevents user-interface operations from silently changing externally sourced biological facts.

## Frontend Architecture

The Angular application is organized around core infrastructure and feature-specific views:

```text
core/
  auth/
    auth.service.ts
    admin.guard.ts

  models/

  services/
    genomic-api.service.ts


features/
  gene-explorer/
  gene-detail/
  admin-login/
  admin-annotations/
```

`GenomicApiService` centralizes communication with the Spring Boot REST API.

`AuthService` manages administrator login, JWT storage, authentication state, and sign-out.

`adminGuard` protects the administration route.

## Authentication Flow in Angular

The browser authentication flow is:

```text
Admin link
    |
    v
/admin
    |
    +---- valid JWT ----> Admin dashboard
    |
    +---- no valid JWT -> /admin/login
                            |
                            v
                         Login
                            |
                            v
                     JWT stored in
                     sessionStorage
                            |
                            v
                     Admin dashboard
```

The JWT is stored in `sessionStorage`, which keeps authentication scoped to the browser session.

Sign-out removes the token and returns the user to the public application.

The route guard is a user-interface convenience layer.

Actual authorization is enforced by Spring Security on the backend.

## Gene Explorer

The public Gene Explorer supports filtering by:

```text
symbol
chromosome
geneType
keyword
```

Keyword search also includes gene synonyms.

The explorer links directly to individual gene detail views.

## Gene Detail

The Gene Detail view presents:

- genomic metadata
- gene synonyms
- public curated annotations
- Ensembl transcripts
- ClinVar variants
- clinical-significance indicators
- source provenance

Curated annotations displayed here are retrieved from the public annotations endpoint.

## Administration Interface

The administration interface supports:

```text
Load curated annotations for a gene
Create annotation
Edit annotation
Delete annotation
Sign out
```

The administrator works with Ensembl gene IDs.

Loading annotations is a read operation.

If no curated annotations exist for the selected gene, the interface explicitly reports an empty result rather than creating data automatically.

Creating, updating, and deleting records requires a valid administrator JWT.

## Container Architecture

Docker Compose provides a reproducible environment containing:

```text
                 +-----------+
                 |   MySQL   |
                 +-----+-----+
                       |
               +-------+-------+
               |               |
               v               v
         +-----------+   +-----------+
         |  Backend  |   | Pipeline  |
         +-----+-----+   +-----------+
               |
               v
         +-----------+
         | Frontend  |
         |  Nginx    |
         +-----------+
```

The MySQL container remains internal to the Docker Compose network and does not publish its database port to the host.

The frontend Nginx container serves the Angular application and proxies `/api` requests to the backend container.

The Python pipeline runs as an optional Compose profile and connects directly to MySQL using the dedicated ingestion account.

Secrets and administrator credentials are supplied to containers from a local `.env` file.

The real `.env` file is excluded from source control.

## Database Migration Flow

On a fresh deployment:

```text
MySQL starts
     |
     v
Initialization script
creates database users
     |
     v
Health check passes
     |
     v
Spring Boot starts
     |
     v
Flyway applies migrations
     |
     v
Hibernate validates schema
     |
     v
REST API becomes available
```

Migration history includes the core genomic schema and the curated-annotation extension.

## Complete Data Flow

Imported biological data follow:

```text
Ensembl / ClinVar
       |
       v
Python retrieval
       |
       v
Normalization
       |
       v
Validation
       |
       v
MySQL persistence
       |
       v
Spring Boot public API
       |
       v
Angular genomic explorer
```

Human-curated data follow:

```text
Administrator
       |
       v
Angular Admin Login
       |
       v
JWT authentication
       |
       v
Protected Spring API
       |
       v
curated_annotation
       |
       v
Public Gene Detail display
```

## CI

GitHub Actions validates three independent components:

- Java backend tests
- Python pipeline tests
- Angular production build

This keeps each software layer independently testable while Docker Compose provides end-to-end local validation.

## Design Principles

The architecture emphasizes:

- separation of concerns
- biological data provenance
- reference-assembly awareness
- least-privilege database access
- separation of imported and curated data
- idempotent ingestion
- explicit schema migrations
- DTO-based API boundaries
- stateless authentication
- role-based authorization
- defense in depth
- reproducible deployment
- independently testable software layers
