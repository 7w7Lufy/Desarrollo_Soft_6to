/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package lasalle.oaxaca.edu.mx.cliente_microservice.persistence.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

/**
 * Clase que se encarga de contener el objeto tipo cliente, ayuda a la creación de la BD, según las especificaciones
 * @author chris
 * @version 
 * @date
 */
@Entity
@Table(name = "clientes")
@Builder
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class ClienteEntity {
    @Id
    @Column(length = 13)
    private String rfc;
    
    @Column(nullable = false, length = 30)
    private String apellido_p;
    
    @Column(nullable = false, length = 30)
    private String apellido_m;
    
    @Column(nullable = false, length = 50)
    private String nombre;
}