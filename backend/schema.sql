CREATE DATABASE IF NOT EXISTS petschool
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE petschool;

CREATE TABLE IF NOT EXISTS tutores (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nome VARCHAR(120) NOT NULL,
    cpf_cnpj VARCHAR(18),
    telefone VARCHAR(30) NOT NULL,
    email VARCHAR(254),
    data_nascimento DATE,
    rua VARCHAR(160),
    numero VARCHAR(20),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    estado CHAR(2),
    cep VARCHAR(9),
    PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS pets (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nome VARCHAR(120) NOT NULL,
    especie VARCHAR(60) NOT NULL,
    tutor_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_pets_tutores
        FOREIGN KEY (tutor_id)
        REFERENCES tutores (id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB;
