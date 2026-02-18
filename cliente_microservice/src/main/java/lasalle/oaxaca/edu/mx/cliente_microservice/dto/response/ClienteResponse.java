/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package lasalle.oaxaca.edu.mx.cliente_microservice.dto.response;

import lombok.Builder;
import lombok.Getter;

/**
 *
 * @author chris
 */
@Getter
@Builder
public class ClienteResponse {
    private String rfc;
    private String apellido_p;
    private String apellido_m;
    private String nombre;
}