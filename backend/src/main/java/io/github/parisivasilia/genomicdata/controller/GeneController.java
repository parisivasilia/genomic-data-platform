package io.github.parisivasilia.genomicdata.controller;

import io.github.parisivasilia.genomicdata.dto.GeneDetailResponse;
import io.github.parisivasilia.genomicdata.dto.GeneSummaryResponse;
import io.github.parisivasilia.genomicdata.service.GeneService;
import io.github.parisivasilia.genomicdata.exception.ResourceNotFoundException;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;


@RestController
@RequestMapping("/api/v1/genes")
public class GeneController {

    private final GeneService geneService;

    public GeneController(GeneService geneService) {
        this.geneService = geneService;
    }

    @GetMapping
    public Page<GeneSummaryResponse> getGenes(
            @RequestParam(required = false)
            String symbol,

            @RequestParam(required = false)
            String chromosome,

            @RequestParam(required = false)
            String geneType,

            @RequestParam(required = false)
            String keyword,

            Pageable pageable
    ) {
        return geneService.getGenes(
                symbol,
                chromosome,
                geneType,
                keyword,
                pageable
        );
    }

    @GetMapping("/{id}")
    public GeneDetailResponse getGeneById(
            @PathVariable String id
    ) {
         return geneService.getGeneById(id)
            .orElseThrow(
                    () -> new ResourceNotFoundException(
                            "Gene not found: " + id
                    )
        );
    }
}