package lasalle.oaxaca.edu.mx.moto_microservice.service.impl;

import lasalle.oaxaca.edu.mx.moto_microservice.dto.request.MotoCreateRequest;
import lasalle.oaxaca.edu.mx.moto_microservice.dto.request.MotoUpdateRequest;
import lasalle.oaxaca.edu.mx.moto_microservice.dto.response.MotoResponse;
import lasalle.oaxaca.edu.mx.moto_microservice.mapper.MotoMapper;
import lasalle.oaxaca.edu.mx.moto_microservice.persistence.entity.MotoEntity;
import lasalle.oaxaca.edu.mx.moto_microservice.repository.MotoRepository;
import lasalle.oaxaca.edu.mx.moto_microservice.service.MotoService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;

@Service
@RequiredArgsConstructor
public class MotoServiceImpl implements MotoService {

    private final MotoRepository motoRepository;
    private final MotoMapper motoMapper;

    @Override
    @Transactional
    public MotoResponse crear(MotoCreateRequest motoCreateRequest) {
        if (motoRepository.existsByPlaca(motoCreateRequest.getPlaca())) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Ya existe una moto con esa placa");
        }

        MotoEntity motoEntity = motoMapper.convertirAEntidad(motoCreateRequest);
        MotoEntity guardada = motoRepository.save(motoEntity);

        return motoMapper.convertirAResponse(guardada);
    }

    @Override
    @Transactional(readOnly = true)
    public List<MotoResponse> obtenerTodas() {
        return motoRepository.findAll()
                .stream()
                .map(motoMapper::convertirAResponse)
                .toList();
    }

    @Override
    @Transactional(readOnly = true)
    public MotoResponse obtenerPorPlaca(String placa) {
        MotoEntity motoEntity = motoRepository.findByPlaca(placa)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Moto no encontrada"));

        return motoMapper.convertirAResponse(motoEntity);
    }

    @Override
    @Transactional
    public MotoResponse actualizar(String placa, MotoUpdateRequest motoUpdateRequest) {
        MotoEntity motoEntity = motoRepository.findByPlaca(placa)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Moto no encontrada"));

        motoMapper.actualizarEntidad(motoEntity, motoUpdateRequest);
        MotoEntity actualizada = motoRepository.save(motoEntity);

        return motoMapper.convertirAResponse(actualizada);
    }

    @Override
    @Transactional
    public void eliminar(String placa) {
        MotoEntity motoEntity = motoRepository.findByPlaca(placa)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Moto no encontrada"));

        motoRepository.delete(motoEntity);
    }
}
