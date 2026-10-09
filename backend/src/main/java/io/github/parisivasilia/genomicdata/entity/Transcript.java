package io.github.parisivasilia.genomicdata.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "transcript")
public class Transcript {

    @Id
    @Column(name = "transcript_id", length = 32)
    private String id;

    @Column(name = "transcript_name", length = 128)
    private String name;

    @Column(name = "transcript_type", length = 64)
    private String transcriptType;

    @Column(name = "chromosome", length = 16)
    private String chromosome;

    @Column(name = "start_position")
    private Long startPosition;

    @Column(name = "end_position")
    private Long endPosition;

    @Column(name = "strand")
    private Byte strand;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "gene_id", nullable = false)
    private Gene gene;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "source_release_id", nullable = false)
    private SourceRelease sourceRelease;

    protected Transcript() {
    }

    public String getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getTranscriptType() {
        return transcriptType;
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

    public Gene getGene() {
        return gene;
    }

    public SourceRelease getSourceRelease() {
        return sourceRelease;
    }
}