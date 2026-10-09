package io.github.parisivasilia.genomicdata.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

import java.math.BigDecimal;

@Entity
@Table(name = "gene")
public class Gene {

    @Id
    @Column(name = "gene_id", length = 32)
    private String id;

    @Column(name = "gene_symbol", length = 64)
    private String symbol;

    @Column(name = "description", columnDefinition = "TEXT")
    private String description;

    @Column(name = "gene_type", length = 64)
    private String geneType;

    @Column(name = "chromosome", length = 16)
    private String chromosome;

    @Column(name = "start_position")
    private Long startPosition;

    @Column(name = "end_position")
    private Long endPosition;

    @Column(name = "strand")
    private Byte strand;

    @Column(name = "gc_content", precision = 5, scale = 2)
    private BigDecimal gcContent;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "source_release_id", nullable = false)
    private SourceRelease sourceRelease;

    protected Gene() {
    }

    public String getId() {
        return id;
    }

    public String getSymbol() {
        return symbol;
    }

    public String getDescription() {
        return description;
    }

    public String getGeneType() {
        return geneType;
    }

    public String getChromosome() {
        return chromosome;
    }

    public Long getStartPosition() {
        return startPosition;
    }

    public Long getEndPosition() {
        return endPosition;
    }

    public Byte getStrand() {
        return strand;
    }

    public BigDecimal getGcContent() {
        return gcContent;
    }

    public SourceRelease getSourceRelease() {
        return sourceRelease;
    }
}