package io.github.parisivasilia.genomicdata.dto;

import java.math.BigDecimal;
import java.util.List;

public record GeneDetailResponse(
        String id,
        String symbol,
        String description,
        String geneType,
        String chromosome,
        Long startPosition,
        Long endPosition,
        Byte strand,
        BigDecimal gcContent,
        List<String> synonyms,
        String sourceName,
        String sourceVersion,
        String referenceAssembly,
        String sourceUrl
) {
}