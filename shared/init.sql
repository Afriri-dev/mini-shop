-- ============================================
-- 🗄️ Script d'initialisation de la base shopdb
-- ============================================

-- Création de la base si elle n’existe pas
CREATE DATABASE IF NOT EXISTS shopdb;
USE shopdb;

-- ==========================
-- Table des utilisateurs
-- ==========================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,        -- identifiant unique
    username VARCHAR(50) NOT NULL UNIQUE,     -- nom d’utilisateur
    password VARCHAR(255) NOT NULL,           -- mot de passe haché
    role ENUM('user', 'admin') DEFAULT 'user' -- rôle de l’utilisateur
);

-- ==========================
-- Table des produits
-- ==========================
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,        -- identifiant unique
    name VARCHAR(100) NOT NULL,               -- nom du produit
    price DECIMAL(10,2) NOT NULL,             -- prix du produit
    stock INT DEFAULT 0                       -- quantité disponible
);

-- ==========================
-- Table des commandes
-- ==========================
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,        -- identifiant unique
    user_id INT NOT NULL,                     -- FK vers users
    product_id INT NOT NULL,                  -- FK vers products
    quantity INT NOT NULL,                    -- nombre d’unités
    status ENUM('pending', 'confirmed', 'shipped') DEFAULT 'pending',
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- ==========================
-- Données initiales
-- ==========================

-- Utilisateurs de test (⚠️ remplacer HASHED_PASSWORD par un vrai hash bcrypt)
INSERT INTO users (username, password, role) VALUES
('admin', 'HASHED_PASSWORD_ADMIN', 'admin'),
('user1', 'HASHED_PASSWORD_USER1', 'user');

-- Produits de test
INSERT INTO products (name, price, stock) VALUES
('Produit A', 10.00, 100),
('Produit B', 20.00, 50),
('Produit C', 15.50, 75);

-- Commandes de test
INSERT INTO orders (user_id, product_id, quantity, status) VALUES
(1, 1, 2, 'confirmed'),   -- admin a commandé 2x Produit A
(2, 2, 1, 'pending');     -- user1 a commandé 1x Produit B