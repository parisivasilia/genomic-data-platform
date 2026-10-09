package io.github.parisivasilia.genomicdata.dto;

public record LoginResponse(
        String accessToken,
        String tokenType,
        long expiresIn
) {
}