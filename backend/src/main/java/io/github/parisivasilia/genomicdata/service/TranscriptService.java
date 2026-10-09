package io.github.parisivasilia.genomicdata.service;

import io.github.parisivasilia.genomicdata.dto.TranscriptResponse;
import io.github.parisivasilia.genomicdata.entity.SourceRelease;
import io.github.parisivasilia.genomicdata.entity.Transcript;
import io.github.parisivasilia.genomicdata.repository.TranscriptRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

@Service
@Transactional(readOnly = true)
public class TranscriptService {

    private final TranscriptRepository transcriptRepository;

    public TranscriptService(
            TranscriptRepository transcriptRepository
    ) {
        this.transcriptRepository = transcriptRepository;
    }

    public Page<TranscriptResponse> getTranscriptsByGeneId(
            String geneId,
            Pageable pageable
    ) {
        return transcriptRepository
                .findByGeneId(geneId, pageable)
                .map(this::toResponse);
    }

    public Optional<TranscriptResponse> getTranscriptById(
            String transcriptId
    ) {
        return transcriptRepository
                .findById(transcriptId)
                .map(this::toResponse);
    }

    private TranscriptResponse toResponse(Transcript transcript) {
        SourceRelease source = transcript.getSourceRelease();

        return new TranscriptResponse(
                transcript.getId(),
                transcript.getName(),
                transcript.getTranscriptType(),
                transcript.getChromosome(),
                transcript.getStartPosition(),
                transcript.getEndPosition(),
                transcript.getStrand(),
                transcript.getGene().getId(),
                source.getSourceName(),
                source.getSourceVersion(),
                source.getReferenceAssembly()
        );
    }
}