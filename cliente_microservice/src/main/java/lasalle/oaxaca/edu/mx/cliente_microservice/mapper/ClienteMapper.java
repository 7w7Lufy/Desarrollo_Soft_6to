/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package lasalle.oaxaca.edu.mx.cliente_microservice.mapper;

import lasalle.oaxaca.edu.mx.cliente_microservice.dto.request.ClienteCreateRequest;
import lasalle.oaxaca.edu.mx.cliente_microservice.persistence.entity.ClienteEntity;
import org.springframework.stereotype.Component;

/**
 * Clase que convierte DTO --> Entity
 * @author chris
 */
@Component
public class ClienteMapper {
    
    public ClienteEntity convertirAEntidad(ClienteCreateRequest ccr) {
        return ClienteEntity.builder()
                .rfc(ccr.getRfc())
                .apellido_p(ccr.getApellido_p())
                .apellido_m(ccr.getApellido_m())
                .nombre(ccr.getNombre())
                .build();
    }
}