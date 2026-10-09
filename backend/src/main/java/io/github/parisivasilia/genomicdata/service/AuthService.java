package io.github.parisivasilia.genomicdata.service;

import io.github.parisivasilia.genomicdata.dto.LoginRequest;
import io.github.parisivasilia.genomicdata.dto.LoginResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.oauth2.jose.jws.MacAlgorithm;
import org.springframework.security.oauth2.jwt.JwtClaimsSet;
import org.springframework.security.oauth2.jwt.JwtEncoder;
import org.springframework.security.oauth2.jwt.JwtEncoderParameters;
import org.springframework.security.oauth2.jwt.JwsHeader;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.time.Instant;
import java.util.List;

@Service
public class AuthService {

    private final String adminUsername;
    private final String adminPasswordHash;
    private final long tokenTtlSeconds;

    private final PasswordEncoder passwordEncoder;
    private final JwtEncoder jwtEncoder;

    public AuthService(
            @Value("${app.admin.username}")
            String adminUsername,

            @Value("${app.admin.password}")
            String adminPassword,

            @Value("${app.jwt.ttl-seconds:3600}")
            long tokenTtlSeconds,

            PasswordEncoder passwordEncoder,
            JwtEncoder jwtEncoder
    ) {
        if (adminUsername == null
                || adminUsername.isBlank()) {
            throw new IllegalStateException(
                    "ADMIN_USERNAME must not be blank"
            );
        }

        if (adminPassword == null
                || adminPassword.isBlank()) {
            throw new IllegalStateException(
                    "ADMIN_PASSWORD must not be blank"
            );
        }

        this.adminUsername = adminUsername;
        this.adminPasswordHash =
                passwordEncoder.encode(adminPassword);

        this.tokenTtlSeconds = tokenTtlSeconds;
        this.passwordEncoder = passwordEncoder;
        this.jwtEncoder = jwtEncoder;
    }

    public LoginResponse login(
            LoginRequest request
    ) {
        boolean validUsername =
                adminUsername.equals(
                        request.username()
                );

        boolean validPassword =
                passwordEncoder.matches(
                        request.password(),
                        adminPasswordHash
                );

        if (!validUsername || !validPassword) {
            throw new ResponseStatusException(
                    HttpStatus.UNAUTHORIZED,
                    "Invalid username or password"
            );
        }

        Instant issuedAt = Instant.now();
        Instant expiresAt =
                issuedAt.plusSeconds(
                        tokenTtlSeconds
                );

        JwtClaimsSet claims =
                JwtClaimsSet.builder()
                        .issuer(
                                "genomic-data-platform"
                        )
                        .subject(adminUsername)
                        .issuedAt(issuedAt)
                        .expiresAt(expiresAt)
                        .claim(
                                "roles",
                                List.of("ADMIN")
                        )
                        .build();

        JwsHeader header =
                JwsHeader
                        .with(MacAlgorithm.HS256)
                        .build();

        String accessToken =
                jwtEncoder
                        .encode(
                                JwtEncoderParameters.from(
                                        header,
                                        claims
                                )
                        )
                        .getTokenValue();

        return new LoginResponse(
                accessToken,
                "Bearer",
                tokenTtlSeconds
        );
    }
}