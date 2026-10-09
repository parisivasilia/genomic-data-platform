package io.github.parisivasilia.genomicdata.entity;

import jakarta.persistence.EmbeddedId;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.MapsId;
import jakarta.persistence.Table;

@Entity
@Table(name = "gene_variant")
public class GeneVariant {

    @EmbeddedId
    private GeneVariantId id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @MapsId("geneId")
    @JoinColumn(name = "gene_id", nullable = false)
    private Gene gene;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @MapsId("variantId")
    @JoinColumn(name = "variant_id", nullable = false)
    private Variant variant;

    protected GeneVariant() {
    }

    public GeneVariant(Gene gene, Variant variant) {
        this.gene = gene;
        this.variant = variant;
        this.id = new GeneVariantId(gene.getId(), variant.getId());
    }

    public GeneVariantId getId() {
        return id;
    }

    public Gene getGene() {
        return gene;
    }

    public Variant getVariant() {
        return variant;
    }
}