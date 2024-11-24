CREATE DATABASE IF NOT EXISTS flowvis;

USE flowvis;

CREATE TABLE usuarios (
    usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_nome VARCHAR(255),
    usuario_user VARCHAR(20) UNIQUE,
    usuario_email VARCHAR(255) UNIQUE,
    usuario_senha CHAR(128) -- hash
);

SELECT * 
FROM usuarios;