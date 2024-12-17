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
    curtidas_count INT DEFAULT 0,
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

CREATE TABLE grupos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    imagem VARCHAR(255) NOT NULL,
    criador_id INT NOT NULL,
    FOREIGN KEY (criador_id) REFERENCES usuario(usuario_id)
);

SELECT *
FROM grupos;

CREATE TABLE grupo_usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    grupo_id INT NOT NULL,
    usuario_id INT NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (grupo_id) REFERENCES grupos(id),
    FOREIGN KEY (usuario_id) REFERENCES usuario(usuario_id),
    UNIQUE (grupo_id, usuario_id)
);

SELECT *
FROM grupo_usuarios;
    
CREATE TABLE post_grupo (
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    grupo_id INT NOT NULL,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    curtidas_count INT DEFAULT 0,
    FOREIGN KEY (grupo_id) REFERENCES grupos(id),
    FOREIGN KEY (user_id) REFERENCES usuario(usuario_id)
);

CREATE TABLE eventos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    grupo_id INT NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    data DATE NOT NULL,
    local VARCHAR(255) NOT NULL,
    descricao TEXT NOT NULL,
    criador_id INT NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (grupo_id) REFERENCES grupos(id),
    FOREIGN KEY (criador_id) REFERENCES usuario(usuario_id)
);


DROP TABLE usuario;
DROP TABLE post;
DROP TABLE curtidas;
DROP TABLE grupos;
DROP TABLE grupo_usuarios;
DROP TABLE post_grupo;
DROP TABLE eventos;

