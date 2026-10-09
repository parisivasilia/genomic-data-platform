package io.github.parisivasilia.genomicdata.entity;

import jakarta.persistence.EmbeddedId;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.MapsId;
import jakarta.persistence.Table;

@Entity
@Table(name = "gene_synonym")
public class GeneSynonym {

    @EmbeddedId
    private GeneSynonymId id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @MapsId("geneId")
    @JoinColumn(name = "gene_id", nullable = false)
    private Gene gene;

    protected GeneSynonym() {
    }

    public GeneSynonym(Gene gene, String synonym) {
        this.gene = gene;
        this.id = new GeneSynonymId(gene.getId(), synonym);
    }

    public GeneSynonymId getId() {
        return id;
    }

    public Gene getGene() {
        return gene;
    }

    public String getSynonym() {
        return id.getSynonym();
    }
}