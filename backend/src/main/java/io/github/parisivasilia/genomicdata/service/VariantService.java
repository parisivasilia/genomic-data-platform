package io.github.parisivasilia.genomicdata.service;

import io.github.parisivasilia.genomicdata.dto.VariantResponse;
import io.github.parisivasilia.genomicdata.entity.SourceRelease;
import io.github.parisivasilia.genomicdata.entity.Variant;
import io.github.parisivasilia.genomicdata.repository.VariantRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

@Service
@Transactional(readOnly = true)
public class VariantService {

    private final VariantRepository variantRepository;

    public VariantService(
            VariantRepository variantRepository
    ) {
        this.variantRepository = variantRepository;
    }

    public Page<VariantResponse> getVariantsByGeneId(
            String geneId,
            Pageable pageable
    ) {
        return variantRepository
                .findByGeneId(geneId, pageable)
                .map(this::toResponse);
    }

    public Optional<VariantResponse> getVariantByClinvarId(
            Long clinvarVariationId
    ) {
        return variantRepository
                .findByClinvarVariationId(
                        clinvarVariationId
                )
                .map(this::toResponse);
    }

    private VariantResponse toResponse(
            Variant variant
    ) {
        SourceRelease source =
                variant.getSourceRelease();

        return new VariantResponse(
                variant.getClinvarVariationId(),
                variant.getClinvarAccession(),
                variant.getRsId(),
                variant.getChromosome(),
                variant.getPosition(),
                variant.getReferenceAllele(),
                variant.getAlternateAllele(),
                variant.getVariantType(),
                variant.getClassificationType(),
                variant.getClinicalSignificance(),
                variant.getReviewStatus(),
                variant.getLastEvaluated(),
                source.getSourceName(),
                source.getSourceVersion(),
                source.getReferenceAssembly()
        );
    }
}