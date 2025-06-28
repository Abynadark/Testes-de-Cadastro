from models.user_system import UserSystem

us = UserSystem()
us.register_user("Alice", "alice@email.com", "alice123")
print(f"Total de usuários cadastrados: {us.total_users()}")