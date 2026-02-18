/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package lasalle.oaxaca.edu.mx.cliente_microservice.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;

/**
 * Estructura que se debe cumplir al momento de actualizar un cliente
 * @author chris
 */
@Getter
@Setter
public class ClienteUpdateRequest {
    @NotBlank
    @Size(max = 13)
    private String rfc;
    
    @NotBlank
    @Size(max = 30)
    private String apellido_p;
    
    @NotBlank
    @Size(max = 30)
    private String apellido_m;
    
    @NotBlank
    @Size(max = 50)
    private String nombre;
}