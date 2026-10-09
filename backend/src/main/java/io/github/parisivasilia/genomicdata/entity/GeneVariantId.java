package io.github.parisivasilia.genomicdata.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;

import java.io.Serializable;
import java.util.Objects;

@Embeddable
public class GeneVariantId implements Serializable {

    @Column(name = "gene_id", length = 32)
    private String geneId;

    @Column(name = "variant_id")
    private Long variantId;

    protected GeneVariantId() {
    }

    public GeneVariantId(String geneId, Long variantId) {
        this.geneId = geneId;
        this.variantId = variantId;
    }

    public String getGeneId() {
        return geneId;
    }

    public Long getVariantId() {
        return variantId;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }

        if (!(o instanceof GeneVariantId that)) {
            return false;
        }

        return Objects.equals(geneId, that.geneId)
                && Objects.equals(variantId, that.variantId);
    }

    @Override
    public int hashCode() {
        return Objects.hash(geneId, variantId);
    }
}