-- ============================================
-- 🗄️ Script d'initialisation de la base shopdb
-- ============================================

-- Création de la base si elle n’existe pas
CREATE DATABASE IF NOT EXISTS shopdb;
USE shopdb;

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,        -- identifiant unique
    username VARCHAR(50) NOT NULL UNIQUE,     -- nom d’utilisateur
    email VARCHAR(100) NOT NULL UNIQUE,       -- email unique pour login
    password VARCHAR(255) NOT NULL,           -- mot de passe haché (bcrypt)
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- ✅ ajout
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- ✅ ajout
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- ==========================
-- Données initiales
-- ==========================

-- Utilisateurs de test (⚠️ remplacer HASHED_PASSWORD par un vrai hash bcrypt)
INSERT INTO users (username, email, password, role) VALUES
('admin', 'admin@example.com', '$2b$12$LMEY6DfoUOGCrAPIbMk5zutTrH53ZAicFy/vHfJS9apjUKRyvCLNq', 'admin'),
('user1', 'user1@example.com', '$2b$12$J/NoeeuGmlnJBBB3DpCaG.pgTfHdYgqCRP449hQoHUqS3kckEV/kO', 'user');

-- Produits de test
INSERT INTO products (name, price, stock) VALUES
('Produit A', 10.00, 100),
('Produit B', 20.00, 50),
('Produit C', 15.50, 75);

-- Commandes de test
INSERT INTO orders (user_id, product_id, quantity, status) VALUES
(1, 1, 2, 'confirmed'),   -- admin a commandé 2x Produit A
(2, 2, 1, 'pending');     -- user1 a commandé 1x Produit B