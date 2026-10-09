package io.github.parisivasilia.genomicdata.dto;

public record TranscriptResponse(
        String id,
        String name,
        String transcriptType,
        String chromosome,
        Long startPosition,
        Long endPosition,
        Byte strand,
        String geneId,
        String sourceName,
        String sourceVersion,
        String referenceAssembly
) {
}