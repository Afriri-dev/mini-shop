import bcrypt

# Mot de passe saisi par l'utilisateur
password_input = "admin123"

# Hash récupéré depuis generate_hash.py
stored_hash = "$2b$12$wzN7e7vwAwmbuFBlRHWpJ.NujKk9RhhaEw65d82MeBl0KfOFYlELi"

# Vérification
if bcrypt.checkpw(password_input.encode("utf-8"), stored_hash.encode("utf-8")):
    print("✅ Mot de passe correct")
else:
    print("❌ Mot de passe incorrect")