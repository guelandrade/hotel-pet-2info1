import logging

from fastapi import FastAPI, HTTPException, Path, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mysql.connector import Error as MySQLError
from pydantic import BaseModel, Field

from database import executar_comando, executar_consulta

app = FastAPI(title="PetSchool API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ],
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)


class Tutor(BaseModel):
    id: int
    nome: str
    telefone: str


class Pet(BaseModel):
    id: int
    nome: str
    especie: str
    tutorId: int


class TutorCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=120)
    telefone: str = Field(min_length=1, max_length=30)


class PetCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=120)
    especie: str = Field(min_length=1, max_length=60)
    tutorId: int = Field(gt=0)


@app.exception_handler(MySQLError)
async def tratar_erro_mysql(request: Request, exc: MySQLError) -> JSONResponse:
    logging.getLogger("uvicorn.error").error("Erro no MySQL: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Não foi possível acessar o banco de dados."},
    )


@app.get("/tutores", response_model=list[Tutor], tags=["Tutores"])
def listar_tutores() -> list[dict]:
    sql = "SELECT id, nome, telefone FROM tutores ORDER BY id"
    return executar_consulta(sql)


@app.post(
    "/tutores",
    response_model=Tutor,
    status_code=201,
    tags=["Tutores"],
)
def criar_tutor(tutor: TutorCreate) -> dict:
    sql = "INSERT INTO tutores (nome, telefone) VALUES (%s, %s)"
    _, tutor_id = executar_comando(sql, (tutor.nome, tutor.telefone))
    if tutor_id is None:
        raise RuntimeError("O MySQL não retornou o ID do tutor criado.")
    return {"id": tutor_id, **tutor.model_dump()}


@app.get("/tutores/{tutor_id}", response_model=Tutor, tags=["Tutores"])
def consultar_tutor(tutor_id: int = Path(gt=0)) -> dict:
    sql = "SELECT id, nome, telefone FROM tutores WHERE id = %s"
    tutores = executar_consulta(sql, (tutor_id,))
    if not tutores:
        raise HTTPException(status_code=404, detail="Tutor não encontrado.")
    return tutores[0]


@app.delete(
    "/tutores/{tutor_id}",
    status_code=204,
    response_class=Response,
    tags=["Tutores"],
)
def excluir_tutor(tutor_id: int = Path(gt=0)) -> Response:
    tutores = executar_consulta(
        "SELECT id FROM tutores WHERE id = %s",
        (tutor_id,),
    )
    if not tutores:
        raise HTTPException(status_code=404, detail="Tutor não encontrado.")

    pets = executar_consulta(
        "SELECT id FROM pets WHERE tutor_id = %s LIMIT 1",
        (tutor_id,),
    )
    if pets:
        raise HTTPException(
            status_code=409,
            detail="Não é possível excluir um tutor que possui pets.",
        )

    linhas_afetadas, _ = executar_comando(
        "DELETE FROM tutores WHERE id = %s",
        (tutor_id,),
    )
    if linhas_afetadas == 0:
        raise HTTPException(status_code=404, detail="Tutor não encontrado.")
    return Response(status_code=204)


@app.get("/pets", response_model=list[Pet], tags=["Pets"])
def listar_pets(
    especie: str | None = Query(default=None, min_length=1, max_length=60),
) -> list[dict]:
    sql = "SELECT id, nome, especie, tutor_id AS tutorId FROM pets"
    if especie is not None:
        sql += " WHERE especie = %s"
        return executar_consulta(sql + " ORDER BY id", (especie,))
    return executar_consulta(sql + " ORDER BY id")


@app.post(
    "/pets",
    response_model=Pet,
    status_code=201,
    tags=["Pets"],
)
def criar_pet(pet: PetCreate) -> dict:
    tutores = executar_consulta(
        "SELECT id FROM tutores WHERE id = %s",
        (pet.tutorId,),
    )
    if not tutores:
        raise HTTPException(status_code=404, detail="Tutor não encontrado.")

    sql = (
        "INSERT INTO pets (nome, especie, tutor_id) "
        "VALUES (%s, %s, %s)"
    )
    _, pet_id = executar_comando(sql, (pet.nome, pet.especie, pet.tutorId))
    if pet_id is None:
        raise RuntimeError("O MySQL não retornou o ID do pet criado.")
    return {"id": pet_id, **pet.model_dump()}


@app.get("/pets/{pet_id}", response_model=Pet, tags=["Pets"])
def consultar_pet(pet_id: int = Path(gt=0)) -> dict:
    sql = (
        "SELECT id, nome, especie, tutor_id AS tutorId "
        "FROM pets WHERE id = %s"
    )
    pets = executar_consulta(sql, (pet_id,))
    if not pets:
        raise HTTPException(status_code=404, detail="Pet não encontrado.")
    return pets[0]


@app.delete(
    "/pets/{pet_id}",
    status_code=204,
    response_class=Response,
    tags=["Pets"],
)
def excluir_pet(pet_id: int = Path(gt=0)) -> Response:
    linhas_afetadas, _ = executar_comando(
        "DELETE FROM pets WHERE id = %s",
        (pet_id,),
    )
    if linhas_afetadas == 0:
        raise HTTPException(status_code=404, detail="Pet não encontrado.")
    return Response(status_code=204)
