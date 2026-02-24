package lasalle.oaxaca.edu.mx.moto_microservice.dto.request;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class MotoCreateRequest {
    @NotBlank
    @Size(max = 10)
    private String placa;

    @NotBlank
    @Size(max = 30)
    private String marca;

    @NotBlank
    @Size(max = 30)
    private String modelo;

    @NotNull
    @Min(1900)
    @Max(2100)
    private Integer anio;

    @NotBlank
    @Size(max = 20)
    private String color;

    @NotNull
    @Min(50)
    @Max(2000)
    private Integer cilindraje;

    @NotBlank
    @Size(max = 20)
    private String tipo;

    @NotNull
    @Min(0)
    private Integer kilometraje;
}
