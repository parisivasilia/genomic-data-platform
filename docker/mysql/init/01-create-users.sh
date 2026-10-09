#!/bin/bash
set -e

mysql -uroot -p"${MYSQL_ROOT_PASSWORD}" <<EOSQL
CREATE USER IF NOT EXISTS 'genomic_api'@'%' IDENTIFIED BY '${API_PASSWORD}';
ALTER USER 'genomic_api'@'%' IDENTIFIED BY '${API_PASSWORD}';

GRANT SELECT
ON genomic_platform.*
TO 'genomic_api'@'%';

GRANT CREATE, INSERT, UPDATE, DELETE
ON genomic_platform.curated_annotation
TO 'genomic_api'@'%';

REVOKE CREATE
ON genomic_platform.curated_annotation
FROM 'genomic_api'@'%';


CREATE USER IF NOT EXISTS 'genomic_migrator'@'%' IDENTIFIED BY '${MIGRATOR_PASSWORD}';
ALTER USER 'genomic_migrator'@'%' IDENTIFIED BY '${MIGRATOR_PASSWORD}';

GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, REFERENCES, INDEX, ALTER
ON genomic_platform.*
TO 'genomic_migrator'@'%';


CREATE USER IF NOT EXISTS 'genomic_ingest'@'%' IDENTIFIED BY '${INGEST_PASSWORD}';
ALTER USER 'genomic_ingest'@'%' IDENTIFIED BY '${INGEST_PASSWORD}';

GRANT SELECT, INSERT, UPDATE
ON genomic_platform.*
TO 'genomic_ingest'@'%';


FLUSH PRIVILEGES;
EOSQL