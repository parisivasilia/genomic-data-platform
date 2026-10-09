package io.github.parisivasilia.genomicdata.controller;

import io.github.parisivasilia.genomicdata.dto.CuratedAnnotationResponse;
import io.github.parisivasilia.genomicdata.service.CuratedAnnotationService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping(
        "/api/v1/genes/{geneId}/annotations"
)
public class CuratedAnnotationController {

    private final CuratedAnnotationService
            annotationService;

    public CuratedAnnotationController(
            CuratedAnnotationService annotationService
    ) {
        this.annotationService = annotationService;
    }

    @GetMapping
    public List<CuratedAnnotationResponse>
    getAnnotations(
            @PathVariable String geneId
    ) {
        return annotationService
                .getAnnotationsForGene(geneId);
    }
}