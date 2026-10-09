package io.github.parisivasilia.genomicdata.repository;

import io.github.parisivasilia.genomicdata.entity.CuratedAnnotation;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface CuratedAnnotationRepository
        extends JpaRepository<CuratedAnnotation, Long> {

    List<CuratedAnnotation>
    findByGeneIdOrderByUpdatedAtDesc(String geneId);
}