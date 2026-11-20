import os
from pathlib import Path
from typing import Any

import mysql.connector
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))


def _conectar():
    variaveis_obrigatorias = ("DB_NAME", "DB_USER", "DB_PASSWORD")
    ausentes = [
        nome for nome in variaveis_obrigatorias if nome not in os.environ
    ]
    if ausentes:
        raise RuntimeError(
            "Configure no backend/.env as variáveis: " + ", ".join(ausentes)
        )

    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )


def executar_consulta(
    sql: str,
    parametros: tuple[object, ...] = (),
) -> list[dict[str, Any]]:
    conexao = _conectar()

    try:
        cursor = conexao.cursor(dictionary=True)
        try:
            cursor.execute(sql, parametros)
            return list(cursor.fetchall())
        finally:
            cursor.close()
    finally:
        conexao.close()


def executar_comando(
    sql: str,
    parametros: tuple[object, ...] = (),
) -> tuple[int, int | None]:
    conexao = _conectar()

    try:
        cursor = conexao.cursor()
        try:
            cursor.execute(sql, parametros)
            conexao.commit()
            return cursor.rowcount, cursor.lastrowid
        except mysql.connector.Error:
            conexao.rollback()
            raise
        finally:
            cursor.close()
    finally:
        conexao.close()
