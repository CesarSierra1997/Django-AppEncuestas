/* CREAR DB Y TABLAS */
CREATE DATABASE IF NOT EXISTS app_encuestas;

USE app_encuestas;

CREATE TABLE usuario_rol (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    rol VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE usuario_usuario (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(254) NOT NULL UNIQUE,
    nombres VARCHAR(200) NULL,
    apellidos VARCHAR(200) NULL,
    usuario_activo BOOLEAN NOT NULL,
    usuario_administrador BOOLEAN NOT NULL,
    rol_id INT NULL,
    numeroDocumento INT NOT NULL,
    tipoDocumento VARCHAR(20) NOT NULL,
    FOREIGN KEY (rol_id) REFERENCES usuario_rol(id)
);

CREATE TABLE encuesta_encuesta (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(200) NOT NULL,
    tipoEncuesta VARCHAR(50) NOT NULL,
    creador_id INT NOT NULL,  -- Nuevo campo que referencia al creador de la encuesta
    FOREIGN KEY (creador_id) REFERENCES usuario_usuario(id)  -- Clave foránea que referencia a la tabla usuario_usuario
);

CREATE TABLE encuesta_preguntageneral (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    texto_pre VARCHAR(200) NOT NULL,
    encuesta_id INT NOT NULL,
    FOREIGN KEY (encuesta_id) REFERENCES encuesta_encuesta(id)
);

CREATE TABLE encuesta_preguntanumerica (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    texto_pre VARCHAR(200) NOT NULL,
    rango INT NOT NULL,
    encuesta_id INT NOT NULL,
    FOREIGN KEY (encuesta_id) REFERENCES encuesta_encuesta(id)
);

CREATE TABLE encuesta_preguntaselectmultiple (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    texto_pre VARCHAR(200) NOT NULL,
    encuesta_id INT NOT NULL,
    FOREIGN KEY (encuesta_id) REFERENCES encuesta_encuesta(id)
);

CREATE TABLE encuesta_preguntasiono (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    texto_pre VARCHAR(200) NOT NULL,
    encuesta_id INT NOT NULL,
    FOREIGN KEY (encuesta_id) REFERENCES encuesta_encuesta(id)
);

CREATE TABLE encuesta_opcionpreguntaselectmultiple (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    opcion VARCHAR(255) NOT NULL,
    pregunta_id INT NOT NULL,
    FOREIGN KEY (pregunta_id) REFERENCES encuesta_preguntaselectmultiple(id)
);

CREATE TABLE encuesta_respuestaencuestaprivada (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    encuesta_id INT NOT NULL,
    usuario_id INT NULL,
    FOREIGN KEY (encuesta_id) REFERENCES encuesta_encuesta(id),
    FOREIGN KEY (usuario_id) REFERENCES usuario_usuario(id)
);

CREATE TABLE encuesta_respuestaencuestapublica (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    tipoDocumento VARCHAR(20) NOT NULL,
    numeroDocumento INT NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    email VARCHAR(254) NOT NULL,
    encuesta_id INT NOT NULL,
    FOREIGN KEY (encuesta_id) REFERENCES encuesta_encuesta(id)
);

CREATE TABLE encuesta_respuestapreguntageneral (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    respuesta VARCHAR(200) NOT NULL,
    pregunta_id INT NOT NULL,
    FOREIGN KEY (pregunta_id) REFERENCES encuesta_preguntageneral(id)
);

CREATE TABLE encuesta_respuestapreguntanumerica (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    respuesta INT NOT NULL,
    pregunta_id INT NOT NULL,
    FOREIGN KEY (pregunta_id) REFERENCES encuesta_preguntanumerica(id)
);

CREATE TABLE encuesta_respuestapreguntaselectmultiple (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    pregunta_id INT NOT NULL,
    respuesta_id INT NOT NULL,
    FOREIGN KEY (pregunta_id) REFERENCES encuesta_preguntaselectmultiple(id),
    FOREIGN KEY (respuesta_id) REFERENCES encuesta_opcionpreguntaselectmultiple(id)
);

CREATE TABLE encuesta_respuestapreguntasiono (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    respuesta BOOLEAN NOT NULL,
    pregunta_id INT NOT NULL,
    FOREIGN KEY (pregunta_id) REFERENCES encuesta_preguntasiono(id)
);

/* INSERTAR DATOS EN LAS TABLAS */

-- Insertar datos en la tabla usuario_rol
INSERT INTO usuario_rol (rol) VALUES ('Administrador');
INSERT INTO usuario_rol (rol) VALUES ('Usuario');

-- Insertar datos en la tabla usuario_usuario
INSERT INTO usuario_usuario (password, last_login, username, email, nombres, apellidos, usuario_activo, usuario_administrador, rol_id, numeroDocumento, tipoDocumento)
VALUES 
('password_hash1', '2024-08-29 10:00:00', 'admin1', 'admin1@example.com', 'Admin', 'Uno', TRUE, TRUE, 1, 1234567890, 'CC'),
('password_hash2', '2024-08-29 11:00:00', 'usuario1', 'usuario1@example.com', 'Usuario', 'Uno', TRUE, FALSE, 2, 9876543210, 'CC');

-- Insertar datos en la tabla encuesta_encuesta
INSERT INTO encuesta_encuesta (titulo, tipoEncuesta, creador_id)
VALUES 
('Encuesta de Satisfacción', 'Privada', 1),
('Encuesta de Conocimientos', 'Pública', 1);

-- Insertar datos en la tabla encuesta_preguntageneral
INSERT INTO encuesta_preguntageneral (texto_pre, encuesta_id)
VALUES 
('¿Cómo califica nuestro servicio?', 1),
('¿Qué tanto sabe sobre el tema X?', 2);

-- Insertar datos en la tabla encuesta_preguntanumerica
INSERT INTO encuesta_preguntanumerica (texto_pre, rango, encuesta_id)
VALUES 
('Califique de 1 a 10', 10, 1);

-- Insertar datos en la tabla encuesta_preguntaselectmultiple
INSERT INTO encuesta_preguntaselectmultiple (texto_pre, encuesta_id)
VALUES 
('Seleccione las opciones que apliquen', 2);

-- Insertar datos en la tabla encuesta_preguntasiono
INSERT INTO encuesta_preguntasiono (texto_pre, encuesta_id)
VALUES 
('¿Está satisfecho con el servicio?', 1);

-- Insertar datos en la tabla encuesta_opcionpreguntaselectmultiple
INSERT INTO encuesta_opcionpreguntaselectmultiple (opcion, pregunta_id)
VALUES 
('Opción A', 1),
('Opción B', 1),
('Opción C', 1);

-- Insertar datos en la tabla encuesta_respuestaencuestaprivada
INSERT INTO encuesta_respuestaencuestaprivada (encuesta_id, usuario_id)
VALUES 
(1, 2);

-- Insertar datos en la tabla encuesta_respuestaencuestapublica
INSERT INTO encuesta_respuestaencuestapublica (tipoDocumento, numeroDocumento, nombre, email, encuesta_id)
VALUES 
('CC', 12345678, 'Juan Pérez', 'juan.perez@example.com', 2);

-- Insertar datos en la tabla encuesta_respuestapreguntageneral
INSERT INTO encuesta_respuestapreguntageneral (respuesta, pregunta_id)
VALUES 
('Muy bueno', 1);

-- Insertar datos en la tabla encuesta_respuestapreguntanumerica
INSERT INTO encuesta_respuestapreguntanumerica (respuesta, pregunta_id)
VALUES 
(9, 1);

-- Insertar datos en la tabla encuesta_respuestapreguntaselectmultiple
INSERT INTO encuesta_respuestapreguntaselectmultiple (pregunta_id, respuesta_id)
VALUES 
(1, 1);

-- Insertar datos en la tabla encuesta_respuestapreguntasiono
INSERT INTO encuesta_respuestapreguntasiono (respuesta, pregunta_id)
VALUES 
(TRUE, 1);

