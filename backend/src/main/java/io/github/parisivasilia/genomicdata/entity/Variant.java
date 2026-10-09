package io.github.parisivasilia.genomicdata.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

import java.time.LocalDate;

@Entity
@Table(name = "variant")
public class Variant {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "variant_id")
    private Long id;

    @Column(
            name = "clinvar_variation_id",
            nullable = false,
            unique = true
    )
    private Long clinvarVariationId;

    @Column(name = "clinvar_accession", length = 32)
    private String clinvarAccession;

    @Column(name = "rs_id", length = 32)
    private String rsId;

    @Column(name = "chromosome", length = 16)
    private String chromosome;

    @Column(name = "position")
    private Long position;

    @Column(
            name = "reference_allele",
            columnDefinition = "TEXT"
    )
    private String referenceAllele;

    @Column(
            name = "alternate_allele",
            columnDefinition = "TEXT"
    )
    private String alternateAllele;

    @Column(name = "variant_type", length = 100)
    private String variantType;

    @Column(name = "classification_type", length = 50)
    private String classificationType;

    @Column(
            name = "clinical_significance",
            length = 255
    )
    private String clinicalSignificance;

    @Column(name = "review_status", length = 255)
    private String reviewStatus;

    @Column(name = "last_evaluated")
    private LocalDate lastEvaluated;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(
            name = "source_release_id",
            nullable = false
    )
    private SourceRelease sourceRelease;

    protected Variant() {
    }

    public Long getId() {
        return id;
    }

    public Long getClinvarVariationId() {
        return clinvarVariationId;
    }

    public String getClinvarAccession() {
        return clinvarAccession;
    }

    public String getRsId() {
        return rsId;
    }

    public String getChromosome() {
        return chromosome;
    }

    public Long getPosition() {
        return position;
    }

    public String getReferenceAllele() {
        return referenceAllele;
    }

    public String getAlternateAllele() {
        return alternateAllele;
    }

    public String getVariantType() {
        return variantType;
    }

    public String getClassificationType() {
        return classificationType;
    }

    public String getClinicalSignificance() {
        return clinicalSignificance;
    }

    public String getReviewStatus() {
        return reviewStatus;
    }

    public LocalDate getLastEvaluated() {
        return lastEvaluated;
    }

    public SourceRelease getSourceRelease() {
        return sourceRelease;
    }
}