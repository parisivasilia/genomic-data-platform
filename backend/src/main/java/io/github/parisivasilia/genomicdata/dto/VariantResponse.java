package io.github.parisivasilia.genomicdata.dto;

import java.time.LocalDate;

public record VariantResponse(
        Long clinvarVariationId,
        String clinvarAccession,
        String rsId,
        String chromosome,
        Long position,
        String referenceAllele,
        String alternateAllele,
        String variantType,
        String classificationType,
        String clinicalSignificance,
        String reviewStatus,
        LocalDate lastEvaluated,
        String sourceName,
        String sourceVersion,
        String referenceAssembly
) {
}