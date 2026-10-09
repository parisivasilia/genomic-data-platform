package io.github.parisivasilia.genomicdata.dto;

import java.math.BigDecimal;

public record GeneSummaryResponse(
        String id,
        String symbol,
        String description,
        String geneType,
        String chromosome,
        Long startPosition,
        Long endPosition,
        Byte strand,
        BigDecimal gcContent
) {
}