package io.github.parisivasilia.genomicdata.dto;

import java.time.Instant;

public record CuratedAnnotationResponse(
        Long id,
        String geneId,
        String title,
        String annotationText,
        String category,
        String createdBy,
        Instant createdAt,
        Instant updatedAt
) {
}