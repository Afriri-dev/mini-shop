import bcrypt

# Mot de passe en clair
password_admin = "admin123"
password_user1 = "user123"

# Génération du hash bcrypt
hashed_admin = bcrypt.hashpw(password_admin.encode("utf-8"), bcrypt.gensalt())
hashed_user1 = bcrypt.hashpw(password_user1.encode("utf-8"), bcrypt.gensalt())

print("Hash admin :", hashed_admin.decode("utf-8"))
print("Hash user1 :", hashed_user1.decode("utf-8"))