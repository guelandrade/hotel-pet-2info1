# API FastAPI da PetSchool

Esta API aplica ao domínio da PetSchool o percurso da atividade: consulta,
consulta por identificador, filtro e cadastro. O Vue usa a FastAPI como backend.

## Endpoints

| Método | Caminho | Resposta |
| --- | --- | --- |
| `GET` | `/tutores` | Lista de tutores |
| `POST` | `/tutores` | Cadastra um tutor |
| `GET` | `/tutores/{tutor_id}` | Um tutor pelo ID |
| `DELETE` | `/tutores/{tutor_id}` | Exclui um tutor sem pets associados |
| `GET` | `/pets` | Lista de pets, incluindo `tutorId` |
| `GET` | `/pets?especie=Cachorro` | Filtra pets por espécie |
| `POST` | `/pets` | Cadastra um pet associado a um tutor existente |
| `GET` | `/pets/{pet_id}` | Um pet pelo ID |
| `DELETE` | `/pets/{pet_id}` | Exclui um pet |

Os IDs e `tutorId` são números no contrato da API. IDs inválidos retornam
`422`; um registro inexistente retorna `404`. Uma lista sem registros retorna
`[]`. Excluir um tutor que ainda possui pets retorna `409`.

## Preparar o MySQL pelo Workbench

Não execute o script sem conferir se já existe um banco com tabelas de tutores
e pets que você queira preservar. No MySQL Workbench, conecte ao servidor e
confira a conexão selecionada:

```sql
SELECT DATABASE();
SHOW DATABASES;
```

Se já houver um banco de projeto, selecione-o na lista de schemas e confira as
tabelas e colunas antes de alterar qualquer coisa:

```sql
SHOW TABLES;
DESCRIBE tutores;
DESCRIBE pets;
```

Se as tabelas já existirem com outra estrutura, não execute
[`schema.sql`](./schema.sql) ainda: compare os nomes e tipos e adapte o script
ou as consultas da API primeiro. `CREATE TABLE IF NOT EXISTS` não migra tabelas
que já existem.

Para criar o schema desta API do zero:

1. Abra [`schema.sql`](./schema.sql) no VS Code.
2. Copie o conteúdo para uma nova aba SQL do Workbench.
3. Execute pelo ícone de raio.
4. Confira os resultados:

```sql
USE petschool;
SHOW TABLES;
DESCRIBE tutores;
DESCRIBE pets;
```

O script cria `petschool.tutores` e `petschool.pets`. `pets.tutor_id` é uma
chave estrangeira para `tutores.id`, e impede pets sem um tutor válido.

Para ter dados de demonstração, execute uma vez, depois de criar as tabelas:

```sql
INSERT INTO tutores (nome, telefone)
VALUES ('Ana', '47999990000');

SET @id_tutor = LAST_INSERT_ID();

INSERT INTO pets (nome, especie, tutor_id)
VALUES ('Safira', 'Cachorro', @id_tutor);

SELECT * FROM tutores;
SELECT id, nome, especie, tutor_id FROM pets;
```

Pule os `INSERT`s se já tiver dados ou não quiser criar exemplos.

## Configurar e iniciar a API

Requer Python 3.10 ou superior e o MySQL Server em execução. A interface
Workbench pode ser fechada depois de executar o SQL; a API conecta ao servidor
MySQL, não ao programa Workbench.

No terminal, a partir da raiz do repositório:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Abra `backend/.env` e ajuste `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` e
`DB_PASSWORD` para a conexão do seu MySQL. O arquivo real `.env` não deve ser
enviado ao Git.

Com o ambiente virtual ativado e ainda dentro de `backend/`, inicie:

```bash
uvicorn main:app --reload
```

Abra <http://127.0.0.1:8000/docs> para testar os endpoints no Swagger. Em outro
terminal, na raiz do repositório, inicie o Vue:

```bash
npm run dev
```

O frontend usa `http://127.0.0.1:8000` por padrão. Para outra URL, defina
`VITE_API_URL` no ambiente antes de iniciar o Vite. As origens de
desenvolvimento e preview (`localhost` e `127.0.0.1`, portas 5173, 5174 e 4173)
estão autorizadas por CORS.

## Testes automatizados

Com as dependências instaladas, dentro de `backend/`:

```bash
python -m unittest discover -s tests
```

Os testes substituem o acesso ao banco por resultados controlados; eles não
validam a conexão com seu MySQL. Para conferir os dados reais, use o Swagger
com o MySQL conectado, depois de conferir o schema no Workbench.
