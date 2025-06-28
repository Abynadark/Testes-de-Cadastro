import unittest
from models.user import User
from models.user_system import UserSystem

class TestUser(unittest.TestCase):

    # Verifica se o método is_valid_email retorna True para um e-mail válido
    def test_email_valido(self):
        user = User("Teste", "email@dominio.com", "abc123")
        self.assertTrue(user.is_valid_email())

    # Verifica se is_valid_email retorna False para e-mail sem '@'
    def test_email_invalido_sem_arroba(self):
        user = User("Teste", "emaildominio.com", "abc123")
        self.assertFalse(user.is_valid_email())

    # Verifica se is_valid_email retorna False para e-mail sem domínio
    def test_email_invalido_sem_dominio(self):
        user = User("Teste", "email@", "abc123")
        self.assertFalse(user.is_valid_email())

    # Verifica se a senha é considerada forte (possui números e comprimento mínimo)
    def test_senha_valida(self):
        user = User("Teste", "email@teste.com", "abc123")
        self.assertTrue(user.is_strong_password())

    # Verifica se a senha é rejeitada por não conter números
    def test_senha_sem_numeros(self):
        user = User("Teste", "email@teste.com", "abcdef")
        self.assertFalse(user.is_strong_password())

    # Verifica se a senha é rejeitada por ser muito curta
    def test_senha_muito_curta(self):
        user = User("Teste", "email@teste.com", "a1")
        self.assertFalse(user.is_strong_password())

    # Verifica se os atributos do usuário são atribuídos corretamente no construtor
    def test_atributos_usuario(self):
        user = User("Nome", "email@teste.com", "senha123")
        self.assertEqual(user.name, "Nome")
        self.assertEqual(user.email, "email@teste.com")
        self.assertEqual(user.password, "senha123")


class TestUserSystem(unittest.TestCase):

    # Cria uma instância nova do sistema de usuários antes de cada teste
    def setUp(self):
        self.us = UserSystem()

    # Testa cadastro válido e verifica se os dados do usuário cadastrado estão corretos
    def test_cadastro_valido(self):
        user = self.us.register_user("Nome", "email@teste.com", "abc123")
        self.assertEqual(user.email, "email@teste.com")
        self.assertEqual(user.name, "Nome")

    # Verifica se o sistema levanta exceção para e-mail inválido durante cadastro
    def test_cadastro_email_invalido(self):
        with self.assertRaises(ValueError) as context:
            self.us.register_user("Nome", "email.com", "abc123")
        self.assertIn("E-mail inválido", str(context.exception))

    # Verifica se o sistema levanta exceção para senha fraca durante cadastro
    def test_cadastro_senha_fraca(self):
        with self.assertRaises(ValueError) as context:
            self.us.register_user("Nome", "email@teste.com", "abc")
        self.assertIn("Senha fraca", str(context.exception))

    # Testa a busca por usuário que existe, verifica se retorna objeto correto
    def test_busca_usuario_existente(self):
        self.us.register_user("Buscar", "buscar@teste.com", "abc123")
        user = self.us.find_user_by_email("buscar@teste.com")
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "Buscar")

    # Testa a busca por usuário inexistente, verifica se retorna None
    def test_busca_usuario_inexistente(self):
        user = self.us.find_user_by_email("inexistente@teste.com")
        self.assertIsNone(user)

    # Verifica se total_users retorna 0 inicialmente e depois o número correto após cadastros
    def test_total_usuarios(self):
        self.assertEqual(self.us.total_users(), 0)
        self.us.register_user("A", "a@a.com", "abc123")
        self.us.register_user("B", "b@b.com", "abc123")
        self.assertEqual(self.us.total_users(), 2)

    # Testa o cadastro de múltiplos usuários e verifica se o total está correto
    def test_cadastro_usuarios_multiplos(self):
        emails = [f"user{i}@User.com" for i in range(5)]
        for i, email in enumerate(emails):
            self.us.register_user(f"User{i}", email, f"pass{i}123")
        self.assertEqual(self.us.total_users(), 5)

    # Verifica que o usuário original com determinado e-mail não é sobrescrito por outro cadastro diferente
    def test_usuario_nao_sobrescreve(self):
        self.us.register_user("Original", "same@email.com", "abc123")
        self.us.register_user("Segundo", "other@email.com", "abc123")
        user = self.us.find_user_by_email("same@email.com")
        self.assertEqual(user.name, "Original")
    
    # Testa se o sistema impede cadastro de usuário com e-mail duplicado (deve levantar exceção)
    def test_cadastro_email_duplicado(self):
        self.us.register_user("João", "joao@email.com", "abc123")
        with self.assertRaises(ValueError) as context:
            self.us.register_user("Outro", "joao@email.com", "abc123")
        self.assertIn("E-mail já cadastrado", str(context.exception))

if __name__ == '__main__':
    unittest.main()
