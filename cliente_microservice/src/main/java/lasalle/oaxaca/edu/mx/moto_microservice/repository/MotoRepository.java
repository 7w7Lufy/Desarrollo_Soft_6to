package lasalle.oaxaca.edu.mx.moto_microservice.repository;

import lasalle.oaxaca.edu.mx.moto_microservice.persistence.entity.MotoEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface MotoRepository extends JpaRepository<MotoEntity, String> {
    Optional<MotoEntity> findByPlaca(String placa);

    boolean existsByPlaca(String placa);
}
