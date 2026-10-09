package io.github.parisivasilia.genomicdata.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.PrePersist;
import jakarta.persistence.PreUpdate;
import jakarta.persistence.Table;

import java.time.Instant;

@Entity
@Table(name = "curated_annotation")
public class CuratedAnnotation {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(
            name = "gene_id",
            nullable = false,
            length = 32
    )
    private String geneId;

    @Column(
            name = "title",
            nullable = false,
            length = 150
    )
    private String title;

    @Column(
            name = "annotation_text",
            nullable = false,
            columnDefinition = "TEXT"
    )
    private String annotationText;

    @Column(
            name = "category",
            length = 100
    )
    private String category;

    @Column(
            name = "created_by",
            nullable = false,
            length = 100
    )
    private String createdBy;

    @Column(
            name = "created_at",
            nullable = false,
            updatable = false
    )
    private Instant createdAt;

    @Column(
            name = "updated_at",
            nullable = false
    )
    private Instant updatedAt;

    protected CuratedAnnotation() {
    }

    public CuratedAnnotation(
            String geneId,
            String title,
            String annotationText,
            String category,
            String createdBy
    ) {
        this.geneId = geneId;
        this.title = title;
        this.annotationText = annotationText;
        this.category = category;
        this.createdBy = createdBy;
    }

    @PrePersist
    void onCreate() {
        Instant now = Instant.now();
        this.createdAt = now;
        this.updatedAt = now;
    }

    @PreUpdate
    void onUpdate() {
        this.updatedAt = Instant.now();
    }

    public void update(
            String title,
            String annotationText,
            String category
    ) {
        this.title = title;
        this.annotationText = annotationText;
        this.category = category;
    }

    public Long getId() {
        return id;
    }

    public String getGeneId() {
        return geneId;
    }

    public String getTitle() {
        return title;
    }

    public String getAnnotationText() {
        return annotationText;
    }

    public String getCategory() {
        return category;
    }

    public String getCreatedBy() {
        return createdBy;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public Instant getUpdatedAt() {
        return updatedAt;
    }
}