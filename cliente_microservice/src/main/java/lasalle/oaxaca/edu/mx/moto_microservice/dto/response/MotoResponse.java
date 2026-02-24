package lasalle.oaxaca.edu.mx.moto_microservice.dto.response;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class MotoResponse {
    private String placa;
    private String marca;
    private String modelo;
    private Integer anio;
    private String color;
    private Integer cilindraje;
    private String tipo;
    private Integer kilometraje;
}
