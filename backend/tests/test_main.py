import unittest
from datetime import date
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app


class PetSchoolApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_cors_permite_operacoes_do_frontend(self) -> None:
        resposta = self.client.options(
            "/pets",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(
            resposta.headers["access-control-allow-origin"],
            "http://localhost:5173",
        )
        self.assertIn("POST", resposta.headers["access-control-allow-methods"])

    def test_cors_permite_porta_alternativa_do_vite(self) -> None:
        resposta = self.client.options(
            "/pets",
            headers={
                "Origin": "http://localhost:5174",
                "Access-Control-Request-Method": "GET",
            },
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(
            resposta.headers["access-control-allow-origin"],
            "http://localhost:5174",
        )

    @patch("main.executar_consulta")
    def test_lista_tutores(self, executar_consulta: unittest.mock.Mock) -> None:
        executar_consulta.return_value = [
            {"id": 1, "nome": "Ana", "telefone": "47999990000"}
        ]

        resposta = self.client.get("/tutores")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(
            resposta.json(),
            [{"id": 1, "nome": "Ana", "telefone": "47999990000"}],
        )

    @patch("main.executar_comando")
    def test_cria_tutor(
        self, executar_comando: unittest.mock.Mock
    ) -> None:
        executar_comando.return_value = (1, 4)

        resposta = self.client.post(
            "/tutores",
            json={"nome": "Ana", "telefone": "47999990000"},
        )

        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(
            resposta.json(),
            {"id": 4, "nome": "Ana", "telefone": "47999990000"},
        )
        executar_comando.assert_called_once_with(
            "INSERT INTO tutores (nome, cpf_cnpj, telefone, email, "
            "data_nascimento, rua, numero, bairro, cidade, estado, cep) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            ("Ana", None, "47999990000", None, None, None, None, None, None, None, None),
        )

    @patch("main.executar_comando")
    def test_cria_tutor_com_dados_complementares(
        self, executar_comando: unittest.mock.Mock
    ) -> None:
        executar_comando.return_value = (1, 5)

        resposta = self.client.post(
            "/tutores",
            json={
                "nome": "Ana",
                "cpfCnpj": "123.456.789-09",
                "telefone": "(47) 99999-0000",
                "email": "ana@example.com",
                "dataNascimento": "1990-05-12",
                "rua": "Rua Central",
                "numero": "10",
                "bairro": "Centro",
                "cidade": "Araquari",
                "estado": "SC",
                "cep": "89245-000",
            },
        )

        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(resposta.json()["cpfCnpj"], "123.456.789-09")
        self.assertEqual(resposta.json()["dataNascimento"], "1990-05-12")
        self.assertEqual(resposta.json()["cidade"], "Araquari")
        self.assertEqual(
            executar_comando.call_args.args[1],
            (
                "Ana",
                "123.456.789-09",
                "(47) 99999-0000",
                "ana@example.com",
                date(1990, 5, 12),
                "Rua Central",
                "10",
                "Centro",
                "Araquari",
                "SC",
                "89245-000",
            ),
        )

    @patch("main.executar_consulta")
    def test_consulta_tutor_por_id_usa_parametro_sql(
        self, executar_consulta: unittest.mock.Mock
    ) -> None:
        executar_consulta.return_value = [
            {"id": 8, "nome": "Ana", "telefone": "47999990000"}
        ]

        resposta = self.client.get("/tutores/8")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()["id"], 8)
        executar_consulta.assert_called_once_with(
            "SELECT id, nome, cpf_cnpj AS cpfCnpj, telefone, email, "
            "data_nascimento AS dataNascimento, rua, numero, bairro, cidade, "
            "estado, cep FROM tutores WHERE id = %s",
            (8,),
        )

    @patch("main.executar_consulta")
    def test_consulta_tutor_inexistente_retorna_404(
        self, executar_consulta: unittest.mock.Mock
    ) -> None:
        executar_consulta.return_value = []

        resposta = self.client.get("/tutores/999")

        self.assertEqual(resposta.status_code, 404)

    @patch("main.executar_consulta")
    def test_lista_pets_preserva_relacao_com_tutor(
        self, executar_consulta: unittest.mock.Mock
    ) -> None:
        executar_consulta.return_value = [
            {
                "id": 3,
                "nome": "Safira",
                "especie": "Cachorro",
                "tutorId": 1,
            }
        ]

        resposta = self.client.get("/pets")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()[0]["tutorId"], 1)

    @patch("main.executar_consulta")
    def test_lista_pets_filtra_por_especie(
        self, executar_consulta: unittest.mock.Mock
    ) -> None:
        executar_consulta.return_value = []

        resposta = self.client.get("/pets?especie=Cachorro")

        self.assertEqual(resposta.status_code, 200)
        executar_consulta.assert_called_once_with(
            "SELECT id, nome, especie, tutor_id AS tutorId FROM pets "
            "WHERE especie = %s ORDER BY id",
            ("Cachorro",),
        )

    @patch("main.executar_consulta")
    def test_lista_pets_filtra_por_tutor(
        self, executar_consulta: unittest.mock.Mock
    ) -> None:
        executar_consulta.return_value = []

        resposta = self.client.get("/pets?tutorId=2")

        self.assertEqual(resposta.status_code, 200)
        executar_consulta.assert_called_once_with(
            "SELECT id, nome, especie, tutor_id AS tutorId FROM pets "
            "WHERE tutor_id = %s ORDER BY id",
            (2,),
        )

    @patch("main.executar_comando")
    @patch("main.executar_consulta")
    def test_cria_pet_com_tutor_existente(
        self,
        executar_consulta: unittest.mock.Mock,
        executar_comando: unittest.mock.Mock,
    ) -> None:
        executar_consulta.return_value = [{"id": 2}]
        executar_comando.return_value = (1, 7)

        resposta = self.client.post(
            "/pets",
            json={"nome": "Safira", "especie": "Cachorro", "tutorId": 2},
        )

        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(
            resposta.json(),
            {
                "id": 7,
                "nome": "Safira",
                "especie": "Cachorro",
                "tutorId": 2,
            },
        )
        executar_comando.assert_called_once_with(
            "INSERT INTO pets (nome, especie, tutor_id) VALUES (%s, %s, %s)",
            ("Safira", "Cachorro", 2),
        )

    @patch("main.executar_comando")
    @patch("main.executar_consulta")
    def test_nao_cria_pet_sem_tutor(
        self,
        executar_consulta: unittest.mock.Mock,
        executar_comando: unittest.mock.Mock,
    ) -> None:
        executar_consulta.return_value = []

        resposta = self.client.post(
            "/pets",
            json={"nome": "Safira", "especie": "Cachorro", "tutorId": 99},
        )

        self.assertEqual(resposta.status_code, 404)
        executar_comando.assert_not_called()

    @patch("main.executar_consulta")
    def test_consulta_pet_por_id_usa_parametro_sql(
        self, executar_consulta: unittest.mock.Mock
    ) -> None:
        executar_consulta.return_value = [
            {
                "id": 3,
                "nome": "Safira",
                "especie": "Cachorro",
                "tutorId": 1,
            }
        ]

        resposta = self.client.get("/pets/3")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()["tutorId"], 1)
        executar_consulta.assert_called_once_with(
            "SELECT id, nome, especie, tutor_id AS tutorId "
            "FROM pets WHERE id = %s",
            (3,),
        )

    @patch("main.executar_consulta")
    def test_consulta_pet_inexistente_retorna_404(
        self, executar_consulta: unittest.mock.Mock
    ) -> None:
        executar_consulta.return_value = []

        resposta = self.client.get("/pets/999")

        self.assertEqual(resposta.status_code, 404)

    @patch("main.executar_comando")
    def test_exclui_pet(
        self, executar_comando: unittest.mock.Mock
    ) -> None:
        executar_comando.return_value = (1, None)

        resposta = self.client.delete("/pets/3")

        self.assertEqual(resposta.status_code, 204)
        executar_comando.assert_called_once_with(
            "DELETE FROM pets WHERE id = %s",
            (3,),
        )

    @patch("main.executar_comando")
    @patch("main.executar_consulta")
    def test_impede_exclusao_de_tutor_com_pets(
        self,
        executar_consulta: unittest.mock.Mock,
        executar_comando: unittest.mock.Mock,
    ) -> None:
        executar_consulta.side_effect = [[{"id": 1}], [{"id": 3}]]

        resposta = self.client.delete("/tutores/1")

        self.assertEqual(resposta.status_code, 409)
        executar_comando.assert_not_called()

    @patch("main.executar_comando")
    @patch("main.executar_consulta")
    def test_exclui_tutor_sem_pets(
        self,
        executar_consulta: unittest.mock.Mock,
        executar_comando: unittest.mock.Mock,
    ) -> None:
        executar_consulta.side_effect = [[{"id": 1}], []]
        executar_comando.return_value = (1, None)

        resposta = self.client.delete("/tutores/1")

        self.assertEqual(resposta.status_code, 204)
        executar_comando.assert_called_once_with(
            "DELETE FROM tutores WHERE id = %s",
            (1,),
        )

    @patch("main.executar_comando")
    def test_exclui_pet_inexistente(
        self, executar_comando: unittest.mock.Mock
    ) -> None:
        executar_comando.return_value = (0, None)

        resposta = self.client.delete("/pets/999")

        self.assertEqual(resposta.status_code, 404)


if __name__ == "__main__":
    unittest.main()
