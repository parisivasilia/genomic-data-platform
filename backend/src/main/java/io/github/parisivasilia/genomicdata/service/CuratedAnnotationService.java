package io.github.parisivasilia.genomicdata.service;

import io.github.parisivasilia.genomicdata.dto.CuratedAnnotationRequest;
import io.github.parisivasilia.genomicdata.dto.CuratedAnnotationResponse;
import io.github.parisivasilia.genomicdata.entity.CuratedAnnotation;
import io.github.parisivasilia.genomicdata.exception.ResourceNotFoundException;
import io.github.parisivasilia.genomicdata.repository.CuratedAnnotationRepository;
import io.github.parisivasilia.genomicdata.repository.GeneRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class CuratedAnnotationService {

    private final CuratedAnnotationRepository annotationRepository;
    private final GeneRepository geneRepository;

    public CuratedAnnotationService(
            CuratedAnnotationRepository annotationRepository,
            GeneRepository geneRepository
    ) {
        this.annotationRepository = annotationRepository;
        this.geneRepository = geneRepository;
    }

    @Transactional(readOnly = true)
    public List<CuratedAnnotationResponse> getAnnotationsForGene(
            String geneId
    ) {
        ensureGeneExists(geneId);

        return annotationRepository
                .findByGeneIdOrderByUpdatedAtDesc(geneId)
                .stream()
                .map(this::toResponse)
                .toList();
    }

    @Transactional
    public CuratedAnnotationResponse create(
            String geneId,
            CuratedAnnotationRequest request,
            String username
    ) {
        ensureGeneExists(geneId);

        CuratedAnnotation annotation =
                new CuratedAnnotation(
                        geneId,
                        request.title().trim(),
                        request.annotationText().trim(),
                        clean(request.category()),
                        username
                );

        CuratedAnnotation saved =
                annotationRepository.save(annotation);

        return toResponse(saved);
    }

    @Transactional
    public CuratedAnnotationResponse update(
            Long id,
            CuratedAnnotationRequest request
    ) {
        CuratedAnnotation annotation =
                annotationRepository
                        .findById(id)
                        .orElseThrow(
                                () ->
                                        new ResourceNotFoundException(
                                                "Annotation not found: " + id
                                        )
                        );

        annotation.update(
                request.title().trim(),
                request.annotationText().trim(),
                clean(request.category())
        );

        return toResponse(annotation);
    }

    @Transactional
    public void delete(Long id) {
        CuratedAnnotation annotation =
                annotationRepository
                        .findById(id)
                        .orElseThrow(
                                () ->
                                        new ResourceNotFoundException(
                                                "Annotation not found: " + id
                                        )
                        );

        annotationRepository.delete(annotation);
    }

    private void ensureGeneExists(String geneId) {
        if (geneRepository.findById(geneId).isEmpty()) {
            throw new ResourceNotFoundException(
                    "Gene not found: " + geneId
            );
        }
    }

    private String clean(String value) {
        if (value == null || value.isBlank()) {
            return null;
        }

        return value.trim();
    }

    private CuratedAnnotationResponse toResponse(
            CuratedAnnotation annotation
    ) {
        return new CuratedAnnotationResponse(
                annotation.getId(),
                annotation.getGeneId(),
                annotation.getTitle(),
                annotation.getAnnotationText(),
                annotation.getCategory(),
                annotation.getCreatedBy(),
                annotation.getCreatedAt(),
                annotation.getUpdatedAt()
        );
    }
}