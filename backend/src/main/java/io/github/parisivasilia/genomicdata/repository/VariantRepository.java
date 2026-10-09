package io.github.parisivasilia.genomicdata.repository;

import io.github.parisivasilia.genomicdata.entity.Variant;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.Repository;
import org.springframework.data.repository.query.Param;

import java.util.Optional;

public interface VariantRepository
        extends Repository<Variant, Long> {

    Optional<Variant> findByClinvarVariationId(
            Long clinvarVariationId
    );

    @Query("""
            SELECT gv.variant
            FROM GeneVariant gv
            WHERE gv.gene.id = :geneId
            """)
    Page<Variant> findByGeneId(
            @Param("geneId") String geneId,
            Pageable pageable
    );
}