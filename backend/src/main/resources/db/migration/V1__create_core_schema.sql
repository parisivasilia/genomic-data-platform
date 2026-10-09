CREATE TABLE source_release (
    source_release_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    source_name VARCHAR(50) NOT NULL,
    source_version VARCHAR(100) NOT NULL,
    reference_assembly VARCHAR(32) NOT NULL,
    source_url VARCHAR(500),
    ingested_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_source_release
        UNIQUE (source_name, source_version, reference_assembly)
);


CREATE TABLE gene (
    gene_id VARCHAR(32) PRIMARY KEY,
    gene_symbol VARCHAR(64),
    description TEXT,
    gene_type VARCHAR(64),
    chromosome VARCHAR(16),
    start_position BIGINT UNSIGNED,
    end_position BIGINT UNSIGNED,
    strand TINYINT,
    gc_content DECIMAL(5,2),
    source_release_id BIGINT NOT NULL,

    CONSTRAINT fk_gene_source_release
        FOREIGN KEY (source_release_id)
        REFERENCES source_release(source_release_id),

    CONSTRAINT chk_gene_coordinates
        CHECK (
            start_position IS NULL
            OR end_position IS NULL
            OR start_position <= end_position
        ),

    CONSTRAINT chk_gene_strand
        CHECK (strand IS NULL OR strand IN (-1, 1)),

    CONSTRAINT chk_gene_gc_content
        CHECK (
            gc_content IS NULL
            OR (gc_content >= 0 AND gc_content <= 100)
        )
);

CREATE INDEX idx_gene_symbol
    ON gene(gene_symbol);

CREATE INDEX idx_gene_chromosome
    ON gene(chromosome);

CREATE INDEX idx_gene_type
    ON gene(gene_type);


CREATE TABLE gene_synonym (
    gene_id VARCHAR(32) NOT NULL,
    synonym VARCHAR(128) NOT NULL,

    PRIMARY KEY (gene_id, synonym),

    CONSTRAINT fk_gene_synonym_gene
        FOREIGN KEY (gene_id)
        REFERENCES gene(gene_id)
        ON DELETE CASCADE
);


CREATE TABLE transcript (
    transcript_id VARCHAR(32) PRIMARY KEY,
    transcript_name VARCHAR(128),
    transcript_type VARCHAR(64),
    chromosome VARCHAR(16),
    start_position BIGINT UNSIGNED,
    end_position BIGINT UNSIGNED,
    strand TINYINT,
    gene_id VARCHAR(32) NOT NULL,
    source_release_id BIGINT NOT NULL,

    CONSTRAINT fk_transcript_gene
        FOREIGN KEY (gene_id)
        REFERENCES gene(gene_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_transcript_source_release
        FOREIGN KEY (source_release_id)
        REFERENCES source_release(source_release_id),

    CONSTRAINT chk_transcript_coordinates
        CHECK (
            start_position IS NULL
            OR end_position IS NULL
            OR start_position <= end_position
        ),

    CONSTRAINT chk_transcript_strand
        CHECK (strand IS NULL OR strand IN (-1, 1))
);

CREATE INDEX idx_transcript_gene
    ON transcript(gene_id);


CREATE TABLE variant (
    variant_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    clinvar_variation_id BIGINT NOT NULL,
    clinvar_accession VARCHAR(32),
    rs_id VARCHAR(32),
    chromosome VARCHAR(16),
    position BIGINT UNSIGNED,
    reference_allele TEXT,
    alternate_allele TEXT,
    variant_type VARCHAR(100),
    clinical_significance VARCHAR(255),
    review_status VARCHAR(255),
    last_evaluated DATE,
    source_release_id BIGINT NOT NULL,

    CONSTRAINT uq_variant_clinvar_variation
        UNIQUE (clinvar_variation_id),

    CONSTRAINT fk_variant_source_release
        FOREIGN KEY (source_release_id)
        REFERENCES source_release(source_release_id)
);

CREATE INDEX idx_variant_rs_id
    ON variant(rs_id);

CREATE INDEX idx_variant_location
    ON variant(chromosome, position);

CREATE INDEX idx_variant_clinical_significance
    ON variant(clinical_significance);


CREATE TABLE gene_variant (
    gene_id VARCHAR(32) NOT NULL,
    variant_id BIGINT NOT NULL,

    PRIMARY KEY (gene_id, variant_id),

    CONSTRAINT fk_gene_variant_gene
        FOREIGN KEY (gene_id)
        REFERENCES gene(gene_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_gene_variant_variant
        FOREIGN KEY (variant_id)
        REFERENCES variant(variant_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_gene_variant_variant
    ON gene_variant(variant_id);