CREATE DATABASE IF NOT EXISTS flowvis;

USE flowvis;

CREATE TABLE usuario (
    usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_nome VARCHAR(255) NOT NULL,
    usuario_user VARCHAR(20) NOT NULL UNIQUE,
    usuario_email VARCHAR(255) NOT NULL UNIQUE,
    usuario_senha CHAR(128) NOT NULL -- hash
);

SELECT * 
FROM usuario;

CREATE TABLE post (
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES usuario(usuario_id)
);

SELECT *
FROM post;

DROP TABLE usuario;