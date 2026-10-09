package io.github.parisivasilia.genomicdata.repository;

import io.github.parisivasilia.genomicdata.entity.Transcript;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.repository.Repository;

import java.util.Optional;

public interface TranscriptRepository
        extends Repository<Transcript, String> {

    Optional<Transcript> findById(String id);

    Page<Transcript> findByGeneId(
            String geneId,
            Pageable pageable
    );
}