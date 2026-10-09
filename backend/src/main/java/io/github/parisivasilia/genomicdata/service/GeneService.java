package io.github.parisivasilia.genomicdata.service;

import io.github.parisivasilia.genomicdata.dto.GeneDetailResponse;
import io.github.parisivasilia.genomicdata.dto.GeneSummaryResponse;
import io.github.parisivasilia.genomicdata.entity.Gene;
import io.github.parisivasilia.genomicdata.entity.GeneSynonym;
import io.github.parisivasilia.genomicdata.entity.SourceRelease;
import io.github.parisivasilia.genomicdata.repository.GeneRepository;
import io.github.parisivasilia.genomicdata.repository.GeneSynonymRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
@Transactional(readOnly = true)
public class GeneService {

    private final GeneRepository geneRepository;
    private final GeneSynonymRepository geneSynonymRepository;

    public GeneService(
            GeneRepository geneRepository,
            GeneSynonymRepository geneSynonymRepository
    ) {
        this.geneRepository = geneRepository;
        this.geneSynonymRepository = geneSynonymRepository;
    }

    public Page<GeneSummaryResponse> getGenes(
            String symbol,
            String chromosome,
            String geneType,
            String keyword,
            Pageable pageable
    ) {
        return geneRepository.search(
                clean(symbol),
                clean(chromosome),
                clean(geneType),
                clean(keyword),
                pageable
        ).map(this::toSummaryResponse);
    }

    public Optional<GeneDetailResponse> getGeneById(
            String id
    ) {
        return geneRepository.findById(id)
                .map(this::toDetailResponse);
    }

    private String clean(String value) {
        if (value == null || value.isBlank()) {
            return null;
        }

        return value.trim();
    }

    private GeneSummaryResponse toSummaryResponse(
            Gene gene
    ) {
        return new GeneSummaryResponse(
                gene.getId(),
                gene.getSymbol(),
                gene.getDescription(),
                gene.getGeneType(),
                gene.getChromosome(),
                gene.getStartPosition(),
                gene.getEndPosition(),
                gene.getStrand(),
                gene.getGcContent()
        );
    }

    private GeneDetailResponse toDetailResponse(
            Gene gene
    ) {
        SourceRelease source = gene.getSourceRelease();

        List<String> synonyms =
                geneSynonymRepository
                        .findByGeneId(gene.getId())
                        .stream()
                        .map(GeneSynonym::getSynonym)
                        .toList();

        return new GeneDetailResponse(
                gene.getId(),
                gene.getSymbol(),
                gene.getDescription(),
                gene.getGeneType(),
                gene.getChromosome(),
                gene.getStartPosition(),
                gene.getEndPosition(),
                gene.getStrand(),
                gene.getGcContent(),
                synonyms,
                source.getSourceName(),
                source.getSourceVersion(),
                source.getReferenceAssembly(),
                source.getSourceUrl()
        );
    }
}