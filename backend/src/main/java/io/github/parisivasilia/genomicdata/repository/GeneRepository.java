package io.github.parisivasilia.genomicdata.repository;

import io.github.parisivasilia.genomicdata.entity.Gene;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.Repository;
import org.springframework.data.repository.query.Param;

import java.util.Optional;

public interface GeneRepository
        extends Repository<Gene, String> {

    Optional<Gene> findById(String id);

    Page<Gene> findAll(Pageable pageable);

    @Query("""
            SELECT g
            FROM Gene g
            WHERE (
                :symbol IS NULL
                OR LOWER(g.symbol) LIKE
                   LOWER(CONCAT('%', :symbol, '%'))
            )
            AND (
                :chromosome IS NULL
                OR LOWER(g.chromosome) =
                   LOWER(:chromosome)
            )
            AND (
                :geneType IS NULL
                OR LOWER(g.geneType) =
                   LOWER(:geneType)
            )
            AND (
                :keyword IS NULL
                OR LOWER(g.symbol) LIKE
                   LOWER(CONCAT('%', :keyword, '%'))
                OR LOWER(g.description) LIKE
                   LOWER(CONCAT('%', :keyword, '%'))
                OR EXISTS (
                    SELECT gs
                    FROM GeneSynonym gs
                    WHERE gs.gene = g
                    AND LOWER(gs.id.synonym) LIKE
                        LOWER(CONCAT('%', :keyword, '%'))
                )
            )
            """)
    Page<Gene> search(
            @Param("symbol") String symbol,
            @Param("chromosome") String chromosome,
            @Param("geneType") String geneType,
            @Param("keyword") String keyword,
            Pageable pageable
    );
}