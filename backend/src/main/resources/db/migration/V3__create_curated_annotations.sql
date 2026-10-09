CREATE TABLE curated_annotation (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    gene_id VARCHAR(32) NOT NULL,

    title VARCHAR(150) NOT NULL,

    annotation_text TEXT NOT NULL,

    category VARCHAR(100) NULL,

    created_by VARCHAR(100) NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_curated_annotation_gene
        FOREIGN KEY (gene_id)
        REFERENCES gene(gene_id)
        ON DELETE CASCADE,

    INDEX idx_curated_annotation_gene_id (gene_id)
);