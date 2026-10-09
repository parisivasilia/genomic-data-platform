package io.github.parisivasilia.genomicdata.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.time.LocalDateTime;

@Entity
@Table(name = "source_release")
public class SourceRelease {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "source_release_id")
    private Long id;

    @Column(name = "source_name", nullable = false, length = 50)
    private String sourceName;

    @Column(name = "source_version", nullable = false, length = 100)
    private String sourceVersion;

    @Column(name = "reference_assembly", nullable = false, length = 32)
    private String referenceAssembly;

    @Column(name = "source_url", length = 500)
    private String sourceUrl;

    @Column(name = "ingested_at", nullable = false, insertable = false, updatable = false)
    private LocalDateTime ingestedAt;

    protected SourceRelease() {
    }

    public SourceRelease(
            String sourceName,
            String sourceVersion,
            String referenceAssembly,
            String sourceUrl) {
        this.sourceName = sourceName;
        this.sourceVersion = sourceVersion;
        this.referenceAssembly = referenceAssembly;
        this.sourceUrl = sourceUrl;
    }

    public Long getId() {
        return id;
    }

    public String getSourceName() {
        return sourceName;
    }

    public String getSourceVersion() {
        return sourceVersion;
    }

    public String getReferenceAssembly() {
        return referenceAssembly;
    }

    public String getSourceUrl() {
        return sourceUrl;
    }

    public LocalDateTime getIngestedAt() {
        return ingestedAt;
    }
}