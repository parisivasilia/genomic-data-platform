package io.github.parisivasilia.genomicdata.repository;

import io.github.parisivasilia.genomicdata.entity.GeneSynonym;
import io.github.parisivasilia.genomicdata.entity.GeneSynonymId;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.Repository;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface GeneSynonymRepository
        extends Repository<GeneSynonym, GeneSynonymId> {

    @Query("""
            SELECT gs
            FROM GeneSynonym gs
            WHERE gs.gene.id = :geneId
            ORDER BY gs.id.synonym
            """)
    List<GeneSynonym> findByGeneId(
            @Param("geneId") String geneId
    );
}