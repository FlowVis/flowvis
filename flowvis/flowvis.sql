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

ALTER TABLE post ADD curtidas_count INT DEFAULT 0;

CREATE TABLE curtidas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    post_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES usuario(usuario_id),
    FOREIGN KEY (post_id) REFERENCES post(post_id)
);
    
SELECT *
FROM curtidas;
    
DROP TABLE usuario;
DROP TABLE post;
DROP TABLE curtidas;