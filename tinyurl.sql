CREATE DATABASE IF NOT EXISTS tinyurl;
USE tinyurl;

CREATE TABLE IF NOT EXISTS links (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(10) UNIQUE NOT NULL,
    url_original TEXT NOT NULL,
    clicks INT DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO links (codigo, url_original, clicks, activo) VALUES
('Ab12Xy', 'https://www.google.com', 5, TRUE),
('Zx98Qr', 'https://www.youtube.com', 2, TRUE),
('Lm45No', 'https://www.github.com', 0, TRUE);