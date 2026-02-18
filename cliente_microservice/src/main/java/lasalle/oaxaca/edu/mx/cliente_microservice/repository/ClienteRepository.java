/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package lasalle.oaxaca.edu.mx.cliente_microservice.repository;

import lasalle.oaxaca.edu.mx.cliente_microservice.persistence.entity.ClienteEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * Clase que accede directamente a los datos
 * @author chris
 */
@Repository
public interface ClienteRepository extends JpaRepository<ClienteEntity, String> {
    // Permite atrapar errores como NotNull
    Optional<ClienteEntity> findByRfc(String rfc);
    
    boolean existsByRfc(String rfc);
}