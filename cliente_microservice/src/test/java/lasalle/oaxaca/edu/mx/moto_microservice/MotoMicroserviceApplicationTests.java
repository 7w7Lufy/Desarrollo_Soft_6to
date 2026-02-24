package lasalle.oaxaca.edu.mx.moto_microservice;

import lasalle.oaxaca.edu.mx.moto_microservice.repository.MotoRepository;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;

@SpringBootTest(properties = {
    "spring.autoconfigure.exclude=org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration,org.springframework.boot.autoconfigure.orm.jpa.HibernateJpaAutoConfiguration"
})
class MotoMicroserviceApplicationTests {

    @MockBean
    private MotoRepository motoRepository;

    @Test
    void contextLoads() {
    }

}
