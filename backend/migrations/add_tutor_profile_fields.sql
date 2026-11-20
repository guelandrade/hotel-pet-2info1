-- Executar uma única vez em bancos criados com o schema anterior.
USE petschool;

ALTER TABLE tutores
    ADD COLUMN cpf_cnpj VARCHAR(18) NULL,
    ADD COLUMN email VARCHAR(254) NULL,
    ADD COLUMN data_nascimento DATE NULL,
    ADD COLUMN rua VARCHAR(160) NULL,
    ADD COLUMN numero VARCHAR(20) NULL,
    ADD COLUMN bairro VARCHAR(100) NULL,
    ADD COLUMN cidade VARCHAR(100) NULL,
    ADD COLUMN estado CHAR(2) NULL,
    ADD COLUMN cep VARCHAR(9) NULL;
