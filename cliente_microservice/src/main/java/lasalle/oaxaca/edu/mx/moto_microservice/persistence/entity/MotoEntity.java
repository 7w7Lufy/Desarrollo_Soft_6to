package lasalle.oaxaca.edu.mx.moto_microservice.persistence.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "motos")
@Builder
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class MotoEntity {
    @Id
    @Column(length = 10)
    private String placa;

    @Column(nullable = false, length = 30)
    private String marca;

    @Column(nullable = false, length = 30)
    private String modelo;

    @Column(nullable = false)
    private Integer anio;

    @Column(length = 20)
    private String color;

    @Column
    private Integer cilindraje;

    @Column(length = 20)
    private String tipo;

    @Column
    private Integer kilometraje;
}
