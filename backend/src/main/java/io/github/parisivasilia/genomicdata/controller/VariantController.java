package io.github.parisivasilia.genomicdata.controller;

import io.github.parisivasilia.genomicdata.dto.VariantResponse;
import io.github.parisivasilia.genomicdata.service.VariantService;
import io.github.parisivasilia.genomicdata.exception.ResourceNotFoundException;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1")
public class VariantController {

    private final VariantService variantService;

    public VariantController(
            VariantService variantService
    ) {
        this.variantService = variantService;
    }

    @GetMapping("/genes/{geneId}/variants")
    public Page<VariantResponse> getVariantsByGene(
            @PathVariable String geneId,
            Pageable pageable
    ) {
        return variantService.getVariantsByGeneId(
                geneId,
                pageable
        );
    }

    @GetMapping("/variants/{clinvarVariationId}")
    public VariantResponse getVariant(
        @PathVariable Long clinvarVariationId
    ) {
        return variantService
            .getVariantByClinvarId(
                    clinvarVariationId
            )
            .orElseThrow(
                    () -> new ResourceNotFoundException(
                            "ClinVar variant not found: "
                                    + clinvarVariationId
                    )
        );
    }
}