package lasalle.oaxaca.edu.mx.moto_microservice.controller;

import jakarta.validation.Valid;
import lasalle.oaxaca.edu.mx.moto_microservice.dto.request.MotoCreateRequest;
import lasalle.oaxaca.edu.mx.moto_microservice.dto.request.MotoUpdateRequest;
import lasalle.oaxaca.edu.mx.moto_microservice.dto.response.MotoResponse;
import lasalle.oaxaca.edu.mx.moto_microservice.service.MotoService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/motos")
@RequiredArgsConstructor
public class MotoController {

    private final MotoService motoService;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public MotoResponse crearMoto(@Valid @RequestBody MotoCreateRequest motoCreateRequest) {
        return motoService.crear(motoCreateRequest);
    }

    @GetMapping
    public List<MotoResponse> obtenerMotos() {
        return motoService.obtenerTodas();
    }

    @GetMapping("/{placa}")
    public MotoResponse obtenerMotoPorPlaca(@PathVariable String placa) {
        return motoService.obtenerPorPlaca(placa);
    }

    @PutMapping("/{placa}")
    public MotoResponse actualizarMoto(
            @PathVariable String placa,
            @Valid @RequestBody MotoUpdateRequest motoUpdateRequest
    ) {
        return motoService.actualizar(placa, motoUpdateRequest);
    }

    @DeleteMapping("/{placa}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void eliminarMoto(@PathVariable String placa) {
        motoService.eliminar(placa);
    }
}
