package io.github.parisivasilia.genomicdata.controller;

import io.github.parisivasilia.genomicdata.dto.TranscriptResponse;
import io.github.parisivasilia.genomicdata.service.TranscriptService;
import io.github.parisivasilia.genomicdata.exception.ResourceNotFoundException;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1")
public class TranscriptController {

    private final TranscriptService transcriptService;

    public TranscriptController(
            TranscriptService transcriptService
    ) {
        this.transcriptService = transcriptService;
    }

    @GetMapping("/genes/{geneId}/transcripts")
    public Page<TranscriptResponse> getTranscriptsByGene(
            @PathVariable String geneId,
            Pageable pageable
    ) {
        return transcriptService.getTranscriptsByGeneId(
                geneId,
                pageable
        );
    }


@GetMapping("/transcripts/{transcriptId}")
public TranscriptResponse getTranscriptById(
        @PathVariable String transcriptId
    ) {
        return transcriptService
                .getTranscriptById(transcriptId)
                .orElseThrow(
                    () -> new ResourceNotFoundException(
                            "Transcript not found: "
                                    + transcriptId
                    )
            );
    }
}