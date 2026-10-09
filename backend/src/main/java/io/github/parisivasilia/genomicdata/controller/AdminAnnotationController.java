package io.github.parisivasilia.genomicdata.controller;

import io.github.parisivasilia.genomicdata.dto.CuratedAnnotationRequest;
import io.github.parisivasilia.genomicdata.dto.CuratedAnnotationResponse;
import io.github.parisivasilia.genomicdata.service.CuratedAnnotationService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/admin")
public class AdminAnnotationController {

    private final CuratedAnnotationService
            annotationService;

    public AdminAnnotationController(
            CuratedAnnotationService annotationService
    ) {
        this.annotationService = annotationService;
    }

    @PostMapping(
            "/genes/{geneId}/annotations"
    )
    @ResponseStatus(HttpStatus.CREATED)
    public CuratedAnnotationResponse create(
            @PathVariable String geneId,
            @Valid
            @RequestBody
            CuratedAnnotationRequest request,
            Authentication authentication
    ) {
        return annotationService.create(
                geneId,
                request,
                authentication.getName()
        );
    }

    @PutMapping("/annotations/{id}")
    public CuratedAnnotationResponse update(
            @PathVariable Long id,
            @Valid
            @RequestBody
            CuratedAnnotationRequest request
    ) {
        return annotationService.update(
                id,
                request
        );
    }

    @DeleteMapping("/annotations/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(
            @PathVariable Long id
    ) {
        annotationService.delete(id);
    }
}