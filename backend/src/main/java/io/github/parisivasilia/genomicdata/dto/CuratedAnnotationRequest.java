package io.github.parisivasilia.genomicdata.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record CuratedAnnotationRequest(

        @NotBlank
        @Size(max = 150)
        String title,

        @NotBlank
        String annotationText,

        @Size(max = 100)
        String category
) {
}