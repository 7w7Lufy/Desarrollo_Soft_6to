package lasalle.oaxaca.edu.mx.moto_microservice.mapper;

import lasalle.oaxaca.edu.mx.moto_microservice.dto.request.MotoCreateRequest;
import lasalle.oaxaca.edu.mx.moto_microservice.dto.request.MotoUpdateRequest;
import lasalle.oaxaca.edu.mx.moto_microservice.dto.response.MotoResponse;
import lasalle.oaxaca.edu.mx.moto_microservice.persistence.entity.MotoEntity;
import org.springframework.stereotype.Component;

@Component
public class MotoMapper {

    public MotoEntity convertirAEntidad(MotoCreateRequest motoCreateRequest) {
        return MotoEntity.builder()
                .placa(motoCreateRequest.getPlaca())
                .marca(motoCreateRequest.getMarca())
                .modelo(motoCreateRequest.getModelo())
                .anio(motoCreateRequest.getAnio())
                .color(motoCreateRequest.getColor())
                .cilindraje(motoCreateRequest.getCilindraje())
                .tipo(motoCreateRequest.getTipo())
                .kilometraje(motoCreateRequest.getKilometraje())
                .build();
    }

    public MotoResponse convertirAResponse(MotoEntity motoEntity) {
        return MotoResponse.builder()
                .placa(motoEntity.getPlaca())
                .marca(motoEntity.getMarca())
                .modelo(motoEntity.getModelo())
                .anio(motoEntity.getAnio())
                .color(motoEntity.getColor())
                .cilindraje(motoEntity.getCilindraje())
                .tipo(motoEntity.getTipo())
                .kilometraje(motoEntity.getKilometraje())
                .build();
    }

    public void actualizarEntidad(MotoEntity motoEntity, MotoUpdateRequest motoUpdateRequest) {
        motoEntity.setMarca(motoUpdateRequest.getMarca());
        motoEntity.setModelo(motoUpdateRequest.getModelo());
        motoEntity.setAnio(motoUpdateRequest.getAnio());
        motoEntity.setColor(motoUpdateRequest.getColor());
        motoEntity.setCilindraje(motoUpdateRequest.getCilindraje());
        motoEntity.setTipo(motoUpdateRequest.getTipo());
        motoEntity.setKilometraje(motoUpdateRequest.getKilometraje());
    }
}
