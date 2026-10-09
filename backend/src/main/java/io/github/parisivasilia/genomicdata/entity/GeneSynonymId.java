package io.github.parisivasilia.genomicdata.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;

import java.io.Serializable;
import java.util.Objects;

@Embeddable
public class GeneSynonymId implements Serializable {

    @Column(name = "gene_id", length = 32)
    private String geneId;

    @Column(name = "synonym", length = 128)
    private String synonym;

    protected GeneSynonymId() {
    }

    public GeneSynonymId(String geneId, String synonym) {
        this.geneId = geneId;
        this.synonym = synonym;
    }

    public String getGeneId() {
        return geneId;
    }

    public String getSynonym() {
        return synonym;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }

        if (!(o instanceof GeneSynonymId that)) {
            return false;
        }

        return Objects.equals(geneId, that.geneId)
                && Objects.equals(synonym, that.synonym);
    }

    @Override
    public int hashCode() {
        return Objects.hash(geneId, synonym);
    }
}