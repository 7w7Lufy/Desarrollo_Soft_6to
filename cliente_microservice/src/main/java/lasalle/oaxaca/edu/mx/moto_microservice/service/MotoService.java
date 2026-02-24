package lasalle.oaxaca.edu.mx.moto_microservice.service;

import lasalle.oaxaca.edu.mx.moto_microservice.dto.request.MotoCreateRequest;
import lasalle.oaxaca.edu.mx.moto_microservice.dto.request.MotoUpdateRequest;
import lasalle.oaxaca.edu.mx.moto_microservice.dto.response.MotoResponse;

import java.util.List;

public interface MotoService {
    MotoResponse crear(MotoCreateRequest motoCreateRequest);

    List<MotoResponse> obtenerTodas();

    MotoResponse obtenerPorPlaca(String placa);

    MotoResponse actualizar(String placa, MotoUpdateRequest motoUpdateRequest);

    void eliminar(String placa);
}
