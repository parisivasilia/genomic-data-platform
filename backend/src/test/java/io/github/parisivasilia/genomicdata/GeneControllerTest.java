package io.github.parisivasilia.genomicdata;

import io.github.parisivasilia.genomicdata.controller.GeneController;
import io.github.parisivasilia.genomicdata.exception.GlobalExceptionHandler;
import io.github.parisivasilia.genomicdata.service.GeneService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import java.util.Optional;

import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

class GeneControllerTest {

    private GeneService geneService;
    private MockMvc mockMvc;

    @BeforeEach
    void setUp() {
        geneService = mock(GeneService.class);

        GeneController controller =
                new GeneController(geneService);

        mockMvc = MockMvcBuilders
                .standaloneSetup(controller)
                .setControllerAdvice(
                        new GlobalExceptionHandler()
                )
                .build();
    }

    @Test
    void missingGeneReturnsStructured404()
            throws Exception {

        String geneId = "ENSG_DOES_NOT_EXIST";

        when(geneService.getGeneById(geneId))
                .thenReturn(Optional.empty());

        mockMvc.perform(
                        get("/api/v1/genes/{id}", geneId)
                )
                .andExpect(status().isNotFound())
                .andExpect(
                        jsonPath("$.status").value(404)
                )
                .andExpect(
                        jsonPath("$.error")
                                .value("Not Found")
                )
                .andExpect(
                        jsonPath("$.message")
                                .value(
                                        "Gene not found: "
                                                + geneId
                                )
                );
    }
}