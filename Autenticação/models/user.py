import re

class User:
    """
    Representa um usuário do sistema.
    """
    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = password

    def is_valid_email(self):
        """
        Verifica se o e-mail possui um formato válido.
        """
        return re.match(r"[^@]+@[^@]+\.[^@]+", self.email) is not None

    def is_strong_password(self):
        """
        Verifica se a senha é considerada forte:
        """
        return len(self.password) >= 6 and any(char.isdigit() for char in self.password)